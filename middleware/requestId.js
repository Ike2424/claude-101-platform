// Request ID middleware.
// - Acepta X-Request-Id entrante si parece válido (correlation a través de proxies).
// - Si no, genera uno corto.
// - Lo expone como req.id, lo añade al response header y al logger via pino-http.
import crypto from 'node:crypto';

const VALID = /^[a-zA-Z0-9_-]{6,64}$/;

export function requestId(req, res, next) {
  const incoming = req.headers['x-request-id'];
  const id = (typeof incoming === 'string' && VALID.test(incoming))
    ? incoming
    : crypto.randomBytes(8).toString('hex');
  req.id = id;
  res.setHeader('X-Request-Id', id);
  next();
}
