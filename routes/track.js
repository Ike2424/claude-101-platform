import { Router } from 'express';
import { logger } from '../lib/logger.js';
import rateLimit from 'express-rate-limit';
import crypto from 'node:crypto';
import { exec } from '../lib/db.js';
import { verifySession } from '../lib/token.js';

const router = Router();

// Hash de IP — no guardamos la IP en claro (anti-PII).
function hashIp(ip) {
  if (!ip) return null;
  const salt = process.env.JWT_SECRET || 'salt';
  return crypto.createHash('sha256').update(ip + salt).digest('hex').slice(0, 16);
}

// Resolver user_id desde la cookie de sesión si existe
function userIdFromReq(req) {
  const tk = req.cookies?.session;
  if (!tk) return null;
  const p = verifySession(tk);
  return p?.uid || null;
}

// Rate limiting suave — para evitar spam pero permitir tráfico real
const trackLimit = rateLimit({
  windowMs: 60 * 1000,
  max: 60, // 60 hits por IP por minuto
  standardHeaders: false,
  legacyHeaders: false,
});

// POST /api/track/page  { path, visitor_id, referrer }
router.post('/page', trackLimit, async (req, res) => {
  const path = String(req.body?.path || '').slice(0, 200);
  const visitor = String(req.body?.visitor_id || '').slice(0, 64) || null;
  const referrer = String(req.body?.referrer || '').slice(0, 200) || null;
  if (!path) return res.status(400).json({ error: 'path requerido' });

  try {
    await exec(
      'INSERT INTO page_views (path, user_id, visitor_id, referrer, ip_hash, ua) VALUES (?, ?, ?, ?, ?, ?)',
      [path, userIdFromReq(req), visitor, referrer, hashIp(req.ip), (req.headers['user-agent'] || '').slice(0, 250)]
    );
  } catch (err) {
    logger.error({ err: err.message }, 'track/page error:');
  }
  res.json({ ok: true });
});

// POST /api/track/event  { type, meta, visitor_id }
router.post('/event', trackLimit, async (req, res) => {
  const type = String(req.body?.type || '').slice(0, 64);
  const visitor = String(req.body?.visitor_id || '').slice(0, 64) || null;
  const meta = req.body?.meta ? JSON.stringify(req.body.meta).slice(0, 2000) : null;
  if (!type) return res.status(400).json({ error: 'type requerido' });

  try {
    await exec(
      'INSERT INTO events (event_type, user_id, visitor_id, meta_json) VALUES (?, ?, ?, ?)',
      [type, userIdFromReq(req), visitor, meta]
    );
  } catch (err) {
    logger.error({ err: err.message }, 'track/event error:');
  }
  res.json({ ok: true });
});

export default router;
