#!/usr/bin/env node
// Purga de datos según los plazos de conservación (docs/rgpd/02-conservacion.md).
//
//   node scripts/purge.mjs            → DRY-RUN: cuenta qué borraría
//   node scripts/purge.mjs --commit   → ejecuta la purga
//
// Portable SQLite/Postgres: filtra en JS (formatos de fecha distintos entre
// motores) y borra por id. NO toca `purchases` (conservación legal).
if (!process.env.LOG_LEVEL) process.env.LOG_LEVEL = 'warn';
const { q, exec, close } = await import('../lib/db.js');

const commit = process.argv.includes('--commit');
const MONTH = 30 * 24 * 60 * 60 * 1000;
const now = Date.now();

// Plazos (configurables por env; ver documento de conservación)
const ANALYTICS_MONTHS = parseInt(process.env.ANALYTICS_RETENTION_MONTHS || '14', 10);
const LEADS_BAJA_MONTHS = parseInt(process.env.LEADS_BAJA_RETENTION_MONTHS || '12', 10);
const TOKENS_DAYS = parseInt(process.env.MAGIC_TOKEN_RETENTION_DAYS || '30', 10);

function parse(ts) {
  if (!ts) return null;
  // Acepta 'YYYY-MM-DD HH:MM:SS[.ffffff][+00]' y ISO con 'T'
  const d = new Date(String(ts).replace(' ', 'T'));
  return isNaN(d) ? null : d.getTime();
}

async function purgeTable(label, table, dateCol, cutoff, extraFilter = () => true) {
  const rows = await q(`SELECT id, ${dateCol} AS dc FROM ${table}`);
  const ids = rows.filter((r) => { const t = parse(r.dc); return t != null && t < cutoff && extraFilter(r); }).map((r) => r.id);
  if (!ids.length) { console.log(`  • ${label}: 0`); return; }
  if (commit) {
    for (let i = 0; i < ids.length; i += 500) {
      const chunk = ids.slice(i, i + 500);
      await exec(`DELETE FROM ${table} WHERE id IN (${chunk.map(() => '?').join(',')})`, chunk);
    }
    console.log(`  ✓ ${label}: ${ids.length} borrados`);
  } else {
    console.log(`  • ${label}: ${ids.length} (se borrarían)`);
  }
}

try {
  console.log(commit ? 'PURGA (REAL):' : 'PURGA (dry-run — usa --commit para ejecutar):');
  // magic_tokens usados o caducados hace más de TOKENS_DAYS
  await purgeTable(`magic_tokens usados/caducados >${TOKENS_DAYS}d`, 'magic_tokens', 'created_at',
    now - TOKENS_DAYS * 24 * 60 * 60 * 1000, (r) => true);
  // analítica propia más antigua que ANALYTICS_MONTHS
  await purgeTable(`page_views >${ANALYTICS_MONTHS}m`, 'page_views', 'created_at', now - ANALYTICS_MONTHS * MONTH);
  await purgeTable(`events >${ANALYTICS_MONTHS}m`, 'events', 'created_at', now - ANALYTICS_MONTHS * MONTH);
  // leads dados de baja hace más de LEADS_BAJA_MONTHS (ya conservada la prueba de baja)
  await purgeTable(`book_leads de baja >${LEADS_BAJA_MONTHS}m`, 'book_leads', 'unsubscribed_at', now - LEADS_BAJA_MONTHS * MONTH);
  console.log('\nNota: purchases (facturas) NO se purga — conservación legal.');
} catch (err) {
  console.error('Error:', err.message);
  process.exitCode = 1;
} finally {
  await close();
}
