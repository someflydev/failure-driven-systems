# Idempotent Report Jobs

## Phase

Phase 2: Async After Synchronous Pain. This exercise belongs here because the
learner has already observed slow synchronous reporting, background job status,
bounded retries, and duplicate execution risk.

## Concepts

- Explicit idempotency keys.
- Database-backed duplicate prevention.
- Worker retry safety.
- Durable side-effect identity.
- Difference between request, job, and side-effect idempotency.

## Prerequisites

- `exercises/phase-2/01-synchronous-report-pain.md`
- `exercises/phase-2/02-background-report-worker.md`
- `exercises/phase-2/03-job-status-and-eventual-consistency.md`
- `exercises/phase-2/04-retries-before-idempotency.md`
- `docs/async/phase-2-job-lifecycle.md`
- `docs/async/idempotency.md`
- `services/api/opledger_api/routes.py`
- `services/api/opledger_api/report_jobs.py`
- `services/api/opledger_api/models.py`
- `services/api/tests/test_crud_api.py`
- `services/api/tests/test_report_jobs.py`
- Alembic migration workflow.

## Build/Change Task

Add or review idempotency for work request summary report jobs.

The enqueue endpoint should accept an explicit `Idempotency-Key` header. A
repeated key for the same report type should return the original `ReportJob`
instead of creating another durable record or enqueueing duplicate work. A
different key should create a different job when the caller intends a separate
request.

Enforce the duplicate boundary in Postgres with a unique constraint. Application
code may check first for a nicer path, but the database must remain the
authority when two requests arrive close together.

Make duplicate worker execution safe for completed jobs. If a job is already
`succeeded` and already has durable `result_json`, another worker execution
should not rebuild the report or replace the output.

## Constraints

- Do not claim idempotency is solved for every future feature.
- Do not rely only on in-memory locks.
- Do not make Redis the source of truth for duplicate prevention.
- Do not add another durable job status name.
- Do not introduce distributed locks.
- Preserve retries for failed jobs.
- Keep the public job status model consistent across enqueue, worker, status,
  and result routes.

## Failure Modes

- Checking for duplicates in application code without a database constraint.
- Treating Redis queue state as durable request identity.
- Re-enqueueing work when a duplicate request should return the original job.
- Making all report requests collapse together when no idempotency key was
  provided.
- Blocking legitimate new report requests that use different keys.
- Skipping failed-job retries because duplicate execution protection is too
  broad.
- Overwriting completed report output during duplicate worker execution.

## Expected Reasoning

After completing this exercise, explain why request idempotency, job
idempotency, and side-effect idempotency are separate concerns.

You should be able to defend why the endpoint uses an explicit key instead of
silently fingerprinting every request, why Postgres must enforce uniqueness,
and why completed output changes the worker's behavior while failed jobs remain
retryable.

## Verification

- Run `./scripts/verify.sh`.
- Confirm the migration adds a uniqueness constraint for report idempotency.
- Enqueue a report twice with the same `Idempotency-Key` and confirm both
  responses contain the same `id`.
- Enqueue with a different `Idempotency-Key` and confirm a new job is created.
- Execute the same completed worker job again and confirm `result_json` is not
  replaced and `attempt_count` is not incremented.
- Confirm documentation includes the phrase "duplicates must be tolerated or
  prevented consciously".

## Reflection Questions

- What does the idempotency key identify: the HTTP request, the report output,
  or the caller's intent?
- Why is an application-level duplicate check insufficient under concurrency?
- Why should requests without an idempotency key still create new jobs?
- What would break if Redis were treated as the duplicate-prevention authority?
- Why is it safe to no-op a completed job with output but not every failed job?
- Which future side effect would need its own idempotency design first:
  notifications, exported files, audit rows, or billing events? Why?

## LLM Usage

Use an LLM as a reviewer after you have written your own explanation of the
duplicate boundary. Ask it to critique whether your tests prove database-backed
idempotency, whether your worker guard accidentally disables legitimate
retries, and whether your explanation separates request, job, and side-effect
idempotency. Do not ask it to invent a broad idempotency architecture before
you identify the concrete duplicated effect.

## Path-Specific Extensions

Backend: add a direct database test that proves the unique constraint rejects
two jobs with the same report type and idempotency key.

Operations: write a short operator note explaining how to recognize a repeated
client request versus a new report request in job records.

Architecture: compare explicit idempotency keys with deterministic request
fingerprints and state which one fits this endpoint better.

Interview: practice explaining why idempotency is not the same as exactly-once
execution.

## Deployment/Debugging Actions If Relevant

Apply the migration in local or deployed environments before depending on
idempotent enqueue behavior. Verify through the API and database that duplicate
keys return the original job row.
