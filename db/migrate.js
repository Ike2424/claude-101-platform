// Migración idempotente. Llamable en CLI o programáticamente desde server.js
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { db, DRIVER, one, close } from '../lib/db.js';
import { logger } from '../lib/logger.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function loadSchema() {
  const schemaPath = path.join(__dirname, 'schema.sql');
  let sql = fs.readFileSync(schemaPath, 'utf-8');
  if (DRIVER === 'postgres') {
    sql = sql
      .replace(/INTEGER PRIMARY KEY AUTOINCREMENT/g, 'SERIAL PRIMARY KEY')
      .replace(/\bCURRENT_TIMESTAMP\b/g, 'NOW()');
  }
  return sql;
}

export async function runMigration() {
  const sql = loadSchema();
  if (DRIVER === 'sqlite') {
    db.exec(sql);
  } else {
    // Postgres: split por ;, ignorar líneas vacías y comentarios
    const stmts = sql
      .split(/;\s*(?:\n|$)/)
      .map(s => s.trim())
      .filter(s => s && !s.startsWith('--'));
    for (const stmt of stmts) {
      try { await db.query(stmt); }
      catch (err) {
        // CREATE TABLE IF NOT EXISTS lanza notice no error en pg, pero por si acaso
        if (!/already exists/i.test(err.message)) throw err;
      }
    }
  }
}

export async function isInitialized() {
  try {
    if (DRIVER === 'sqlite') {
      const r = one("SELECT name FROM sqlite_master WHERE type='table' AND name='users'");
      return !!r;
    } else {
      const r = await one("SELECT to_regclass('public.users') AS exists");
      return !!r?.exists;
    }
  } catch { return false; }
}

// Si se ejecuta como CLI: corre y sale
const isMain = import.meta.url === `file://${process.argv[1]}`;
if (isMain) {
  logger.info({ driver: DRIVER }, 'Running migration');
  try {
    await runMigration();
    logger.info('✓ Migración completada');
    await close();
    process.exit(0);
  } catch (err) {
    logger.error({ err }, '✗ Migración falló');
    await close();
    process.exit(1);
  }
}
