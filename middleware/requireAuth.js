import { verifySession } from '../lib/token.js';
import { one } from '../lib/db.js';

// Lee la cookie 'session', verifica JWT, carga el usuario.
// Si no está autenticado:
//   - peticiones HTML → redirect a /login
//   - peticiones API   → 401 JSON
export async function requireAuth(req, res, next) {
  try {
    const token = req.cookies?.session;
    if (!token) return reject(req, res);

    const payload = verifySession(token);
    if (!payload?.uid) return reject(req, res);

    const user = await one('SELECT id, email, has_paid, paid_at FROM users WHERE id = ?', [payload.uid]);
    if (!user) return reject(req, res);

    req.user = user;
    next();
  } catch (err) {
    next(err);
  }
}

function reject(req, res) {
  const wantsJson = req.path.startsWith('/api/') || req.accepts(['html', 'json']) === 'json';
  if (wantsJson) return res.status(401).json({ error: 'No autenticado' });
  // Guardamos a dónde quería ir para redirigirle tras login
  const next = encodeURIComponent(req.originalUrl);
  return res.redirect(`/login?next=${next}`);
}
