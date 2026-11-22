# Final project talk outline

## 1. Problem and goal (2 min)

- Why a secure, observable API is needed.
- Scope of SecureAPI: task and profile endpoints, PostgreSQL persistence.
- What phases 8-9 added: monitoring, operations and production review.

## 2. Architecture walkthrough (4 min)

- Diagram from `docs/architecture.md`.
- FastAPI middleware, routers, database and Nginx edge.
- `app/monitoring.py`: standard-library Prometheus text format, escaped labels,
  matched-route paths, bounded cardinality.
- `app/telemetry.py`: OpenTelemetry request and task-creation spans.
- Reference `monitoring/` for scrape config, alerts and Grafana provisioning.

## 3. Delivery pipeline (4 min)

- `terraform/` provisions VPS, network and DNS prerequisites.
- `ansible/site.yml` configures the host and secrets.
- `compose.prod.yaml` defines the production stack; `./scripts/deploy.sh`
  performs the release.
- External prerequisites: VPS, domain, DNS, and Docker Hub/registry credentials.

## 4. Live demonstration (5 min)

- `GET /health` and a task CRUD flow.
- `GET /metrics` showing `http_requests_total`, error and latency series.
- Grafana dashboard: request rate, error rate, latency and service up.
- Trigger an alert condition and show the notification path.

## 5. Verification and reviews (3 min)

- `pytest -q`, `ruff check app tests`, `ruff format --check app tests`.
- Test coverage, security, deployment and backup checklists from
  `docs/reviews.md`.
- Backup with `./scripts/backup_db.sh`, restore drill with
  `./scripts/restore_db.sh`.

## 6. Risks and next steps (2 min)

- Cardinality and exposure controls on `/metrics`.
- Alert tuning, log retention and backup encryption review.
- Registry credential rotation and further hardening from `docs/security.md`.

## Demo fallback

If the live environment is unavailable, use the recorded dashboard screenshots,
the sample `/metrics` output and the verification checklist from
`docs/deployment.md`.
