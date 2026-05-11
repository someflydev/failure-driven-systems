# Optional Polyglot Report Renderer Extension

This is an optional extension spec. It is not required for the main OpsLedger
path, and it should not be used to turn the repository into a polyglot
showcase.

The main implementation remains Python/FastAPI. This extension asks a learner
to reimplement only the stateless report-rendering service in Go or
TypeScript/Node while preserving the existing `report-rendering.v1` contract.
Do not move API routes, worker orchestration, Postgres ownership, Redis queue
coordination, report job state, or notification attempts into the extension.

## Goal

Build a contract-compatible report renderer in one alternate runtime:

- Go, if the learning goal is small operational binaries, HTTP services,
  context deadlines, and static compilation.
- TypeScript/Node, if the learning goal is schema-driven contract work and
  full-stack team workflow.

The extension is about runtime tradeoff defense and contract compatibility,
not about proving one language is universally better.

## Required Contract

The alternate service must implement the contract in:

- `docs/contracts/report-rendering-v1.md`

It must accept the same complete rendering snapshot and return behavior that is
compatible with the Python reporting service. It must not read from Postgres,
Redis, the API database models, or any source-of-truth store.

## Expected Learner Deliverables

- A short design note explaining why Go or TypeScript was chosen.
- Contract tests or request/response fixtures proving compatibility with
  `report-rendering.v1`.
- Bounded timeout behavior documented for callers.
- Structured logs that preserve request and correlation IDs.
- A health endpoint appropriate for local development.
- A rollback note explaining how to return to the Python renderer.
- A final defense that names what became easier and what became harder.

## Constraints

- Keep this outside the main path unless a later prompt explicitly adopts it.
- Do not add this service to the default Compose stack.
- Do not change the API, worker, durable report job schema, or Postgres
  ownership.
- Do not add a second language implementation without tests proving contract
  compatibility.
- Do not claim performance improvements without measurement against equivalent
  inputs and resource settings.
- Do not use this extension as justification for more services.

## Verification Expectations

At minimum, the learner should be able to show:

- Python and alternate renderers produce compatible responses for the same
  fixtures.
- Bad input, missing required fields, and incompatible versions fail visibly.
- Timeout and health behavior are documented.
- Logs include enough context to debug a report-rendering call.
- The Python main path still passes `./scripts/verify.sh`.

## Discussion Questions

- Was the alternate runtime solving a measured problem, a team constraint, or
  only a learning goal?
- What new build, test, deploy, and incident-debugging work appeared?
- Which contract edge case was easiest to miss?
- How would you decide whether to keep, remove, or never deploy this renderer?
