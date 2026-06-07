// ============================================================
// Claude 101 — Express server (production-ready entry point)
// ============================================================
import 'dotenv/config';
import express from 'express';
import cookieParser from 'cookie-parser';
import compression from 'compression';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { logger, httpLogger } from './lib/logger.js';
import { close as closeDb } from './lib/db.js';
import { runMigration, isInitialized } from './db/migrate.js';
import { initSentry, captureException } from './lib/sentry.js';
import { requestId } from './middleware/requestId.js';

import authRouter from './routes/auth.js';
import checkoutRouter from './routes/checkout.js';
import webhookRouter from './routes/webhook.js';
import courseRouter from './routes/course.js';
import adminRouter from './routes/admin.js';
import trackRouter from './routes/track.js';
import contactRouter from './routes/contact.js';
import certificatesRouter from './routes/certificates.js';
import quizRouter from './routes/quiz.js';
import { requireAuth } from './middleware/requireAuth.js';
import { requirePaid } from './middleware/requirePaid.js';
import { vhost } from './middleware/vhost.js';
import { errorHandler } from './middleware/errorHandler.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PORT = parseInt(process.env.PORT || '3000', 10);
const PUBLIC_URL = process.env.PUBLIC_URL || `http://localhost:${PORT}`;
const isProd = process.env.NODE_ENV === 'production';

// ============================================================
// 1) Validación de env vars al arranque
// NO matamos el proceso: si JWT_SECRET falta, generamos un secret efímero
// (auth funcionará pero los tokens no sobreviven a reinicio) y avisamos
// muy fuerte en logs y en /api/status. Así el operador puede ver el
// problema en lugar de un cryptic "Healthcheck failure" de Railway.
// ============================================================
const envIssues = [];

function validateEnv() {
  if (!process.env.JWT_SECRET) {
    const tmp = `ephemeral_${Math.random().toString(36).slice(2)}${Date.now().toString(36)}`;
    process.env.JWT_SECRET = tmp;
    envIssues.push('JWT_SECRET');
    logger.error({ }, '⚠ JWT_SECRET no configurado — usando secret efímero. Configúralo en Railway: openssl rand -hex 32');
  }
  if (!process.env.STRIPE_SECRET_KEY || /placeholder/i.test(process.env.STRIPE_SECRET_KEY)) {
    envIssues.push('STRIPE_SECRET_KEY');
    logger.warn('STRIPE_SECRET_KEY no configurado o placeholder — checkouts fallarán.');
  }
  if (!process.env.STRIPE_WEBHOOK_SECRET && isProd) {
    envIssues.push('STRIPE_WEBHOOK_SECRET');
    logger.warn('STRIPE_WEBHOOK_SECRET no configurado — el webhook devolverá 400 en producción.');
  }
  if (isProd && (process.env.MAIL_PROVIDER || 'console') === 'console') {
    envIssues.push('MAIL_PROVIDER');
    logger.warn('MAIL_PROVIDER=console en producción — los magic links solo se imprimirán en logs.');
  }
}
validateEnv();

// ============================================================
// 2) Auto-migración al boot (idempotente)
// IMPORTANTE: ya NO matamos el proceso si la migración falla.
// El servidor sigue arriba para que el healthcheck de Railway responda
// y podamos diagnosticar via /healthz y /api/status. Antes hacíamos
// process.exit(1) y Railway reportaba "Healthcheck failure" sin pista.
// ============================================================
let schemaReady = false;
let schemaError = null;

async function ensureSchema() {
  try {
    const ready = await isInitialized();
    if (!ready) {
      logger.info('Schema no encontrado — ejecutando migración inicial');
    } else {
      logger.debug('Schema ya inicializado; ejecutando migración idempotente');
    }
    await runMigration();
    schemaReady = true;
    logger.info('Schema OK');
  } catch (err) {
    schemaError = err;
    logger.error({ err }, 'Fallo aplicando schema — el servidor sigue arriba para diagnóstico. Revisa /healthz y /api/status.');
  }
}

