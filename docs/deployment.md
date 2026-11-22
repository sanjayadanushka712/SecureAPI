# Deployment

The production rollout is a three-step chain: `terraform/` provisions the
infrastructure, `ansible/site.yml` configures the host, and `compose.prod.yaml`
runs the application stack. `./scripts/deploy.sh` performs the final compose
update on the VPS.

## Prerequisites

- A Linux VPS with SSH access and a sudo-capable user.
- A registered domain with DNS records pointing at the VPS (and time for TTL
  propagation) before requesting TLS certificates.
- An SSH public key registered with the provider and an Ansible vault for
  domain, email and admin password values.
- Terraform state storage and an Ansible inventory for the target host.
- Firewall rules allowing HTTP/HTTPS, SSH and, if needed, restricted access to
  monitoring ports.

## Flow

1. **Infrastructure** — from `terraform/`, initialize, review the plan, then
   apply. Record the VPS IP and confirm the domain resolves to it.
2. **Configuration** — run the playbook in `ansible/site.yml`. Provide the
   domain, Certbot email and Grafana admin user through an Ansible vault or the
   host's secret store.
3. **Environment** — create the production `.env` on the VPS from the Ansible
   template. It defines `DOMAIN`, `CERTBOT_EMAIL`, `POSTGRES_DB`,
   `POSTGRES_USER`, `GRAFANA_ADMIN_USER` and backup settings. The database and
   Grafana passwords live in `./secrets/*.txt`, not in `.env`. Keep both out of
   version control and readable only by the service user.
4. **Application** — run `./scripts/deploy.sh` to build and recreate the
   services declared in `compose.prod.yaml`. The `cert-init` service issues or
   bootstraps certificates before Nginx starts.
5. **Monitoring** — verify `monitoring/prometheus/prometheus.yml` targets
   `api:8000` and `postgres-exporter:9187`, and that Grafana provisioning under
   `monitoring/` is mounted into the Grafana container.

## Verification checklist

- [ ] `curl -fsS https://<domain>/health` returns `{"status":"healthy"}`.
- [ ] Metrics are scrapeable internally at `api:8000/metrics` from Prometheus,
      and public `https://<domain>/metrics` returns 404.
- [ ] The API, database, Nginx and exporters are up in `docker compose -f compose.prod.yaml ps`.
- [ ] `cert-init` exited successfully and certificates exist under the `certs`
      volume.
- [ ] Prometheus targets are healthy at the configured endpoints.
- [ ] The Grafana "SecureAPI Overview" dashboard shows request rate, error
      rate, latency and service up panels.
- [ ] TLS certificate is valid and HTTP redirects to HTTPS.
- [ ] A smoke request creates and reads a task through the public domain.

## Rollback

1. Stop traffic at the edge or mark the host unavailable if the release is
   actively breaking requests.
2. Redeploy the previously known-good image tag with `./scripts/deploy.sh` and
   `compose.prod.yaml`, then re-run the verification checklist.
3. If the database schema is incompatible, restore the last good dump with
   `./scripts/restore_db.sh` before restarting the API.
4. If infrastructure changes caused the failure, revert the last Terraform
   change from `terraform/` and re-run `ansible/site.yml` to reconcile the host.
5. Record the cause, the rollback commands used and the follow-up action.
