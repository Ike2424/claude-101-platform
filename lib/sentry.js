// Sentry opt-in. Si SENTRY_DSN no está configurado, todas las funciones son no-op.
// Esto permite mantener Sentry como dependencia opcional sin romper el boot.
import { logger } from './logger.js';

let _Sentry = null;
let _initialized = false;

export async function initSentry() {
  const dsn = process.env.SENTRY_DSN;
  if (!dsn) {
    logger.debug('SENTRY_DSN no configurado — monitoring desactivado');
    return null;
  }
  try {
    const Sentry = await import('@sentry/node');
    Sentry.init({
      dsn,
      environment: process.env.NODE_ENV || 'development',
      tracesSampleRate: parseFloat(process.env.SENTRY_TRACES_SAMPLE_RATE || '0.1'),
      release: process.env.RELEASE_VERSION || 'claude-101@1.0.0',
      beforeSend(event) {
        // No enviar errores 4xx, ya están en logs
        if (event.tags?.status_code && event.tags.status_code < 500) return null;
        return event;
      },
    });
    _Sentry = Sentry;
    _initialized = true;
    logger.info({ env: process.env.NODE_ENV }, 'Sentry initialized');
    return Sentry;
  } catch (err) {
    logger.warn({ err: err.message }, 'No se pudo inicializar Sentry (no instalado). Continúa sin él.');
    return null;
  }
}

export function captureException(err, context = {}) {
  if (!_initialized) return;
  try { _Sentry.captureException(err, { extra: context }); } catch {}
}

export function captureMessage(msg, level = 'info') {
  if (!_initialized) return;
  try { _Sentry.captureMessage(msg, level); } catch {}
}

export function isEnabled() { return _initialized; }
