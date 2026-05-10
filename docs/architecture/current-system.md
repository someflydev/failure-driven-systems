# Current System Architecture

OpsLedger is currently a small, self-operated system intended to fit one Linux
VPS with Dokku, Docker, Postgres, Redis, and ordinary process logs. The local
development shape is larger than the first Dokku deployment path because later
phases added a worker, Redis, one stateless reporting service, metrics, and
performance exercises.

## Runtime Shape

- API: FastAPI application in `services/api/opledger_api/`, served by the
  repo-root `Dockerfile` with Uvicorn on container port `8000`.
- Postgres: durable source of truth for customers, work requests, status
  events, report jobs, notification attempts, and the customer dashboard read
  model. Migrations live in `services/api/migrations/versions/`.
- Redis: coordination layer for RQ report jobs and the Phase 5 dashboard cache.
  It is not authoritative; durable status and source data remain in Postgres.
- Worker: RQ worker launched by `python -m opledger_api.worker`. It consumes
  report jobs, updates durable job state in Postgres, calls report rendering,
  and records local notification attempts.
- Reporting service: stateless FastAPI service in `services/reporting/` on
  container port `8001`. It accepts a complete `report-rendering.v1` snapshot
  and does not connect to Postgres or Redis.
- Logs: structured JSON logs from API, worker, and reporting service. Request
  IDs and correlation IDs connect API calls, report jobs, worker attempts, and
  reporting-service calls.
- Metrics: lightweight Prometheus-compatible `/metrics` endpoints on the API
  and reporting service. Worker metrics are process-local, so durable job and
  notification endpoints remain the reliable cross-process inspection surface.

## Local Compose Mode

`docker-compose.yml` runs Postgres, Redis, the API, the worker, and the
reporting service:

- API is exposed on `${API_PORT:-18080}` and talks to Postgres at
  `postgres:5432` and Redis at `redis:6379`.
- Redis is exposed locally on `${REDIS_PORT:-56379}`.
- Postgres is exposed locally on `${POSTGRES_PORT:-55432}`.
- Reporting is exposed on `${REPORTING_PORT:-18081}` and is reached by the
  worker at `http://reporting:8001`.
- The worker uses `OPLEDGER_REPORT_RENDERING_SERVICE_TIMEOUT_SECONDS`, default
  `2`, to bound remote rendering calls.

This mode is the main teaching environment for Phases 2 through 5 because it
makes queue, cache, worker, reporting boundary, and observability failures easy
to reproduce.

## Dokku Mode

The documented Dokku path in `deploy/dokku/README.md` is still intentionally
API-first:

- one Dokku app named `opledger-api`;
- one Dokku Postgres service named `opledger-db`;
- Dockerfile-based deploys from Git;
- explicit Alembic migrations with `dokku run`;
- health checks at `/health/live` and `/health/ready`;
- process logs through `dokku logs`;
- rollback by config restore, tagged image deploy, or Git revert plus forward
  database repair when needed.

Later deployment work may add worker, Redis, and reporting-service process
docs for Dokku. Until then, the repo should not claim a full production Dokku
multi-process deployment has already been completed.

## Source-Of-Truth Boundaries

Postgres owns durable facts. Redis can lose queued or cached state without
changing the source of truth. The reporting service owns no facts; it renders
only the payload it receives. The worker owns execution progress but records
user-visible job and notification state in Postgres.

## Failure Modes To Expect

- Postgres unavailable: `/health/ready` fails, durable reads and writes fail,
  and Redis cannot compensate for missing source-of-truth access.
- Redis unavailable: report enqueue and cache access degrade or fail, but
  source-of-truth records in Postgres are not corrupted.
- Worker stopped: report jobs can remain queued or running in durable status
  until the worker resumes or an operator investigates.
- Reporting service slow or invalid: worker calls time out or fail contract
  validation; durable report job state records the failure.
- Cache stale: the dashboard cache can lag behind Postgres and the derived
  read model; source-of-truth work request endpoints remain authoritative.
- Metrics unavailable externally: `/metrics` is intended for local or internal
  use and should not be published directly without protection.

## Current Scale Assumption

The architecture assumes a modest learning workload on a 4 GB RAM, 3 vCPU VPS:
low request rates, small datasets, bounded local performance baselines, and one
operator or small team that can inspect logs, database state, health, and
deployment config directly.
