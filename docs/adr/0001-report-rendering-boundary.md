# ADR 0001: Report Rendering Boundary

## Status

Accepted for learning

## Context

OpsLedger has report generation that reads customers, work requests, and status
events to produce a work request summary. Phase 2 moved slow or retry-prone
report generation into background jobs, but Postgres remains the durable source
of truth for job state and report results.

Phase 3 started by making internal module boundaries explicit. Service
boundaries are expensive, so this ADR first evaluated report rendering as a
possible future extraction before approving any second deployable service.
The workload is a small learning system on local Compose and a constrained VPS,
operated by one learner or a small team. Relevant artifacts include
`services/reporting/reporting_service/`, `services/api/opledger_api/reporting_client.py`,
`docs/contracts/report-rendering-v1.md`, `docker-compose.yml`, and
`scenarios/phase-3/reporting-timeout.md`.

## Decision

Extract only report rendering into a small stateless HTTP service for Phase 3
learning. The new service receives a complete `report-rendering.v1` input
payload and returns rendered report output. It does not connect to Postgres,
Redis, or any other source-of-truth store.

The core API and worker still own data assembly, job orchestration, durable job
state, retries, and persisted report results. The worker calls the reporting
service only when `OPLEDGER_REPORT_RENDERING_SERVICE_URL` is configured. When
that URL is absent, it uses the same pure in-process renderer explicitly for
local development and tests.

## Arguments For Extraction

- Report rendering can be modeled as pure computation over an input snapshot.
- Slow rendering could eventually need different CPU or memory sizing than
  request intake.
- A separate runtime could isolate expensive report failures from normal API
  request handling.
- The input and output contracts are easier to define than workflow mutation
  contracts because rendering does not own source-of-truth facts.
- The extraction gives learners concrete practice with HTTP boundaries,
  timeouts, service configuration, local Compose complexity, and visible
  bounded failure.

## Arguments Against Extraction

- Current evidence does not show independent scaling or deployment pressure.
- Remote calls would add timeout, retry, versioning, and observability work.
- A new service would complicate local development and Phase 3 learning before
  learners have defended a concrete need.
- The existing worker-backed design already removes report generation from
  user-facing request paths.
- In a small production system, a pure in-process renderer would likely be
  cheaper to operate and easier to reason about.

## Alternatives Considered

- Keep rendering in-process only: cheaper for the current small production
  shape, but it would not teach network contracts, timeouts, partial failure,
  or mixed-version behavior.
- Extract a stateful reporting service: rejected because moving source data or
  report job ownership would create data consistency problems before the
  learner has evidence that the pure rendering boundary is insufficient.
- Extract more modules at the same time: rejected because it would obscure the
  cost of one boundary and turn the exercise into service sprawl.

## Consequences

The code keeps report rendering isolated enough to test directly and call
through either local function calls or a remote HTTP boundary. Callers depend on
the report contract, not on incidental query details.

Making `report-rendering.v1` explicit showed that most of the rendering
boundary can be modeled as pure computation over a caller-provided snapshot:
the database query path assembles counts and timestamps, then the renderer
returns a deterministic response for that typed request. This is useful
internal design even before service extraction because the worker no longer
depends on incidental report query details.

The extraction adds an extra Compose service, a runtime dependency from the
worker to HTTP rendering, timeout and error mapping behavior, and another health
surface to inspect. It intentionally does not add a service-owned database,
service mesh, gRPC, Kubernetes, notifications extraction, or job orchestration
extraction. Those would hide the lesson behind too many moving parts.

## Failure Modes

- Reporting service unavailable: worker calls fail and report job state records
  the failure instead of pretending the job succeeded.
- Reporting service slow: the worker timeout bounds the call and marks the job
  attempt failed.
- Invalid response: contract validation fails and preserves durable error
  evidence.
- Mixed versions: additive fields should be tolerated, but missing or
  incompatible required fields should fail visibly.
- Local development drift: tests may pass with the in-process renderer while
  Compose exposes remote-call behavior, so both paths need exercise coverage.

## Operational Cost

The split adds a second HTTP process, a health endpoint, config for
`OPLEDGER_REPORT_RENDERING_SERVICE_URL`, timeout tuning, local Compose startup
order, extra logs, and more debugging paths. On a tiny VPS, this cost may not
be justified outside the learning objective unless rendering develops real CPU,
memory, release, or ownership pressure.

## Rollback Or Reversal

Unset `OPLEDGER_REPORT_RENDERING_SERVICE_URL` to use the in-process renderer in
host development and tests. In a deployment that has adopted the service,
folding it back requires preserving the `report-rendering.v1` behavior in the
API codebase, updating worker config, and removing the extra process only after
report jobs have been checked for failures caused by the boundary.

## Interview Defense

The reporting service is defensible as a narrow learning extraction because it
is stateless pure computation over a supplied snapshot. It is not proof that
OpsLedger should become a microservice system. For a small production workload,
I would keep or remove the extraction based on measured rendering pressure,
team ownership needs, and whether the added timeout, deploy, and debugging cost
is paying for itself.
