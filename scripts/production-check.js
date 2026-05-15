// ============================================================
// production-check.js — Valida que .env esté listo para producción.
// Uso: npm run check:prod
// Exit code 0 si todo OK, 1 si falta algo crítico.
// ============================================================
import 'dotenv/config';

const C = { red: '\x1b[31m', green: '\x1b[32m', yellow: '\x1b[33m', blue: '\x1b[34m', dim: '\x1b[2m', reset: '\x1b[0m', bold: '\x1b[1m' };

const env = process.env;
const isLive = String(env.PUBLIC_URL || '').startsWith('https://');

function check(name, ok, msg, opts = {}) {
  const icon = ok ? `${C.green}✓${C.reset}` : (opts.warn ? `${C.yellow}!${C.reset}` : `${C.red}✗${C.reset}`);
  const label = ok ? '' : (opts.warn ? ` ${C.yellow}(warning)${C.reset}` : ` ${C.red}(blocker)${C.reset}`);
  console.log(`  ${icon} ${name}${label}`);
  if (msg) console.log(`     ${C.dim}${msg}${C.reset}`);
  return { ok, blocker: !ok && !opts.warn };
}

function header(s) {
  console.log(`\n${C.bold}${C.blue}${s}${C.reset}`);
  console.log(C.dim + '─'.repeat(64) + C.reset);
}

console.log(`\n${C.bold}Claude 101 — Production readiness check${C.reset}\n`);
console.log(`  Public URL:  ${C.dim}${env.PUBLIC_URL || '(no definido)'}${C.reset}`);
console.log(`  Modo:        ${isLive ? C.green + 'producción' + C.reset : C.yellow + 'desarrollo' + C.reset}`);

const results = [];

header('1. Seguridad básica');
results.push(check(
  'JWT_SECRET fuerte',
  !!env.JWT_SECRET && env.JWT_SECRET.length >= 32 && !/cambia_esto|dev_only/i.test(env.JWT_SECRET),
  env.JWT_SECRET?.length < 32 ? 'Debe tener mínimo 32 chars. Usa: openssl rand -hex 32' : ''
));
results.push(check(
  'ADMIN_TOKEN fuerte',
  !!env.ADMIN_TOKEN && env.ADMIN_TOKEN.length >= 32 && !/cambia_esto|dev_admin/i.test(env.ADMIN_TOKEN),
  'Token de acceso al panel /admin'
));

header('2. Stripe');
const STRIPE_BAD = /xxxxxx|placeholder|tu_clave|change/i;
results.push(check(
  'STRIPE_SECRET_KEY',
  !!env.STRIPE_SECRET_KEY
    && /^sk_(live|test)_[A-Za-z0-9]{12,}/.test(env.STRIPE_SECRET_KEY)
    && !STRIPE_BAD.test(env.STRIPE_SECRET_KEY),
  env.STRIPE_SECRET_KEY?.startsWith('sk_test_') ? 'Modo TEST detectado. Para cobrar en producción usa sk_live_' : ''
));
results.push(check(
  'STRIPE_PUBLISHABLE_KEY',
  !!env.STRIPE_PUBLISHABLE_KEY
    && /^pk_(live|test)_[A-Za-z0-9]{12,}/.test(env.STRIPE_PUBLISHABLE_KEY)
    && !STRIPE_BAD.test(env.STRIPE_PUBLISHABLE_KEY)
));
results.push(check(
  'STRIPE_WEBHOOK_SECRET',
  !!env.STRIPE_WEBHOOK_SECRET && /^whsec_/.test(env.STRIPE_WEBHOOK_SECRET) && !env.STRIPE_WEBHOOK_SECRET.includes('xxxxxx'),
  'Webhook secret de Stripe (obtenido al configurar endpoint en dashboard)'
));
results.push(check(
  'COURSE_PRICE_CENTS',
  !!env.COURSE_PRICE_CENTS && parseInt(env.COURSE_PRICE_CENTS, 10) > 0,
  `Actual: ${env.COURSE_PRICE_CENTS || '?'} céntimos`
));

