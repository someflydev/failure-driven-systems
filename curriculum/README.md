# Curriculum

The curriculum is organized into six phases. Concepts must appear only when the
learner has enough direct experience to understand the failure or friction that
motivates them.

## Phase 1: Single Service Fundamentals

Start with one deployable service and Postgres as the source of truth. The
learner should practice request handling, validation, persistence, transactions,
migrations, logs, configuration, and simple deployment through Dokku.

Phase 1 deployment materials:

- `deploy/dokku/README.md`
- `deploy/dokku/checklist.md`
- `ops/runbooks/dokku-api-incident.md`
- `exercises/phase-1/06-dokku-first-deploy.md`

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

Phase 2 concrete path:

- `lessons/phase-2/README.md`
- `docs/async/phase-2-job-lifecycle.md`
- `docs/async/idempotency.md`
- `docs/async/side-effects-and-outbox.md`
- `scenarios/phase-2/`
- `reviews/checklists/phase-2-async-review.md`
- `quizzes/phase-2.md`
- `interviews/phase-2-backend-distributed.md`
- `reviews/rubrics/phase-2-capstone.md`

Boundaries:

- Do not extract services yet.
- Do not introduce Kubernetes or k3s yet.
- Do not add caching or read-model optimization yet.
- Do not add a broad observability stack; durable status, logs, tests, and
  focused scenario evidence are enough.

## Phase 3: Careful Boundaries

Teach module boundaries, data ownership, interfaces, and coupling before any
service extraction. The default remains a modular monolith unless a concrete
failure makes separate deployment or ownership defensible.

Concepts may include bounded contexts, internal APIs, dependency direction,
transaction boundaries, and integration contracts. Service sprawl is treated as
a cost, not a maturity signal.

Phase 3 concrete path:

- `lessons/phase-3/README.md`
- `docs/architecture/modular-monolith.md`
- `docs/adr/0001-report-rendering-boundary.md`
- `docs/contracts/report-rendering-v1.md`
- `docs/contracts/compatibility-playbook.md`
- `scenarios/phase-3/`
- `reviews/checklists/phase-3-service-boundary-review.md`
- `quizzes/phase-3.md`
- `interviews/phase-3-distributed-boundaries.md`
- `reviews/rubrics/phase-3-capstone.md`

Boundaries:

- Extract only the stateless report renderer in this phase.
- Do not add another deployable service.
- Do not move source-of-truth ownership out of the core API and Postgres.
- Do not introduce Kubernetes or k3s yet.
- Do not add caching, performance optimization, or broad observability stack
  work.
- Require learners to defend the extraction decision, including the option to
  fold the renderer back into the monolith.

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

Runtime and language comparisons belong here because learners can now tie
Python, Go, TypeScript/Node, JVM, Rust, BEAM/Elixir, and polyglot tradeoffs to
actual OpsLedger components instead of debating them generically.

LLM use belongs here as interviewer, critic, and reviewer. The learner should
answer, defend, revise, and explain. The LLM should not replace the learner's
reasoning or produce unexamined architecture.
