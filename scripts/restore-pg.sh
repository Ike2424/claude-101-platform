#!/usr/bin/env bash
# ============================================================
# Restore Postgres desde un backup hecho con backup-pg.sh
# ============================================================
# Uso:
#   DATABASE_URL=... ./scripts/restore-pg.sh ./backups/claude101_XXX.sql.gz
#
# ⚠ DESTRUCTIVO: el backup tiene --clean --if-exists, así que DROPea las
# tablas antes de recrearlas. Confirma con I_UNDERSTAND=yes
# ============================================================
set -euo pipefail

FILE="${1:-}"
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Uso: $0 <backup.sql.gz>" >&2
  exit 1
fi

if [ -z "${DATABASE_URL:-}" ]; then
  echo "✗ DATABASE_URL no definido" >&2
  exit 1
fi

if [ "${I_UNDERSTAND:-}" != "yes" ]; then
  echo "⚠ Este script DROPea las tablas existentes y restaura desde $FILE"
  echo "  Para confirmar, ejecuta de nuevo con: I_UNDERSTAND=yes $0 $FILE"
  exit 1
fi

if ! command -v psql >/dev/null 2>&1; then
  echo "✗ psql no encontrado. Instala postgresql-client." >&2
  exit 1
fi

echo "→ Restaurando $FILE en $DATABASE_URL"
gunzip -c "$FILE" | psql "$DATABASE_URL" --single-transaction --set ON_ERROR_STOP=1
echo "✓ Restore completado."
