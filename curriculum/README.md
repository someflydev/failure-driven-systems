# Curriculum

The curriculum is organized into six phases. Concepts must appear only when the
learner has enough direct experience to understand the failure or friction that
motivates them.

## Phase 1: Single Service Fundamentals

Start with one deployable service and Postgres as the source of truth. The
learner should practice request handling, validation, persistence, transactions,
migrations, logs, configuration, and simple deployment through Dokku.

Boundaries:

- Do not introduce queues yet.
- Do not introduce Redis yet.
- Do not split services yet.
- Do not introduce k3s yet.
- Do not teach architecture diagrams before the learner can explain the running
  system.

## Phase 2: Async After Synchronous Pain

Introduce asynchronous work only after synchronous flows create observable pain:
slow requests, retry hazards, partial completion, user-visible delays, or
operational coupling.

Concepts may include background jobs, idempotency, retries, dead-letter thinking,
outbox-style reasoning, and backpressure. The learner must be able to explain
what failed in the synchronous design before naming the async pattern.

## Phase 3: Careful Boundaries

Teach module boundaries, data ownership, interfaces, and coupling before any
service extraction. The default remains a modular monolith unless a concrete
failure makes separate deployment or ownership defensible.

Concepts may include bounded contexts, internal APIs, dependency direction,
transaction boundaries, and integration contracts. Service sprawl is treated as
a cost, not a maturity signal.

## Phase 4: Observability And Incidents

Operational judgment becomes explicit. Learners should investigate failures,
read logs, inspect database state, reason about deploys, write incident
timelines, and propose small corrective changes.

Concepts may include metrics, traces, structured logs, alerts, runbooks, error
budgets, rollback thinking, and incident review. Tooling should remain modest
and compatible with the constrained VPS environment.

## Phase 5: Performance, Caching, And Read Models

Introduce optimization only after measurement shows pressure. Redis, caching,
read models, denormalization, pagination strategy, indexing strategy, and
materialized views should be tied to observed bottlenecks or product needs.

Every derived-state lesson must identify the source of truth, invalidation or
rebuild strategy, and failure mode when derived state becomes stale or wrong.

## Phase 6: Architecture And Interviews

The final phase turns experience into explanation. Learners practice defending
architecture decisions, comparing alternatives, identifying failure modes, and
answering system design questions from concrete project history.

LLM use belongs here as interviewer, critic, and reviewer. The learner should
answer, defend, revise, and explain. The LLM should not replace the learner's
reasoning or produce unexamined architecture.
