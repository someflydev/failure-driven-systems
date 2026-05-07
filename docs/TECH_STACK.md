# Technical Stack

OpsLedger starts as a single Python API backed by Postgres. This stack is
intentionally ordinary: it supports the curriculum goals without requiring
distributed infrastructure before learners have experienced the pressure that
would justify it.

## Default API Stack

FastAPI is the default web framework because it gives learners a practical
request/response API model, strong type-hinted request and response shapes,
OpenAPI documentation, and a production-relevant ecosystem while keeping early
application code small.

Postgres is the default source of truth. The API reads `DATABASE_URL` or
`OPLEDGER_DATABASE_URL`, with a safe local default for a developer-owned
Postgres database. Later lessons can use it to make durable state, transactions,
constraints, migrations, indexing, and ownership boundaries visible. SQLAlchemy
and Alembic are included now as the standard database and migration tooling for
the Phase 1 customer, work request, and status history tables.

Docker Compose is the default local container workflow for Phase 1. The
repo-root `docker-compose.yml` runs only the API and Postgres so learners can
practice container startup, explicit migrations, health checks, and database
connectivity failures without introducing phase 2 infrastructure.

Dokku is the default early deployment target for Phase 1. The root `Dockerfile`
is the deployment artifact for the single API service, and Dokku Postgres
provides `DATABASE_URL` through service linking. Migrations remain explicit
operator actions.

## Python Tooling

Python tooling is rooted at the repository top level and managed with `uv`.
The project requires Python 3.12 through `pyproject.toml`, so local development
and verification use the same interpreter family:

```sh
uv venv --python 3.12
uv sync
./scripts/verify.sh
```

The initial quality gates are Ruff formatting, Ruff linting, mypy type checks,
and pytest. These gates are intentionally strict enough to shape habits while
remaining realistic for a small scaffold.

## Deferred Choices

Redis, background workers, queues, k3s manifests, caching, and service
extraction are deferred. They should appear only after later prompts create a
concrete failure, operational need, or teaching moment.

## Later Language Discussions

Other runtimes can be discussed later as architecture tradeoffs, not as early
defaults:

- Go may fit small operational services, CLIs, or concurrency-heavy components.
- JVM languages may fit teams that need mature enterprise integrations or
  long-lived service platforms.
- Node may fit full-stack teams or event-heavy product surfaces.
- Rust may fit performance-sensitive or safety-critical components.
- Elixir may fit systems centered on supervision, concurrency, and realtime
  messaging.

Those comparisons are useful only when grounded in the measured needs and
constraints of OpsLedger as it evolves.
