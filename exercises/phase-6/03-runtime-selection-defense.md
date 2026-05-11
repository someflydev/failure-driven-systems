# Runtime Selection Defense

## Phase

Phase 6: architecture defense, system design, and interview readiness.

This exercise belongs here because the learner can now compare runtime choices
against the actual OpsLedger API, worker, reporting service, Postgres, Redis,
and deployment constraints instead of ranking languages in the abstract.

## Concepts

- Runtime and language tradeoffs.
- Component boundaries and contract compatibility.
- Team productivity and incident-debugging capability.
- Deployment and operability cost.
- Performance claims grounded in evidence.
- Polyglot restraint.

## Prerequisites

Read these before starting:

- `docs/architecture/current-system.md`
- `docs/TECH_STACK.md`
- `docs/adr/0001-report-rendering-boundary.md`
- `docs/adr/0002-fastapi-python-primary-stack.md`
- `docs/contracts/report-rendering-v1.md`
- `docs/languages/README.md`
- every comparison doc in `docs/languages/`
- `docs/languages/polyglot-systems.md`
- `exercises/phase-6/01-decision-memo-defense.md`
- `exercises/phase-6/02-datastore-tradeoff-defense.md`

You should also understand why the reporting service is stateless, why the API
and worker own durable workflow behavior, and why the main implementation
stays Python/FastAPI.

## Build/Change Task

Write a runtime selection defense for one proposed OpsLedger component:

- keep the API in Python/FastAPI;
- keep the worker in Python/RQ;
- rewrite the stateless reporting service in Go;
- rewrite the stateless reporting service in TypeScript/Node;
- introduce a JVM service for a specific enterprise integration;
- reject Rust for the current report worker;
- reject BEAM/Elixir until OpsLedger has realtime workflow pressure.

Your defense must include:

- the component and current responsibilities;
- the workload evidence or team constraint being considered;
- the selected runtime and two rejected alternatives;
- strengths and weaknesses of the selected runtime for this component;
- deployment, testing, logging, metrics, timeout, and rollback implications;
- how contract compatibility would be proven;
- at least four failure modes;
- a short "do not add this yet" argument when the evidence is weak;
- a two-minute interview answer.

## Constraints

- Do not implement a second-language service in the main path.
- Do not add runtime dependencies, service manifests, lockfiles, generated
  clients, or containers.
- Do not make unsupported speed, memory, or concurrency claims.
- Do not disparage languages; explain fit, constraints, and tradeoffs.
- Do not move source-of-truth ownership out of Postgres.
- Do not let an LLM choose the runtime before you write your own defense.

## Failure Modes

- The defense picks a language because it is popular rather than because
  OpsLedger has a matching constraint.
- The answer treats a stateless report renderer like a source-of-truth service.
- Contract compatibility is assumed instead of tested.
- Logs, metrics, correlation IDs, or timeout behavior are ignored.
- The small-team debugging cost of a second runtime is missing.
- The answer cannot explain what evidence would reverse the decision.

## Expected Reasoning

After completing the exercise, you should be able to defend why Python remains
the main OpsLedger stack, identify the narrow cases where another runtime could
fit, and explain how a polyglot component changes operations even when the code
is simple.

## Verification

- Run `./scripts/verify.sh`.
- Confirm your defense cites at least three concrete OpsLedger artifacts.
- Confirm every runtime claim is tied to a component, workload, or team
  constraint.
- Confirm contract compatibility, observability, timeout behavior, and
  rollback are addressed.
- Confirm no runtime code, dependencies, service manifests, lockfiles, or
  generated artifacts were added.

## Reflection Questions

- Which current OpsLedger component has the cleanest contract boundary?
- What would a second runtime make harder during an incident?
- What measurement would make the Python implementation good enough?
- Which team skill constraint matters more than the language benchmark?
- What would make you fold a polyglot component back into the Python codebase?

## LLM Usage

Use an LLM only after writing your own defense. Ask it to challenge unsupported
performance claims, missing operational costs, weak contract testing, and
language bias. Do not ask it to produce the first draft or choose the runtime
for you.

## Path-Specific Extensions

Backend path: include request handling, serialization, validation, timeouts,
and contract-test implications.

Operations path: include build pipeline, container image, health checks, logs,
metrics, config, dependency updates, and rollback.

Architecture path: compare at least three runtimes and state the evidence that
would make each one reasonable.

Interview path: answer five follow-up questions from
`interviews/phase-6-language-runtime.md` without notes.

## Deployment/Debugging Actions If Relevant

No deployment is required. If your defense depends on runtime evidence, cite
the specific baseline, profile, log event, metric, scenario, health check, or
durable database row you inspected.
