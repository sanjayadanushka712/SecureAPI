#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

git pull --ff-only
docker compose -f compose.prod.yaml build
docker compose -f compose.prod.yaml up -d
./scripts/healthcheck.sh
