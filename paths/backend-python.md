# Backend/Python Systems Engineer Path

## Target Outcome

Build and defend a Python/FastAPI backend that handles validation,
transactions, durable state, tests, background work, and a narrow service
boundary without losing source-of-truth clarity.

## Recommended Phase Emphasis

- Phase 1: strongest emphasis on API semantics, SQLAlchemy models, migrations,
  transactions, status history, tests, and Dokku basics.
- Phase 2: strong emphasis on report job APIs, worker behavior, durable status,
  retries, idempotency, and side-effect safety.
- Phase 3: moderate emphasis on module boundaries, report rendering contracts,
  and the reporting-service extraction.
- Phase 4: enough observability to debug backend behavior from logs, metrics,
  and durable status.
- Phase 5: enough performance work to explain pagination, indexes, and cache
  behavior without turning the path into a data specialization.
- Phase 6: defend Python/FastAPI and the current service shape from evidence.

## Required Exercises

- Implementation: `exercises/phase-1/01-basic-crud.md`,
  `exercises/phase-1/02-transactions-and-history.md`,
  `exercises/phase-2/02-background-report-worker.md`,
  `exercises/phase-2/05-idempotent-report-jobs.md`
- Debugging: `exercises/phase-1/04-db-down-debugging.md`,
  `scenarios/phase-2/worker-unavailable.md`,
  `scenarios/phase-2/duplicate-job-execution.md`
- Review: `reviews/checklists/phase-1-api-review.md`,
  `reviews/checklists/phase-2-async-review.md`
- Explanation: `interviews/phase-1-backend.md`,
  `interviews/phase-2-backend-distributed.md`,
  `exercises/phase-6/03-runtime-selection-defense.md`

## Optional Extensions

- `exercises/phase-3/02-contract-before-network.md`
- `exercises/phase-3/03-extract-reporting-service.md`
- `exercises/phase-5/02-pagination-and-indexes.md`
- `extensions/polyglot-report-renderer/README.md`, only if used to defend why
  the main path stays Python.

## Review/Interview Checkpoints

- After Phase 1, run `reviews/checklists/phase-1-api-review.md` and
  `interviews/phase-1-backend.md`.
- After Phase 2, run `reviews/checklists/phase-2-async-review.md` and
  `interviews/mock-panels/backend-implementation-panel.md`.
- Before the final portfolio defense, use
  `interviews/role-tracks/backend-python.md`.

## Portfolio Artifacts To Produce

- API walkthrough naming route, schema, model, migration, test, and transaction
  boundary.
- Async report job evidence showing API acceptance, Redis coordination, worker
  execution, and Postgres status.
- Test explanation naming the highest-risk regression covered and one weak
  edge case.
- Short runtime defense citing `docs/languages/python.md`.

## What Not To Overfocus On

- Do not turn this path into framework trivia.
- Do not claim Redis owns business truth.
- Do not present service extraction as automatic seniority.
- Do not skip failure scenarios because unit tests pass.
