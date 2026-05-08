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

Docker Compose is the default local container workflow. In Phase 1 it ran only
the API and Postgres. In Phase 2 it also runs Redis and an API-codebase worker
so learners can compare synchronous report generation with queued background
work without extracting a separate service.

Dokku is the default early deployment target for Phase 1. The root `Dockerfile`
is the deployment artifact for the single API service, and Dokku Postgres
provides `DATABASE_URL` through service linking. Migrations remain explicit
operator actions.

## Background Work

RQ is the default Python job library for Phase 2 report work. It is intentionally
small: one Redis-backed queue, one worker process, and jobs that call functions
inside the existing API codebase. This keeps the architecture as one core
service plus one worker process while making the request path visibly shorter.

Redis is now justified as a queue transport because the synchronous report
exercise creates observable request-path pain. Redis is not the system of
record. Report job requests, status, errors, and finished report payloads are
stored in Postgres through the `report_jobs` table so users can inspect what
happened even if Redis is restarted or flushed. Pending Redis jobs may be lost
when Redis is ephemeral; the durable Postgres row makes that loss visible
instead of silently erasing the fact that work was requested.

Local host worker command:

```sh
./scripts/worker.sh
```

Local Docker Compose runs the worker alongside the API, Postgres, and Redis:

```sh
./scripts/dev-up.sh
```

RQ retries are now explicitly bounded for Phase 2 report work. The default is
three total attempts: the original worker execution plus two retries, with
backoff intervals of 1 and 5 seconds. Retry attempts update durable
`report_jobs` metadata in Postgres so learners can inspect attempt counts and
errors. Duplicate execution handling, idempotency, and dead-letter workflows
remain later lessons.

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

k3s manifests, caching, and service extraction are deferred. Idempotency,
duplicate execution handling, and dead-letter workflows are also deferred until
later prompts create the concrete failure or teaching moment.

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
