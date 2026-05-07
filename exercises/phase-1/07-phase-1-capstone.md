# Phase 1 Capstone

## Phase

Phase 1. This capstone belongs at the end of the single-service phase because
the learner must build, test, deploy, break, debug, and explain one synchronous
API backed by Postgres before moving to later system patterns.

## Concepts

- Small CRUD improvement design
- Schema, route, model, migration, and test alignment
- Relational constraints and transactions
- Explicit migrations
- Liveness versus readiness
- Dokku deployment or blocker documentation
- Sanitized operational evidence
- LLM critique after independent reasoning

## Prerequisites

- Complete `exercises/phase-1/01-basic-crud.md`.
- Complete `exercises/phase-1/02-transactions-and-history.md`.
- Complete `exercises/phase-1/03-test-matrix-and-edge-cases.md`.
- Complete `exercises/phase-1/04-db-down-debugging.md`.
- Complete `exercises/phase-1/05-local-container-workflow.md`.
- Complete `exercises/phase-1/06-dokku-first-deploy.md` or document why Dokku
  access is unavailable.
- Read `reviews/checklists/phase-1-api-review.md`.
- Read `reviews/rubrics/phase-1-capstone.md`.
- Inspect the current API implementation and tests under `services/api/`.

## Build/Change Task

Make one small safe CRUD improvement to the current OpsLedger API. Choose a
change that a reviewer can understand in one sitting, such as a stricter
validation rule, a small list filter, a narrow response field improvement, or a
minor route behavior that fits customers, work requests, or status history.

Before writing code, write brief notes that answer:

- What user or operator problem does this improve?
- Which table, schema, route, and tests will change?
- Which existing behavior must not change?
- What database constraint or transaction boundary matters?
- Why is this still Phase 1 scope?

Then implement the change, test it, and update any durable docs only if the
observable API contract changes.

## Constraints

- Keep one FastAPI service and one Postgres source of truth.
- Keep the change small enough to review against the Phase 1 API checklist.
- Do not add queues, workers, Redis, caching, service extraction, Kubernetes,
  k3s, or new deployment platforms.
- Do not add authentication, permissions, reporting, notifications, or broad
  architecture layers.
- Do not make an LLM produce the first design, implementation, or explanation.
- Do not commit real `.env` files, credentials, full database URLs, or copied
  secret-bearing command output.

## Failure Modes

- Choosing a change that is too broad for a capstone.
- Updating Pydantic schemas without matching database constraints when durable
  integrity is required.
- Updating the model without an Alembic migration when the table shape changes.
- Adding a route behavior without a focused test.
- Breaking existing status update and status history behavior.
- Treating Docker Compose startup or Dokku deploy success as proof that
  migrations ran.
- Recording secrets while trying to capture deployment evidence.
- Asking an LLM for critique before writing independent notes.

## Expected Reasoning

The learner should be able to explain the improvement, the request and response
behavior, where the durable facts live, which constraints protect them, which
tests prove the behavior, how deployment was checked, what happened when the
database was unavailable, and why no later-phase infrastructure was needed.

## Verification

- Run `./scripts/verify.sh` before starting and after the change.
- Add or update focused tests for the new CRUD behavior.
- If the database schema changes, add an Alembic migration and inspect it.
- Run the API locally or through Docker Compose and exercise the changed path.
- Confirm `GET /health/live` returns `200`.
- Confirm `GET /health/ready` returns `200` when Postgres is reachable.
- Deploy to Dokku and record sanitized evidence, or document the exact blocker
  that prevents deployment.
- If deployed, run the explicit migration command and one database-backed API
  check.
- Simulate database unavailability locally or in the approved exercise
  environment.
- Confirm liveness still reports the process and readiness reports the database
  failure clearly.
- Restore the valid database connection and confirm readiness returns to `200`.
- Review the finished work against `reviews/rubrics/phase-1-capstone.md`.

## Reflection Questions

- Why was this the smallest useful CRUD improvement?
- Which facts are protected by request validation, and which are protected by
  the database?
- Did the change require a migration? Why or why not?
- What evidence proves the code works locally?
- What evidence proves the deployed service is live and ready, or what exact
  blocker prevented deploy?
- What did the database unavailable drill show that normal tests did not?
- What would make this change risky to roll back?
- Which later-phase tools might someone be tempted to add, and why are they not
  justified yet?

## LLM Usage

Write your design notes, implementation notes, test results, deployment or
blocker notes, failure-drill notes, and tradeoff explanation first. Then use an
LLM as a critic. Ask it to find missing evidence, weak reasoning, unsafe secret
handling, untested edge cases, and premature complexity. Revise only points you
understand and can defend.

## Path-Specific Extensions

Backend path: add one additional edge-case test around validation, conflict,
not-found, pagination, or status history.

Operations path: write a short incident note from the database unavailable
drill with timeline, impact, evidence, recovery, and follow-up.

Architecture path: write a one-page defense of why the capstone remains one
service and one database.

Interview path: answer three prompts from `interviews/phase-1-backend.md` using
only evidence from your capstone.

## Deployment/Debugging Actions If Relevant

Use `./scripts/verify.sh`, `./scripts/dev-up.sh`, `./scripts/migrate.sh
--compose`, `curl` checks for `/health/live` and `/health/ready`, Dokku deploy
commands from `deploy/dokku/README.md`, `dokku logs opledger-api --tail`, and
the database unavailable scenario in `scenarios/phase-1/db-unavailable.md`.