// ============================================================
// 3) Express app
// ============================================================
const app = express();

// Confiar en proxy (Railway/Render/Fly/Heroku)
app.set('trust proxy', 1);
app.disable('x-powered-by');

// HTTPS redirect en producción
app.use((req, res, next) => {
  if (isProd && req.headers['x-forwarded-proto'] === 'http') {
    return res.redirect(301, `https://${req.headers.host}${req.url}`);
  }
  next();
});

// Request ID — antes del logger para que se incluya en cada línea
app.use(requestId);

// Logger de cada request (sin payload por defecto)
app.use(httpLogger({
  logger,
  genReqId: (req) => req.id,
  customLogLevel: (req, res, err) => {
    if (err || res.statusCode >= 500) return 'error';
    if (res.statusCode >= 400) return 'warn';
    return 'debug';
  },
  serializers: {
    req: (req) => ({ method: req.method, url: req.url, id: req.id }),
    res: (res) => ({ statusCode: res.statusCode }),
  },
}));

// vhost (subdominios opt-in)
app.use(vhost);

// ============================================================
// 4) Seguridad — Helmet con CSP relajada para nuestras necesidades.
// IMPORTANTE: 'script-src-attr https://cdnjs.cloudflare.com' y 'style-src-attr' permiten inline event
// handlers (onsubmit, onclick, oninput) y estilos inline en atributos HTML,
// que el frontend de la landing usa para los formularios de checkout/login.
// Sin esto, los formularios no disparan el JS.
// ============================================================
app.use(helmet({
  contentSecurityPolicy: {
    useDefaults: true,
    directives: {
      'default-src': ["'self'"],
      'script-src': ["'self'", "'unsafe-inline'", 'https://cdnjs.cloudflare.com', 'https://www.googletagmanager.com'], // inline + cdnjs + Google Analytics
      'script-src-attr': ["'unsafe-inline'"],      // inline event handlers (onsubmit, onclick, oninput)
      'style-src': ["'self'", "'unsafe-inline'", 'https://fonts.googleapis.com'],
      'style-src-attr': ["'unsafe-inline'"],       // inline style attributes
      'font-src': ["'self'", 'https://fonts.gstatic.com', 'data:'],
      'img-src': ["'self'", 'data:', 'https:'],
      'connect-src': ["'self'", 'https://api.stripe.com', 'https://www.googletagmanager.com', 'https://www.google-analytics.com', 'https://*.google-analytics.com', 'https://*.analytics.google.com', 'https://region1.google-analytics.com'],
      'frame-src': ["'self'", 'https://js.stripe.com', 'https://hooks.stripe.com'],
      'object-src': ["'none'"],
      'base-uri': ["'self'"],
      'form-action': ["'self'", 'https://checkout.stripe.com'],
    },
  },
  crossOriginEmbedderPolicy: false, // permitimos iframes del curso
  hsts: isProd ? { maxAge: 31536000, includeSubDomains: true, preload: true } : false,
}));

// Compresión gzip
app.use(compression());

// ============================================================
// 5) CRÍTICO: webhook de Stripe necesita body RAW.
// SE MONTA ANTES de express.json().
// ============================================================
app.use('/api/stripe/webhook', webhookRouter);

// Body parsers
app.use(express.json({ limit: '64kb' }));
app.use(express.urlencoded({ extended: false, limit: '64kb' }));
app.use(cookieParser());

// Rate limit global suave (anti-DDoS básico)
app.use('/api/', rateLimit({
  windowMs: 60_000,
  max: parseInt(process.env.RATE_LIMIT_PER_MIN || '120', 10),
  standardHeaders: true,
  legacyHeaders: false,
  skip: (req) => req.path === '/api/stripe/webhook',
}));

// ============================================================
// 6) APIs
// ============================================================
app.use('/api/auth', authRouter);
app.use('/api/checkout', checkoutRouter);
app.use('/api/track', trackRouter);
app.use('/api/contact', contactRouter);
app.use('/api/admin', adminRouter);
app.use('/api/certificates', certificatesRouter);
app.use('/api/quiz', quizRouter);

