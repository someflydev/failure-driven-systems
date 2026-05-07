# Synchronous Report Pain

## Phase

Phase 2: Async After Synchronous Pain. This exercise belongs here because the
learner first needs to observe how report generation affects a user-facing HTTP
request before moving the work out of that path.

## Concepts

- Derived reports over source-of-truth tables.
- Request latency and user-visible waiting.
- Local-only failure simulation with configuration.
- Evidence-based reasoning before introducing new infrastructure.

## Prerequisites

- Phase 1 CRUD and status history exercises.
- `curriculum/PHASE_PLAN.md`
- `docs/DOCTRINE.md`
- `docs/data-models/phase-1.md`
- `services/api/opledger_api/routes.py`
- `services/api/opledger_api/reports.py`
- `services/api/opledger_api/config.py`
- `services/api/tests/test_crud_api.py`
- Local API and Postgres workflow from Phase 1.

## Build/Change Task

Use `POST /reports/work-requests/summary` to generate a synchronous summary of
current work requests and status history. Seed several work requests, move at
least one through a status transition, and confirm that the summary includes
the total request count, counts by status, and the status event count.

Then enable the local report delay configuration and call the same endpoint
with a delay request. Measure how long the HTTP request takes and note what the
caller can and cannot do while waiting for the response.

## Constraints

- Do not add Redis.
- Do not add a worker.
- Do not add background jobs.
- Do not add caching.
- Do not fake asynchronous behavior with fire-and-forget work inside the web
  process.
- Keep Postgres as the source of truth for customers, work requests, and status
  events.
- Treat the report response as derived data. It can be regenerated from source
  tables.

## Failure Modes

- Treating a derived report as the source of truth.
- Hiding the latency problem by testing only empty databases.
- Enabling artificial delay outside local learning or test environments.
- Claiming the system is asynchronous before any work has actually moved out of
  the request path.
- Measuring only server logs without recording what the caller experienced.

## Expected Reasoning

After completing the exercise, explain why the report is derived data, which
tables contain the durable facts, and why a slow report blocks the HTTP caller.
Be precise about what improved behavior you expect later before changing the
architecture.

## Verification

- Run `./scripts/verify.sh`.
- Create at least two customers and work requests through the API.
- Update at least one work request status so a status event exists.
- Call `POST /reports/work-requests/summary` without delay and record the
  response body.
- Enable `OPLEDGER_REPORT_DELAY_ENABLED=true` locally.
- Call `POST /reports/work-requests/summary?delay_seconds=3` and record the
  observed latency.
- Before implementing any later asynchronous design, write down what you expect
  to happen to request latency and user feedback.

## Reflection Questions

- Which fields in the report are derived from `work_requests`?
- Which fields in the report are derived from `work_request_status_events`?
- What does the caller experience during the artificial delay?
- Why is adding a delay through configuration safer than making every report
  slow by default?
- What evidence would convince you that report work should leave the request
  path?
- What new failure modes might appear when report work is moved elsewhere?

## LLM Usage

Use an LLM as a reviewer after you have measurements. Ask it to challenge your
latency evidence, your source-of-truth explanation, and your assumptions about
what should improve later. Do not ask it to invent measurements you did not
capture.

## Path-Specific Extensions

Backend: add more seeded status histories and compare the report output against
manual database queries.

Operations: capture API logs and terminal timing evidence from a delayed
request, then write a short operator note describing the user impact.

Architecture: sketch the current synchronous request path and mark exactly
where the caller waits.

Interview: practice explaining why the first Phase 2 step intentionally avoids
new infrastructure.

## Deployment/Debugging Actions If Relevant

Run this locally first. Do not enable artificial delay in production-like
deployments unless the lesson explicitly asks for a controlled drill and a
rollback plan.
