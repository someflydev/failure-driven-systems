# Local Container Workflow

## Phase

Phase 1. This exercise belongs in the single-service phase because it makes the
API and Postgres dependency runnable in a repeatable local environment without
introducing queues, workers, caches, or orchestration layers.

## Concepts

- Docker Compose service boundaries
- Environment-driven configuration
- Postgres container lifecycle
- Explicit database migrations
- Liveness versus readiness
- Diagnosing broken database connectivity

## Prerequisites

- Complete `exercises/phase-1/01-basic-crud.md`.
- Complete `exercises/phase-1/04-db-down-debugging.md`.
- Read `docs/runbooks/DB_CONNECTIVITY.md`.
- Inspect `Dockerfile`.
- Inspect `docker-compose.yml`.
- Inspect `.env.example`.
- Inspect `services/api/opledger_api/config.py`.
- Inspect `services/api/migrations/env.py`.

## Build/Change Task

Bring up the local Docker Compose environment, apply migrations, confirm the
health endpoints, deliberately break database connectivity, and record the
symptoms. Your notes should identify:

- the commands used to start the stack
- the command used to apply migrations
- the liveness response before and after the break
- the readiness response before and after the break
- the Compose logs that show the API or database symptom
- the exact local-only change that broke connectivity
- the exact local-only action that restored readiness

## Constraints

- Use only the API and Postgres services in `docker-compose.yml`.
- Do not add Redis, queues, workers, k3s, service extraction, or deployment
  manifests.
- Do not hide the workflow behind a single magic script.
- Do not commit a real `.env` file.
- Do not log full database URLs, passwords, or copied shell history containing
  secrets.
- Do not modify application code unless the observed symptoms are misleading.

## Failure Modes

- Treating `docker compose up` as proof that migrations ran.
- Calling `/health/live` and assuming normal traffic can reach Postgres.
- Breaking the wrong variable and mistaking an API restart issue for a database
  connectivity issue.
- Forgetting to restore the valid Compose configuration.
- Leaving local containers, volumes, or `.env` values in a confusing state.

## Expected Reasoning

The learner should be able to explain which pieces run in separate containers,
why the API uses `postgres` as the database host inside Compose, why migrations
remain explicit, and why a live API can still be not ready when the database is
unreachable.

## Verification

- Run `./scripts/verify.sh`.
- Run `docker compose config --services` and confirm only `postgres` and `api`
  are listed.
- Start the stack with `docker compose up --build`.
- In another shell, run `./scripts/migrate.sh --compose`.
- Confirm `curl -i http://127.0.0.1:18080/health/live` returns `200`.
- Confirm `curl -i http://127.0.0.1:18080/health/ready` returns `200`.
- Temporarily break the API database host or password locally.
- Restart the API container.
- Confirm liveness still returns `200`.
- Confirm readiness returns `503` with sanitized database details.
- Restore the valid local configuration and confirm readiness returns `200`.

## Reflection Questions

- Why does Compose use the service name `postgres` instead of `localhost` from
  inside the API container?
- What does the Postgres healthcheck prove, and what does it not prove?
- Why are migrations not run automatically as part of `docker compose up`?
- Which endpoint should a load balancer or deployment gate trust for database
  dependency readiness?
- What local evidence would convince you this failure does not justify Redis or
  a worker?

## LLM Usage

Use an LLM as a reviewer after you collect command output and sanitized logs.
Ask it to challenge your diagnosis, identify missing checks, or interview you
about container networking and readiness. Do not ask it to produce a finished
incident explanation before you have written your own.

## Path-Specific Extensions

Backend path: add one focused test or note that proves readiness responses stay
sanitized when database connection attempts fail.

Operations path: write a short local runbook entry for starting, migrating,
checking, breaking, and restoring the Compose stack.

Architecture path: explain why this local container workflow prepares for
deployment thinking without introducing service extraction.

Interview path: practice explaining how you would debug an API container that
is live but not ready on a small VPS.

## Deployment/Debugging Actions If Relevant

Use `docker compose logs api`, `docker compose logs postgres`,
`docker compose ps`, `./scripts/migrate.sh --compose`, and the two health
endpoints to collect evidence before changing code or configuration.
