// Captación de leads (newsletter / libro) CON prueba de consentimiento.
// El literal y la versión salen de lib/consent.js (fuente única): se usan
// para renderizar la casilla en el front y se guardan tal cual en el INSERT.
import { Router } from 'express';
import rateLimit from 'express-rate-limit';
import crypto from 'node:crypto';
import { logger } from '../lib/logger.js';
import { exec, isUniqueViolation } from '../lib/db.js';
import { CONSENT_TEXT, CONSENT_VERSION } from '../lib/consent.js';

const router = Router();

const limit = rateLimit({ windowMs: 60_000, max: 5, standardHeaders: true, legacyHeaders: false });

function hashIp(ip) {
  if (!ip) return null;
  const salt = process.env.JWT_SECRET || 'salt';
  return crypto.createHash('sha256').update(ip + salt).digest('hex').slice(0, 16);
}

// GET /api/lead/consent → literal + versión (para renderizar la casilla)
router.get('/consent', (_req, res) => {
  res.json({ text: CONSENT_TEXT, version: CONSENT_VERSION });
});

// POST /api/lead { email, consent, source? }
router.post('/', limit, async (req, res) => {
  const email = String(req.body?.email || '').trim().toLowerCase().slice(0, 200);
  const consent = req.body?.consent === true || req.body?.consent === 'true' || req.body?.consent === 'on';
  const source = String(req.body?.source || 'newsletter').trim().slice(0, 40);

  if (!email || !email.includes('@')) return res.status(400).json({ error: 'Email inválido' });
  if (!consent) return res.status(400).json({ error: 'Debes marcar la casilla de consentimiento para suscribirte.' });

  try {
    // El texto y la versión NO vienen del cliente: se sellan aquí (no repudio).
    await exec(
      `INSERT INTO book_leads (email, source, consent, consent_text, consent_version, ip_hash)
       VALUES (?, ?, 1, ?, ?, ?)`,
      [email, source, CONSENT_TEXT, CONSENT_VERSION, hashIp(req.ip)]
    );
  } catch (err) {
    if (isUniqueViolation(err)) {
      // Ya existe: reactiva (si estaba de baja) y actualiza la prueba de consentimiento.
      await exec(
        `UPDATE book_leads
         SET consent = 1, consent_text = ?, consent_version = ?, unsubscribed_at = NULL,
             source = COALESCE(source, ?), updated_at = CURRENT_TIMESTAMP
         WHERE email = ?`,
        [CONSENT_TEXT, CONSENT_VERSION, source, email]
      );
    } else {
      logger.error({ err: err.message }, 'lead insert error');
      return res.status(500).json({ error: 'No se pudo procesar. Inténtalo más tarde.' });
    }
  }

  res.json({ ok: true });
});

export default router;
