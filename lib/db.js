// ============================================================
// DB abstraction — SQLite (dev) o Postgres (prod).
// Producción:
//   - Connection retry con backoff
//   - Graceful close para SIGTERM
//   - Logging de queries lentas
//   - API uniforme: q/one/exec con placeholders ?
// ============================================================
import 'dotenv/config';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { logger } from './logger.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const DRIVER = (process.env.DB_DRIVER || 'sqlite').toLowerCase();
const SLOW_MS = parseInt(process.env.DB_SLOW_QUERY_MS || '200', 10);

let _db;
let _ready = false;
let _closing = false;

async function connectWithRetry(connect, label, attempts = 8) {
  let lastErr;
  for (let i = 0; i < attempts; i++) {
    try {
      const result = await connect();
      logger.info({ db: label, attempt: i + 1 }, 'DB connected');
      return result;
    } catch (err) {
      lastErr = err;
      const wait = Math.min(500 * Math.pow(2, i), 5000);
      logger.warn({ db: label, attempt: i + 1, wait, err: err.message }, 'DB connect failed; retrying');
      await new Promise(r => setTimeout(r, wait));
    }
  }
  throw new Error(`No se pudo conectar a ${label} tras ${attempts} intentos: ${lastErr?.message}`);
}

if (DRIVER === 'sqlite') {
  const { default: Database } = await import('better-sqlite3');
  const dbPath = process.env.SQLITE_PATH || path.join(__dirname, '..', 'db', 'claude101.db');
  _db = await connectWithRetry(() => {
    const inst = new Database(dbPath);
    inst.pragma('journal_mode = WAL');
    inst.pragma('foreign_keys = ON');
    inst.pragma('busy_timeout = 5000');
    inst.pragma('synchronous = NORMAL');
    return inst;
  }, `sqlite (${dbPath})`);
  _ready = true;
} else if (DRIVER === 'postgres') {
  const { default: pg } = await import('pg');
  // CRÍTICO: bigint (OID 20) → int. Sin esto, COUNT(*) devuelve string y rompe comparaciones.
  pg.types.setTypeParser(20, (val) => parseInt(val, 10));
  // numeric (OID 1700) → float. COALESCE(SUM(...)) usa numeric.
  pg.types.setTypeParser(1700, (val) => parseFloat(val));
  const url = process.env.DATABASE_URL;
  if (!url) throw new Error('DATABASE_URL requerido cuando DB_DRIVER=postgres');
  _db = new pg.Pool({
    connectionString: url,
    max: parseInt(process.env.PG_POOL_MAX || '10', 10),
    idleTimeoutMillis: 30_000,
    connectionTimeoutMillis: 5_000,
    ssl: url.includes('sslmode=require') || process.env.PG_SSL === 'true' ? { rejectUnauthorized: false } : undefined,
  });
  _db.on('error', (err) => logger.error({ err }, 'Postgres pool error'));
  // Test connection
  await connectWithRetry(async () => {
    const c = await _db.connect();
    await c.query('SELECT 1');
    c.release();
    return true;
  }, 'postgres');
  _ready = true;
} else {
  throw new Error(`DB_DRIVER desconocido: ${DRIVER}`);
}

export const db = _db;
export function isReady() { return _ready && !_closing; }

// pgify — adapta SQL escrito para SQLite al dialecto de Postgres.
// - Reemplaza ? por $1, $2, ...
// - Reemplaza CURRENT_TIMESTAMP por NOW()::text (las columnas de tiempo
//   están definidas como TEXT en schema.sql; sin el cast Postgres rechaza
//   el INSERT/UPDATE con "column ... is of type text but expression is of
//   type timestamp with time zone").
function pgify(sql) {
  let i = 0;
  let s = sql.replace(/\?/g, () => `$${++i}`);
  s = s.replace(/\bCURRENT_TIMESTAMP\b/g, "NOW()::text");
  return s;
}