// SEO
app.get('/robots.txt', (_req, res) => {
  res.type('text/plain').send(`User-agent: *
Allow: /
Disallow: /admin
Disallow: /api/
Disallow: /app
Disallow: /account
Disallow: /course.html
Disallow: /claude-101-videos/

User-agent: GPTBot
Allow: /
Disallow: /admin
Disallow: /api/

User-agent: ClaudeBot
Allow: /
Disallow: /admin
Disallow: /api/

User-agent: PerplexityBot
Allow: /
Disallow: /admin
Disallow: /api/

User-agent: Google-Extended
Allow: /

User-agent: anthropic-ai
Allow: /

Sitemap: ${PUBLIC_URL}/sitemap.xml
`);
});

app.get('/sitemap.xml', (_req, res) => {
  const urls = [
    { loc: '/', priority: '1.0', changefreq: 'weekly' },
    { loc: '/sobre', priority: '0.7', changefreq: 'monthly' },
    { loc: '/blog', priority: '0.9', changefreq: 'weekly' },
    { loc: '/blog/5-prompts-que-cambian-tu-flujo-de-trabajo', priority: '0.8', changefreq: 'monthly' },
    { loc: '/blog/claude-vs-chatgpt-cual-elegir', priority: '0.8', changefreq: 'monthly' },
    { loc: '/blog/como-empezar-con-claude', priority: '0.8', changefreq: 'monthly' },
    { loc: '/blog/que-datos-puedo-compartir-con-claude', priority: '0.8', changefreq: 'monthly' },
    { loc: '/blog/como-usar-claude-ai-guia-completa', priority: '0.8', changefreq: 'monthly' },
    { loc: '/blog/que-es-claude-ia-anthropic', priority: '0.8', changefreq: 'monthly' },
    { loc: '/blog/como-escribir-prompts-claude', priority: '0.8', changefreq: 'monthly' },
    { loc: '/blog/ia-para-pymes-autonomos', priority: '0.8', changefreq: 'monthly' },
    { loc: '/blog/claude-gratis-vs-pro', priority: '0.8', changefreq: 'monthly' },
    { loc: '/blog/claude-code-que-es', priority: '0.8', changefreq: 'monthly' },
    { loc: '/recursos', priority: '0.8', changefreq: 'monthly' },
    { loc: '/docs', priority: '0.6', changefreq: 'monthly' },
    { loc: '/comunidad', priority: '0.6', changefreq: 'monthly' },
    { loc: '/contacto', priority: '0.6', changefreq: 'monthly' },
    { loc: '/login', priority: '0.4', changefreq: 'monthly' },
    { loc: '/terminos', priority: '0.3', changefreq: 'yearly' },
    { loc: '/privacidad', priority: '0.3', changefreq: 'yearly' },
  ];
  const today = new Date().toISOString().split('T')[0];
  res.type('application/xml').send(`<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(u => `  <url>
    <loc>${PUBLIC_URL}${u.loc}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>${u.changefreq}</changefreq>
    <priority>${u.priority}</priority>
  </url>`).join('\n')}
</urlset>`);
});

// Healthcheck — SIEMPRE 200 mientras el proceso esté vivo.
// Railway hace probe a esta ruta. Si devolvemos != 2xx, marca el deploy como
// "Healthcheck failure". Por eso devolvemos 200 incluso si el schema falló:
// el operador puede ver el error en el cuerpo y en /api/status sin que Railway
// reinicie el container en bucle.
app.get('/healthz', (_req, res) => {
  res.status(200).json({
    status: 'ok',
    uptime_sec: Math.round(process.uptime()),
    node: process.version,
    db: process.env.DB_DRIVER || 'sqlite',
    env: process.env.NODE_ENV || 'development',
    schema_ready: schemaReady,
    schema_error: schemaError ? String(schemaError.message || schemaError) : null,
    timestamp: new Date().toISOString(),
  });
});

