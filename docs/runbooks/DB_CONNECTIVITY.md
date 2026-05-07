# Database Connectivity Runbook

OpsLedger uses Postgres as its source of truth. `/health/live` only confirms
that the API process can respond. `/health/ready` confirms that the API can
open a database connection and run a lightweight `select 1`.

## Local Configuration

The API reads `DATABASE_URL` first and `OPLEDGER_DATABASE_URL` second. If neither
is set, local development defaults to:

```sh
postgresql+psycopg://localhost:5432/opledger
```

Use local credentials you control. Do not commit real passwords, production
URLs, or shell history snippets that include secrets.

## Recognize Failures

When Postgres is unavailable, `/health/live` should still return `200` with
`{"status":"ok"}`. `/health/ready` should return `503` with a sanitized database
status and an error class, not a raw connection string or password.

Common local causes:

- Postgres is not running.
- The database or role does not exist.
- `DATABASE_URL` points at the wrong host, port, database, or driver.
- Local firewall or socket settings block the connection.

## Local Checks

Run the API:

```sh
uv run uvicorn opledger_api.main:app --app-dir services/api --reload
```

Check liveness:

```sh
curl -i http://127.0.0.1:8000/health/live
```

Check readiness:

```sh
curl -i http://127.0.0.1:8000/health/ready
```

Run migrations once domain tables exist:

```sh
DATABASE_URL=postgresql+psycopg://localhost:5432/opledger \
  uv run alembic -c services/api/alembic.ini upgrade head
```

Create future migrations after SQLAlchemy models are added:

```sh
uv run alembic -c services/api/alembic.ini revision --autogenerate -m "describe change"
```

## Dokku Later

On Dokku, attach Postgres so the deployed app receives `DATABASE_URL` from the
platform. Treat Dokku config output as sensitive because it may include
credentials.

Useful checks later:

- Confirm the app has a `DATABASE_URL` config variable.
- Confirm the Postgres service is linked to the app.
- Inspect app logs for the readiness error class.
- Run migrations during the release process before routing traffic to code that
requires new tables.

Do not paste full Dokku database URLs into issues, runbooks, commits, or chat.
