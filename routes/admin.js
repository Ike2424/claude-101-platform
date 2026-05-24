import { Router } from 'express';
import rateLimit from 'express-rate-limit';
import { logger } from '../lib/logger.js';
import crypto from 'node:crypto';
import { q, one, exec, sql } from '../lib/db.js';
import { makeMagicToken } from '../lib/token.js';
import { sendMagicLink } from '../lib/mail.js';
import { requireAdmin } from '../middleware/requireAdmin.js';

const router = Router();

const PUBLIC_URL = process.env.PUBLIC_URL || 'http://localhost:3000';
const MINUTES = parseInt(process.env.MAGIC_LINK_LIFETIME_MIN || '20', 10);

function safeEq(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string') return false;
  if (a.length !== b.length) return false;
  return crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b));
}


// Rate limiter estricto para login admin (anti brute-force)
const loginLimiter = rateLimit({
  windowMs: 60_000,
  max: 5,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Demasiados intentos. Espera 1 minuto.' },
});

// ============================================================
// POST /api/admin/login { token }
// Valida el token y setea cookie httpOnly.
// ============================================================
router.post('/login', loginLimiter, (req, res) => {
  const token = String(req.body?.token || '');
  const expected = process.env.ADMIN_TOKEN || '';
  if (!expected) return res.status(500).json({ error: 'ADMIN_TOKEN no configurado' });
  if (!safeEq(token, expected)) {
    return res.status(401).json({ error: 'Token inválido' });
  }
  res.cookie('admin_token', token, {
    httpOnly: true,
    sameSite: 'lax',
    secure: PUBLIC_URL.startsWith('https://'),
    maxAge: 1000 * 60 * 60 * 24 * 30, // 30 días
    path: '/',
  });
  res.json({ ok: true });
});

// ============================================================
// POST /api/admin/logout
// ============================================================
router.post('/logout', (req, res) => {
  res.clearCookie('admin_token', { path: '/' });
  res.json({ ok: true });
});

// ============================================================
// A partir de aquí, todas las rutas requieren admin.
// ============================================================
router.use(requireAdmin);

// ============================================================
// GET /api/admin/stats
// ============================================================
router.get('/stats', async (_req, res) => {
  const totalUsers = (await one('SELECT COUNT(*) AS n FROM users'))?.n ?? 0;
  const paidUsers = (await one('SELECT COUNT(*) AS n FROM users WHERE has_paid = 1'))?.n ?? 0;
  const totalRevenue = (await one(
    `SELECT COALESCE(SUM(amount_cents), 0) AS s FROM purchases WHERE status = 'completed'`
  ))?.s ?? 0;
  const completedPurchases = (await one(
    `SELECT COUNT(*) AS n FROM purchases WHERE status = 'completed'`
  ))?.n ?? 0;
  const refunded = (await one(
    `SELECT COUNT(*) AS n FROM purchases WHERE status = 'refunded'`
  ))?.n ?? 0;
  // Compras por día (últimos 14 días)
  const byDay = await q(
    `SELECT DATE(created_at) AS day, COUNT(*) AS n, COALESCE(SUM(amount_cents),0) AS revenue
     FROM purchases WHERE status = 'completed'
     GROUP BY DATE(created_at)
     ORDER BY day DESC
     LIMIT 14`
  );
  res.json({
    total_users: totalUsers,
    paid_users: paidUsers,
    completed_purchases: completedPurchases,
    refunded: refunded,
    total_revenue_cents: totalRevenue,
    by_day: byDay,
  });
});

// ============================================================
// GET /api/admin/users?limit=50&offset=0&search=foo
// ============================================================
router.get('/users', async (req, res) => {
  const limit = Math.min(parseInt(req.query.limit || '50', 10), 200);
  const offset = parseInt(req.query.offset || '0', 10);
  const search = String(req.query.search || '').trim().toLowerCase();
  const where = search ? 'WHERE LOWER(email) LIKE ?' : '';
  const params = search ? [`%${search}%`, limit, offset] : [limit, offset];
  const rows = await q(
    `SELECT id, email, has_paid, paid_at, stripe_customer, created_at
     FROM users ${where}
     ORDER BY created_at DESC
     LIMIT ? OFFSET ?`,
    params
  );
  res.json({ users: rows });
});

// ============================================================
// GET /api/admin/purchases?limit=50&offset=0
// ============================================================
router.get('/purchases', async (req, res) => {
  const limit = Math.min(parseInt(req.query.limit || '50', 10), 200);
  const offset = parseInt(req.query.offset || '0', 10);
  const rows = await q(
    `SELECT id, email, stripe_session_id, amount_cents, currency, status, created_at
     FROM purchases
     ORDER BY created_at DESC
     LIMIT ? OFFSET ?`,
    [limit, offset]
  );
  res.json({ purchases: rows });
});

