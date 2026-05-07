# Dokku Deployment Checklist

Use this checklist before and after deploying the Phase 1 OpsLedger API to
Dokku.

## Preflight

- Confirm the target is one Dokku VPS, not a cluster or managed app platform.
- Confirm the app name: `opledger-api`.
- Confirm the Postgres service name: `opledger-db`.
- Confirm the repo-root `Dockerfile` is present.
- Confirm the Dockerfile exposes and runs the API on container port `8000`.
- Confirm Dokku proxies public HTTP traffic to container port `8000`.
- Confirm Dokku Postgres is installed.
- Confirm `dokku postgres:link opledger-db opledger-api` has provided
  `DATABASE_URL`.
- Confirm `OPLEDGER_ENVIRONMENT=dokku`.
- Confirm `OPLEDGER_DATABASE_CONNECT_TIMEOUT_SECONDS` is set to a small value
  such as `3`.
- Confirm no real secrets are committed in `.env` files or docs.
- Run `./scripts/verify.sh` locally before pushing.
- If this is not the first deploy, tag the current known-good image before
  pushing a new one.

## Deploy

- Push the intended Git commit to Dokku.
- Confirm the app builds from the root `Dockerfile`.
- Confirm one web process is running with `dokku ps:report opledger-api`.
- Run migrations explicitly with `dokku run`.
- Confirm `/health/live` returns `200`.
- Confirm `/health/ready` returns `200`.
- Inspect `dokku logs opledger-api --tail`.
- Record sanitized evidence: commit, deploy time, health statuses, and any
  relevant log event names.
- Record whether a known-good image tag exists for rollback.

## Post-Deploy

- Exercise one basic API path that depends on the database.
- Confirm readiness still returns `200` after the API has handled traffic.
- Confirm logs are readable and do not expose full database URLs.
- Note whether any config, migration, or proxy step was surprising.
- Keep rollback notes tied to the exact deploy and migration that ran.
