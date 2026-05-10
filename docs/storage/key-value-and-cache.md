# Key-Value Stores And Cache

## Problem This Paradigm Solves

Key-value stores solve fast lookup by exact key, short-lived coordination, rate
limits, locks, counters, sessions, and cached responses. They are strongest
when values can be regenerated or safely lost.

## What OpsLedger Would Gain

OpsLedger already uses Redis for two bounded roles: RQ report job coordination
and one short-lived dashboard response cache. Redis shortens the request path
for report generation and speeds the dashboard read path when a cached response
is available.

The current gain is intentionally narrow. Redis does not own customer identity,
work request state, status history, report output, notification attempts, or
the dashboard read model. If Redis loses data, Postgres should still show the
durable facts and the user-visible state.

## What OpsLedger Would Pay Operationally

OpsLedger pays for another process, configuration value, health surface, logs,
metrics, outage drills, and local/deployment wiring. Operators must understand
which failures are queue failures, cache failures, worker failures, and
Postgres failures.

Cache also creates stale data risk. The dashboard can show an old response
while source-of-truth endpoints already show current work request state.

## Failure Modes

- Redis unavailable: enqueue or cache access fails or degrades.
- Lost queue entry: an accepted-looking Redis job can disappear if durable
  Postgres job state is not checked.
- Stale cache: dashboard summaries lag the read model or source tables.
- Cache stampede: many cache misses hit Postgres at once.
- Hidden correctness dependency: code starts trusting Redis as durable truth.

## Interview Explanation Prompts

- Why is Redis acceptable for OpsLedger queues and cache but not source of
  truth?
- What can a user infer from Postgres when Redis is down?
- What is the difference between the dashboard read model and Redis cache?
- How would you roll back the cache without losing durable data?
- When would you remove Redis rather than expand its role?
