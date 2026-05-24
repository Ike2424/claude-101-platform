// Sistema de certificados de finalización
import { Router } from 'express';
import crypto from 'node:crypto';
import { one, exec, q } from '../lib/db.js';
import { logger } from '../lib/logger.js';
import { requireAuth } from '../middleware/requireAuth.js';
import { requirePaid } from '../middleware/requirePaid.js';

const router = Router();

const TOTAL_LESSONS = 32;

// Genera código único base64url 12 caracteres
function makeCode() {
  return crypto.randomBytes(9).toString('base64url');
}

// Devuelve el certificado del usuario (si lo tiene) — gated por auth+paid
router.get('/me', requireAuth, requirePaid, async (req, res) => {
  const cert = await one(
    'SELECT id, code, full_name, issued_at FROM certificates WHERE user_id = ?',
    [req.user.id]
  );
  if (!cert) {
    // Comprobar si tiene completed=32 para mostrar el botón
    const r = await one('SELECT COUNT(*) AS n FROM progress WHERE user_id = ?', [req.user.id]);
    const completed = r?.n ?? 0;
    return res.json({ has_certificate: false, completed, total: TOTAL_LESSONS, eligible: completed >= TOTAL_LESSONS });
  }
  res.json({ has_certificate: true, ...cert, verify_url: `${process.env.PUBLIC_URL}/verify/${cert.code}` });
});

// Emite certificado (POST con full_name)
router.post('/issue', requireAuth, requirePaid, async (req, res) => {
  const fullName = String(req.body?.full_name || '').trim().slice(0, 100);
  if (!fullName || fullName.length < 2) {
    return res.status(400).json({ error: 'Nombre inválido (mínimo 2 caracteres)' });
  }

  // Verificar que tiene 32 lecciones completadas
  const r = await one('SELECT COUNT(*) AS n FROM progress WHERE user_id = ?', [req.user.id]);
  const completed = r?.n ?? 0;
  if (completed < TOTAL_LESSONS) {
    return res.status(400).json({ error: `Completa todas las lecciones primero (${completed}/${TOTAL_LESSONS})` });
  }

  // ¿Ya tiene certificado?
  const existing = await one('SELECT code FROM certificates WHERE user_id = ?', [req.user.id]);
  if (existing) {
    return res.json({ ok: true, code: existing.code, already_existed: true });
  }

  // Emitir nuevo
  const code = makeCode();
  try {
    await exec(
      'INSERT INTO certificates (user_id, code, full_name, lessons_completed) VALUES (?, ?, ?, ?)',
      [req.user.id, code, fullName, completed]
    );
    logger.info({ user_id: req.user.id, code }, 'Certificate issued');
    res.json({ ok: true, code, verify_url: `${process.env.PUBLIC_URL}/verify/${code}` });
  } catch (err) {
    logger.error({ err: err.message }, 'Error issuing certificate');
    res.status(500).json({ error: 'No se pudo emitir el certificado' });
  }
});

// Validación pública por código (sin auth, página pública)
router.get('/verify/:code', async (req, res) => {
  const code = String(req.params.code || '').trim();
  if (!code) return res.status(400).json({ valid: false, error: 'Código requerido' });

  const cert = await one(
    `SELECT c.code, c.full_name, c.issued_at, c.lessons_completed, u.email
     FROM certificates c
     LEFT JOIN users u ON u.id = c.user_id
     WHERE c.code = ?`,
    [code]
  );
  if (!cert) return res.status(404).json({ valid: false, error: 'Certificado no encontrado' });

  res.json({
    valid: true,
    full_name: cert.full_name,
    issued_at: cert.issued_at,
    lessons_completed: cert.lessons_completed,
    course: 'Claude 101 — Aprende a trabajar con Claude',
    issuer: 'Tacto Agencia SLU · academia101.com',
  });
});

export default router;
