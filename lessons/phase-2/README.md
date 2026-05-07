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

The current service can generate a work request summary report synchronously.
The report is derived from `work_requests` and `work_request_status_events`.
No report table, worker, Redis dependency, background process, or cache exists
yet.

## Learning Path

1. `exercises/phase-2/01-synchronous-report-pain.md`: measure a synchronous
   report request, enable a controlled local delay, observe the user-facing
   wait, and explain why request-path work can become a problem.

## Important Boundary

Do not add a queue before completing the first exercise. The queue comes after
the learner has measured the slow request, recorded the user impact, and formed
a concrete expectation for what should improve.
