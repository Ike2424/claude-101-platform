// Structured logger con pino.
// - Producción: JSON line-by-line (compatible con Datadog/Logflare/Railway).
// - Dev: pretty colored si pino-pretty está disponible.
// Redacta automáticamente campos sensibles.
import 'dotenv/config';
import pino from 'pino';

const isProd = process.env.NODE_ENV === 'production';
const level = process.env.LOG_LEVEL || (isProd ? 'info' : 'debug');

const baseOpts = {
  level,
  base: { service: 'claude-101', env: isProd ? 'prod' : 'dev' },
  timestamp: pino.stdTimeFunctions.isoTime,
  redact: {
    paths: [
      'req.headers.authorization',
      'req.headers.cookie',
      'req.body.password',
      'req.body.token',
      'req.body.code',
      'req.body.email', // PII en logs: privacidad
      '*.token',
      '*.secret',
      '*.password',
      '*.STRIPE_SECRET_KEY',
      '*.STRIPE_WEBHOOK_SECRET',
      '*.JWT_SECRET',
      '*.ADMIN_TOKEN',
      '*.GOOGLE_CLIENT_SECRET',
      '*.RESEND_API_KEY',
    ],
    censor: '[REDACTED]',
  },
};

let transport;
if (!isProd) {
  try {
    // Solo intenta cargar pino-pretty si está instalado
    await import('pino-pretty');
    transport = { target: 'pino-pretty', options: { colorize: true, translateTime: 'HH:MM:ss', ignore: 'pid,hostname,service,env' } };
  } catch {
    // Fallback a JSON
  }
}

export const logger = transport
  ? pino({ ...baseOpts, transport })
  : pino(baseOpts);

// Para middlewares Express
export { default as httpLogger } from 'pino-http';
