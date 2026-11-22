# Security review

## Review checklist

- [ ] No secrets, tokens or credentials are committed; production values live in
      the VPS `.env`, an Ansible vault and the Terraform secret store.
- [ ] `compose.prod.yaml` exposes only the ports required by the reverse proxy
      and monitoring, and uses restart policies and persistent volumes.
- [ ] Nginx enforces HTTPS, security headers, request size limits and basic
      rate limiting.
- [ ] Database credentials are unique to production and rotated on a schedule.
- [ ] Production passwords are supplied through `./secrets/*.txt`, and the
       placeholder values created by Ansible are replaced before go-live.

- [ ] Backup artifacts produced by `./scripts/backup_db.sh` are encrypted at
      rest and access to `./scripts/restore_db.sh` is restricted.
- [ ] `/metrics` is blocked at Nginx and reachable only on the internal Compose
       network; it does not expose secrets in labels.

- [ ] Alert routing in `monitoring/` does not leak sensitive payloads.
- [ ] Dependencies are pinned in `requirements.txt` and reviewed for known
      vulnerabilities before release.
- [ ] SSH is key-only, root login is disabled, and the firewall is limited to
      required ports via `ansible/site.yml`.
- [ ] Terraform state in `terraform/` is stored remotely with restricted access
      and encryption.

## Hardening notes

- Label values in `app/monitoring.py` are escaped and normalized; numeric and
  UUID path segments are replaced with placeholders so user-supplied IDs cannot
  create unbounded metric series or inject text into the exposition format.
- The HTTP middleware records the router's matched path (for example
  `/tasks/{task_id}`) rather than the raw URL whenever it is available.
- OpenTelemetry uses the local API with no exporter, so spans carry method and
  route metadata only and do not leave the process.
- Run containers as non-root where possible, apply read-only filesystems to
  stateless services, and keep the PostgreSQL data volume private to the
  database service.
- Keep the VPS patched through the Ansible playbook and restrict access to
  Grafana and Prometheus dashboards.
- Verify backups with a scheduled restore drill; an untested backup is not a
  recovery plan.
