#!/usr/bin/env bash
# ============================================================
# Backup Postgres con pg_dump + rotación + opcional S3
# ============================================================
# Uso:
#   ./scripts/backup-pg.sh                # backup local en ./backups/
#   S3_BUCKET=mi-bucket ./scripts/backup-pg.sh    # también sube a S3
#
# Requiere: pg_dump (postgresql-client), aws-cli si usas S3.
# Variable obligatoria: DATABASE_URL
# Rotación: mantiene los últimos N (BACKUP_RETAIN, def 14)
# Programar via cron:  0 3 * * * cd /app && DATABASE_URL=... ./scripts/backup-pg.sh
# ============================================================
set -euo pipefail

if [ -z "${DATABASE_URL:-}" ]; then
  echo "✗ DATABASE_URL no definido" >&2
  exit 1
fi

if ! command -v pg_dump >/dev/null 2>&1; then
  echo "✗ pg_dump no encontrado. Instala postgresql-client." >&2
  exit 1
fi

BACKUP_DIR="${BACKUP_DIR:-./backups}"
RETAIN="${BACKUP_RETAIN:-14}"
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
FILE="$BACKUP_DIR/claude101_${TIMESTAMP}.sql.gz"

echo "→ pg_dump → $FILE"
pg_dump "$DATABASE_URL" \
  --no-owner --no-privileges --clean --if-exists --quote-all-identifiers \
  | gzip -9 > "$FILE"

SIZE=$(du -h "$FILE" | cut -f1)
echo "✓ Backup creado ($SIZE)"

# Subir a S3 si está configurado
if [ -n "${S3_BUCKET:-}" ]; then
  if ! command -v aws >/dev/null 2>&1; then
    echo "✗ S3_BUCKET configurado pero aws-cli no instalado" >&2
    exit 1
  fi
  S3_KEY="postgres/claude101_${TIMESTAMP}.sql.gz"
  aws s3 cp "$FILE" "s3://${S3_BUCKET}/${S3_KEY}" --storage-class STANDARD_IA
  echo "✓ Subido a s3://${S3_BUCKET}/${S3_KEY}"
fi

# Rotación local: borrar más antiguos de $RETAIN
COUNT=$(ls -1 "$BACKUP_DIR"/claude101_*.sql.gz 2>/dev/null | wc -l | tr -d ' ')
if [ "$COUNT" -gt "$RETAIN" ]; then
  REMOVE=$((COUNT - RETAIN))
  echo "→ Rotación: borrando $REMOVE backups antiguos"
  ls -1t "$BACKUP_DIR"/claude101_*.sql.gz | tail -n "$REMOVE" | xargs rm -f
fi

echo "Done."
