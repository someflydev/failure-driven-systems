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
- `services/api/tests/test_notifications.py`

The current service can generate a work request summary report synchronously and
can enqueue the same report for a Redis/RQ worker. The report is derived from
`work_requests` and `work_request_status_events`; durable report job status is
stored in Postgres through `report_jobs`. Duplicate report enqueue requests can
be tied to an explicit idempotency key. Redis carries queued work but is not the
system of record. Completed queued reports also create local notification
attempts in Postgres; the local adapter writes durable attempt status and logs
instead of contacting an external provider.

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
6. `exercises/phase-2/06-safe-side-effects.md`: inspect the local report
   completion notification workflow, confirm duplicate triggers do not create
   duplicate attempts, and explain the remaining gap before a full outbox
   dispatcher.
7. `exercises/phase-2/07-phase-2-capstone.md`: run at least two failure
   scenarios, inspect durable status and logs, fix or explain one issue, and
   defend the retry/idempotency design.

## Scenario Drills

Use these drills after the matching exercise introduces the behavior. They are
practice material, not replacement instructions for the exercises.

- `scenarios/phase-2/worker-unavailable.md`: stop the worker, enqueue a report,
  and explain why durable status can be inspectable while work is not
  progressing.
- `scenarios/phase-2/duplicate-job-execution.md`: run the same completed job
  path more than once and verify that completed output and notification attempts
  are not duplicated.
- `scenarios/phase-2/delayed-job-completion.md`: hold the worker down, observe
  delayed `queued` or `running` status, and write user-facing language for
  eventual consistency.
- `scenarios/phase-2/report-retry-failure.md`: inject worker failure, observe
  bounded retries, and explain why attempts are evidence rather than safety.
- `scenarios/phase-2/failed-notification-side-effect.md`: force the local
  notification adapter failure path and inspect the durable failed attempt.
- `scenarios/phase-2/redis-unavailable.md`: stop Redis, observe enqueue
  failure, and state what the app can and cannot do without queue
  coordination.

Small helper scripts live under `scripts/scenarios/` for common local drills.
Read each scenario first; the scripts are shortcuts for Compose commands, not
hidden setup.

## Review And Assessment

- `reviews/checklists/phase-2-async-review.md`: review checklist for async job
  behavior, Redis/Postgres ownership, retries, idempotency, side effects, and
  user-visible consistency.
- `quizzes/phase-2.md`: short-answer quiz on async work, retries, duplicates,
  Redis versus Postgres, and eventual consistency.
- `interviews/phase-2-backend-distributed.md`: mock interview prompts with
  strong-answer traits.
- `reviews/rubrics/phase-2-capstone.md`: capstone scoring guide.

## Important Boundary

Do not add cache layers or a separate reporting service in Phase 2 yet.
Idempotency is scoped explicitly: report enqueue requests, duplicate completed
report execution, and the local report completion notification each have their
own durable key. Future side effects still need their own duplicate-prevention
design.
