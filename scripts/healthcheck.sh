#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

HEALTH_URL="${HEALTH_URL:-http://localhost/health}"

if command -v curl >/dev/null 2>&1 && curl -fsS "$HEALTH_URL" >/dev/null; then
    printf 'healthcheck: ok\n'
    exit 0
fi

NGINX_ID="$(docker compose -f compose.prod.yaml ps -q nginx)"
if [ -z "$NGINX_ID" ]; then
    printf 'healthcheck: nginx is not running\n' >&2
    exit 1
fi

docker exec "$NGINX_ID" sh -c \
    'curl -fsS http://localhost/health >/dev/null || wget -q -O /dev/null http://localhost/health'
printf 'healthcheck: ok\n'