// Status (diagnóstico)
app.get('/api/status', (_req, res) => {
  const isProd2 = (process.env.NODE_ENV === 'production') || (process.env.PUBLIC_URL || '').startsWith('https://');
  const checks = {
    jwt_secret: { ok: !!process.env.JWT_SECRET && !/cambia_esto|dev_only/i.test(process.env.JWT_SECRET), critical: true },
    admin_token: { ok: !!process.env.ADMIN_TOKEN && !/cambia_esto|dev_admin/i.test(process.env.ADMIN_TOKEN), critical: true },
    stripe_secret: { ok: !!process.env.STRIPE_SECRET_KEY && !/placeholder|xxxxxx/i.test(process.env.STRIPE_SECRET_KEY), critical: true },
    stripe_webhook: { ok: !!process.env.STRIPE_WEBHOOK_SECRET && !/placeholder|xxxxxx/i.test(process.env.STRIPE_WEBHOOK_SECRET || ''), critical: true },
    mail_provider: { ok: ['resend', 'smtp'].includes((process.env.MAIL_PROVIDER || '').toLowerCase()), critical: isProd2 },
    public_url: { ok: !!process.env.PUBLIC_URL && process.env.PUBLIC_URL.startsWith('http'), critical: false },
    db_driver: { ok: !!process.env.DB_DRIVER, critical: false },
  };
  const features = {
    google_oauth: !!(process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET),
    vhost: process.env.ENABLE_VHOST === 'true',
    mail_mode: (process.env.MAIL_PROVIDER || 'console').toLowerCase(),
  };
  const blockers = Object.entries(checks).filter(([_, v]) => v.critical && !v.ok).map(([k]) => k);
  res.json({
    environment: isProd2 ? 'production' : 'development',
    ready_for_production: blockers.length === 0,
    blockers, checks, features,
    uptime_sec: Math.round(process.uptime()),
  });
});

// Config pública
app.get('/api/config', (_req, res) => {
  res.json({
    course_name: process.env.COURSE_PUBLIC_NAME || 'Claude 101',
    tagline: process.env.COURSE_TAGLINE || 'Aprende a trabajar con Claude desde cero',
    price_cents: parseInt(process.env.COURSE_PRICE_CENTS || '4900', 10),
    currency: (process.env.COURSE_CURRENCY || 'eur').toLowerCase(),
    support_email: process.env.SUPPORT_EMAIL || 'hola@claude101.com',
    community_url: process.env.COMMUNITY_URL || '#',
    company: process.env.COMPANY_NAME || 'Claude 101',
  });
});

// ============================================================
// 7) Rutas gated
// ============================================================
app.get('/app', requireAuth, requirePaid, (_req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'app.html'));
});

// Alias /app/curso → /app (algunos links históricos lo usan)
app.get('/app/curso', requireAuth, requirePaid, (_req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'app.html'));
});

// Página de progreso del usuario
app.get('/app/progreso', requireAuth, requirePaid, (_req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'progreso.html'));
});

// Glosario interactivo cruzado
app.get('/app/glosario', requireAuth, requirePaid, (_req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'glosario.html'));
});

// Playground de prompts
app.get('/app/playground', requireAuth, requirePaid, (_req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'playground.html'));
});

// Resumenes PDF
app.get('/app/resumenes', requireAuth, requirePaid, (_req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'resumenes.html'));
});

app.get('/account', requireAuth, (_req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'account.html'));
});

app.get('/course.html', requireAuth, requirePaid, (_req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'course.html'));
});

app.use('/claude-101-videos', requireAuth, requirePaid,
  express.static(path.join(__dirname, 'public', 'claude-101-videos'))
);

app.use('/api/course', requireAuth, requirePaid, courseRouter);

