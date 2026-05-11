# Phase 6 Language And Runtime Mock Interview

Use these prompts after the learner has read `docs/languages/` and completed
the Phase 6 runtime selection exercise. The goal is to defend runtime choices
from OpsLedger evidence, not to rank languages by reputation.

## Current Stack

### Why is Python/FastAPI still the primary OpsLedger stack?

Strong-answer traits:

- Names the API, worker, reporting implementation, tests, and repo-root `uv`
  workflow.
- Connects Python to readable backend coordination, FastAPI schemas,
  SQLAlchemy, Alembic, pytest, Ruff, and mypy.
- Says the current pressure is architecture, data ownership, retries,
  observability, and performance measurement, not proven Python runtime limits.
- Names the cost: runtime type risk, dependency discipline, CPU-bound work, and
  the need for tests.

### Which OpsLedger component is easiest to rewrite in another language?

Strong-answer traits:

- Chooses the stateless reporting service.
- Points to `report-rendering.v1` as a stable contract.
- Explains that the service owns no Postgres or Redis facts.
- Says the API and worker are harder because they own durable workflow state.

## Go

### Would you rewrite the report renderer in Go?

Strong-answer traits:

- Allows it as an optional contract-compatible exercise or measured narrow
  rewrite.
- Names Go strengths: small binaries, HTTP standard library, context
  deadlines, concurrency, and simple containers.
- Requires contract tests, logs, metrics, timeout behavior, and rollback.
- Rejects it if there is no measured pressure or team fluency.

## TypeScript And Node

### When would TypeScript/Node be a good OpsLedger choice?

Strong-answer traits:

- Frames it as team productivity or schema-sharing, not automatic speed.
- Names full-stack teams, API clients, tooling, and I/O-heavy services.
- Mentions event-loop blocking risk for CPU-heavy rendering.
- Requires dependency discipline, contract tests, and operational parity with
  the Python service.

## JVM

### Why not move OpsLedger to a JVM stack now?

Strong-answer traits:

- Acknowledges JVM strengths for enterprise integration, mature service
  platforms, typing, diagnostics, and large-team standards.
- Names the current mismatch: small VPS, small team, readable learning system,
  and no enterprise integration pressure.
- Mentions memory, startup, build-tool, and framework complexity.
- Leaves room for a future integration-heavy component if evidence changes.

## Rust

### Would Rust help OpsLedger?

Strong-answer traits:

- Names potential Rust fit: CPU-heavy rendering, resource-sensitive utility, or
  safety-critical parser after profiling.
- Says Rust does not solve database ownership, retries, stale cache, or
  contract compatibility by itself.
- Mentions learning curve and incident-debugging cost.
- Keeps the core API and worker in Python unless measured evidence changes.

## BEAM And Elixir

### When would BEAM/Elixir fit OpsLedger?

Strong-answer traits:

- Names realtime operations dashboards, collaboration, pub/sub, supervision,
  or long-running concurrent workflow coordination.
- Distinguishes BEAM supervision from durable Postgres job state.
- Rejects Elixir for current report rendering unless there is a specific
  concurrency or realtime need.
- Mentions team fluency in releases, supervision, processes, and observability.

## Polyglot Judgment

### How do you know a polyglot design is justified?

Strong-answer traits:

- Starts with a component-specific constraint and evidence.
- Requires a narrow boundary, stable contract, equivalent observability,
  test coverage, and rollback.
- Names the extra cost: toolchains, lockfiles, CI, containers, config, logs,
  metrics, dependency updates, and incident debugging.
- Says novelty or resume value is not enough.

### What would make you fold a second-language renderer back into Python?

Strong-answer traits:

- Names weak or absent performance evidence, contract drift, incident-debugging
  burden, dependency churn, or team turnover.
- Explains rollback through the existing Python renderer and worker config.
- Confirms no durable state should be lost because rendering is stateless.
- Preserves the contract even if the deployment shape changes.
