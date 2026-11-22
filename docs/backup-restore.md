# Backup and restore

PostgreSQL is the only stateful service in `compose.prod.yaml`, so backups are
taken from the database container rather than from application files.

## Backup

Run on the VPS as the service user with the production `.env` in place:

```bash
./scripts/backup_db.sh
```

The script writes a PostgreSQL dump to the configured backup directory. Confirm
the file is non-empty, timestamped, and copied to off-host storage. Keep the
backup directory outside the container's data volume and restrict permissions.

## Restore

```bash
./scripts/restore_db.sh <backup-file>
```

Before restoring:

1. Announce a maintenance window and stop or quiesce writers.
2. Take a final backup of the current state in case the restore must be undone.
3. Verify the chosen dump file and its checksum.
4. Stop the API service from `compose.prod.yaml` so it cannot write during the
   restore, then run `./scripts/restore_db.sh <backup-file>`.
5. Start the stack with `./scripts/deploy.sh` and run the verification checklist
   in `docs/deployment.md`.

## Verification drill

- [ ] Restore the most recent dump into a scratch database created via
      `ansible/site.yml` or the compose stack.
- [ ] Check row counts and a sample of task records.
- [ ] Confirm `/health` and `/metrics` on the restored instance.
- [ ] Record the duration of the backup, transfer and restore steps.
- [ ] Review retention and encryption settings for stored dumps.
