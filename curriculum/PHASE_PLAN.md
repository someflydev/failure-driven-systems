# OpsLedger Phase Plan

This plan maps the six curriculum phases to concrete OpsLedger capabilities.
Each phase keeps concepts constrained until learners have experienced the
failure or friction that makes the next idea useful.

## Phase 1: Single Service Fundamentals

OpsLedger capability:

- Create, view, update, and list customers and work requests.
- Record status events as work requests move through a simple lifecycle.
- Attach operator notes to work requests.
- Deploy one synchronous service backed by Postgres on a small VPS with Dokku.

Allowed concepts:

- Request handling, validation, persistence, transactions, migrations, logs,
  configuration, simple deployment, and Postgres as source of truth.

Disallowed concepts:

- Queues, Redis, background workers, service extraction, k3s, distributed
  tracing, caching layers, event-driven architecture, and premature read models.

Expected failure experiences:

- Invalid input, missing constraints, confusing status changes, failed
  migrations, weak logs, bad configuration, and basic deploy or rollback
  mistakes.

Explanation outcomes:

- Explain where truth lives, why a transaction is needed, how a status change is
  recorded, how to inspect a failure, and why one deployable service is enough.

## Phase 2: Async After Synchronous Pain

OpsLedger capability:

- Generate reports from work request history.
- Record notification attempts for status changes or report readiness.
- Move slow or retry-prone work out of user-facing request paths.

Allowed concepts:

- Background jobs, retries, idempotency, retry limits, dead-letter thinking,
  worker visibility, outbox-style reasoning, and backpressure.

Disallowed concepts:

- Service extraction, Redis as a default dependency, k3s, broad event
  streaming, independent notification services, and speculative workflow
  orchestration.

Expected failure experiences:

- Slow report requests, duplicate notification attempts, partial completion,
  retry hazards, worker crashes, stuck jobs, and user confusion after a request
  succeeds but follow-up work fails.

Explanation outcomes:

- Explain why synchronous handling hurt the system, what can be retried safely,
  how duplicate side effects are prevented, and how failed background work is
  found and repaired.

## Phase 3: Careful Boundaries

OpsLedger capability:

- Separate internal modules for request intake, workflow state, reporting, and
  notifications while preserving one deployable service by default.
- Define ownership and interfaces around data changes and side effects.

Allowed concepts:

- Module boundaries, dependency direction, data ownership, internal APIs,
  transaction boundaries, integration contracts, and consistency boundaries.

Disallowed concepts:

- Starting from multiple deployable services, database-per-service as a default,
  k3s manifests, message brokers as architecture decoration, and extraction
  without a concrete operational or ownership failure.

Expected failure experiences:

- Tangled dependencies, unclear ownership of status changes, reporting logic
  coupled to write paths, notification code leaking across modules, and
  transaction boundaries that are hard to reason about.

Explanation outcomes:

- Explain which module owns each decision, where coupling remains acceptable,
  what would justify extraction, and what extra costs a split service would add.

## Phase 4: Observability And Incidents

OpsLedger capability:

- Operate OpsLedger under realistic failures: bad deploys, failed migrations,
  stuck reports, noisy notifications, confusing status histories, and degraded
  request handling.
- Produce runbooks and incident timelines tied to actual evidence.

Allowed concepts:

- Structured logs, metrics, traces when justified, alerts, runbooks, incident
  review, rollback thinking, health checks, and operational dashboards that fit
  the constrained VPS.

Disallowed concepts:

- Cluster-centered operations before the VPS deployment model has created the
  need, large observability stacks by default, vague SLOs with no user impact,
  and incident writeups that are not grounded in system evidence.

Expected failure experiences:

- Missing correlation IDs, unclear error ownership, silent worker failure,
  noisy alerts, misleading health checks, slow diagnosis, and rollback
  uncertainty.

Explanation outcomes:

- Explain what happened, how the evidence proves it, what users experienced,
  what small corrective change reduces recurrence, and what should alert a
  human next time.

## Phase 5: Performance, Caching, And Read Models

OpsLedger capability:

- Improve slow work request lists, report queries, dashboard summaries, and
  high-read operational views after measurement shows pressure.
- Introduce derived read models or caching only where the source of truth and
  rebuild path are clear.

Allowed concepts:

- Query plans, indexes, pagination strategy, materialized views, denormalized
  read models, cache keys, invalidation, rebuilds, staleness, Redis when
  justified, and load testing within modest infrastructure limits.

Disallowed concepts:

- Cache-first design, Redis before measured need, derived state without rebuild
  strategy, denormalization that hides truth, and performance work with no
  baseline measurement.

Expected failure experiences:

- Slow dashboards, expensive report queries, pagination drift, stale summaries,
  over-broad cache invalidation, hot reads, and fixes that improve one path
  while harming another.

Explanation outcomes:

- Explain the measured bottleneck, why the chosen optimization fits it, where
  truth lives, how derived state is corrected, and what new failure mode was
  accepted.

## Phase 6: Architecture And Interviews

OpsLedger capability:

- Use the full OpsLedger project history to defend architecture decisions,
  compare alternatives, and answer interview-style system design questions.
- Evaluate whether one carefully extracted boundary is warranted based on the
  failures already observed.

Allowed concepts:

- Architecture tradeoff analysis, system design narratives, capacity reasoning,
  failure-mode comparison, boundary extraction criteria, migration planning, and
  LLM-assisted interview practice where the learner remains accountable.

Disallowed concepts:

- Memorized architecture diagrams, invented scale requirements, unexamined LLM
  answers, technology name-dropping, and service extraction presented as a
  maturity badge.

Expected failure experiences:

- Weak explanations, unsupported scale claims, vague consistency answers,
  inability to defend boundaries, and confusion between source-of-truth and
  derived-state responsibilities.

Explanation outcomes:

- Defend why OpsLedger started as one service, why async work was added, why
  boundaries were drawn where they were, what would justify a service split,
  and how operational evidence shaped the design.
