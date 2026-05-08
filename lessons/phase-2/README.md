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

The current service can generate a work request summary report synchronously and
can enqueue the same report for a Redis/RQ worker. The report is derived from
`work_requests` and `work_request_status_events`; durable report job status is
stored in Postgres through `report_jobs`. Redis carries queued work but is not
the system of record.

## Learning Path

1. `exercises/phase-2/01-synchronous-report-pain.md`: measure a synchronous
   report request, enable a controlled local delay, observe the user-facing
   wait, and explain why request-path work can become a problem.
2. `exercises/phase-2/02-background-report-worker.md`: enqueue the report,
   run the worker, inspect persisted job status, stop the worker, and compare
   queued behavior with the synchronous route.

## Important Boundary

Do not add retries, idempotency, duplicate suppression, cache layers, or a
separate reporting service in Phase 2 yet. The current queue is only enough to
move report generation out of the request path and make worker operation
observable.
