# Modular Monolith Boundaries

## Phase

Phase 3: Careful Boundaries. This exercise belongs here because learners have
already built synchronous request paths and async report jobs, and now need to
name internal ownership before considering service extraction.

## Concepts

- Modular monolith boundaries.
- Ownership of facts.
- Coupling and dependency direction.
- Internal contracts.
- Transaction and consistency boundaries.
- Extraction tradeoffs.

## Prerequisites

- `curriculum/PHASE_PLAN.md`
- `docs/SYSTEM_EVOLUTION.md`
- `docs/architecture/modular-monolith.md`
- `docs/async/phase-2-job-lifecycle.md`
- `docs/async/idempotency.md`
- `docs/async/side-effects-and-outbox.md`
- `exercises/phase-2/07-phase-2-capstone.md`
- The API modules under `services/api/opledger_api/`

## Build/Change Task

Review the API modules and write a short boundary review for `customers`,
`work_requests`, `reports`, `async_jobs`, and `notifications`.

For each module, identify the facts it owns, the facts it only reads, the
public API routes or worker paths that depend on it, and the coupling that
would break if the module were extracted into a separate service.

Then choose one boundary and propose one small code or documentation change
that would make ownership clearer without changing runtime behavior.

## Constraints

- Do not create a new deployable service.
- Do not move database ownership.
- Do not add service-to-service HTTP.
- Do not introduce a generic repository or service framework.
- Do not change public API behavior.
- Treat "service boundaries are expensive" as a design constraint, not a slogan.

## Failure Modes

- Treating every module as a future service by default.
- Confusing report output with source-of-truth work request data.
- Letting notification side effects leak into report rendering.
- Moving transaction boundaries without proving what remains consistent.
- Hiding coupling by renaming files instead of describing ownership.
- Ignoring what operators lose when a local function call becomes a remote call.

## Expected Reasoning

After the exercise, explain why OpsLedger can have internal boundaries while
remaining one deployable service. You should be able to name which module owns
customer identity, work request lifecycle state, report job status, report
rendering, and notification attempts.

You should also be able to explain what would break if each module were
extracted, especially which facts would cross the boundary and which failures
would become network or deployment failures.

## Verification

- Run `./scripts/verify.sh`.
- Confirm all existing API behavior still passes tests.
- Confirm no new Docker service was added.
- Confirm your boundary review names coupling for every reviewed module.
- Confirm any change you make keeps Postgres as the source of truth.

## Reflection Questions

- Which module owns facts, and which module only computes a derived result?
- What coupling is acceptable inside one deployable service but risky over a
  network boundary?
- Which route would become hardest to keep consistent if split into a service?
- What operational evidence would make extraction worth discussing again?
- Which failure mode would be introduced only after service extraction?

## LLM Usage

Write your own module ownership notes first. Then ask an LLM to challenge your
boundary review for hidden coupling, unclear fact ownership, and unsupported
claims about extraction. Do not ask it to invent an extraction plan before you
have defended why the monolith boundary is insufficient.

## Path-Specific Extensions

Backend: add one focused test that locks down behavior across a boundary you
find easy to accidentally break.

Operations: describe the logs, health checks, and runbook steps that would need
to change if report rendering became a separate process.

Architecture: write a short argument for and against extracting report
rendering, then compare it with `docs/adr/0001-report-rendering-boundary.md`.

Interview: explain the difference between module boundaries and service
boundaries using OpsLedger's report rendering path.

## Deployment/Debugging Actions If Relevant

Use local test output and existing Compose checks only. Deployment to Dokku is
not required for this exercise.
