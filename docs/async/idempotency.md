# Report Job Idempotency

OpsLedger introduces idempotency only for Phase 2 work request summary report
jobs. It does not claim that every future endpoint, worker, notification, or
export is globally idempotent.

The operating rule is: duplicates must be tolerated or prevented consciously.
Background workers, HTTP retries, client timeouts, and queue redelivery can all
make the same business intent appear more than once.

## Request Idempotency

`POST /reports/work-requests/summary/jobs` accepts an explicit
`Idempotency-Key` header. When a caller repeats the same key for the same
report type, the API returns the original `ReportJob` row instead of creating a
second durable job record or enqueueing duplicate work.

The key is caller supplied because the API cannot always infer whether two
report requests with identical parameters represent one retry or two real
requests. A deterministic request fingerprint can be useful when the request
body contains stable business identifiers, but this endpoint has no body and no
natural time window. An explicit key makes the caller state the duplicate
boundary.

Requests without an `Idempotency-Key` still create new jobs. That preserves the
meaning of a fresh report request.

## Database Constraint

The `report_jobs` table enforces uniqueness on:

```text
(report_type, idempotency_key)
```

The route checks for an existing row before insertion, but the database
constraint is the authority. Two near-simultaneous requests can both pass an
application-level existence check. The unique constraint makes one insert win;
the loser rolls back and reloads the original job.

Redis is not the authority for duplicate prevention. Redis/RQ coordinates work
delivery, but Postgres owns durable request identity and user-visible job
state.

## Job Idempotency

A report job can be delivered to a worker more than once. Retries after failure
are expected, and duplicate execution after success must not overwrite a
completed durable result.

Before generating the report, the worker loads the durable `ReportJob`. If the
job is already `succeeded` and has `result_json`, the worker exits without
incrementing `attempt_count`, rebuilding the report, or changing the stored
output. Failed jobs can still be retried because they do not have completed
output.

## Side-Effect Idempotency

The current report output is stored on the `report_jobs` row. That makes the
duplicate-execution guard small: do not create a second result when the first
durable result already exists.

OpsLedger's first concrete side effect is a local report completion
notification. It uses a `notification_attempts` row with a durable
`report_job:{report_job_id}:completed` key so duplicate triggers return the
existing attempt instead of writing another durable side effect.

Future effects need their own duplicate strategy. Examples:

- notification sends need a stable notification identity or send ledger
- exported files need deterministic object names or unique export records
- audit rows need event identity so retries do not write conflicting history
- billing events need stronger external idempotency guarantees

Request idempotency prevents duplicate job records for repeated enqueue
attempts. Job idempotency prevents completed worker output from being
regenerated. Side-effect idempotency prevents repeated external or durable
effects when execution happens more than once. They are related, but they are
not interchangeable.