// 7.5) BLINDAJE DEL CONTENIDO DE PAGO
// express.static (extensions:['html']) serviría /course, /glosario.html, etc.
// SIN login+pago. Forzamos auth+pago en el acceso DIRECTO.
const PAID_PAGES = new Set([
  '/course', '/course.html',
  '/glosario', '/glosario.html',
  '/resumenes', '/resumenes.html',
  '/playground', '/playground.html',
  '/progreso', '/progreso.html',
  '/app.html',
]);
app.use((req, res, next) => {
  if (req.method === 'GET' && PAID_PAGES.has(req.path)) {
    return requireAuth(req, res, () => requirePaid(req, res, next));
  }
  next();
});

// ============================================================
// 8) Static público
// ============================================================
app.use(express.static(path.join(__dirname, 'public'), {
  index: 'index.html',
  extensions: ['html'],
  maxAge: isProd ? '1h' : 0,
  setHeaders: (res, filePath) => {
    if (filePath.endsWith('.html')) res.setHeader('Cache-Control', 'no-cache');
    if (filePath.endsWith('.css') || filePath.endsWith('.js')) {
      res.setHeader('Cache-Control', isProd ? 'public, max-age=3600' : 'no-cache');
    }
  },
}));

// 404
app.use((req, res) => {
  if (req.accepts('html')) {
    res.status(404).sendFile(path.join(__dirname, 'public', 'index.html'));
  } else {
    res.status(404).json({ error: 'Not found' });
  }
});

// Error handler (siempre el último)
app.use(errorHandler);

// ============================================================
// 9) Arranque + graceful shutdown
// ============================================================
let server;

async function start() {
  // CRÍTICO: empezamos a escuchar INMEDIATAMENTE en 0.0.0.0.
  // Railway hace healthcheck a /healthz a los pocos segundos del deploy.
  // Si app.listen() corre después de migrate/sentry init, el healthcheck
  // se cae con "Healthcheck failure" aunque la app esté bien.
  // Bind explícito a 0.0.0.0 (no localhost) — necesario en contenedores.
  server = app.listen(PORT, '0.0.0.0', () => {
    logger.info({
      port: PORT,
      host: '0.0.0.0',
      public_url: PUBLIC_URL,
      db: process.env.DB_DRIVER || 'sqlite',
      mail: process.env.MAIL_PROVIDER || 'console',
      env: process.env.NODE_ENV || 'development',
    }, 'Claude 101 listening');
  });
  server.keepAliveTimeout = 65_000;
  server.headersTimeout = 66_000;

  // Init en background — fallos aquí NO matan al servidor, solo se loguean.
  // /healthz seguirá respondiendo 200 y /api/status mostrará el problema.
  initSentry().catch(err =>
    logger.error({ err }, 'Sentry init falló (no fatal)')
  );
  ensureSchema().catch(err =>
    logger.error({ err }, 'ensureSchema lanzó una excepción inesperada (no fatal)')
  );
}

let shuttingDown = false;
async function shutdown(signal) {
  if (shuttingDown) return;
  shuttingDown = true;
  logger.info({ signal }, 'Graceful shutdown initiated');

  // 1. Dejar de aceptar conexiones nuevas
  if (server) {
    await new Promise(resolve => {
      server.close((err) => {
        if (err) logger.error({ err }, 'Error closing HTTP server');
        else logger.info('HTTP server closed');
        resolve();
      });
      // Forzar cierre tras 25s (Railway/Fly mata a los 30s)
      setTimeout(() => {
        logger.warn('Force closing after 25s');
        resolve();
      }, 25_000).unref();
    });
  }

  // 2. Cerrar DB
  await closeDb();

  logger.info('Shutdown complete');
  process.exit(0);
}

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));

process.on('unhandledRejection', (reason) => {
  logger.error({ err: reason }, 'Unhandled promise rejection');
  // No exit — dejamos que el process siga vivo. Si es repetitivo, monitoring lo detectará.
});
process.on('uncaughtException', (err) => {
  logger.fatal({ err }, 'Uncaught exception — shutting down');
  shutdown('uncaughtException').then(() => process.exit(1));
});

start().catch(err => {
  logger.fatal({ err }, 'Failed to start server');
  process.exit(1);
});
