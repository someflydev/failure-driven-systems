# Practical Distributed Systems Engineer Path

## Target Outcome

Explain and debug partial failure in a modest real system: async jobs, Redis
coordination, durable status, service contracts, timeouts, retries,
correlation IDs, incidents, and rollback tradeoffs.

## Recommended Phase Emphasis

- Phase 1: enough single-service grounding to explain the baseline before
  distributed failure is introduced.
- Phase 2: strongest emphasis on async work, retries, idempotency, duplicate
  execution, worker outages, Redis outages, and user-visible consistency.
- Phase 3: strongest emphasis on service-boundary costs, report-rendering
  contracts, timeouts, bad responses, and mixed-version behavior.
- Phase 4: strong emphasis on incident timelines, correlation IDs, logs,
  metrics, runbooks, status updates, and postmortems.
- Phase 5: moderate emphasis on cache outage and staleness failure modes.
- Phase 6: defend why the system stays small and which boundary costs are
  accepted.

## Required Exercises

- Implementation: `exercises/phase-2/02-background-report-worker.md`,
  `exercises/phase-2/04-retries-before-idempotency.md`,
  `exercises/phase-3/03-extract-reporting-service.md`
- Debugging: `scenarios/phase-2/worker-unavailable.md`,
  `scenarios/phase-2/report-retry-failure.md`,
  `scenarios/phase-2/redis-unavailable.md`,
  `scenarios/phase-3/reporting-timeout.md`,
  `scenarios/phase-3/reporting-bad-response.md`,
  `scenarios/phase-4/worker-stalled-incident.md`
- Review: `reviews/checklists/phase-2-async-review.md`,
  `reviews/checklists/phase-3-service-boundary-review.md`,
  `reviews/checklists/incident-review.md`
- Explanation: `interviews/phase-2-backend-distributed.md`,
  `interviews/phase-3-distributed-boundaries.md`,
  `interviews/phase-4-operational-debugging.md`

## Optional Extensions

- `scenarios/phase-3/mixed-version-contract.md`
- `scenarios/phase-5/redis-cache-unavailable.md`
- `deploy/k3s/README.md`, only after defending why orchestration is a later
  learning path rather than the starting point.

## Review/Interview Checkpoints

- After Phase 2, explain accepted-but-incomplete work using durable report job
  state.
- After Phase 3, run
  `reviews/checklists/phase-3-service-boundary-review.md`.
- After Phase 4, run `interviews/mock-panels/distributed-systems-debugging-panel.md`.
- Before the final portfolio defense, use
  `interviews/role-tracks/distributed-systems.md`.

## Portfolio Artifacts To Produce

- Failure matrix separating API, Postgres, Redis, worker, reporting service,
  and cache symptoms.
- Incident timeline with correlation IDs, durable status, logs, and metrics.
- Contract failure explanation for timeout, malformed response, and
  mixed-version behavior.
- Decision note on why Redis is coordination, not truth.

## What Not To Overfocus On

- Do not invent large-scale requirements.
- Do not replace evidence with diagrams.
- Do not call every async workflow event-driven architecture.
- Do not skip the monolith baseline that makes later boundaries intelligible.
