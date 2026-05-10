# ADR 0004: Redis For Queue And Cache With Postgres Durability

## Status

Accepted

## Context

Phase 2 introduced Redis and RQ after synchronous report generation created
request-path pain. Phase 5 reused Redis for one dashboard cache after baseline
and staleness exercises. The current local stack runs Redis through
`docker-compose.yml`, and the API config reads `OPLEDGER_REDIS_URL`.

Relevant docs include `docs/async/phase-2-job-lifecycle.md`,
`docs/performance/caching.md`, `scenarios/phase-2/redis-unavailable.md`, and
`scenarios/phase-5/redis-cache-unavailable.md`.

## Decision

Use Redis as an ephemeral coordination layer for RQ report jobs and as the
cache backend for the derived customer dashboard endpoint. Keep report job
requests, job status, attempts, completed output, notification attempts, and
source data durable in Postgres.

## Alternatives Considered

- Run slow reports synchronously: simplest, but Phase 2 intentionally measured
  the user-facing pain before moving report work to a worker.
- Use Postgres-only job polling: fewer dependencies, but less representative of
  common worker queue operations and retry coordination.
- Use a managed queue: operationally useful, but outside the baseline
  self-operated VPS constraint.
- Cache in-process only: cheaper, but it would not exercise shared cache
  failure, stale data, or Redis outage behavior across processes.

## Consequences

Redis shortens request paths for report work and speeds one read-model endpoint
when the cache is warm. Its failures are bounded because authoritative facts
remain in Postgres.

The tradeoff is another process to run, inspect, and secure. Pending queued
jobs or cached values may disappear if Redis is restarted or flushed. The
system must make that loss visible through durable Postgres state and honest
user-facing status.

## Failure Modes

- Redis unavailable during enqueue: report job creation or queue coordination
  fails and must be visible to the API caller and logs.
- Worker unavailable: durable job state can stop progressing even though the
  original request was accepted.
- Redis cache unavailable: dashboard reads should fall back to Postgres-backed
  read model behavior without corrupting source data.
- Stale cache: dashboard output can lag current source-of-truth state until TTL,
  bypass, or rebuild behavior catches up.

## Operational Cost

Local Compose and any later full deployment must run Redis alongside Postgres,
the API, and the worker. Operators need Redis health checks, log evidence,
cache metrics, and scenario drills. The cost is acceptable here because Redis
now serves two explicitly taught roles, not because every system needs Redis.

## Rollback Or Reversal

Queue usage can be temporarily avoided only by returning to synchronous report
generation or disabling report enqueue paths, which reintroduces request-path
pain. Cache usage can be bypassed with endpoint controls or removed while
leaving the read model intact. Neither rollback should delete durable Postgres
report job or dashboard source data.

## Interview Defense

Redis is deliberately non-authoritative in OpsLedger. It handles coordination
and cache speed, while Postgres keeps facts. That is the key tradeoff: accept
an extra operational process and possible lost ephemeral state, but avoid
making Redis the place where correctness lives.
