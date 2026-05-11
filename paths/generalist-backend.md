# High-Leverage Generalist Backend Engineer Path

## Target Outcome

Become credible across the full backend loop: implement a feature, test it,
deploy or simulate deployment, debug runtime failures, measure performance,
review the work, and explain tradeoffs without overbuilding.

## Recommended Phase Emphasis

- Phase 1: strong enough to own the basic API, database, tests, containers, and
  first deployment path.
- Phase 2: strong enough to reason about worker-backed async behavior and safe
  side effects.
- Phase 3: moderate boundary and contract practice.
- Phase 4: strong operational debugging and incident response practice.
- Phase 5: moderate performance, indexing, read-model, and cache practice.
- Phase 6: strong concise explanation and interview readiness.

## Required Exercises

- Implementation: `exercises/phase-1/01-basic-crud.md`,
  `exercises/phase-1/05-local-container-workflow.md`,
  `exercises/phase-2/06-safe-side-effects.md`,
  `exercises/phase-5/02-pagination-and-indexes.md`
- Debugging: `exercises/phase-1/04-db-down-debugging.md`,
  `scenarios/phase-4/reporting-service-latency-incident.md`,
  `scenarios/phase-4/noisy-nonfatal-errors.md`,
  `scenarios/phase-5/redis-cache-unavailable.md`
- Review: `reviews/checklists/phase-1-api-review.md`,
  `reviews/checklists/incident-review.md`,
  `reviews/checklists/system-wide-review.md`
- Explanation: `interviews/mock-panels/backend-implementation-panel.md`,
  `interviews/mock-panels/distributed-systems-debugging-panel.md`,
  `exercises/phase-6/05-mock-interview-panel.md`

## Optional Extensions

- `exercises/phase-1/06-dokku-first-deploy.md`
- `exercises/phase-3/04-timeouts-and-contracts.md`
- `exercises/phase-5/04-caching-and-staleness.md`
- `exercises/phase-6/04-dokku-vs-k3s-defense.md`

## Review/Interview Checkpoints

- After Phase 1, prove the system runs locally and explain one deploy blocker
  or successful deploy.
- After Phase 4, run an incident review with
  `reviews/checklists/incident-review.md`.
- Before the final portfolio defense, use
  `reviews/checklists/system-wide-review.md` and
  `interviews/role-tracks/generalist-backend.md`.

## Portfolio Artifacts To Produce

- One feature walkthrough from request to database to tests.
- One operational debugging note with evidence and a discarded hypothesis.
- One performance note with measurement before change.
- One two-minute system explanation covering API, Postgres, Redis, worker, and
  reporting service.

## What Not To Overfocus On

- Do not chase every optional extension.
- Do not specialize so narrowly that deployment, operations, or explanation are
  neglected.
- Do not add platform complexity before the constrained system needs it.
- Do not use LLM critique before making a serious attempt.
