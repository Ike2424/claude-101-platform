# syntax=docker/dockerfile:1.7
# =====================================================
# Claude 101 — production image
# Multi-stage · Node 22 LTS · non-root · slim runtime
# =====================================================

# ---------- BUILDER ----------
FROM node:22-bookworm-slim AS builder

ENV NODE_ENV=production \
    NPM_CONFIG_FUND=false \
    NPM_CONFIG_AUDIT=false

# Herramientas para compilar better-sqlite3
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 make g++ ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Cache de deps: copiar solo manifests primero
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev --include=optional || npm install --omit=dev --include=optional

# Copiar fuente
COPY . .

# Pre-compilar binarios nativos
RUN npm rebuild better-sqlite3 || true

# ---------- RUNTIME ----------
FROM node:22-bookworm-slim AS runtime

ENV NODE_ENV=production \
    PORT=3000 \
    NPM_CONFIG_FUND=false \
    NPM_CONFIG_AUDIT=false

# Solo deps de runtime, sin toolchain
RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates dumb-init \
 && rm -rf /var/lib/apt/lists/* \
 && groupadd --system --gid 1001 app \
 && useradd  --system --uid 1001 --gid app --home /app --shell /usr/sbin/nologin app

WORKDIR /app

# Copiar solo lo necesario desde el builder
COPY --from=builder --chown=app:app /build/node_modules ./node_modules
COPY --from=builder --chown=app:app /build/package.json ./package.json
COPY --from=builder --chown=app:app /build/server.js ./server.js
COPY --from=builder --chown=app:app /build/db ./db
COPY --from=builder --chown=app:app /build/lib ./lib
COPY --from=builder --chown=app:app /build/middleware ./middleware
COPY --from=builder --chown=app:app /build/routes ./routes
COPY --from=builder --chown=app:app /build/scripts ./scripts
COPY --from=builder --chown=app:app /build/public ./public

# Volumen para SQLite (si DB_DRIVER=sqlite)
RUN mkdir -p /app/db && chown -R app:app /app/db
VOLUME /app/db

USER app

EXPOSE 3000

# Healthcheck Docker (libre uso por k8s/Fly/Railway)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["node", "scripts/healthcheck.js"]

# dumb-init: PID 1 que reenvía señales correctamente (graceful shutdown OK)
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]
