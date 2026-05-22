// Middleware admin: comparación constante de tiempo del token contra ADMIN_TOKEN del env.
// El token se envía:
//   - Para HTML: como cookie 'admin_token' (setea POST /api/admin/login)
//   - Para API: como header Authorization: Bearer <token> O misma cookie
import crypto from 'node:crypto';

function safeEq(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string') return false;
  if (a.length !== b.length) return false;
  return crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b));
}

export function requireAdmin(req, res, next) {
  const expected = process.env.ADMIN_TOKEN;
  if (!expected || expected.startsWith('cambia_esto') || expected.startsWith('dev_admin_token')) {
    // En dev avisa, pero permite si el token coincide
    if (!expected) return res.status(500).json({ error: 'ADMIN_TOKEN no configurado' });
  }

  const fromHeader = (req.headers.authorization || '').replace(/^Bearer\s+/i, '');
  const fromCookie = req.cookies?.admin_token || '';
  const got = fromHeader || fromCookie;

  if (!safeEq(got, expected)) {
    return res.status(401).json({ error: 'No autorizado' });
  }
  next();
}
