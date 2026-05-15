// ============================================================
// Migra datos de SQLite → Postgres.
// Uso:
//   SOURCE_SQLITE=./db/claude101.db \
//   DATABASE_URL=postgres://user:pass@host:5432/db \
//   node scripts/migrate-sqlite-to-postgres.js
//
// Antes de correr:
//   - Asegúrate de tener el schema aplicado en Postgres:
//     DB_DRIVER=postgres DATABASE_URL=... npm run migrate
//   - Haz backup del Postgres si tiene datos previos.
//
// Por defecto NO sobrescribe filas existentes (skip on conflict).
// Pasa --truncate para borrar antes de copiar (¡destructivo!).
// ============================================================
import 'dotenv/config';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import Database from 'better-sqlite3';
import pg from 'pg';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuración bigint → int (igual que en runtime)
pg.types.setTypeParser(20, (v) => parseInt(v, 10));

const SQLITE_PATH = process.env.SOURCE_SQLITE || path.join(__dirname, '..', 'db', 'claude101.db');
const DATABASE_URL = process.env.DATABASE_URL;
const TRUNCATE = process.argv.includes('--truncate');
const DRY = process.argv.includes('--dry-run');

if (!DATABASE_URL) {
  console.error('✗ Falta DATABASE_URL');
  process.exit(1);
}

// Tablas en orden de dependencias (foreign keys)
const TABLES = [
  'users',
  'purchases',
  'magic_tokens',
  'webhook_events',
  'progress',
  'page_views',
  'events',
  'coupons',
];

function quoteIdent(name) { return `"${name}"`; }
function placeholders(n) { return Array.from({ length: n }, (_, i) => `$${i + 1}`).join(', '); }

async function main() {
  console.log(`\nSQLite → Postgres migration`);
  console.log(`  source: ${SQLITE_PATH}`);
  console.log(`  target: ${DATABASE_URL.replace(/:[^:@]+@/, ':***@')}`);
  console.log(`  mode:   ${DRY ? 'DRY-RUN (no writes)' : TRUNCATE ? 'TRUNCATE+COPY' : 'INSERT ON CONFLICT DO NOTHING'}\n`);

  const sqlite = new Database(SQLITE_PATH, { readonly: true });
  const pool = new pg.Pool({ connectionString: DATABASE_URL, ssl: DATABASE_URL.includes('sslmode=require') ? { rejectUnauthorized: false } : undefined });

  const client = await pool.connect();
  let totalRows = 0;
  try {
    if (!DRY) await client.query('BEGIN');

    for (const table of TABLES) {
      // Verificar que existe en sqlite
      const exists = sqlite.prepare(
        "SELECT name FROM sqlite_master WHERE type='table' AND name = ?"
      ).get(table);
      if (!exists) {
        console.log(`  ↷ ${table}: no existe en SQLite, salto`);
        continue;
      }
      const rows = sqlite.prepare(`SELECT * FROM ${quoteIdent(table)}`).all();
      if (!rows.length) {
        console.log(`  · ${table}: 0 filas`);
        continue;
      }

      if (TRUNCATE && !DRY) {
        await client.query(`TRUNCATE TABLE ${quoteIdent(table)} RESTART IDENTITY CASCADE`);
      }

      const cols = Object.keys(rows[0]);
      const colList = cols.map(quoteIdent).join(', ');
      const onConflict = TRUNCATE ? '' : ' ON CONFLICT DO NOTHING';

      let inserted = 0;
      for (const row of rows) {
        const values = cols.map(c => row[c]);
        if (DRY) { inserted++; continue; }
        try {
          const r = await client.query(
            `INSERT INTO ${quoteIdent(table)} (${colList}) VALUES (${placeholders(cols.length)})${onConflict}`,
            values
          );
          if (r.rowCount) inserted++;
        } catch (err) {
          console.error(`  ✗ ${table} row ${row.id || JSON.stringify(row).slice(0, 80)}: ${err.message}`);
          throw err;
        }
      }

      // Re-sincronizar secuencia AUTOINCREMENT en postgres
      if (!DRY && rows.length && cols.includes('id')) {
        const seqName = `${table}_id_seq`;
        try {
          await client.query(
            `SELECT setval($1, (SELECT COALESCE(MAX(id), 0) FROM ${quoteIdent(table)}) + 1, false)`,
            [seqName]
          );
        } catch { /* puede no haber secuencia si no se creó como SERIAL */ }
      }

      console.log(`  ✓ ${table}: ${inserted}/${rows.length} ${DRY ? 'serían copiadas' : 'copiadas'}`);
      totalRows += inserted;
    }

    if (!DRY) await client.query('COMMIT');
    console.log(`\n✓ Migración OK. Total: ${totalRows} filas.`);
  } catch (err) {
    if (!DRY) await client.query('ROLLBACK');
    console.error(`\n✗ Migración abortada: ${err.message}`);
    process.exit(1);
  } finally {
    client.release();
    await pool.end();
    sqlite.close();
  }
}

main().catch(err => { console.error(err); process.exit(1); });
