# Dokku First Deploy

## Phase

Phase 1. This exercise belongs in the single-service phase because it asks the
learner to deploy the existing OpsLedger API and operate it on a modest Dokku
VPS before introducing orchestration or extra services.

## Concepts

- Dockerfile-based Dokku deployment
- Environment-driven configuration
- Dokku Postgres linking
- Explicit migrations after deploy
- Liveness versus readiness in a deployed environment
- Process logs and sanitized evidence capture
- Small rollback decisions

## Prerequisites

- Complete `exercises/phase-1/05-local-container-workflow.md`.
- Read `deploy/dokku/README.md`.
- Read `deploy/dokku/checklist.md`.
- Read `ops/runbooks/dokku-api-incident.md`.
- Inspect `Dockerfile`.
- Inspect `services/api/opledger_api/config.py`.
- Inspect `services/api/opledger_api/health.py`.
- Inspect `services/api/migrations/env.py`.

## Build/Change Task

Deploy the current OpsLedger API to Dokku, attach Postgres, run migrations, and
capture evidence that the deployed service is live, ready, and logging useful
operational events.

Your notes should include:

- the deployed Git commit
- the Dokku app name
- the Postgres service name
- sanitized config evidence showing `DATABASE_URL` exists
- the migration command and result
- `/health/live` response status
- `/health/ready` response status
- one readable request log line or event name
- one rollback or revert decision you would make if this deploy failed

## Constraints

- Use one Dokku app and one Dokku Postgres service.
- Use the repository's root `Dockerfile`.
- Do not add Redis, queues, workers, service extraction, or k3s manifests.
- Do not use managed cloud Postgres as the default path.
- Do not commit real `.env` files or copied secrets.
- Do not paste full database URLs into exercise notes.
- Do not make migrations run automatically at container boot.

## Failure Modes

- Deploying successfully but forgetting to run migrations.
- Treating `/health/live` as proof that database-backed routes work.
- Setting local Compose variables such as `POSTGRES_PASSWORD` on the Dokku app
  instead of linking Postgres.
- Forgetting Dokku proxy configuration for the Dockerfile's container port
  `8000`.
- Capturing secrets while trying to prove configuration.
- Rolling back code without considering whether a migration already changed the
  database.

## Expected Reasoning

The learner should be able to explain why Dokku is enough for this phase, how
the app receives `DATABASE_URL`, why migrations are explicit, why readiness is a
stronger deployment signal than liveness, and what rollback risks appear when a
deploy includes both code and schema changes.

## Verification

- Run `./scripts/verify.sh` locally before deploy.
- Confirm `dokku proxy:ports-report opledger-api` maps public HTTP traffic to
  container port `8000`.
- Confirm `dokku config:show opledger-api` includes `DATABASE_URL` without
  recording its full value.
- Deploy with `git push dokku HEAD:main` or the equivalent intended branch.
- Run `dokku run opledger-api uv run --no-sync alembic -c services/api/alembic.ini upgrade head`.
- Confirm `curl -i http://opledger-api.YOUR_DOKKU_DOMAIN/health/live` returns
  `200`.
- Confirm `curl -i http://opledger-api.YOUR_DOKKU_DOMAIN/health/ready` returns
  `200`.
- Inspect `dokku logs opledger-api --tail`.
- Record sanitized evidence and a short deploy timeline.

## Reflection Questions

- What did Dokku provide that you would otherwise have to operate yourself?
- Why does linking Postgres matter more than manually copying database
  credentials?
- What does readiness prove that liveness does not?
- Why are migrations a separate operator action in this phase?
- If the deploy failed after migrations ran, what would make rollback risky?
- What evidence would convince you this problem does not require k3s yet?

## LLM Usage

Use an LLM after you write your own deploy notes. Ask it to review your
evidence for missing checks, unsafe secret handling, weak rollback reasoning, or
confusion between liveness and readiness. Do not ask it to invent deploy
evidence you did not collect.

## Path-Specific Extensions

Backend path: add one small API smoke request after readiness passes and explain
which table or migration it depends on.

Operations path: write a five-step incident timeline for a failed migration or
bad `DATABASE_URL`.

Architecture path: compare this Dokku deployment with a later orchestration path
and identify what complexity is intentionally deferred.

Interview path: practice explaining how you would debug a deployed API that is
live but not ready.

## Deployment/Debugging Actions If Relevant

Use `dokku ps:report opledger-api`, `dokku config:show opledger-api`,
`dokku logs opledger-api --tail`, the explicit Alembic migration command, and
the two health endpoints before changing code or adding infrastructure.
