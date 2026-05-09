# Phase 2 Backend And Distributed Systems Mock Interview

Use these prompts after the learner has completed the Phase 2 exercises and
written scenario notes. The goal is concrete reasoning from OpsLedger evidence,
not memorized distributed-systems slogans.

## Async Design

### Why did OpsLedger add a background worker?

Strong-answer traits:

- Starts from measured synchronous report pain.
- Explains why slow request-path work hurts users and operators.
- Describes the API, Redis queue, worker, and Postgres status surfaces.
- Avoids claiming a separate service was required.

### What does `202 Accepted` mean in this system?

Strong-answer traits:

- Says the request was accepted for later work.
- Separates acceptance from completion.
- Names the status and result endpoints.
- Explains honest caller behavior while the report is unavailable.

## Durable State And Queue Coordination

### What owns truth: Redis or Postgres?

Strong-answer traits:

- Names Postgres as owner of durable user-visible state.
- Names Redis as queue and retry coordination.
- Explains what can be lost or unavailable in Redis.
- Uses a worker-down or Redis-down scenario as evidence.

### How do you debug a report that never completes?

Strong-answer traits:

- Checks job status, attempt metadata, result availability, and errors.
- Inspects worker logs and whether the worker is running.
- Distinguishes Redis unavailable, worker unavailable, and job failure.
- Avoids changing retry code before collecting evidence.

## Retries And Idempotency

### Why are retries dangerous without idempotency?

Strong-answer traits:

- Explains that the same business intent may execute more than once.
- Names duplicate output, notification attempts, audit rows, files, or provider
  sends as risks.
- Separates attempt evidence from duplicate prevention.
- Connects the answer to the retry failure scenario.

### Explain the three idempotency boundaries in Phase 2.

Strong-answer traits:

- Request idempotency: repeated enqueue with same key returns original job.
- Job idempotency: duplicate worker execution after success does not rebuild
  completed output.
- Side-effect idempotency: notification completion key prevents duplicate
  attempts.
- States that future effects need their own design.

## Side Effects

### Why does notification failure not make the report fail?

Strong-answer traits:

- Separates report result from later delivery attempt.
- Explains durable `notification_attempts` visibility.
- Names the local adapter and deterministic failed-recipient path.
- Discusses the remaining outbox gap honestly.

### What would change with a real email provider?

Strong-answer traits:

- Mentions credentials, provider idempotency, rate limits, retries, delivery
  status, bounces, and observability.
- Explains why a dispatcher would be needed for recovery.
- Keeps provider work out of the current phase.
- Avoids hiding provider failures in logs only.

## Scope And Architecture

### Why not split the worker into a separate service boundary yet?

Strong-answer traits:

- Distinguishes a separate process from a separate service ownership boundary.
- Explains that one codebase keeps data ownership and transactions visible.
- Names the extra costs of service extraction.
- States what future evidence could justify extraction.

### Why is caching not part of this phase?

Strong-answer traits:

- Says Phase 2 is about async reliability, not read performance.
- Names Postgres as source of truth for report state.
- Explains that caching would introduce staleness and invalidation questions
  before measured pressure exists.
- Defers performance work to the appropriate phase.
