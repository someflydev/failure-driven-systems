# Data/Backend Engineer Path

## Target Outcome

Defend source-of-truth ownership, query shape, derived state, cache staleness,
and datastore choices while still proving backend implementation competence in
the same OpsLedger system.

## Recommended Phase Emphasis

- Phase 1: strong emphasis on relational modeling, migrations, transactions,
  constraints, and status history.
- Phase 2: moderate emphasis on durable async status and idempotency.
- Phase 3: moderate emphasis on contract payload ownership and why the
  reporting service does not own facts.
- Phase 4: enough operational work to prove data symptoms from logs, metrics,
  and database observations.
- Phase 5: strongest emphasis on baselines, query inspection, indexes, read
  models, Redis cache, staleness, and fallback.
- Phase 6: strongest emphasis on datastore tradeoff defense and refusing
  unjustified storage systems.

## Required Exercises

- Implementation: `exercises/phase-1/02-transactions-and-history.md`,
  `exercises/phase-5/02-pagination-and-indexes.md`,
  `exercises/phase-5/03-derived-read-models.md`,
  `exercises/phase-5/04-caching-and-staleness.md`
- Debugging: `scenarios/phase-1/db-unavailable.md`,
  `scenarios/phase-5/stale-cache.md`,
  `scenarios/phase-5/redis-cache-unavailable.md`
- Review: `reviews/checklists/phase-5-performance-review.md`,
  `reviews/checklists/system-wide-review.md`
- Explanation: `interviews/phase-5-performance-scaling.md`,
  `interviews/phase-6-storage-systems.md`,
  `exercises/phase-6/02-datastore-tradeoff-defense.md`

## Optional Extensions

- `docs/storage/search-indexes.md` comparison memo for whether OpsLedger needs
  search.
- `docs/storage/analytical-stores.md` comparison memo for when dashboard needs
  would exceed the current read model.
- `exercises/phase-2/05-idempotent-report-jobs.md` for database-backed
  duplicate prevention.

## Review/Interview Checkpoints

- After Phase 1, explain `docs/data-models/phase-1.md` against the implemented
  migrations.
- After Phase 5, run `reviews/checklists/phase-5-performance-review.md`.
- During Phase 6, use `interviews/phase-6-storage-systems.md` and
  `interviews/role-tracks/data-backend.md`.

## Portfolio Artifacts To Produce

- Source-of-truth map for customers, work requests, status events, report jobs,
  notification attempts, read models, and cache.
- Before/after query-plan notes from `docs/performance/query-inspection.md`.
- Staleness demonstration showing source-of-truth endpoints remain correct.
- Datastore decision memo explaining why Postgres plus Redis is enough today.

## What Not To Overfocus On

- Do not add a new datastore without evidence.
- Do not treat cache or read models as authoritative.
- Do not optimize before recording a baseline.
- Do not make the path only SQL; backend API behavior still matters.
