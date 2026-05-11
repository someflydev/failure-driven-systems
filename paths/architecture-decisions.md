# Architecture/Decision-Capable Engineer Path

## Target Outcome

Defend architecture decisions from built OpsLedger evidence: constraints,
source-of-truth ownership, failure modes, operational cost, rollback,
alternatives, and what evidence would change the decision.

## Recommended Phase Emphasis

- Phase 1: understand the single-service baseline and Postgres ownership.
- Phase 2: understand why async was added and what Redis does not own.
- Phase 3: strong emphasis on modular boundaries, contracts, and whether the
  reporting extraction should stay.
- Phase 4: strong emphasis on incidents as architecture feedback.
- Phase 5: strong emphasis on measured pressure before indexes, read models,
  or cache.
- Phase 6: strongest emphasis on ADRs, storage/runtime/platform comparisons,
  system-wide review, and mock panels.

## Required Exercises

- Implementation: `exercises/phase-3/02-contract-before-network.md`,
  `exercises/phase-3/03-extract-reporting-service.md`,
  `exercises/phase-5/03-derived-read-models.md`
- Debugging: `scenarios/phase-3/reporting-timeout.md`,
  `scenarios/phase-4/ambiguous-logs-before-correlation.md`,
  `scenarios/phase-5/stale-cache.md`
- Review: `reviews/checklists/architecture-review.md`,
  `reviews/checklists/system-wide-review.md`,
  `reviews/checklists/phase-3-service-boundary-review.md`
- Explanation: `exercises/phase-6/01-decision-memo-defense.md`,
  `exercises/phase-6/02-datastore-tradeoff-defense.md`,
  `exercises/phase-6/03-runtime-selection-defense.md`,
  `exercises/phase-6/04-dokku-vs-k3s-defense.md`

## Optional Extensions

- `docs/adr/TEMPLATE.md` for a new decision memo that rejects an attractive but
  unjustified change.
- `extensions/polyglot-report-renderer/README.md` as a bounded polyglot
  experiment, not a main-path rewrite.
- `deploy/k3s/checklist.md` for orchestration tradeoff practice after the
  Dokku baseline is clear.

## Review/Interview Checkpoints

- After Phase 3, defend the reporting-service extraction using
  `reviews/checklists/phase-3-service-boundary-review.md`.
- After Phase 5, explain how measurement changed or constrained architecture.
- During Phase 6, use `reviews/checklists/architecture-review.md`,
  `reviews/checklists/system-wide-review.md`, and
  `interviews/mock-panels/architecture-staff-engineer-panel.md`.
- Before the final portfolio defense, use
  `interviews/role-tracks/architecture-decisions.md`.

## Portfolio Artifacts To Produce

- Current architecture narrative grounded in
  `docs/architecture/current-system.md`.
- One ADR or decision memo with rejected alternatives and rollback.
- Boundary defense for API, worker, reporting service, Postgres, and Redis.
- Revision note naming evidence that would change the decision.

## What Not To Overfocus On

- Do not make the path purely theoretical.
- Do not produce architecture diagrams without implementation or incident
  evidence.
- Do not imply more services, datastores, or platforms are automatically
  better.
- Do not ignore team size, VPS constraints, deploy cost, or rollback.