header('3. Email');
const mail = (env.MAIL_PROVIDER || '').toLowerCase();
results.push(check(
  'MAIL_PROVIDER configurado',
  ['resend', 'smtp'].includes(mail),
  mail === 'console'
    ? 'Modo console solo válido en desarrollo. En producción usa "resend" o "smtp"'
    : (mail === '' ? 'No definido. Pon MAIL_PROVIDER=resend o smtp' : ''),
  { warn: !isLive }
));
if (mail === 'resend') {
  results.push(check('RESEND_API_KEY', !!env.RESEND_API_KEY && env.RESEND_API_KEY.startsWith('re_')));
}
if (mail === 'smtp') {
  results.push(check('SMTP_HOST', !!env.SMTP_HOST));
  results.push(check('SMTP_USER', !!env.SMTP_USER));
  results.push(check('SMTP_PASS', !!env.SMTP_PASS));
}
results.push(check(
  'MAIL_FROM',
  !!env.MAIL_FROM && env.MAIL_FROM.includes('@') && !env.MAIL_FROM.includes('tudominio') && !env.MAIL_FROM.includes('localhost'),
  'Email From debe estar verificado en tu provider'
));

header('4. Dominio / URL pública');
results.push(check(
  'PUBLIC_URL en HTTPS',
  isLive,
  'En producción debe ser https://tudominio.com',
  { warn: !isLive }
));
results.push(check(
  'SUPPORT_EMAIL configurado',
  !!env.SUPPORT_EMAIL && !env.SUPPORT_EMAIL.includes('tudominio') && env.SUPPORT_EMAIL.includes('@')
));

header('5. Base de datos');
const driver = (env.DB_DRIVER || 'sqlite').toLowerCase();
results.push(check(
  `DB_DRIVER (${driver})`,
  ['sqlite', 'postgres'].includes(driver)
));
if (driver === 'postgres') {
  results.push(check('DATABASE_URL', !!env.DATABASE_URL && env.DATABASE_URL.startsWith('postgres://')));
} else if (isLive) {
  console.log(`  ${C.yellow}!${C.reset} SQLite en producción ${C.yellow}(warning)${C.reset}`);
  console.log(`     ${C.dim}SQLite vale para self-hosted con disco persistente. En Railway/Render usa Postgres.${C.reset}`);
}

header('6. Funciones opcionales');
const hasGoogle = !!(env.GOOGLE_CLIENT_ID && env.GOOGLE_CLIENT_SECRET);
console.log(`  ${hasGoogle ? C.green+'✓'+C.reset : C.dim+'·'+C.reset} Google OAuth ${hasGoogle ? '' : C.dim+'(no configurado, opcional)'+C.reset}`);
console.log(`  ${env.ENABLE_VHOST === 'true' ? C.green+'✓'+C.reset : C.dim+'·'+C.reset} Subdominios vhost ${env.ENABLE_VHOST === 'true' ? '(activado)' : C.dim+'(no activado, opcional)'+C.reset}`);
console.log(`  ${env.COMMUNITY_URL && !env.COMMUNITY_URL.includes('discord.gg/claude101') ? C.green+'✓'+C.reset : C.dim+'·'+C.reset} Discord/comunidad ${env.COMMUNITY_URL && !env.COMMUNITY_URL.includes('claude101') ? '' : C.dim+'(URL placeholder)'+C.reset}`);

// Resumen
const blockers = results.filter(r => r.blocker).length;
const warnings = results.filter(r => !r.ok && !r.blocker).length;
console.log('\n' + C.dim + '─'.repeat(64) + C.reset);
if (blockers === 0) {
  console.log(`${C.green}${C.bold}✓ READY FOR PRODUCTION${C.reset}  · ${warnings} warning(s)\n`);
  process.exit(0);
} else {
  console.log(`${C.red}${C.bold}✗ NOT READY${C.reset}  · ${blockers} blocker(s) · ${warnings} warning(s)`);
  console.log(`${C.dim}Configura los items críticos en .env y vuelve a ejecutar.${C.reset}\n`);
  process.exit(1);
}
