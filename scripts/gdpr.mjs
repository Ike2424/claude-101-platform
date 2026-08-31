#!/usr/bin/env node
// Ejercicio de derechos RGPD por email.
//
//   node scripts/gdpr.mjs export <email>          → acceso + portabilidad (JSON)
//   node scripts/gdpr.mjs export <email> out.json → guarda el JSON en un fichero
//   node scripts/gdpr.mjs delete <email>          → supresión (dry-run: muestra qué borraría)
//   node scripts/gdpr.mjs delete <email> --commit → supresión REAL
//
// Regla legal: las FACTURAS (tabla purchases) tienen obligación de conservación
// (art. 30 Código de Comercio / normativa fiscal) y NO se borran. La supresión
// elimina el resto de datos personales y desvincula la cuenta.
import fs from 'node:fs';
// Silencia el log "DB connected" para que el export a stdout sea JSON limpio.
if (!process.env.LOG_LEVEL) process.env.LOG_LEVEL = 'warn';
const { q, one, exec, close, DRIVER } = await import('../lib/db.js');

const [, , action, emailArg, ...rest] = process.argv;
const email = (emailArg || '').trim().toLowerCase();
const commit = rest.includes('--commit');
const outFile = rest.find((r) => !r.startsWith('--'));

if (!action || !email || !email.includes('@')) {
  console.error('Uso: node scripts/gdpr.mjs <export|delete> <email> [out.json|--commit]');
  process.exit(1);
}

async function gatherUser() {
  const user = await one('SELECT * FROM users WHERE email = ?', [email]);
  const uid = user?.id ?? -1;
  return {
    user: user || null,
    purchases: await q('SELECT * FROM purchases WHERE email = ?', [email]),
    book_leads: await q('SELECT * FROM book_leads WHERE email = ?', [email]),
    magic_tokens: await q('SELECT id, user_id, expires_at, used_at, ip, user_agent, created_at FROM magic_tokens WHERE user_id = ?', [uid]),
    certificates: await q('SELECT * FROM certificates WHERE user_id = ?', [uid]),
    progress: await q('SELECT * FROM progress WHERE user_id = ?', [uid]),
    quiz_attempts: await q('SELECT * FROM quiz_attempts WHERE user_id = ?', [uid]),
    page_views: await q('SELECT * FROM page_views WHERE user_id = ?', [uid]),
    events: await q('SELECT * FROM events WHERE user_id = ?', [uid]),
  };
}

async function doExport() {
  const data = await gatherUser();
  const payload = { subject: email, exported_driver: DRIVER, note: 'Datos personales asociados a este email. purchases se conserva por obligación legal.', data };
  const json = JSON.stringify(payload, null, 2);
  if (outFile) { fs.writeFileSync(outFile, json); console.log(`✓ Export escrito en ${outFile}`); }
  else console.log(json);
}

async function doDelete() {
  const data = await gatherUser();
  const uid = data.user?.id ?? -1;
  const plan = [
    ['book_leads (email)', 'DELETE FROM book_leads WHERE email = ?', [email]],
    ['magic_tokens', 'DELETE FROM magic_tokens WHERE user_id = ?', [uid]],
    ['certificates (nombre)', 'DELETE FROM certificates WHERE user_id = ?', [uid]],
    ['progress', 'DELETE FROM progress WHERE user_id = ?', [uid]],
    ['quiz_attempts', 'DELETE FROM quiz_attempts WHERE user_id = ?', [uid]],
    ['page_views (desvincula)', 'UPDATE page_views SET user_id = NULL WHERE user_id = ?', [uid]],
    ['events (desvincula)', 'UPDATE events SET user_id = NULL WHERE user_id = ?', [uid]],
    ['users (cuenta)', 'DELETE FROM users WHERE email = ?', [email]],
  ];

  console.log(`Sujeto: ${email}`);
  console.log(`CONSERVADO por obligación legal: purchases (${data.purchases.length} factura/s).`);
  console.log(commit ? '\nEjecutando supresión REAL:' : '\nDRY-RUN (no borra nada). Añade --commit para ejecutar:');
  for (const [label, sql, params] of plan) {
    if (commit) { await exec(sql, params); console.log(`  ✓ ${label}`); }
    else console.log(`  • ${label}`);
  }
  if (commit) console.log('\n✓ Supresión completada. Se conservan las facturas por el plazo legal.');
}

try {
  if (action === 'export') await doExport();
  else if (action === 'delete') await doDelete();
  else { console.error(`Acción desconocida: ${action}`); process.exit(1); }
} catch (err) {
  console.error('Error:', err.message);
  process.exitCode = 1;
} finally {
  await close();
}
