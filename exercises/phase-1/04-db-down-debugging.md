# Database Down Debugging

## Phase

Phase 1. This exercise belongs in the first synchronous service phase because
the learner should experience a direct database dependency failure before
retries, queues, workers, or deployment automation make the failure less
obvious.

## Concepts

- Liveness versus readiness
- Request logs as the first diagnostic tool
- Sanitized database failure messages
- Environment-driven database configuration
- Local operational debugging
- Rollback and recovery thinking

## Prerequisites

- Complete `exercises/phase-1/01-basic-crud.md`.
- Complete `exercises/phase-1/03-test-matrix-and-edge-cases.md`.
- Read `docs/runbooks/DB_CONNECTIVITY.md`.
- Read `ops/runbooks/phase-1-first-response.md`.
- Read `scenarios/phase-1/db-unavailable.md`.
- Inspect `services/api/opledger_api/main.py`.
- Inspect `services/api/opledger_api/health.py`.
- Run `./scripts/verify.sh` before changing behavior.

## Build/Change Task

Run the database unavailable scenario and collect evidence before changing code.
Your notes should identify:

- the liveness response
- the readiness response
- the request log line for each health check
- the sanitized database readiness failure log line
- the exact local-only change that broke connectivity
- the exact local-only action that restored readiness

If the existing logs do not make those facts clear, improve the logs with the
smallest code change that keeps Phase 1 simple.

## Constraints

- Inspect logs before changing code.
- Do not add retry loops for database failures.
- Do not add queues, workers, Redis, Docker Compose, k3s, tracing, Prometheus,
  dashboards, or distributed correlation IDs.
- Do not log full connection strings, credentials, secret environment values,
  or full request bodies.
- Do not catch broad exceptions in CRUD routes to make the symptoms disappear.
- Do not commit local env files or shell history snippets with secrets.

## Failure Modes

- Treating `/health/live` as proof that the service can handle normal traffic.
- Skipping logs and guessing from code.
- Logging credentials while trying to make failures easier to debug.
- Adding retries before proving what failed.
- Hiding a database outage behind a generic `500` response or broad exception
  handler.
- Forgetting to restore the local database connection after the scenario.

## Expected Reasoning

The learner should be able to explain why liveness still succeeds, why
readiness fails, which dependency failed, what evidence proves it, and why the
first response is diagnosis and recovery rather than retries or queues.

## Verification

- Run `./scripts/verify.sh`.
- Start the API locally.
- Confirm request logs appear for `GET /health/live` and `GET /health/ready`.
- Temporarily run the API with an invalid local `DATABASE_URL`.
- Confirm `/health/live` returns `200`.
- Confirm `/health/ready` returns `503`.
- Confirm readiness logs include a sanitized error class and database target.
- Restore the valid local database connection.
- Confirm `/health/ready` returns `200` when Postgres is reachable.

## Reflection Questions

- Which check tells you the process is alive?
- Which check tells you the database dependency is ready?
- What did the logs show that the HTTP response alone did not?
- What information was intentionally absent from the logs?
- Why are retries and queues banned in this exercise?
- What would change about your response if the failure started immediately
  after a migration?

## LLM Usage

Use an LLM as an incident reviewer after you collect your own evidence. Paste
only sanitized log lines and responses. Ask it to challenge your diagnosis,
identify missing checks, or interview you about liveness and readiness. Do not
ask it to invent a code fix before you can explain the failure.

## Path-Specific Extensions

Backend path: add or revise one focused test that proves readiness failures stay
sanitized.

Operations path: write a short incident note with timeline, impact, evidence,
root cause, recovery, and one follow-up.

Architecture path: explain why this failure does not justify adding a queue,
worker, cache, or second service.

Interview path: practice explaining how you would debug a live-but-not-ready
service on a small VPS.

## Deployment/Debugging Actions If Relevant

Run the guided local scenario in `scenarios/phase-1/db-unavailable.md`. If a
local Postgres instance is unavailable, run the invalid `DATABASE_URL` variant
and record that full recovery to ready status remains a deferred local
integration check.
