# Database Unavailable Scenario

## Phase

Phase 1. This scenario teaches the learner to use logs, health endpoints,
configuration, and database reachability before adding retries, queues, workers,
or new infrastructure.

## Setup

Prerequisites:

- Run `./scripts/verify.sh` successfully.
- Know the local API command from `README.md`.
- Know which local Postgres instance or connection string you intend to use.
- Do not commit `.env` files, shell snippets with secrets, or real credentials.

Start the API in one terminal:

```sh
uv run uvicorn opledger_api.main:app --app-dir services/api --host 127.0.0.1 --port 18080 --reload
```

In another terminal, confirm liveness and readiness:

```sh
curl -i http://127.0.0.1:18080/health/live
curl -i http://127.0.0.1:18080/health/ready
```

If Postgres is not running yet, readiness may already be failing. That is a
valid starting point for the scenario.

## Break Database Connectivity

Choose one local-only break:

- Stop your local Postgres process.
- Point only the current shell command at an unused local port:

```sh
DATABASE_URL=postgresql+psycopg://localhost:59999/opledger \
  uv run uvicorn opledger_api.main:app --app-dir services/api --host 127.0.0.1 --port 18080
```

- Point only the current shell command at a database name that does not exist:

```sh
DATABASE_URL=postgresql+psycopg://localhost:55432/opledger_missing \
  uv run uvicorn opledger_api.main:app --app-dir services/api --host 127.0.0.1 --port 18080
```

Do not write these broken values to a repo file. Do not use a production
connection string for this scenario.

## Observe

Run:

```sh
curl -i http://127.0.0.1:18080/health/live
curl -i http://127.0.0.1:18080/health/ready
```

Then inspect the API terminal logs. Look for:

- request log lines with `event=http_request`, method, path, status, and
  duration
- `GET /health/live` returning `200`
- `GET /health/ready` returning `503`
- `event=database_readiness_failed` with an error class and sanitized target
  fields

Expected symptoms:

- The process is live even when the database is unavailable.
- Readiness is not healthy because the service cannot prove database access.
- The response and logs identify the driver, host, port, database name, and
  error class without exposing passwords or full connection strings.
- CRUD routes that need the database may fail or hang until the connection
  timeout is reached.

## What Not To Fix Yet

Do not add retry loops for database connectivity in Phase 1.

Do not add queues, background workers, Redis, Docker Compose, k3s, tracing,
Prometheus, dashboards, or distributed correlation IDs for this scenario.

Do not hide the failure with broad exception handling. The point is to see the
dependency failure clearly, prove which dependency is down, and make a small
operator decision.

## Recover

Restore the correct database connection:

- start Postgres again, or
- restart the API without the intentionally broken `DATABASE_URL`, or
- point `DATABASE_URL` back at the local database you control.

Confirm:

```sh
curl -i http://127.0.0.1:18080/health/live
curl -i http://127.0.0.1:18080/health/ready
```

Readiness should return `200` only after the API can connect and run its
lightweight database check.

## Reflection Questions

- What evidence proved the API process was still running?
- What evidence proved the database dependency was not ready?
- Which log line would you paste into an incident note, and what secret data
  must not appear in it?
- Why is a retry loop the wrong first response in this phase?
- What would you check next if readiness failed after the database process was
  restarted?
