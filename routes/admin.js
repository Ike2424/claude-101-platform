import { Router } from 'express';
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

// ============================================================
// POST /api/admin/login { token }
// Valida el token y setea cookie httpOnly.
// ============================================================
router.post('/login', (req, res) => {
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
router.get('/stats', (_req, res) => {
  const totalUsers = one('SELECT COUNT(*) AS n FROM users')?.n ?? 0;
  const paidUsers = one('SELECT COUNT(*) AS n FROM users WHERE has_paid = 1')?.n ?? 0;
  const totalRevenue = one(
    `SELECT COALESCE(SUM(amount_cents), 0) AS s FROM purchases WHERE status = 'completed'`
  )?.s ?? 0;
  const completedPurchases = one(
    `SELECT COUNT(*) AS n FROM purchases WHERE status = 'completed'`
  )?.n ?? 0;
  const refunded = one(
    `SELECT COUNT(*) AS n FROM purchases WHERE status = 'refunded'`
  )?.n ?? 0;
  // Compras por día (últimos 14 días)
  const byDay = q(
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
router.get('/users', (req, res) => {
  const limit = Math.min(parseInt(req.query.limit || '50', 10), 200);
  const offset = parseInt(req.query.offset || '0', 10);
  const search = String(req.query.search || '').trim().toLowerCase();
  const where = search ? 'WHERE LOWER(email) LIKE ?' : '';
  const params = search ? [`%${search}%`, limit, offset] : [limit, offset];
  const rows = q(
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
router.get('/purchases', (req, res) => {
  const limit = Math.min(parseInt(req.query.limit || '50', 10), 200);
  const offset = parseInt(req.query.offset || '0', 10);
  const rows = q(
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
router.post('/users/:id/revoke', (req, res) => {
  const id = parseInt(req.params.id, 10);
  if (!id) return res.status(400).json({ error: 'id inválido' });
  exec(`UPDATE users SET has_paid = 0, updated_at = CURRENT_TIMESTAMP WHERE id = ?`, [id]);
  res.json({ ok: true });
});

// ============================================================
// POST /api/admin/users/:id/grant
// ============================================================
router.post('/users/:id/grant', (req, res) => {
  const id = parseInt(req.params.id, 10);
  if (!id) return res.status(400).json({ error: 'id inválido' });
  exec(
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

  let user = one('SELECT id FROM users WHERE email = ?', [email]);
  if (!user) {
    exec(
      `INSERT INTO users (email, has_paid, paid_at) VALUES (?, 1, CURRENT_TIMESTAMP)`,
      [email]
    );
    user = one('SELECT id FROM users WHERE email = ?', [email]);
  } else {
    exec(
      `UPDATE users SET has_paid = 1, paid_at = COALESCE(paid_at, CURRENT_TIMESTAMP), updated_at = CURRENT_TIMESTAMP WHERE id = ?`,
      [user.id]
    );
  }

  // Opcional: enviar magic link inmediato
  if (req.body?.send_link) {
    try {
      const { raw, hash } = makeMagicToken();
      const expires = new Date(Date.now() + MINUTES * 60 * 1000).toISOString();
      exec(
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
router.get('/analytics', (req, res) => {
  const days = Math.min(parseInt(req.query.days || '30', 10), 365);
  // Dialect-aware: funciona en SQLite y Postgres
  const sinceExpr = sql.dateAgo(days);
  const dateOfCreated = sql.dateOf('created_at');
  const dateOfCompleted = sql.dateOf('completed_at');

  // Visitas totales y únicas
  const totalViews = one(`SELECT COUNT(*) AS n FROM page_views WHERE created_at >= ${sinceExpr}`)?.n ?? 0;
  const uniqueVisitors = one(
    `SELECT COUNT(DISTINCT visitor_id) AS n FROM page_views
     WHERE created_at >= ${sinceExpr} AND visitor_id IS NOT NULL`
  )?.n ?? 0;

  // Visitas por día (para la curva)
  const viewsByDay = q(
    `SELECT ${dateOfCreated} AS day, COUNT(*) AS views, COUNT(DISTINCT visitor_id) AS uniques
     FROM page_views
     WHERE created_at >= ${sinceExpr}
     GROUP BY ${dateOfCreated}
     ORDER BY day ASC`
  );

  // Top páginas
  const topPages = q(
    `SELECT path, COUNT(*) AS hits, COUNT(DISTINCT visitor_id) AS uniques
     FROM page_views
     WHERE created_at >= ${sinceExpr}
     GROUP BY path
     ORDER BY hits DESC
     LIMIT 15`
  );

  // Top referrers (limpia internos)
  const topReferrers = q(
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
  );

  // Eventos del periodo
  const eventCounts = q(
    `SELECT event_type, COUNT(*) AS n FROM events
     WHERE created_at >= ${sinceExpr}
     GROUP BY event_type
     ORDER BY n DESC`
  );

  // Funnel: visitas únicas a "/" → checkout_started → checkout_completed (= compras)
  const landingUniques = one(
    `SELECT COUNT(DISTINCT visitor_id) AS n FROM page_views
     WHERE created_at >= ${sinceExpr} AND path = '/' AND visitor_id IS NOT NULL`
  )?.n ?? 0;
  const checkoutStarted = one(
    `SELECT COUNT(DISTINCT visitor_id) AS n FROM events
     WHERE created_at >= ${sinceExpr} AND event_type = 'checkout_started' AND visitor_id IS NOT NULL`
  )?.n ?? 0;
  const purchasesInPeriod = one(
    `SELECT COUNT(*) AS n FROM purchases
     WHERE status = 'completed' AND created_at >= ${sinceExpr}`
  )?.n ?? 0;

  // Curso: lecciones más completadas
  const topLessons = q(
    `SELECT lesson_id, COUNT(*) AS completions
     FROM progress
     WHERE completed_at >= ${sinceExpr}
     GROUP BY lesson_id
     ORDER BY completions DESC
     LIMIT 15`
  );

  // Curso: usuarios activos (con al menos 1 completion en el periodo)
  const activeLearners = one(
    `SELECT COUNT(DISTINCT user_id) AS n FROM progress
     WHERE completed_at >= ${sinceExpr}`
  )?.n ?? 0;

  // Curso: distribución de completion por usuario (cuántas lecciones han hecho)
  // Postgres exige alias en subconsultas → "AS t"
  const completionDist = q(
    `SELECT done, COUNT(*) AS users FROM (
       SELECT user_id, COUNT(*) AS done FROM progress GROUP BY user_id
     ) AS t GROUP BY done ORDER BY done ASC`
  );

  // Ingresos por día
  const revenueByDay = q(
    `SELECT ${dateOfCreated} AS day, COUNT(*) AS sales, COALESCE(SUM(amount_cents),0) AS revenue
     FROM purchases
     WHERE status = 'completed' AND created_at >= ${sinceExpr}
     GROUP BY ${dateOfCreated}
     ORDER BY day ASC`
  );

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

// ============================================================
// Cupones — CRUD básico
// ============================================================
router.get('/coupons', (_req, res) => {
  const rows = q(
    `SELECT id, code, discount_pct, max_uses, uses, expires_at, active, created_at
     FROM coupons ORDER BY created_at DESC LIMIT 100`
  );
  res.json({ coupons: rows });
});

router.post('/coupons', (req, res) => {
  const code = String(req.body?.code || '').trim().toUpperCase();
  const pct = parseInt(req.body?.discount_pct || '0', 10);
  const max = req.body?.max_uses ? parseInt(req.body.max_uses, 10) : null;
  const exp = req.body?.expires_at || null;
  if (!code || pct < 1 || pct > 100) return res.status(400).json({ error: 'Datos inválidos' });
  try {
    exec(
      'INSERT INTO coupons (code, discount_pct, max_uses, expires_at) VALUES (?, ?, ?, ?)',
      [code, pct, max, exp]
    );
    res.json({ ok: true });
  } catch (err) {
    res.status(400).json({ error: err.message.includes('UNIQUE') ? 'Código duplicado' : 'Error' });
  }
});

router.post('/coupons/:id/toggle', (req, res) => {
  const id = parseInt(req.params.id, 10);
  exec('UPDATE coupons SET active = 1 - active WHERE id = ?', [id]);
  res.json({ ok: true });
});

router.post('/coupons/:id/delete', (req, res) => {
  const id = parseInt(req.params.id, 10);
  exec('DELETE FROM coupons WHERE id = ?', [id]);
  res.json({ ok: true });
});

export default router;
