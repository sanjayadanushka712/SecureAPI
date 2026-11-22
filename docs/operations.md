# Operations

## Logs

- API and proxy logs come from `docker compose -f compose.prod.yaml logs --follow api nginx`.
- Host provisioning and hardening actions are recorded by `ansible/site.yml` runs;
  keep the output with the deployment record.
- Infrastructure changes are tracked through Terraform runs in `terraform/`.
- Avoid logging secrets or full request bodies; the middleware logs metrics and
  spans only.

## Metrics

`GET /metrics` is served by the FastAPI app with content type
`text/plain; version=0.0.4; charset=utf-8`. Exposed series include:

| Metric | Meaning |
| --- | --- |
| `http_requests_total` | Total observed HTTP requests |
| `http_requests_by_route_total` | Requests by method, matched path and status |
| `http_errors_total` | Requests with a 5xx status |
| `http_request_duration_seconds_sum` / `_count` | Latency totals used for averages |
| `http_requests_in_flight` | Requests currently being processed |

Prometheus configuration in `monitoring/prometheus/prometheus.yml` scrapes
`api:8000/metrics` and `postgres-exporter:9187/metrics`. The Grafana dashboard
in `monitoring/grafana/dashboards/secureapi.json` shows request rate, error rate,
latency and service up. `/metrics` requests are excluded from observation and
blocked at Nginx, so use the internal target rather than the public domain.

## Alerts

- `APIDown`: the API target has not been scraped for one minute.
- `HighServerErrorRate`: more than 5% 5xx responses over five minutes.
- `HighRequestLatency`: average latency above one second for five minutes.

Alert rules live in `monitoring/prometheus/alerts.yml`. Route them to the team's
existing Alertmanager or notification integration; do not store credentials in
the repository.

## Troubleshooting

| Symptom | Checks |
| --- | --- |
| `/health` fails | Container status, database secret, logs of the API service |
| Nginx will not start | `cert-init` logs, `DOMAIN`, DNS, contents of the `certs` volume |
| Prometheus shows API down | Network alias `api`, port 8000, scrape path in `monitoring/prometheus/prometheus.yml` |
| Grafana panels empty | Datasource UID, dashboard provisioning path under `monitoring/`, time range |
| High 5xx rate | API logs, database connectivity, recent `./scripts/deploy.sh` changes |
| High latency | Database pool saturation, exporter metrics, request rate panel |
| Database errors after deploy | `./scripts/backup_db.sh` snapshot, then `./scripts/restore_db.sh` if needed |
| Host configuration drift | Re-run `ansible/site.yml` and compare the Terraform state in `terraform/` |

## Routine checks

- Confirm backups from `./scripts/backup_db.sh` are present and off-host daily.
- Review alerts and dashboard trends after every `./scripts/deploy.sh` release.
- Re-run the verification checklist in `docs/deployment.md` after infrastructure
  changes.
