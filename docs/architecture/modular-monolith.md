# Modular Monolith Boundaries

Phase 3 keeps OpsLedger as one deployable service while making internal
ownership explicit. The goal is to teach boundary reasoning before introducing
distributed-system costs.

Service boundaries are expensive. A new deployable service adds independent
release coordination, network failure, duplicated observability needs, security
surface area, local development friction, and harder data consistency questions.
OpsLedger should absorb those costs only after a concrete operational or team
ownership failure proves that an internal module boundary is not enough.

## Current Modules

- `customers`: owns customer identity rules, including duplicate email
  handling. Other modules may reference a customer, but they should not decide
  customer uniqueness.
- `work_requests`: owns work request lifecycle state and status history. It
  records status transitions and protects terminal states.
- `reports`: owns report rendering as pure computation over existing durable
  data. It does not own work request facts; it reads them to produce derived
  output.
- `async_jobs`: owns durable report job status and queue coordination. Postgres
  remains the user-visible source of truth, while Redis/RQ remains coordination
  for worker execution.
- `notifications`: owns durable notification attempts and the local delivery
  adapter. It records side-effect attempts separately from report success.
- `health`: owns liveness and readiness endpoints for the single API process.
- `shared`, `config`, and `db`: provide cross-cutting HTTP dependencies,
  settings, database sessions, and readiness helpers. They are shared
  infrastructure, not domain owners.

## Why These Are Not Services Yet

The modules still share one database and one deployment unit because OpsLedger
has not observed a failure that requires independent scaling, deployment,
runtime isolation, or data ownership. Splitting now would turn simple in-process
function calls into remote contracts without solving a proven problem.

Report rendering is the best first candidate boundary because it can be treated
as deterministic computation over source-of-truth tables. It can be tested and
reasoned about behind an internal contract without moving ownership of
customers, work requests, status events, report jobs, or notification attempts.

## Contract Questions Before Extraction

Before extracting any module, a learner should be able to answer:

- Which module owns each fact that would cross the boundary?
- What input contract is stable enough to call remotely?
- What output contract is durable enough for old callers to tolerate change?
- What happens when the callee is unavailable, slow, or returns partial data?
- Which database writes must remain in the same transaction?
- Which operational evidence proves that in-process modularity is insufficient?

Until those answers are specific, the modular monolith is the teaching target.
