# Phase 3 Service Boundary Review Checklist

Use this checklist when reviewing the extracted reporting service or any
proposal to add another service boundary. Keep feedback tied to evidence from
OpsLedger, not to generic microservice preference.

## Ownership

- The reporting service owns no source-of-truth facts.
- Postgres in the core API still owns customers, work requests, status events,
  report jobs, persisted report results, and notification attempts.
- The worker owns snapshot assembly, job orchestration, durable status, retry
  policy, and persistence.
- Review notes name what would become inconsistent if data ownership moved
  across the boundary.

## Contract Stability

- The boundary uses `report-rendering.v1` request and response schemas.
- Required fields, field types, status names, and literals remain stable.
- Additive fields are optional and safe for old callers or old providers to
  ignore.
- Invalid contract responses are rejected instead of being stored as partial
  report results.
- Compatibility tests are consumer-driven, not only provider happy-path tests.

## Timeout Behavior

- The worker uses `OPLEDGER_REPORT_RENDERING_SERVICE_TIMEOUT_SECONDS`.
- Slow reporting calls fail in bounded time and record durable job evidence.
- Timeout, non-2xx, malformed JSON, and invalid contract responses are
  distinguishable enough for debugging.
- User-facing behavior does not imply that `202 Accepted` means rendering
  completed.

## Retries

- There are no unbounded retries across the reporting boundary.
- Retry behavior is explained in terms of idempotency and durable attempt
  evidence.
- The review names which operations are safe to repeat and which side effects
  remain outside the renderer.
- Retry changes are not used to hide a contract or deployment failure.

## Deployment Cost

- Local Compose complexity is acknowledged as part of the extraction cost.
- The reporting service has its own health surface and runtime configuration.
- The review names what operators must inspect in addition to the API, worker,
  Redis, and Postgres.
- The learner explains why this cost is acceptable for Phase 3 learning and
  why it may be unjustified for a small production system.

## Debugging

- Scenario notes include job status, result endpoint behavior, worker logs, and
  reporting service logs.
- The evidence distinguishes a slow provider from a bad provider response.
- The review does not rely only on stack traces or local assumptions.
- Failure injection remains disabled by default and local/test only.

## Rollback

- A rollback plan names whether callers can return to the in-process renderer
  by removing `OPLEDGER_REPORT_RENDERING_SERVICE_URL`.
- Contract changes remain backward-compatible during mixed-version deploys.
- Breaking changes require a new version or a coordinated migration plan.
- The review states when folding the renderer back into the monolith would be
  cheaper than operating a separate service.

## Scope Control

- Do not add another extracted service.
- Do not add a database to the reporting service.
- Do not add k3s, service mesh, tracing, caching, or broad observability stack
  work in Phase 3.
- Treat service extraction as an expensive decision to defend, not a maturity
  badge.
