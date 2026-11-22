# SecureAPI

A FastAPI backend with PostgreSQL, SQLAlchemy, pytest, Docker Compose, Nginx,
Prometheus and Grafana. Local development uses `compose.yaml`; the production
stack uses `compose.prod.yaml`.

## Local development

```bash
cp .env.example .env
docker compose up -d
python -m uvicorn app.main:app --reload
```

Run the test suite and lint checks with:

```bash
pytest
ruff check .
ruff format --check .
```

## Production deployment

```bash
cp .env.example .env
mkdir -p secrets
printf '%s' 'REPLACE_WITH_DB_PASSWORD' > secrets/db_password.txt
printf '%s' 'REPLACE_WITH_GRAFANA_PASSWORD' > secrets/grafana_admin_password.txt
docker compose -f compose.prod.yaml up -d
./scripts/healthcheck.sh
```

Set `DOMAIN` in `.env` to a real DNS name before deploying to a VPS. With the
default `localhost`, the stack bootstraps a self-signed certificate. See
[docs/deployment.md](docs/deployment.md) for the full Terraform → Ansible →
Compose flow and [docs/architecture.md](docs/architecture.md) for the system
overview.

## Documentation

- [Deployment](docs/deployment.md)
- [Architecture](docs/architecture.md)
- [Security](docs/security.md)
- [Operations](docs/operations.md)
- [Backup and restore](docs/backup-restore.md)
- [Final reviews](docs/reviews.md)
- [Presentation outline](docs/presentation.md)

Items left unchecked below require a real VPS, domain, DNS and credentials; the
code and configuration needed for them are included.

## Roadmap

### Phase 3 — Production Docker

- [x] Production Dockerfile
- [x] Docker Compose for API, PostgreSQL and Redis
- [x] Environment-based configuration
- [x] Secrets management
- [x] Health checks, restart policies and persistent volumes

### Phase 4 — Nginx, DNS and HTTPS

- [x] Nginx reverse proxy
- [x] Domain and DNS configuration
- [x] HTTPS with Let's Encrypt
- [x] Security headers and request limits

### Phase 5 — Real VPS Deployment

- [ ] Provision a Linux VPS
- [x] SSH hardening and firewall configuration
- [x] Deploy SecureAPI
- [x] Configure production environment variables
- [x] Database backups and recovery
- [x] Application updates and troubleshooting

### Phase 6 — Ansible

- [x] Ansible inventory and configuration
- [x] Playbooks and roles
- [x] Automated server setup
- [x] Automated application deployment

### Phase 7 — Terraform

- [x] Infrastructure as Code
- [x] Providers and resources
- [x] Variables and outputs
- [x] State management
- [ ] Provision VPS infrastructure

### Phase 8 — Monitoring and Operations

- [x] Prometheus metrics
- [x] Grafana dashboards
- [x] Application and server logs
- [x] OpenTelemetry basics
- [x] Alerts and troubleshooting

### Phase 9 — Final Production Review

- [ ] Security review
- [ ] Test coverage review
- [ ] Deployment verification
- [ ] Backup and restore test
- [x] GitHub README and architecture documentation
- [x] Final project presentation
