-- ============================================================
-- Claude 101 — Esquema de base de datos
-- Compatible con SQLite y PostgreSQL (sintaxis común)
-- ============================================================

-- USERS: identidad y estado de acceso
CREATE TABLE IF NOT EXISTS users (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  email           TEXT NOT NULL UNIQUE,
  has_paid        INTEGER NOT NULL DEFAULT 0,    -- 0/1 (boolean)
  paid_at         TEXT,                          -- ISO timestamp
  stripe_customer TEXT,                          -- cus_xxx
  created_at      TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_stripe_customer ON users(stripe_customer);

-- PURCHASES: histórico de pagos (auditoría + reconciliación)
CREATE TABLE IF NOT EXISTS purchases (
  id                       INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id                  INTEGER,
  email                    TEXT NOT NULL,         -- email tal y como llegó del checkout
  stripe_session_id        TEXT NOT NULL UNIQUE,  -- cs_xxx
  stripe_payment_intent_id TEXT,
  amount_cents             INTEGER NOT NULL,
  currency                 TEXT NOT NULL,
  status                   TEXT NOT NULL,         -- 'completed' | 'pending' | 'refunded'
  raw_event_json           TEXT,                  -- payload por completitud
  created_at               TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_purchases_email ON purchases(email);
CREATE INDEX IF NOT EXISTS idx_purchases_session ON purchases(stripe_session_id);

-- MAGIC_TOKENS: tokens passwordless de un solo uso
CREATE TABLE IF NOT EXISTS magic_tokens (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id     INTEGER NOT NULL,
  token_hash  TEXT NOT NULL UNIQUE,              -- SHA-256 del token, nunca el token en claro
  expires_at  TEXT NOT NULL,
  used_at     TEXT,                              -- NULL si no se ha usado
  ip          TEXT,                              -- ip de origen
  user_agent  TEXT,
  created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_magic_tokens_hash ON magic_tokens(token_hash);
CREATE INDEX IF NOT EXISTS idx_magic_tokens_expires ON magic_tokens(expires_at);

-- WEBHOOK_EVENTS: idempotencia de Stripe (evita procesar el mismo evento 2 veces)
CREATE TABLE IF NOT EXISTS webhook_events (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  stripe_id     TEXT NOT NULL UNIQUE,            -- evt_xxx
  type          TEXT NOT NULL,
  processed_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_webhook_events_stripe_id ON webhook_events(stripe_id);

-- PROGRESS: opcional — guarda lecciones completadas por usuario
CREATE TABLE IF NOT EXISTS progress (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id     INTEGER NOT NULL,
  lesson_id   TEXT NOT NULL,                     -- e.g. 'l1-1', 'l3-2'
  completed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (user_id, lesson_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_progress_user ON progress(user_id);

-- PAGE_VIEWS: visitas a páginas (públicas y privadas)
CREATE TABLE IF NOT EXISTS page_views (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  path       TEXT NOT NULL,                     -- '/', '/login', '/app', '/course/m1' etc
  user_id    INTEGER,                           -- NULL si es anónimo
  visitor_id TEXT,                              -- ID anónimo en localStorage (no es PII)
  referrer   TEXT,
  ip_hash    TEXT,                              -- IP hasheada (anti-PII)
  ua         TEXT,
  country    TEXT,                              -- opcional, si geo está disponible
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_page_views_path ON page_views(path);
CREATE INDEX IF NOT EXISTS idx_page_views_created ON page_views(created_at);
CREATE INDEX IF NOT EXISTS idx_page_views_visitor ON page_views(visitor_id);

-- EVENTS: eventos discretos (checkout_started, lesson_viewed, video_completed, etc)
CREATE TABLE IF NOT EXISTS events (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  event_type TEXT NOT NULL,                     -- 'checkout_started' | 'lesson_viewed' | 'video_played' | ...
  user_id    INTEGER,
  visitor_id TEXT,
  meta_json  TEXT,                              -- payload arbitrario JSON
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_created ON events(created_at);
CREATE INDEX IF NOT EXISTS idx_events_user ON events(user_id);

-- COUPONS: cupones internos (validados antes de pasar a Stripe)
CREATE TABLE IF NOT EXISTS coupons (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  code         TEXT NOT NULL UNIQUE,
  discount_pct INTEGER NOT NULL,                -- 0..100
  max_uses     INTEGER,                         -- NULL = ilimitados
  uses         INTEGER NOT NULL DEFAULT 0,
  expires_at   TEXT,                            -- NULL = sin caducidad
  active       INTEGER NOT NULL DEFAULT 1,
  created_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_coupons_code ON coupons(code);

-- CERTIFICATES: certificados de finalización del curso
CREATE TABLE IF NOT EXISTS certificates (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id     INTEGER NOT NULL,
  code        TEXT NOT NULL UNIQUE,              -- código verificable (base64url 12 chars)
  full_name   TEXT NOT NULL,                     -- nombre tal y como aparece en el certificado
  issued_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  lessons_completed INTEGER NOT NULL DEFAULT 32, -- snapshot del total
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_certificates_user ON certificates(user_id);
CREATE INDEX IF NOT EXISTS idx_certificates_code ON certificates(code);
