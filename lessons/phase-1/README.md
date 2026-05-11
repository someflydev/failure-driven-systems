# Phase 1 Lesson Index

Phase 1 turns OpsLedger into one understandable, deployable backend service:
FastAPI, Postgres, synchronous request-response routes, explicit migrations,
health checks, logs, and Dokku deployment. Work through the materials in this
order so each lesson creates the need for the next one.

## Orientation

1. Read `README.md` for the project purpose, local workflow, and Phase 1
   operational materials.
2. Read `docs/DOMAIN.md` for OpsLedger's domain boundaries.
3. Read `docs/data-models/phase-1.md` for the implemented relational model.
4. Read `curriculum/README.md` and `curriculum/PHASE_PLAN.md` for the Phase 1
   boundaries and the concepts deferred to later phases.

## Application Surface

Inspect the current API before attempting the exercises:

- `services/api/opledger_api/models.py`
- `services/api/opledger_api/schemas.py`
- `services/api/opledger_api/routes.py`
- `services/api/opledger_api/health.py`
- `services/api/migrations/versions/`
- `services/api/tests/`

The current service supports customers, work requests, status updates, status
history, dependency-free liveness, and database-backed readiness.

## Learning Path

1. `exercises/phase-1/01-basic-crud.md`: build and reason about customer and
   work request CRUD.
2. `exercises/phase-1/02-transactions-and-history.md`: record status history
   in the same transaction as the current status update.
3. `exercises/phase-1/03-test-matrix-and-edge-cases.md`: design test coverage
   before using an LLM as a reviewer.
4. `exercises/phase-1/04-db-down-debugging.md`: diagnose a live-but-not-ready
   API when Postgres is unavailable.
5. `exercises/phase-1/05-local-container-workflow.md`: run the API and
   Postgres through Docker Compose, migrate explicitly, and inspect logs.
6. `exercises/phase-1/06-dokku-first-deploy.md`: deploy the single API service
   to Dokku, link Postgres, migrate, and capture sanitized evidence.
7. `exercises/phase-1/07-phase-1-capstone.md`: make one small CRUD
   improvement, test it, deploy or document the blocker, run the database
   unavailable drill, and explain the tradeoffs.

## Failure Scenario And Runbooks

Use these when the lesson asks for debugging or operational evidence:

- `scenarios/phase-1/db-unavailable.md`
- `docs/runbooks/DB_CONNECTIVITY.md`
- `ops/runbooks/phase-1-first-response.md`
- `ops/runbooks/dokku-api-incident.md`

The expected habit is evidence first: health responses, logs, configuration,
database reachability, migration state, then the smallest justified change.

## Deployment Docs

Use these for the local-to-Dokku path:

- `deploy/dokku/README.md`
- `deploy/dokku/checklist.md`

Phase 1 deployment stays intentionally small: one Dokku app, one Dokku Postgres
service, the repo-root `Dockerfile`, explicit migrations, and readable logs.

## Review Gates

Use these checks before treating Phase 1 as complete:

- `reviews/README.md`
- `quizzes/README.md`
- `interviews/README.md`
- `reviews/checklists/phase-1-api-review.md`
- `quizzes/phase-1.md`
- `interviews/phase-1-backend.md`
- `reviews/rubrics/phase-1-capstone.md`

Passing Phase 1 means the learner can build, test, deploy, break, debug, and
explain the single-service system without reaching for later-phase tools.
