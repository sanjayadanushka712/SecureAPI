#!/bin/sh
set -eu

DB_PASSWORD_FILE="${DB_PASSWORD_FILE:-/run/secrets/db_password}"
POSTGRES_USER="${POSTGRES_USER:-secureapi}"
POSTGRES_DB="${POSTGRES_DB:-secureapi}"

if [ -f "$DB_PASSWORD_FILE" ]; then
    DB_PASSWORD=$(tr -d '\r\n' < "$DB_PASSWORD_FILE")
else
    DB_PASSWORD="${POSTGRES_PASSWORD:-secureapi_dev_password}"
fi

export POSTGRES_USER POSTGRES_DB
export DATABASE_URL="postgresql+psycopg://${POSTGRES_USER}:${DB_PASSWORD}@db:5432/${POSTGRES_DB}"
unset DB_PASSWORD

if [ "$#" -eq 0 ]; then
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers "${WEB_CONCURRENCY:-4}"
fi

exec "$@"
