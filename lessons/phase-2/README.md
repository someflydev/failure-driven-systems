# Phase 2 Lesson Index

Phase 2 starts by making OpsLedger reporting uncomfortable inside the
request-response path. Learners should measure and explain that discomfort
before adding machinery that moves work elsewhere.

## Current Application Surface

Inspect these files before starting the first lesson:

- `services/api/opledger_api/routes.py`
- `services/api/opledger_api/reports.py`
- `services/api/opledger_api/schemas.py`
- `services/api/opledger_api/config.py`
- `services/api/tests/test_crud_api.py`
- `services/api/tests/test_report_jobs.py`

The current service can generate a work request summary report synchronously and
can enqueue the same report for a Redis/RQ worker. The report is derived from
`work_requests` and `work_request_status_events`; durable report job status is
stored in Postgres through `report_jobs`. Duplicate report enqueue requests can
be tied to an explicit idempotency key. Redis carries queued work but is not the
system of record.

## Learning Path

1. `exercises/phase-2/01-synchronous-report-pain.md`: measure a synchronous
   report request, enable a controlled local delay, observe the user-facing
   wait, and explain why request-path work can become a problem.
2. `exercises/phase-2/02-background-report-worker.md`: enqueue the report,
   run the worker, inspect persisted job status, stop the worker, and compare
   queued behavior with the synchronous route.
3. `exercises/phase-2/03-job-status-and-eventual-consistency.md`: inspect job
   status and result endpoints, explain `202 Accepted`, and describe what users
   can safely assume while report generation is eventually consistent.
4. `exercises/phase-2/04-retries-before-idempotency.md`: trigger controlled
   report worker failure, inspect retry attempts, and identify duplicate
   side-effect risks before implementing idempotency.
5. `exercises/phase-2/05-idempotent-report-jobs.md`: add database-backed
   request idempotency for report enqueueing, protect completed report output
   from duplicate worker execution, and explain remaining side-effect risks.

## Important Boundary

Do not add cache layers or a separate reporting service in Phase 2 yet.
Idempotency is currently scoped to work request summary report jobs; future
side effects still need their own duplicate-prevention design.
