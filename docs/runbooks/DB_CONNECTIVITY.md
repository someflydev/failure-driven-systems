# Database Connectivity Runbook

OpsLedger uses Postgres as its source of truth. `/health/live` only confirms
that the API process can respond. `/health/ready` confirms that the API can
open a database connection and run a lightweight `select 1`.

## Local Configuration

The API reads `DATABASE_URL` first and `OPLEDGER_DATABASE_URL` second. If neither
is set, local development defaults to:

```sh
postgresql+psycopg://localhost:55432/opledger
```

Local examples avoid standard service ports. If you run Postgres in a container
or local supervisor, bind the host side to `55432` or set `DATABASE_URL` to the
project-specific port you chose.

Use local credentials you control. Do not commit real passwords, production
URLs, or shell history snippets that include secrets.

## Recognize Failures

When Postgres is unavailable, `/health/live` should still return `200` with
`{"status":"ok"}`. `/health/ready` should return `503` with a sanitized database
status and an error class, not a raw connection string or password.

The API should also log `event=database_readiness_failed` with the error class
and sanitized target fields. Use that log line with request logs from the same
time window before changing code.

Common local causes:

- Postgres is not running.
- The database or role does not exist.
- `DATABASE_URL` points at the wrong host, port, database, or driver.
- Local firewall or socket settings block the connection.

## Local Checks

Run the API:

```sh
uv run uvicorn opledger_api.main:app --app-dir services/api --host 127.0.0.1 --port 18080 --reload
```

Check liveness:

```sh
curl -i http://127.0.0.1:18080/health/live
```

Check readiness:

```sh
curl -i http://127.0.0.1:18080/health/ready
```

Run migrations once domain tables exist:

```sh
DATABASE_URL=postgresql+psycopg://localhost:55432/opledger \
  uv run alembic -c services/api/alembic.ini upgrade head
```

Create future migrations after SQLAlchemy models are added:

```sh
uv run alembic -c services/api/alembic.ini revision --autogenerate -m "describe change"
```

## Docker Compose Checks

The current repo-root `docker-compose.yml` includes Postgres, Redis, the API,
the worker, and the stateless reporting service. Earlier Phase 1 work
introduced only API and Postgres; later phases added Redis-backed jobs,
reporting, and cache behavior. Start the current local stack with:

```sh
docker compose up --build
```

Or use the small wrapper:

```sh
./scripts/dev-up.sh
```

Confirm the declared services match the current stack:

```sh
docker compose config --services
```

The expected services are `postgres`, `redis`, `api`, `reporting`, and
`worker`.

Apply migrations explicitly after the containers are running:

```sh
./scripts/migrate.sh --compose
```

Check the API from the host:

```sh
curl -i http://127.0.0.1:18080/health/live
curl -i http://127.0.0.1:18080/health/ready
```

Inside Compose, the API uses `postgres` as the database host because that is the
service name on the Compose network. From the host, Postgres is published on
port `55432` by default.

`/health/ready` currently checks whether the API can reach Postgres. It does
not prove Redis, reporting service, or worker liveness. For later-phase
dependencies, use job status endpoints, service health checks, and logs in
addition to API readiness.

Useful local diagnostics:

```sh
docker compose ps
docker compose logs api
docker compose logs postgres
docker compose logs redis
docker compose logs worker
docker compose logs reporting
```

Stop containers without deleting the database volume:

```sh
./scripts/dev-down.sh
```

Stop containers and delete the local Postgres volume only when you intentionally
want a clean database:

```sh
./scripts/dev-down.sh -v
```

## Dokku

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

For the broader Phase 1 response flow, see
`ops/runbooks/phase-1-first-response.md`. For a guided local drill, see
`scenarios/phase-1/db-unavailable.md`.
