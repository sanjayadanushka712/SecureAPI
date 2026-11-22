#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

POSTGRES_USER="${POSTGRES_USER:-secureapi}"
POSTGRES_DB="${POSTGRES_DB:-secureapi}"
BACKUP_DIR="${BACKUP_DIR:-./backups}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-7}"
BACKUP_FILE="${BACKUP_DIR}/${POSTGRES_DB}_$(date +%Y%m%d_%H%M%S).dump.gz"

mkdir -p "$BACKUP_DIR"

docker compose -f compose.prod.yaml exec -T db \
    pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --format=custom | gzip > "$BACKUP_FILE"

find "$BACKUP_DIR" -maxdepth 1 -type f -name "${POSTGRES_DB}_*.dump.gz" -mtime "+${RETENTION_DAYS}" -delete

printf 'Backup created: %s\n' "$BACKUP_FILE"
