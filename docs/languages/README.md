# OpsLedger Runtime Decision Guide

OpsLedger currently uses Python and FastAPI for the API, worker code, and the
stateless reporting service. That is an intentional default for a small
learning system, not a claim that Python is always the best runtime.

Runtime choices should be defended the same way datastore and service-boundary
choices are defended: start with the workload, team, operational target,
failure modes, and rollback path. A second language is justified only when the
constraint is strong enough to pay for another build, test, deploy, debugging,
and hiring surface.

## Current Baseline

- API: Python/FastAPI owns HTTP routes, validation, transactions, and durable
  state changes.
- Worker: Python/RQ executes report jobs, updates durable job state, calls
  report rendering, and records notification attempts.
- Reporting service: Python/FastAPI stateless HTTP service that renders a
  complete `report-rendering.v1` snapshot.
- Postgres: durable source of truth.
- Redis: ephemeral queue and dashboard-cache coordination.
- Deployment target: local Compose for learning and a Dokku-first path for the
  API on a constrained VPS.

The cheapest responsible answer remains: keep the main path Python/FastAPI
until measured CPU, memory, concurrency, release ownership, ecosystem, or team
constraints make that choice the bottleneck.

## Decision Questions

Before proposing another runtime for an OpsLedger component, answer:

1. Which component is under pressure: API, worker, reporting service, CLI,
   background processor, dashboard support, or future integration?
2. What evidence shows pressure: baseline, incident, log, metric, profile,
   deployment issue, team constraint, or contract requirement?
3. Is the work stateful or stateless? Which facts would the component own?
4. Can the existing Python implementation be improved with simpler changes?
5. What new operational surface appears: packaging, container image, health
   checks, logs, metrics, config, dependency updates, and rollback?
6. Can the component be isolated behind a stable contract?
7. Does the team have enough fluency to debug this runtime during an incident?
8. What would make the team reverse the decision?

If these answers are weak, do not add a language boundary.

## Comparison Index

- `docs/languages/python.md`
- `docs/languages/go.md`
- `docs/languages/typescript-node.md`
- `docs/languages/jvm.md`
- `docs/languages/rust.md`
- `docs/languages/beam-elixir.md`
- `docs/languages/polyglot-systems.md`

## Interview Framing

A strong OpsLedger runtime answer does not rank languages in the abstract. It
says what the component does, what currently hurts, what the runtime improves,
what it costs a small team, and how the boundary can fail. For example:
"I would keep the API and worker in Python because they own transactions, job
state, and the current test workflow. I might consider Go or TypeScript for the
stateless report renderer only behind the existing report-rendering contract,
and only if profiling, team skill, or deployment constraints made that move
worth another service toolchain."
