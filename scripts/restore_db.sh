#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
    printf 'Usage: %s <backup-file>\n' "$0" >&2
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    printf 'Backup file not found: %s\n' "$BACKUP_FILE" >&2
    exit 1
fi

BACKUP_FILE="$(cd "$(dirname "$BACKUP_FILE")" && pwd)/$(basename "$BACKUP_FILE")"
cd "$(dirname "${BASH_SOURCE[0]}")/.."

POSTGRES_USER="${POSTGRES_USER:-secureapi}"
POSTGRES_DB="${POSTGRES_DB:-secureapi}"

gunzip -c "$BACKUP_FILE" | docker compose -f compose.prod.yaml exec -T db \
    pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists

printf 'Restore completed from: %s\n' "$BACKUP_FILE"
