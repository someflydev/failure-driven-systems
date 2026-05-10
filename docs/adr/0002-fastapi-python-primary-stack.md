# ADR 0002: FastAPI And Python As The Primary Stack

## Status

Accepted

## Context

OpsLedger is a learning system for one engineer or a small team operating a
modest backend on a constrained VPS. The current workload is CRUD, report job
orchestration, worker execution, simple HTTP service boundaries, logs, metrics,
and small performance baselines.

The implemented code lives under `services/api/opledger_api/` and
`services/reporting/reporting_service/`. Tooling is repo-root Python 3.12 with
`uv`, Ruff, mypy, and pytest as described in `docs/TECH_STACK.md` and
`pyproject.toml`.

## Decision

Use Python and FastAPI as the primary application stack for the API and the one
stateless reporting service. Keep the worker in the same Python codebase so
Phase 2 through Phase 5 learners can inspect request paths, job paths,
database writes, logs, and tests without crossing language boundaries.

This does not claim Python is the best runtime for every future component.

## Alternatives Considered

- Go: attractive for small operational binaries and concurrency-heavy services,
  but it would split the early curriculum across language ecosystems before
  the system has runtime pressure that needs it.
- Node: useful for full-stack teams, but OpsLedger's current backend learning
  goals benefit more from Python's type-hinted FastAPI, SQLAlchemy, and pytest
  ecosystem.
- JVM stack: strong for enterprise teams and long-lived service platforms, but
  heavier than needed for a small VPS learning system.
- Rust or Elixir: reasonable for specific performance, safety, or concurrency
  needs, but no current OpsLedger measurement or failure justifies that cost.

## Consequences

FastAPI gives learners visible request and response schemas, OpenAPI output,
dependency injection, and ordinary HTTP behavior. Python keeps tests, scripts,
baseline tooling, worker code, and report rendering in one accessible language.

The tradeoff is that CPU-heavy rendering, very high concurrency, or memory
pressure may eventually point to another runtime or tighter implementation.
The current measured workload does not require that move.

## Failure Modes

- Slow CPU-bound report rendering can tie up a worker process.
- Weak type discipline can leak runtime errors if schemas and tests are not
  maintained.
- Python dependency or packaging drift can break deployment if `uv.lock` and
  verification are ignored.
- FastAPI route behavior can look correct locally while failing readiness in a
  deployed environment without Postgres connectivity.

## Operational Cost

The team operates one Python dependency graph, one `uv` workflow, one root
`Dockerfile`, and a single verification gate through `./scripts/verify.sh`.
The cost is modest, but every deploy still needs migrations, config checks,
logs, health checks, and rollback planning.

## Rollback Or Reversal

Individual components can be rewritten later behind stable contracts. The
report rendering boundary is the easiest candidate because
`docs/contracts/report-rendering-v1.md` already describes the HTTP contract.
Rewriting the core API would be a larger migration because it owns routes,
database transactions, migrations, and durable job state.

## Interview Defense

Python with FastAPI fits OpsLedger because the workload is ordinary backend
coordination, the team is small, the teaching value of readable code is high,
and the operational target is a small VPS rather than a high-throughput
platform. I would revisit this if measured CPU, memory, latency, hiring, or
ecosystem constraints made Python the bottleneck instead of the surrounding
architecture.
