# Dokku Deployment

This is the Phase 1 deployment path for the single-service OpsLedger API.
Dokku is used here because it teaches release discipline, configuration,
process logs, database attachment, explicit migrations, health checks, and
rollback thinking before the curriculum introduces orchestration.

The app already has a root `Dockerfile`, so Dokku should use Dockerfile-based
deployment. No `Procfile` is required for Phase 1.

## Assumptions

- One Linux VPS with Dokku installed.
- Docker is available through Dokku.
- The Dokku Postgres plugin is installed on the VPS.
- The deployment app name is `opledger-api`.
- The Dokku Postgres service name is `opledger-db`.
- The repository is deployed from Git.

The API image runs Uvicorn on container port `8000`, as defined by the
repo-root `Dockerfile`. Dokku should proxy public HTTP traffic to that internal
port.

## Create The App

Run these commands on the Dokku host:

```sh
dokku apps:create opledger-api
dokku proxy:ports-add opledger-api http:80:8000
```

If an incorrect proxy mapping already exists, inspect and clear it before
adding the expected mapping:

```sh
dokku proxy:ports-report opledger-api
dokku proxy:ports-clear opledger-api
dokku proxy:ports-add opledger-api http:80:8000
```

## Provision And Link Postgres

Run these commands on the Dokku host:

```sh
dokku postgres:create opledger-db
dokku postgres:link opledger-db opledger-api
```

The link provides `DATABASE_URL` to the app. Do not paste the full value into
notes, issues, commits, or chat.

Confirm the app has the expected config keys without copying secret values:

```sh
dokku config:show opledger-api
```

The API accepts either `DATABASE_URL` or `OPLEDGER_DATABASE_URL`. Prefer the
`DATABASE_URL` created by the Dokku Postgres link.

## Set App Config

Set only non-secret operational config explicitly:

```sh
dokku config:set opledger-api \
  OPLEDGER_ENVIRONMENT=dokku \
  OPLEDGER_DATABASE_CONNECT_TIMEOUT_SECONDS=3
```

Do not set `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, or
`POSTGRES_PORT` on the app. Those names are local Docker Compose inputs, not the
Dokku application contract.

## Deploy

From your local repository checkout:

```sh
git remote add dokku dokku@YOUR_DOKKU_HOST:opledger-api
git push dokku main
```

After a successful first deploy, you can tag the running image before later
deploys so there is a simple known-good image target. Run this on the Dokku
host:

```sh
dokku tags:create opledger-api previous
```

If your local branch is not named `main`, push the current branch to Dokku's
`main` branch:

```sh
git push dokku HEAD:main
```

After deploy, confirm one web process is running:

```sh
dokku ps:report opledger-api
```

## Run Migrations

Migrations are explicit. Run them after a successful deploy and before sending
normal traffic to routes that depend on the schema:

```sh
dokku run opledger-api uv run --no-sync alembic -c services/api/alembic.ini upgrade head
```

The Alembic environment reads `DATABASE_URL`, and the application converts
`postgres://` or `postgresql://` values to the SQLAlchemy `postgresql+psycopg://`
driver form internally.

## Check Health

Use the deployed hostname for normal checks:

```sh
curl -i http://opledger-api.YOUR_DOKKU_DOMAIN/health/live
curl -i http://opledger-api.YOUR_DOKKU_DOMAIN/health/ready
```

Expected results:

- `/health/live` returns `200` when the API process can answer requests.
- `/health/ready` returns `200` only when the API can connect to Postgres.
- `/health/ready` returns `503` with sanitized database target details when
  Postgres is unavailable.

If you do not have a wildcard Dokku domain, use the host and port mapping that
your Dokku install exposes.

## Inspect Logs

Read logs before changing code or configuration:

```sh
dokku logs opledger-api --tail
```

Look for:

- `event=http_request`
- `path=/health/live`
- `path=/health/ready`
- `event=database_readiness_failed`
- startup or import errors from Uvicorn
- Alembic errors from migration commands

Do not paste full connection strings or secrets into durable notes.

## Rollback Or Revert Basics

Rollback thinking should start with the smallest change that can restore
service.

If the issue is bad config, restore the previous value and restart:

```sh
dokku config:set opledger-api OPLEDGER_DATABASE_CONNECT_TIMEOUT_SECONDS=3
dokku ps:restart opledger-api
```

If the issue is a bad application deploy and you tagged the previous running
image before deploying, redeploy that known-good tag:

```sh
dokku tags:deploy opledger-api previous
```

If no known-good image tag exists or the schema changed in a risky way, revert
the Git commit locally, redeploy, and decide separately whether the database
needs a forward repair migration. Do not run destructive database changes just
to make a rollback feel clean.

Cloud platforms would change who operates Postgres, networking, TLS, and image
rollbacks. The Phase 1 default remains a self-operated Dokku VPS so those
responsibilities stay visible.
