// ============================================================
// setup-demo.js — Carga datos de demo y crea super usuario.
// Idempotente: se puede correr múltiples veces sin duplicar.
//
// Uso: npm run setup-demo
//
// Esto crea:
//   1. Un super usuario demo con acceso vitalicio
//   2. Un magic link inmediato (impreso en consola)
//   3. Cupones de muestra
//   4. Page views y eventos de ejemplo para que el admin no esté vacío
// ============================================================
import 'dotenv/config';
import { one, exec } from '../lib/db.js';
import { makeMagicToken } from '../lib/token.js';

const DEMO_EMAIL = 'demo@claude101.local';
const PUBLIC_URL = process.env.PUBLIC_URL || 'http://localhost:3000';

function line(c = '─', n = 64) { return c.repeat(n); }

console.log('\n' + line('━'));
console.log('  Claude 101 — Setup demo');
console.log(line('━') + '\n');

// 1) Super usuario
let user = one('SELECT id FROM users WHERE email = ?', [DEMO_EMAIL]);
if (!user) {
  exec(
    `INSERT INTO users (email, has_paid, paid_at, stripe_customer)
     VALUES (?, 1, CURRENT_TIMESTAMP, 'cus_demo')`,
    [DEMO_EMAIL]
  );
  user = one('SELECT id FROM users WHERE email = ?', [DEMO_EMAIL]);
  console.log(`✓ Super usuario creado: ${DEMO_EMAIL} (id ${user.id})`);
} else {
  exec(
    `UPDATE users SET has_paid = 1, paid_at = COALESCE(paid_at, CURRENT_TIMESTAMP), updated_at = CURRENT_TIMESTAMP
     WHERE id = ?`,
    [user.id]
  );
  console.log(`✓ Super usuario ya existía (id ${user.id}) — reactivado acceso`);
}

// 2) Magic link inmediato
const { raw, hash } = makeMagicToken();
const expires = new Date(Date.now() + 60 * 60 * 1000).toISOString(); // 1h
exec(
  `INSERT INTO magic_tokens (user_id, token_hash, expires_at, ip, user_agent)
   VALUES (?, ?, ?, ?, ?)`,
  [user.id, hash, expires, '127.0.0.1', 'setup-demo']
);
const magicLink = `${PUBLIC_URL}/api/auth/verify?token=${encodeURIComponent(raw)}`;

// 3) Cupones de muestra
const sampleCoupons = [
  { code: 'BIENVENIDO20', pct: 20, max: null, exp: null },
  { code: 'LANZAMIENTO', pct: 30, max: 50, exp: null },
  { code: 'FRIENDS10', pct: 10, max: null, exp: null },
];
let couponsCreated = 0;
for (const c of sampleCoupons) {
  const exists = one('SELECT id FROM coupons WHERE code = ?', [c.code]);
  if (!exists) {
    exec(
      'INSERT INTO coupons (code, discount_pct, max_uses, expires_at, active) VALUES (?, ?, ?, ?, 1)',
      [c.code, c.pct, c.max, c.exp]
    );
    couponsCreated++;
  }
}
console.log(`✓ Cupones de muestra: ${couponsCreated} nuevos / ${sampleCoupons.length} totales`);

// 4) Algunas page_views y events para que el admin tenga datos
const dataExists = one('SELECT COUNT(*) AS n FROM page_views')?.n ?? 0;
if (dataExists < 50) {
  const paths = ['/', '/login', '/terminos', '/privacidad', '/', '/', '/'];
  const referrers = ['https://www.google.com/', 'https://x.com/', 'https://news.ycombinator.com/', null];
  for (let i = 0; i < 60; i++) {
    const path = paths[i % paths.length];
    const ref = referrers[i % referrers.length];
    const visitor = `seed-${Math.floor(i / 4)}`;
    exec(
      `INSERT INTO page_views (path, visitor_id, referrer, ip_hash, ua, created_at)
       VALUES (?, ?, ?, ?, ?, datetime('now', '-' || ? || ' days'))`,
      [path, visitor, ref, 'seed-hash', 'Mozilla/5.0 (seed)', Math.floor(i / 4)]
    );
  }
  // Algunos eventos
  for (let i = 0; i < 12; i++) {
    exec(
      `INSERT INTO events (event_type, visitor_id, meta_json, created_at)
       VALUES (?, ?, ?, datetime('now', '-' || ? || ' days'))`,
      [i % 3 === 0 ? 'checkout_started' : 'cta_hero_click', `seed-${i}`, '{}', Math.floor(i / 2)]
    );
  }
  console.log('✓ Datos seed para analytics insertados (60 visitas, 12 eventos)');
} else {
  console.log(`✓ Ya hay ${dataExists} page_views en DB — no se insertan más`);
}

// 5) Algunas purchases falsas para que el funnel/revenue tenga datos
const purchasesExists = one('SELECT COUNT(*) AS n FROM purchases')?.n ?? 0;
if (purchasesExists < 3) {
  for (let i = 0; i < 4; i++) {
    try {
      exec(
        `INSERT INTO purchases (user_id, email, stripe_session_id, amount_cents, currency, status, created_at)
         VALUES (?, ?, ?, ?, 'eur', 'completed', datetime('now', '-' || ? || ' days'))`,
        [user.id, DEMO_EMAIL, `cs_demo_seed_${Date.now()}_${i}`, 4900, i]
      );
    } catch {}
  }
  console.log('✓ Compras seed insertadas (4 ventas demo)');
} else {
  console.log(`✓ Ya hay ${purchasesExists} purchases — no se insertan más`);
}

// 6) Progress demo
const progressExists = one('SELECT COUNT(*) AS n FROM progress')?.n ?? 0;
if (progressExists < 3) {
  const lessons = ['l1-1', 'l1-2', 'l2-1', 'l3-1'];
  for (const l of lessons) {
    try {
      exec('INSERT INTO progress (user_id, lesson_id) VALUES (?, ?)', [user.id, l]);
    } catch {}
  }
  console.log('✓ Progreso de curso demo insertado');
}

// ============================================================
// RESUMEN
// ============================================================
console.log('\n' + line('━'));
console.log('  CREDENCIALES DE PRUEBA');
console.log(line('━'));
console.log('');
console.log('  🔑 Super usuario (acceso al curso):');
console.log(`     Email:       ${DEMO_EMAIL}`);
console.log('     Magic link válido 1 hora:');
console.log(`     ${magicLink}`);
console.log('');
console.log('  👤 Admin panel:');
console.log(`     URL:         ${PUBLIC_URL}/admin`);
console.log(`     Token:       ${process.env.ADMIN_TOKEN || '(definelo en .env)'}`);
console.log('');
console.log('  🏷️  Cupones de prueba (úsalos en la landing):');
sampleCoupons.forEach(c => console.log(`     ${c.code}  →  -${c.pct}%${c.max ? ` (máx ${c.max} usos)` : ''}`));
console.log('');
console.log(line('━'));
console.log('  ABRIR EN EL NAVEGADOR');
console.log(line('━'));
console.log('');
console.log(`  Landing:    ${PUBLIC_URL}/`);
console.log(`  Admin:      ${PUBLIC_URL}/admin`);
console.log(`  Mi cuenta:  ${PUBLIC_URL}/account  (tras usar el magic link)`);
console.log('');
console.log('  Para entrar al curso como demo: clica el magic link de arriba.');
console.log('');
