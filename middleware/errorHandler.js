// Global error handler. Debe ir AL FINAL del stack de middlewares.
import { logger } from '../lib/logger.js';
import { captureException } from '../lib/sentry.js';

export function errorHandler(err, req, res, _next) {
  const status = err.status || err.statusCode || 500;
  const expose = status < 500;

  // Logging diferenciado: 4xx info, 5xx error con stack
  if (status >= 500) {
    logger.error({ err, path: req.path, method: req.method, request_id: req.id }, 'Unhandled error');
    captureException(err, { path: req.path, method: req.method, request_id: req.id });
  } else {
    logger.warn({ status, msg: err.message, path: req.path, request_id: req.id }, 'Client error');
  }

  // Si ya empezamos a enviar respuesta, delegar a Express
  if (res.headersSent) return;

  const wantsJson = req.path.startsWith('/api/') || req.accepts(['html', 'json']) === 'json';

  if (wantsJson) {
    return res.status(status).json({
      error: expose ? err.message : 'Error interno',
      ...(process.env.NODE_ENV !== 'production' && status >= 500 ? { stack: err.stack } : {}),
    });
  }
  return res.status(status).send(expose ? err.message : 'Error interno');
}
