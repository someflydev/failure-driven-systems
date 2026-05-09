# Contract Before Network

## Phase

Phase 3: Careful Boundaries. This exercise belongs here because learners need
to practice contract compatibility while report rendering is still an internal
module boundary, before adding HTTP, deployment, or network failure.

## Concepts

- Versioned module contracts.
- Backward-compatible schema changes.
- Required versus optional fields.
- Unknown field behavior.
- Deterministic rendering tests.
- Difference between internal contracts and deployable services.

## Prerequisites

- `docs/architecture/modular-monolith.md`
- `docs/adr/0001-report-rendering-boundary.md`
- `docs/contracts/report-rendering-v1.md`
- `exercises/phase-3/01-modular-monolith-boundaries.md`
- `services/api/opledger_api/report_contracts.py`
- `services/api/opledger_api/reports.py`
- `services/api/opledger_api/report_jobs.py`
- `services/api/tests/test_report_rendering_contract.py`

## Build/Change Task

Change the report rendering contract in a backward-compatible way while keeping
report rendering inside the monolith.

Choose one small optional addition, such as an optional input field that changes
non-core rendering behavior or an optional response field with a safe default.
Update the contract schema, renderer, contract tests, and contract
documentation. The old minimum valid request must still validate, and the same
known input should still produce deterministic output unless your new optional
field is present.

## Constraints

- Do not create a separate service.
- Do not add HTTP calls between modules.
- Do not add protobuf, Avro, gRPC, or a schema registry.
- Do not move source-of-truth facts out of Postgres.
- Do not make existing optional fields required.
- Do not remove or rename existing v1 fields.
- Do not change queue, retry, or notification behavior unless the contract
  change truly requires it.

## Failure Modes

- Calling a field "optional" while tests or code require every caller to send
  it.
- Accepting unknown fields and accidentally hiding caller/renderer drift.
- Changing deterministic output for existing inputs.
- Treating `report-rendering.v1` as approval to add a second deployable
  service.
- Moving database queries into the renderer and blurring source-of-truth
  ownership.
- Updating docs without adding compatibility tests.

## Expected Reasoning

After completing the exercise, explain why your change is backward-compatible
for existing callers and persisted report results. You should be able to name
which tests prove old callers still work, which tests prove the new field works,
and why the boundary is still an internal module contract rather than a network
contract.

You should also be able to describe what would become harder if this contract
were used over HTTP: version negotiation, timeout behavior, retries,
observability, and operational rollback.

## Verification

- Run `./scripts/verify.sh`.
- Confirm the old minimum valid render request still validates.
- Confirm a request using your new optional field validates and produces the
  expected behavior.
- Confirm an unknown field still fails validation.
- Temporarily remove one required contract field in a local test run and
  confirm the contract tests fail, then restore it before committing.
- Confirm docs still distinguish the internal module boundary from a deployable
  service boundary.

## Reflection Questions

- Why is this change backward-compatible?
- Which existing caller would break if the field were required?
- Why does rejecting unknown fields help before there is any network boundary?
- What source-of-truth facts still belong to Postgres rather than the renderer?
- What additional failure modes would HTTP introduce that this exercise avoids?

## LLM Usage

Write the schema change and tests yourself first. Then ask an LLM to review
whether the change is truly backward-compatible, whether the tests prove old
and new callers both work, and whether any wording accidentally implies a
service extraction has happened.

Do not ask an LLM to design an extraction plan for this exercise.

## Path-Specific Extensions

Backend: add a focused test that proves the async worker persists the new
optional response field only when expected.

Operations: list the logs, metrics, and rollback notes that would be needed if
this contract later crossed an HTTP boundary.

Architecture: write a short note explaining why a versioned contract is useful
inside one deployable service.

Interview: explain the difference between schema compatibility and network
resilience using this report rendering boundary.

## Deployment/Debugging Actions If Relevant

Use local verification only. Deployment is not required, and no new runtime
process should be introduced for this exercise.
