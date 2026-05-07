# Dokku API Incident Runbook

Use this runbook when the Phase 1 OpsLedger API misbehaves on Dokku. Gather
evidence before changing code, adding services, or changing architecture.

## First Commands

Run these from the Dokku host unless noted otherwise:

```sh
dokku ps:report opledger-api
dokku config:show opledger-api
dokku logs opledger-api --tail
```

Run these from a machine that can reach the deployed app:

```sh
curl -i http://opledger-api.YOUR_DOKKU_DOMAIN/health/live
curl -i http://opledger-api.YOUR_DOKKU_DOMAIN/health/ready
```

Do not copy full `DATABASE_URL` values into notes, issues, commits, or chat.

## Bad Environment Variable

Symptoms:

- App boots but behaves differently than expected.
- `/health/ready` reports an unexpected database host, port, or database.
- Logs show `event=database_readiness_failed`.

Checks:

```sh
dokku config:show opledger-api
```

Expected config:

- `DATABASE_URL` from `dokku postgres:link`.
- `OPLEDGER_ENVIRONMENT=dokku`.
- `OPLEDGER_DATABASE_CONNECT_TIMEOUT_SECONDS=3` or another small intentional
  value.

Response:

- Restore the last known good config value.
- Restart the app with `dokku ps:restart opledger-api`.
- Recheck `/health/live` and `/health/ready`.

## Database Unavailable

Symptoms:

- `/health/live` returns `200`.
- `/health/ready` returns `503`.
- Logs show `event=database_readiness_failed`.

Checks:

```sh
dokku postgres:info opledger-db
dokku postgres:links opledger-db
dokku logs opledger-api --tail
```

Response:

- Confirm the Postgres service exists and is linked to `opledger-api`.
- Confirm `DATABASE_URL` is present on the app.
- Restart the app only after confirming config and service state.
- Avoid increasing connection timeouts until you know why the database is slow
  or unavailable.

## Migration Failure

Symptoms:

- Deploy succeeds but CRUD routes fail.
- Alembic reports a failed revision.
- Readiness may still be healthy because the database is reachable.

Checks:

```sh
dokku run opledger-api uv run --no-sync alembic -c services/api/alembic.ini current
dokku run opledger-api uv run --no-sync alembic -c services/api/alembic.ini history
```

Response:

- Identify the revision that failed.
- Decide whether the safest repair is rerunning the migration, deploying a code
  fix, or writing a forward repair migration.
- Do not drop tables, edit production migration history, or erase data to make
  a failed deploy look clean.

## App Boot Failure

Symptoms:

- `/health/live` does not answer.
- `dokku ps:report` shows failed or restarting containers.
- Logs show import, dependency, Uvicorn, or command errors.

Checks:

```sh
dokku logs opledger-api --tail
dokku ps:report opledger-api
```

Response:

- Confirm the root `Dockerfile` was used.
- Confirm the deploy included `pyproject.toml`, `uv.lock`, and `services/api`.
- If the failure started with the latest deploy, use image rollback if
  available or revert the Git commit and redeploy.
- Run migrations only after the app image can boot.

## High Memory

Symptoms:

- The app restarts under load.
- The VPS becomes sluggish.
- Dokku or Docker reports memory pressure.

Checks:

```sh
dokku ps:report opledger-api
docker stats
free -m
```

Response:

- Keep one web process for Phase 1 unless you have measured spare capacity.
- Check for repeated failing requests or health checks creating noise.
- Prefer reducing load, fixing an obvious leak, or restoring the previous
  deploy before adding infrastructure.

## Unreadable Logs

Symptoms:

- Logs are missing request paths, status codes, or readiness failure details.
- Logs include secrets or full database URLs.
- The incident timeline cannot be reconstructed.

Checks:

```sh
dokku logs opledger-api --tail
```

Response:

- Look for `event=http_request` and `event=database_readiness_failed`.
- Record sanitized details only: status code, path, error class, host, port,
  and database name.
- Treat missing or unsafe logs as a follow-up bug after service is restored.

## Out Of Scope For This Runbook

- Redis
- Queues
- Workers
- k3s manifests
- Managed cloud databases as the default fix
- Large observability stacks before basic logs and health checks are understood
