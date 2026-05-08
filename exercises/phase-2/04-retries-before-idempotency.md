# Retries Before Idempotency

## Phase

Phase 2: Async After Synchronous Pain. This exercise belongs here because the
learner has already moved report generation to a worker and now needs to see
how retries change failure behavior before the system is made idempotent.

## Concepts

- Bounded retry attempts.
- Backoff as an operational choice.
- Durable failure evidence.
- Controlled local failure injection.
- Duplicate side-effect risk.
- Retry behavior before idempotency.

## Prerequisites

- `exercises/phase-2/01-synchronous-report-pain.md`
- `exercises/phase-2/02-background-report-worker.md`
- `exercises/phase-2/03-job-status-and-eventual-consistency.md`
- `docs/async/phase-2-job-lifecycle.md`
- `scenarios/phase-2/report-retry-failure.md`
- `services/api/opledger_api/report_jobs.py`
- `services/api/opledger_api/models.py`
- `services/api/opledger_api/config.py`
- `services/api/tests/test_report_jobs.py`
- Local API, Postgres, Redis, worker, and migration workflow.

## Build/Change Task

Run the report retry failure scenario. Enable local failure injection for the
report worker, enqueue a report, observe failed attempts, and inspect the
durable job state through the status endpoint and database.

Before implementing any idempotency fix, write a short note answering: what
could duplicate? Consider the current report result write and plausible next
side effects such as notification sends, audit rows, exported files, or billing
events.

Then review the bounded retry configuration. Identify the maximum total
attempts, the backoff intervals, and which fields persist after each attempt.

## Constraints

- Do not solve idempotency yet.
- Do not add duplicate suppression.
- Do not add a second service.
- Do not make retries unbounded.
- Do not hide worker exceptions.
- Do not enable failure injection outside local or test environments.
- Keep Postgres as the durable source of job truth.
- Treat Redis/RQ retry metadata as coordination, not the user-facing record.

## Failure Modes

- Saying retries are safe because the report "usually" succeeds.
- Forgetting that a retry re-runs application code.
- Recording only logs and leaving no durable failed-attempt evidence.
- Allowing an infinite retry loop.
- Confusing RQ retry count with total attempt count.
- Enabling failure injection in production-like settings.
- Naming an idempotency pattern before identifying the duplicated effect it
  would prevent.

## Expected Reasoning

After completing this exercise, explain why a failed report job can be retried
without losing the evidence of prior attempts. Be precise about which fields in
`report_jobs` change on each attempt and why RQ's retry metadata is not enough
for user-facing status.

You should also be able to answer "what could duplicate?" before naming the
final pattern. The important reasoning step is identifying repeated effects,
not memorizing an idempotency label.

## Verification

- Run `./scripts/verify.sh`.
- Start the local stack with `./scripts/dev-up.sh`.
- Apply migrations with `./scripts/migrate.sh --compose`.
- Run `scenarios/phase-2/report-retry-failure.md`.
- Confirm the Compose-managed worker is stopped before starting the
  injected-failure worker, so only one worker consumes the report queue.
- Confirm a failed job records `attempt_count`, `last_error`,
  `last_failed_at`, `finished_at`, and `status = failed`.
- Confirm the default retry behavior is three total attempts: original attempt
  plus two RQ retries.
- Confirm the default backoff is 1 second before the first retry and 5 seconds
  before the second retry.
- Confirm the exercise note answers "what could duplicate?" before naming the
  final idempotency pattern.

## Reflection Questions

- What exactly happens again when RQ retries the report job?
- Which persisted fields prove that more than one attempt occurred?
- What could duplicate if report completion later sends a notification?
- What could duplicate if report completion later writes an audit row or stores
  an exported file?
- Why does bounded retry improve recovery without solving duplicate effects?
- Why should failure injection be disabled by default and limited to local or
  test environments?

## LLM Usage

Use an LLM as a reviewer after you have captured your own attempt evidence and
duplicate-risk note. Ask it to challenge whether your "what could duplicate?"
answer is concrete enough, whether your retry count math is correct, and
whether your proposed next fix is justified by observed behavior. Do not ask it
to provide the idempotency solution before you identify the repeated effects.

## Path-Specific Extensions

Backend: add a focused test that proves the durable attempt count changes when
the worker function is executed more than once.

Operations: capture worker logs and status endpoint output for each attempt,
then write an incident-style note explaining what the operator can trust.

Architecture: diagram the retry path and mark which facts live in Postgres,
which live in Redis, and which facts disappear when Redis is lost.

Interview: practice explaining why retries and idempotency are related but not
the same design decision.

## Deployment/Debugging Actions If Relevant

Run this exercise locally only. Do not enable report failure injection in
production-like deployments.
