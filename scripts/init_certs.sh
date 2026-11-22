#!/bin/sh
set -eu

DOMAIN="${DOMAIN:-localhost}"
EMAIL="${CERTBOT_EMAIL:-admin@example.com}"
LIVE_DIR="/etc/letsencrypt/live/${DOMAIN}"

if [ -f "${LIVE_DIR}/fullchain.pem" ] && [ -f "${LIVE_DIR}/privkey.pem" ]; then
    exit 0
fi

if [ "$DOMAIN" = "localhost" ]; then
    mkdir -p "$LIVE_DIR"
    openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
        -subj "/CN=${DOMAIN}" \
        -keyout "${LIVE_DIR}/privkey.pem" \
        -out "${LIVE_DIR}/fullchain.pem"
else
    certbot certonly --standalone --non-interactive --agree-tos \
        --email "$EMAIL" -d "$DOMAIN"
fi
