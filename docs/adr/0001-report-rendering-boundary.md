# ADR 0001: Report Rendering Boundary

## Status

Proposed

## Context

OpsLedger has report generation that reads customers, work requests, and status
events to produce a work request summary. Phase 2 moved slow or retry-prone
report generation into background jobs, but Postgres remains the durable source
of truth for job state and report results.

Phase 3 starts by making internal module boundaries explicit. Service
boundaries are expensive, so this ADR evaluates report rendering as a possible
future extraction without approving a second deployable service now.

## Decision

Keep report rendering inside the API process for now, behind the `reports`
module. Treat the module as a clear internal boundary with a narrow rendering
contract, but do not add service-to-service HTTP, a second database, or a new
deployment unit.

## Arguments For Later Extraction

- Report rendering can be modeled as pure computation over an input snapshot.
- Slow rendering could eventually need different CPU or memory sizing than
  request intake.
- A separate runtime could isolate expensive report failures from normal API
  request handling.
- The input and output contracts are easier to define than workflow mutation
  contracts because rendering does not own source-of-truth facts.

## Arguments Against Extraction Now

- Current evidence does not show independent scaling or deployment pressure.
- The renderer still reads source-of-truth data owned by the core API database.
- Remote calls would add timeout, retry, versioning, and observability work.
- A new service would complicate local development and Phase 3 learning before
  learners have defended a concrete need.
- The existing worker-backed design already removes report generation from
  user-facing request paths.

## Consequences

The code should keep report rendering isolated enough to test directly and call
from either synchronous routes or background jobs. Callers should depend on the
report contract, not on incidental query details. Future prompts may revisit
extraction only if measured operational evidence shows the modular monolith is
the wrong boundary.

Making `report-rendering.v1` explicit showed that most of the rendering
boundary can be modeled as pure computation over a caller-provided snapshot:
the database query path assembles counts and timestamps, then the renderer
returns a deterministic response for that typed request. This is useful
internal design even before service extraction because the worker no longer
depends on incidental report query details.

The exercise also exposed costs that would exist before any HTTP boundary:
required fields, extra-field behavior, optional-field compatibility, persisted
result shape, and versioning all need tests. Those contract concerns are
separate from network concerns. A later service extraction would still need
timeouts, retries, deployment isolation, observability, and runbook updates in
addition to the schema contract described in
`docs/contracts/report-rendering-v1.md`.
