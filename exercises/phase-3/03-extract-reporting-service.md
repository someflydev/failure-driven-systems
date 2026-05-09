# Extract the Stateless Reporting Service

## Phase

Phase 3. This work belongs here because the learner has already seen async
jobs, durable state, and explicit module contracts before crossing a network
boundary.

## Concepts

- Service extraction versus module boundaries
- Stateless service design
- HTTP contract compatibility
- Timeouts and bounded failure
- Local Docker Compose complexity
- Source-of-truth ownership

## Prerequisites

- `docs/contracts/report-rendering-v1.md`
- `docs/adr/0001-report-rendering-boundary.md`
- `docs/TECH_STACK.md`
- `services/api/opledger_api/report_contracts.py`
- `services/api/opledger_api/report_jobs.py`
- `docker-compose.yml`
- Phase 2 report job lifecycle and retry exercises
- The repo-root `uv` Python 3.12 workflow

## Build/Change Task

Extract the work request summary renderer into `services/reporting/` as a small
FastAPI service. The service must accept the existing render request contract
and return the existing report response contract.

Wire the report worker so it can call the reporting service when a base URL is
configured. The worker must keep an explicit timeout, map remote failures to a
clear error, and avoid unbounded retries. If an in-process renderer remains for
local development, make that default explicit in configuration and docs.

Update Docker Compose so local development can run the API, Postgres, Redis,
worker, and reporting service together.

## Constraints

- Extract only report rendering.
- Do not extract notifications, customers, work requests, or job orchestration.
- Do not give the reporting service a database connection.
- Do not add Kubernetes, service mesh, gRPC, distributed tracing, or a new
  persistence store.
- Keep the core API/Postgres as the source of truth for report job state and
  source facts.

## Failure Modes

- The reporting service secretly reads from the core database.
- The worker waits forever on a slow or unavailable reporting service.
- Remote rendering failures are hidden behind vague job errors.
- Compose startup becomes order-dependent without useful health checks.
- Tests only cover happy-path JSON and miss contract validation.
- The learner argues extraction is automatically better because it is a
  service.

## Expected Reasoning

The learner should be able to explain why this extraction is educational: it
turns an already explicit pure boundary into a real network dependency with
configuration, timeout, deployment, and failure behavior.

The learner should also be able to explain why the same extraction may not be
worth it in a small production system: it adds another deployable unit, another
runtime failure mode, another health surface, and remote-call latency without
clear independent scaling or ownership pressure.

## Verification

- Run `./scripts/verify.sh`.
- Start the local stack with `./scripts/dev-up.sh` or `docker compose up
  --build`.
- Confirm `GET /health/live` works for both the API and reporting service.
- Enqueue a report job and confirm the worker stores a successful report result.
- Stop the reporting service and confirm the worker failure is visible,
  bounded by the configured timeout, and recorded in durable report job state.
- Confirm the reporting service has no database configuration or connection.

## Reflection Questions

- What facts does the reporting service own?
- What facts does the core API still own?
- What behavior changed when a function call became an HTTP call?
- Which failures are now easier to isolate?
- Which failures are now possible that did not exist before extraction?
- What production evidence would justify keeping this service extracted?
- What production evidence would argue for folding it back into the monolith?

## LLM Usage

Use an LLM as a reviewer after you have implemented the boundary. Ask it to
look for hidden database ownership, unbounded waits, vague error mapping, and
tests that do not prove the service contract. Do not ask it to defend the
extraction for you before you can explain the tradeoffs yourself.

## Path-Specific Extensions

Backend: add a compatibility test that proves an optional request field remains
ignored by the renderer.

Operations: write a short incident note describing what an operator sees when
the reporting service is down but Redis and Postgres are healthy.

Architecture: compare this extraction with extracting notifications and explain
which boundary has clearer ownership.

Interview: practice explaining why "stateless" does not mean "free to operate."

## Deployment/Debugging Actions If Relevant

Run the stack locally, inspect worker logs while the reporting service is
healthy, then stop only the reporting service and inspect the resulting durable
job failure. Record the configured timeout and the exact error class stored for
the failed job.
