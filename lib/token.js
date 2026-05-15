// JWT helpers + utilidades de tokens passwordless
import 'dotenv/config';
import { logger } from './logger.js';
import crypto from 'node:crypto';
import jwt from 'jsonwebtoken';

const SECRET = process.env.JWT_SECRET;
if (!SECRET || SECRET.includes('CAMBIA_ESTO')) {
  logger.warn('⚠ JWT_SECRET no está configurado o usa el valor por defecto. Cambialo en .env');
}

const SESSION_LIFETIME = process.env.SESSION_LIFETIME || '180d';

export function signSession(payload) {
  return jwt.sign(payload, SECRET, { expiresIn: SESSION_LIFETIME });
}

export function verifySession(token) {
  try {
    return jwt.verify(token, SECRET);
  } catch {
    return null;
  }
}

// Tokens passwordless de magic link:
// - Generamos un secreto random URL-safe (32 bytes)
// - Guardamos SOLO su SHA-256 en la DB
// - En el email mandamos el secreto en claro
// Esto significa que si la DB se filtra, los tokens no se pueden usar.
export function makeMagicToken() {
  const raw = crypto.randomBytes(32).toString('base64url');
  const hash = crypto.createHash('sha256').update(raw).digest('hex');
  return { raw, hash };
}

export function hashMagicToken(raw) {
  return crypto.createHash('sha256').update(raw).digest('hex');
}