// ============================================================
// POST /api/admin/users/:id/revoke
// ============================================================
router.post('/users/:id/revoke', async (req, res) => {
  const id = parseInt(req.params.id, 10);
  if (!id) return res.status(400).json({ error: 'id inválido' });
  await exec(`UPDATE users SET has_paid = 0, updated_at = CURRENT_TIMESTAMP WHERE id = ?`, [id]);
  res.json({ ok: true });
});

// ============================================================
// POST /api/admin/users/:id/grant
// ============================================================
router.post('/users/:id/grant', async (req, res) => {
  const id = parseInt(req.params.id, 10);
  if (!id) return res.status(400).json({ error: 'id inválido' });
  await exec(
    `UPDATE users SET has_paid = 1, paid_at = COALESCE(paid_at, CURRENT_TIMESTAMP), updated_at = CURRENT_TIMESTAMP WHERE id = ?`,
    [id]
  );
  res.json({ ok: true });
});

// ============================================================
// POST /api/admin/grant-by-email { email }
// Crea (o actualiza) un usuario y le da acceso. Útil para conceder manualmente.
// ============================================================
router.post('/grant-by-email', async (req, res) => {
  const email = String(req.body?.email || '').trim().toLowerCase();
  if (!email || !email.includes('@')) return res.status(400).json({ error: 'email inválido' });

  let user = await one('SELECT id FROM users WHERE email = ?', [email]);
  if (!user) {
    await exec(
      `INSERT INTO users (email, has_paid, paid_at) VALUES (?, 1, CURRENT_TIMESTAMP)`,
      [email]
    );
    user = await one('SELECT id FROM users WHERE email = ?', [email]);
  } else {
    await exec(
      `UPDATE users SET has_paid = 1, paid_at = COALESCE(paid_at, CURRENT_TIMESTAMP), updated_at = CURRENT_TIMESTAMP WHERE id = ?`,
      [user.id]
    );
  }

  // Opcional: enviar magic link inmediato
  if (req.body?.send_link) {
    try {
      const { raw, hash } = makeMagicToken();
      const expires = new Date(Date.now() + MINUTES * 60 * 1000).toISOString();
      await exec(
        'INSERT INTO magic_tokens (user_id, token_hash, expires_at, ip, user_agent) VALUES (?, ?, ?, ?, ?)',
        [user.id, hash, expires, req.ip || null, 'admin-grant']
      );
      const link = `${PUBLIC_URL}/api/auth/verify?token=${encodeURIComponent(raw)}`;
      await sendMagicLink({ to: email, link });
    } catch (err) {
      logger.error({ err: err }, 'Error enviando magic link:');
    }
  }

  res.json({ ok: true, user_id: user.id });
});