function logSlow(sql, ms) {
  if (ms > SLOW_MS) logger.warn({ sql: sql.slice(0, 120), ms }, 'Slow DB query');
}

export function q(sql, params = []) {
  if (_closing) throw new Error('DB closing');
  const t = Date.now();
  try {
    if (DRIVER === 'sqlite') {
      const r = _db.prepare(sql).all(...params);
      logSlow(sql, Date.now() - t);
      return r;
    }
    return _db.query(pgify(sql), params).then(r => { logSlow(sql, Date.now() - t); return r.rows; });
  } catch (err) {
    logger.error({ err, sql: sql.slice(0, 120) }, 'DB query failed');
    throw err;
  }
}

export function one(sql, params = []) {
  if (_closing) throw new Error('DB closing');
  const t = Date.now();
  try {
    if (DRIVER === 'sqlite') {
      const r = _db.prepare(sql).get(...params);
      logSlow(sql, Date.now() - t);
      return r;
    }
    return _db.query(pgify(sql), params).then(r => { logSlow(sql, Date.now() - t); return r.rows[0]; });
  } catch (err) {
    logger.error({ err, sql: sql.slice(0, 120) }, 'DB one failed');
    throw err;
  }
}

export function exec(sql, params = []) {
  if (_closing) throw new Error('DB closing');
  const t = Date.now();
  try {
    if (DRIVER === 'sqlite') {
      const r = _db.prepare(sql).run(...params);
      logSlow(sql, Date.now() - t);
      return r;
    }
    return _db.query(pgify(sql), params).then(r => { logSlow(sql, Date.now() - t); return r; });
  } catch (err) {
    logger.error({ err, sql: sql.slice(0, 120) }, 'DB exec failed');
    throw err;
  }
}

// ============================================================
// SQL helpers dialect-aware
// Para que queries con funciones de fecha funcionen en ambos drivers.
// ============================================================
export const sql = {
  // Devuelve fragmento "X días atrás" como filtro
  // Uso: q(`SELECT * FROM x WHERE created_at >= ${sql.dateAgo(30)}`)
  dateAgo(days) {
    const n = parseInt(days, 10);
    if (!Number.isFinite(n) || n < 0) throw new Error('dateAgo: days inválido');
    // En Postgres añadimos ::text porque created_at se guarda como TEXT (ISO format),
    // que ordena lexicográficamente igual que un timestamp.
    return DRIVER === 'sqlite'
      ? `datetime('now', '-${n} days')`
      : `((NOW() - INTERVAL '${n} days')::text)`;
  },
  // Devuelve el día (YYYY-MM-DD) de una columna timestamp/text
  dateOf(col) {
    return DRIVER === 'sqlite'
      ? `DATE(${col})`
      : `to_char((${col})::timestamp, 'YYYY-MM-DD')`;
  },
  // Timestamp actual
  now() {
    return DRIVER === 'sqlite' ? `CURRENT_TIMESTAMP` : `NOW()::text`;
  },
  // Quote literal seguro para LIKE (escapa %_)
  likeEscape(s) {
    return String(s).replace(/[%_\\]/g, '\\$&');
  },
};

// Helper para detectar errores de unique constraint (compatible sqlite/pg)
export function isUniqueViolation(err) {
  if (!err) return false;
  const msg = String(err.message || '');
  if (msg.includes('UNIQUE')) return true;          // SQLite
  if (err.code === '23505') return true;             // Postgres
  return false;
}

// Cierre limpio — llamado por graceful shutdown
export async function close() {
  if (_closing) return;
  _closing = true;
  logger.info({ db: DRIVER }, 'Closing DB');
  try {
    if (DRIVER === 'sqlite' && _db?.close) _db.close();
    else if (DRIVER === 'postgres' && _db?.end) await _db.end();
  } catch (err) {
    logger.error({ err }, 'Error closing DB');
  }
}
