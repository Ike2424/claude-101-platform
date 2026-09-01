// Migraciones incrementales idempotentes, compatibles con SQLite y Postgres.
// Se ejecutan tras runMigration() (schema.sql). Añadir columnas a tablas ya
// creadas no es idempotente "de fábrica" en SQLite (no soporta IF NOT EXISTS
// en ADD COLUMN), así que comprobamos antes de alterar.
import { db, DRIVER } from '../lib/db.js';
import { logger } from '../lib/logger.js';

async function columnExists(table, column) {
  if (DRIVER === 'sqlite') {
    const rows = db.prepare(`PRAGMA table_info(${table})`).all();
    return rows.some((r) => r.name === column);
  }
  const r = await db.query(
    `SELECT 1 FROM information_schema.columns WHERE table_name = $1 AND column_name = $2`,
    [table, column]
  );
  return r.rowCount > 0;
}

async function tableExists(table) {
  if (DRIVER === 'sqlite') {
    const r = db.prepare(`SELECT name FROM sqlite_master WHERE type='table' AND name=?`).get(table);
    return !!r;
  }
  const r = await db.query(`SELECT to_regclass($1) AS t`, [`public.${table}`]);
  return !!r.rows?.[0]?.t;
}

// Añade una columna solo si no existe. `def` es el fragmento SQL del tipo
// (idéntico en ambos motores para tipos simples como TEXT/INTEGER).
export async function ensureColumn(table, column, def) {
  if (!(await tableExists(table))) return false;
  if (await columnExists(table, column)) return false;
  if (DRIVER === 'sqlite') {
    db.exec(`ALTER TABLE ${table} ADD COLUMN ${column} ${def}`);
  } else {
    await db.query(`ALTER TABLE ${table} ADD COLUMN IF NOT EXISTS ${column} ${def}`);
  }
  logger.info({ table, column }, 'Migración: columna añadida');
  return true;
}

// Punto de entrada llamado desde server.js tras runMigration().
export async function runExtraMigrations() {
  try {
    // Bloque 2 — prueba del consentimiento (por si la tabla es anterior a estas columnas)
    await ensureColumn('book_leads', 'consent_text', 'TEXT');
    await ensureColumn('book_leads', 'consent_version', 'TEXT');
    await ensureColumn('book_leads', 'ip_hash', 'TEXT');
    // Bloque 3 — baja
    await ensureColumn('book_leads', 'unsubscribed_at', 'TEXT');
  } catch (err) {
    logger.error({ err: err.message }, 'runExtraMigrations falló');
  }
}
