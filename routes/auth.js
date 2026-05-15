import { Router } from 'express';
import { logger } from '../lib/logger.js';
import rateLimit from 'express-rate-limit';
import { one, exec } from '../lib/db.js';
import { makeMagicToken, hashMagicToken, signSession, verifySession } from '../lib/token.js';
import { sendMagicLink } from '../lib/mail.js';
import * as Google from '../lib/google.js';

const router = Router();

const MINUTES = parseInt(process.env.MAGIC_LINK_LIFETIME_MIN || '20', 10);
const PUBLIC_URL = process.env.PUBLIC_URL || 'http://localhost:3000';

// Rate limiting agresivo en endpoints de auth para frenar fuerza bruta / spam de emails
const authLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 6,
  standardHeaders: true,
  legacyHeaders: false,
});

// POST /api/auth/magic-link  { email }
// Envía un enlace por email si el usuario existe y ha pagado.
// Para no filtrar quién pagó, respondemos siempre OK (enumeration-safe).
router.post('/magic-link', authLimiter, async (req, res) => {
  const email = (req.body?.email || '').trim().toLowerCase();
  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: 'Email inválido' });
  }

  const user = one('SELECT id, has_paid FROM users WHERE email = ?', [email]);

  if (user && user.has_paid) {
    const { raw, hash } = makeMagicToken();
    const expires = new Date(Date.now() + MINUTES * 60 * 1000).toISOString();
    exec(
      'INSERT INTO magic_tokens (user_id, token_hash, expires_at, ip, user_agent) VALUES (?, ?, ?, ?, ?)',
      [user.id, hash, expires, req.ip || null, req.headers['user-agent'] || null]
    );
    const link = `${PUBLIC_URL}/api/auth/verify?token=${encodeURIComponent(raw)}`;
    try {
      await sendMagicLink({ to: email, link });
    } catch (err) {
      logger.error({ err: err }, 'Error enviando magic link:');
    }
  } else {
    // Si no tiene cuenta o no ha pagado: log silencioso, respondemos OK igual
    logger.info(`[auth] magic-link solicitado para email sin acceso: ${email}`);
  }

  res.json({ ok: true, message: 'Si existe una cuenta con acceso, recibirás un email en breve.' });
});

// GET /api/auth/verify?token=...
// Marca el token como usado, emite cookie de sesión, redirige a /app
router.get('/verify', authLimiter, (req, res) => {
  const raw = String(req.query.token || '');
  if (!raw) return res.redirect('/login?error=missing');

  const hash = hashMagicToken(raw);
  const row = one(
    `SELECT mt.id, mt.user_id, mt.expires_at, mt.used_at, u.email, u.has_paid
     FROM magic_tokens mt
     JOIN users u ON u.id = mt.user_id
     WHERE mt.token_hash = ?`,
    [hash]
  );

  if (!row) return res.redirect('/login?error=invalid');
  if (row.used_at) return res.redirect('/login?error=used');
  if (new Date(row.expires_at) < new Date()) return res.redirect('/login?error=expired');
  if (!row.has_paid) return res.redirect('/?error=paywall');

  // Marcar como usado
  exec('UPDATE magic_tokens SET used_at = CURRENT_TIMESTAMP WHERE id = ?', [row.id]);

  // Emitir JWT como cookie HTTP-only
  const token = signSession({ uid: row.user_id, email: row.email });
  res.cookie('session', token, {
    httpOnly: true,
    secure: PUBLIC_URL.startsWith('https://'),
    sameSite: 'lax',
    maxAge: 1000 * 60 * 60 * 24 * 180, // 180 días, coincide con SESSION_LIFETIME por defecto
    path: '/',
  });

  res.redirect('/app');
});

// POST /api/auth/logout
router.post('/logout', (req, res) => {
  res.clearCookie('session', { path: '/' });
  res.json({ ok: true });
});

// GET /api/auth/me — útil para el frontend
router.get('/me', (req, res) => {
  const token = req.cookies?.session;
  if (!token) return res.json({ authenticated: false });
  const p = verifySession(token);
  if (!p?.uid) return res.json({ authenticated: false });
  const u = one('SELECT id, email, has_paid, paid_at FROM users WHERE id = ?', [p.uid]);
  if (!u) return res.json({ authenticated: false });
  res.json({ authenticated: true, user: { email: u.email, has_paid: !!u.has_paid, paid_at: u.paid_at } });
});

// ============================================================
// GOOGLE OAUTH
// ============================================================

// GET /api/auth/google  → redirige al consent screen de Google
router.get('/google', (req, res) => {
  if (!Google.isConfigured()) {
    return res.redirect('/login?error=google_disabled');
  }
  const state = Google.makeState();
  res.cookie('oauth_state', state, {
    httpOnly: true, sameSite: 'lax',
    secure: PUBLIC_URL.startsWith('https://'),
    maxAge: 10 * 60 * 1000, path: '/',
  });
  const redirectUri = `${PUBLIC_URL}/api/auth/google/callback`;
  res.redirect(Google.buildAuthUrl({ redirectUri, state }));
});

// GET /api/auth/google/callback  → recibe code de Google
router.get('/google/callback', async (req, res) => {
  if (!Google.isConfigured()) return res.redirect('/login?error=google_disabled');

  const code = String(req.query.code || '');
  const state = String(req.query.state || '');
  const cookieState = req.cookies?.oauth_state || '';

  // CSRF check
  if (!state || state !== cookieState || !Google.verifyState(state)) {
    return res.redirect('/login?error=oauth_state');
  }
  res.clearCookie('oauth_state', { path: '/' });

  if (!code) return res.redirect('/login?error=oauth_no_code');

  try {
    const redirectUri = `${PUBLIC_URL}/api/auth/google/callback`;
    const { id_token } = await Google.exchangeCodeForTokens({ code, redirectUri });
    const payload = await Google.verifyIdToken(id_token);
    const email = String(payload.email || '').toLowerCase();
    if (!email) return res.redirect('/login?error=oauth_no_email');

    // Buscar user. Si no existe O no ha pagado, redirige a paywall.
    let user = one('SELECT id, has_paid FROM users WHERE email = ?', [email]);
    if (!user || !user.has_paid) {
      // Si no existe, lo creamos como "registrado pero no pagado" para tracking
      if (!user) {
        exec(`INSERT INTO users (email, has_paid) VALUES (?, 0)`, [email]);
      }
      return res.redirect('/?error=paywall&email=' + encodeURIComponent(email));
    }

    // Login OK: emitir sesión
    const token = signSession({ uid: user.id, email });
    res.cookie('session', token, {
      httpOnly: true,
      secure: PUBLIC_URL.startsWith('https://'),
      sameSite: 'lax',
      maxAge: 1000 * 60 * 60 * 24 * 180,
      path: '/',
    });
    res.redirect('/app');
  } catch (err) {
    logger.error({ err: err.message }, 'Google OAuth callback error:');
    res.redirect('/login?error=oauth_failed');
  }
});

export default router;