// ============================================================
// GET /api/admin/analytics?days=30
// Devuelve métricas web + curso para los últimos N días.
// ============================================================
router.get('/analytics', async (req, res) => {
  const days = Math.min(parseInt(req.query.days || '30', 10), 365);
  // Dialect-aware: funciona en SQLite y Postgres
  const sinceExpr = sql.dateAgo(days);
  const dateOfCreated = sql.dateOf('created_at');
  const dateOfCompleted = sql.dateOf('completed_at');

  // Wrapper resiliente: si un query falla, log + devolver fallback
  async function tryQ(name, fn, fallback) {
    try { return await fn(); }
    catch (err) {
      logger.error({ err: err?.message, stack: err?.stack?.split('\n').slice(0,3), q: name }, 'analytics query failed:');
      return fallback;
    }
  }

  // Visitas totales y únicas
  const totalViews = await tryQ('totalViews', async () => (await one(`SELECT COUNT(*) AS n FROM page_views WHERE created_at >= ${sinceExpr}`))?.n ?? 0, 0);
  const uniqueVisitors = await tryQ('uniqueVisitors', async () => (await one(
    `SELECT COUNT(DISTINCT visitor_id) AS n FROM page_views
     WHERE created_at >= ${sinceExpr} AND visitor_id IS NOT NULL`
  ))?.n ?? 0, 0);

  // Visitas por día (para la curva)
  const viewsByDay = await tryQ('viewsByDay', async () => await q(
    `SELECT ${dateOfCreated} AS day, COUNT(*) AS views, COUNT(DISTINCT visitor_id) AS uniques
     FROM page_views
     WHERE created_at >= ${sinceExpr}
     GROUP BY ${dateOfCreated}
     ORDER BY day ASC`
  ), []);

  // Top páginas
  const topPages = await tryQ('topPages', async () => await q(
    `SELECT path, COUNT(*) AS hits, COUNT(DISTINCT visitor_id) AS uniques
     FROM page_views
     WHERE created_at >= ${sinceExpr}
     GROUP BY path
     ORDER BY hits DESC
     LIMIT 15`
  ), []);

  // Top referrers (limpia internos)
  const topReferrers = await tryQ('topReferrers', async () => await q(
    `SELECT referrer, COUNT(*) AS hits
     FROM page_views
     WHERE created_at >= ${sinceExpr}
       AND referrer IS NOT NULL
       AND referrer != ''
       AND referrer NOT LIKE '%' || ? || '%'
     GROUP BY referrer
     ORDER BY hits DESC
     LIMIT 10`,
    [(process.env.PUBLIC_URL || 'localhost').replace(/^https?:\/\//, '').replace(/\/$/, '')]
  ), []);

  // Eventos del periodo
  const eventCounts = await tryQ('eventCounts', async () => await q(
    `SELECT event_type, COUNT(*) AS n FROM events
     WHERE created_at >= ${sinceExpr}
     GROUP BY event_type
     ORDER BY n DESC`
  ), []);

  // Funnel: visitas únicas a "/" → checkout_started → checkout_completed (= compras)
  const landingUniques = await tryQ('landingUniques', async () => (await one(
    `SELECT COUNT(DISTINCT visitor_id) AS n FROM page_views
     WHERE created_at >= ${sinceExpr} AND path = '/' AND visitor_id IS NOT NULL`
  ))?.n ?? 0, 0);
  const checkoutStarted = await tryQ('checkoutStarted', async () => (await one(
    `SELECT COUNT(DISTINCT visitor_id) AS n FROM events
     WHERE created_at >= ${sinceExpr} AND event_type = 'checkout_started' AND visitor_id IS NOT NULL`
  ))?.n ?? 0, 0);
  const purchasesInPeriod = await tryQ('purchasesInPeriod', async () => (await one(
    `SELECT COUNT(*) AS n FROM purchases
     WHERE status = 'completed' AND created_at >= ${sinceExpr}`
  ))?.n ?? 0, 0);

  // Curso: lecciones más completadas
  const topLessons = await tryQ('topLessons', async () => await q(
    `SELECT lesson_id, COUNT(*) AS completions
     FROM progress
     WHERE completed_at >= ${sinceExpr}
     GROUP BY lesson_id
     ORDER BY completions DESC
     LIMIT 15`
  ), []);

  // Curso: usuarios activos (con al menos 1 completion en el periodo)
  const activeLearners = await tryQ('activeLearners', async () => (await one(
    `SELECT COUNT(DISTINCT user_id) AS n FROM progress
     WHERE completed_at >= ${sinceExpr}`
  ))?.n ?? 0, 0);

  // Curso: distribución de completion por usuario (cuántas lecciones han hecho)
  // Postgres exige alias en subconsultas → "AS t"
  const completionDist = await tryQ('completionDist', async () => await q(
    `SELECT done, COUNT(*) AS users FROM (
       SELECT user_id, COUNT(*) AS done FROM progress GROUP BY user_id
     ) AS t GROUP BY done ORDER BY done ASC`
  ), []);

  // Ingresos por día
  const revenueByDay = await tryQ('revenueByDay', async () => await q(
    `SELECT ${dateOfCreated} AS day, COUNT(*) AS sales, COALESCE(SUM(amount_cents),0) AS revenue
     FROM purchases
     WHERE status = 'completed' AND created_at >= ${sinceExpr}
     GROUP BY ${dateOfCreated}
     ORDER BY day ASC`
  ), []);

  res.json({
    period_days: days,
    web: {
      total_views: totalViews,
      unique_visitors: uniqueVisitors,
      views_by_day: viewsByDay,
      top_pages: topPages,
      top_referrers: topReferrers,
    },
    funnel: {
      landing_uniques: landingUniques,
      checkout_started: checkoutStarted,
      purchases: purchasesInPeriod,
      conv_started_pct: landingUniques ? (checkoutStarted / landingUniques * 100).toFixed(2) : '0',
      conv_purchase_pct: landingUniques ? (purchasesInPeriod / landingUniques * 100).toFixed(2) : '0',
    },
    events: eventCounts,
    course: {
      active_learners: activeLearners,
      top_lessons: topLessons,
      completion_distribution: completionDist,
    },
    revenue_by_day: revenueByDay,
  });
});



// GET /api/admin/analytics-min — devuelve SOLO conteos básicos para aislar el bug
router.get('/analytics-min', async (req, res) => {
  const start = Date.now();
  const result = { tests: {}, elapsed_ms: 0 };

  // Test 1: query simple
  try {
    const t = Date.now();
    const r = await one('SELECT COUNT(*) AS n FROM page_views');
    result.tests.simple_count = { ok: true, n: r?.n ?? 0, ms: Date.now() - t };
  } catch (e) { result.tests.simple_count = { ok: false, err: e?.message }; }

  // Test 2: con dateAgo
  try {
    const t = Date.now();
    const since = sql.dateAgo(30);
    const r = await one(`SELECT COUNT(*) AS n FROM page_views WHERE created_at >= ${since}`);
    result.tests.with_dateago = { ok: true, n: r?.n ?? 0, ms: Date.now() - t, expr: since };
  } catch (e) { result.tests.with_dateago = { ok: false, err: e?.message }; }

  // Test 3: con dateOf + GROUP BY
  try {
    const t = Date.now();
    const dateOf = sql.dateOf('created_at');
    const since = sql.dateAgo(30);
    const r = await q(`SELECT ${dateOf} AS day, COUNT(*) AS n FROM page_views WHERE created_at >= ${since} GROUP BY ${dateOf} LIMIT 5`);
    result.tests.dateof_groupby = { ok: true, rows: r.length, sample: r.slice(0, 2), ms: Date.now() - t };
  } catch (e) { result.tests.dateof_groupby = { ok: false, err: e?.message }; }

  // Test 4: subquery
  try {
    const t = Date.now();
    const r = await q(`SELECT done, COUNT(*) AS users FROM (SELECT user_id, COUNT(*) AS done FROM progress GROUP BY user_id) AS t GROUP BY done`);
    result.tests.subquery = { ok: true, rows: r.length, ms: Date.now() - t };
  } catch (e) { result.tests.subquery = { ok: false, err: e?.message }; }

  // Test 5: NOT LIKE con param (el más sospechoso)
  try {
    const t = Date.now();
    const since = sql.dateAgo(30);
    const r = await q(`SELECT referrer FROM page_views WHERE created_at >= ${since} AND referrer IS NOT NULL AND referrer NOT LIKE '%' || ? || '%' LIMIT 3`,
      [(process.env.PUBLIC_URL || 'localhost').replace(/^https?:\/\//, '').replace(/\/$/, '')]);
    result.tests.not_like_param = { ok: true, rows: r.length, ms: Date.now() - t };
  } catch (e) { result.tests.not_like_param = { ok: false, err: e?.message }; }

  result.elapsed_ms = Date.now() - start;
  res.json(result);
});

// GET /api/admin/analytics-raw — diagnóstico raw para ver si hay datos en BD
router.get('/analytics-raw', async (req, res) => {
  try {
    const pageViewsTotal = (await one('SELECT COUNT(*) AS n FROM page_views'))?.n ?? 0;
    const pageViewsLast = await q('SELECT id, path, visitor_id, referrer, created_at FROM page_views ORDER BY id DESC LIMIT 10');
    const eventsTotal = (await one('SELECT COUNT(*) AS n FROM events'))?.n ?? 0;
    const eventsLast = await q('SELECT id, event_type, visitor_id, created_at FROM events ORDER BY id DESC LIMIT 10');
    res.json({
      page_views: { total: pageViewsTotal, last_10: pageViewsLast },
      events: { total: eventsTotal, last_10: eventsLast },
      now: new Date().toISOString(),
    });
  } catch (err) {
    res.status(500).json({ error: err?.message, stack: err?.stack?.split('\n').slice(0, 5) });
  }
});


// ============================================================
// Cupones — CRUD básico
// ============================================================
router.get('/coupons', async (_req, res) => {
  const rows = await q(
    `SELECT id, code, discount_pct, max_uses, uses, expires_at, active, created_at
     FROM coupons ORDER BY created_at DESC LIMIT 100`
  );
  res.json({ coupons: rows });
});

router.post('/coupons', async (req, res) => {
  const code = String(req.body?.code || '').trim().toUpperCase();
  const pct = parseInt(req.body?.discount_pct || '0', 10);
  const max = req.body?.max_uses ? parseInt(req.body.max_uses, 10) : null;
  const exp = req.body?.expires_at || null;
  if (!code || pct < 1 || pct > 100) return res.status(400).json({ error: 'Datos inválidos' });
  try {
    await exec(
      'INSERT INTO coupons (code, discount_pct, max_uses, expires_at) VALUES (?, ?, ?, ?)',
      [code, pct, max, exp]
    );
    res.json({ ok: true });
  } catch (err) {
    res.status(400).json({ error: err.message.includes('UNIQUE') || err.code === '23505' ? 'Código duplicado' : 'Error' });
  }
});

router.post('/coupons/:id/toggle', async (req, res) => {
  const id = parseInt(req.params.id, 10);
  await exec('UPDATE coupons SET active = 1 - active WHERE id = ?', [id]);
  res.json({ ok: true });
});

router.post('/coupons/:id/delete', async (req, res) => {
  const id = parseInt(req.params.id, 10);
  await exec('DELETE FROM coupons WHERE id = ?', [id]);
  res.json({ ok: true });
});

export default router;
