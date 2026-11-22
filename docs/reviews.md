# Final reviews

Use these checklists for the phase 9 sign-off. Record results, owners and dates
in the project tracker; do not store credentials in the repository.

## Test coverage review

- [ ] `pytest -q` passes locally and against a clean database.
- [ ] `ruff check app tests` and `ruff format --check app tests` pass.
- [ ] Task CRUD and validation tests cover success and failure cases.
- [ ] Monitoring tests cover `/metrics` status, content type, metric presence,
      and counter increments without depending on global counter values.
- [ ] Live-server tests confirm health and unknown-route behavior.
- [ ] A coverage report is reviewed for untested error branches, with no new
      dependencies added solely for reporting.

## Security review

- [ ] All items in `docs/security.md` are checked.
- [ ] Production `.env` on the VPS contains real values and is not committed.
- [ ] `./secrets/*.txt` contains rotated production values and no placeholders.
- [ ] HTTPS, firewall and SSH settings applied by `ansible/site.yml` are verified.
- [ ] `terraform/` state and variables contain no plaintext secrets.
- [ ] `/metrics` labels cannot carry raw user IDs or arbitrary paths.

## Deployment review

- [ ] `terraform/` plan matches the intended VPS, network and DNS state.
- [ ] `ansible/site.yml` runs cleanly from a fresh host.
- [ ] `compose.prod.yaml` starts all services with correct restart policies.
- [ ] Rollout via `./scripts/deploy.sh` completed without manual changes.
- [ ] Every verification item in `docs/deployment.md` passed.
- [ ] Alert rules and dashboard in `monitoring/` produce expected data.

## Backup and restore review

- [ ] `./scripts/backup_db.sh` produces a restorable, encrypted dump.
- [ ] Retention and off-host copy are configured and verified.
- [ ] A restore drill with `./scripts/restore_db.sh` succeeded and was timed.
- [ ] The rollback procedure in `docs/deployment.md` was rehearsed.
- [ ] Gaps and follow-up actions are recorded with owners.
