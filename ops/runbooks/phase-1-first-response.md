# Phase 1 First Response Runbook

Use this runbook when the Phase 1 OpsLedger API behaves unexpectedly. The goal
is to gather evidence before changing code or adding infrastructure.

## First Checks

Confirm the API process is live:

```sh
curl -i http://127.0.0.1:18080/health/live
```

Confirm the API can reach Postgres:

```sh
curl -i http://127.0.0.1:18080/health/ready
```

Interpretation:

- `/health/live` returning `200` means the process can answer a simple request.
- `/health/ready` returning `503` means the process should not receive normal
  traffic because a required dependency is unavailable.
- A live process is not the same as a ready service.

## Logs

Inspect the API process logs before editing code. Phase 1 logs should show:

- timestamp
- level
- request method
- request path
- response status
- request duration
- sanitized database readiness failure details when readiness fails

Look for `event=http_request` and `event=database_readiness_failed`.

Do not paste full connection strings, credentials, tokens, or request bodies
into notes, issues, commits, or chat.

## Environment Variables

Check the values that control database access without exposing secrets:

- Is `DATABASE_URL` set?
- If not, is `OPLEDGER_DATABASE_URL` set?
- Does the value point at the expected host, port, and database?
- Is the driver compatible with the API's SQLAlchemy configuration?
- Is the connect timeout unexpectedly high or low?

Use sanitized notes such as `host=localhost port=55432 database=opledger`.
Avoid recording usernames, passwords, or full URLs.

## Database Reachability

Check whether Postgres is running and reachable from the same machine or
environment as the API.

Local examples:

```sh
curl -i http://127.0.0.1:18080/health/ready
```

If you use `psql`, prefer a local development connection and avoid copying the
full URL into durable notes. Confirm:

- the server is listening on the expected port
- the database exists
- the role has permission to connect
- the API can run a basic query

## Recent Migrations

If readiness is healthy but CRUD routes fail, check whether the database schema
matches the current code.

Ask:

- Did a migration run before this code started serving traffic?
- Did a recent migration fail partway through?
- Does the failing route depend on a new table, column, constraint, or enum-like
  check?
- Is the failure a schema mismatch rather than a code path bug?

For local development, the migration command is:

```sh
DATABASE_URL=postgresql+psycopg://localhost:55432/opledger \
  uv run alembic -c services/api/alembic.ini upgrade head
```

For the Phase 1 Docker Compose workflow, run migrations inside the API
container:

```sh
./scripts/migrate.sh --compose
```

Use only local credentials you control.

## Rollback Thinking

Before changing code, decide whether the safest move is to restore the last
known working state.

Ask:

- Did the problem start immediately after a code deploy, config change, or
  migration?
- Can the app run correctly with the previous code and current schema?
- Did the migration make rollback risky because it changed or removed data?
- Is the user impact reduced more quickly by restoring config than by editing
  application code?

Phase 1 rollback thinking should stay small and concrete. Do not introduce
queues, retries, dashboards, or orchestration to solve an unclear first failure.

## Out Of Scope For Phase 1

- Retry loops for database failures
- Queues and background workers
- Redis
- k3s
- OpenTelemetry, Prometheus, dashboards, and tracing
- Broad exception handling that hides database failures
