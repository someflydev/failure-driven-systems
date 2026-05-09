# Phase 2 Async Review Checklist

Use this checklist when reviewing Phase 2 report jobs, retries, idempotency,
notification attempts, and scenario evidence. Keep feedback tied to behavior
that exists now.

## Async API Behavior

- The synchronous report route remains available for comparison and controlled
  delay practice.
- The enqueue route returns `202 Accepted` only after creating an inspectable
  `report_jobs` row.
- The status endpoint reports durable Postgres state, not RQ internals.
- The result endpoint returns report output only after `status = succeeded` and
  `result_json` exists.
- User-facing language does not imply that accepted means complete.

## Redis And Postgres Ownership

- Postgres owns report job identity, status, attempt metadata, failures,
  completed output, idempotency keys, and notification attempts.
- Redis owns queue coordination and retry scheduling only.
- Queue failure is visible as `503 report_queue_unavailable` and durable failed
  job evidence.
- Reviews do not treat Redis job ids as user-facing truth.

## Retries And Failure Evidence

- Retry limits are bounded and configured explicitly.
- Failed worker attempts persist `last_error`, `error_message`,
  `last_failed_at`, `finished_at`, and incremented `attempt_count`.
- Retries re-raise worker failures so RQ can apply the configured policy.
- Attempt evidence is not described as idempotency or duplicate prevention.

## Idempotency And Duplicates

- Repeated enqueue requests with the same `Idempotency-Key` return the original
  report job.
- The database uniqueness constraint is the final guard for request
  idempotency.
- Duplicate worker execution after success returns without rebuilding output.
- Duplicate notification triggers return the existing durable attempt.
- Requests without an idempotency key still create fresh report jobs.

## Side Effects

- Report success and notification delivery are separate durable facts.
- Notification attempts have their own idempotency key.
- A local adapter failure records a failed attempt without changing the report
  back to failed.
- The current workflow is not described as a full outbox dispatcher.
- The crash window between report completion and attempt creation is named.

## Scenario Evidence

- Worker unavailable, delayed completion, retry failure, duplicate execution,
  failed notification, and Redis unavailable drills have concrete observations.
- Learner notes include status responses, logs or test output, and at least one
  database-backed inspection.
- Scenario cleanup restores stopped Compose services.
- No scenario requires deleting volumes or using real notification providers.

## Scope Control

- Do not add extracted services.
- Do not add Kubernetes or k3s manifests.
- Do not add caching or performance optimization in Phase 2.
- Do not add broad observability stacks; logs, status endpoints, tests, and
  durable rows are enough.
