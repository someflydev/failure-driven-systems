# Phase 5 Lesson Path

Phase 5 teaches performance work as an evidence discipline. OpsLedger now has
enough source-of-truth tables, derived reports, async job state, metrics, and a
small VPS deployment target for performance questions to be real. The lesson is
not to add cache first; it is to measure, explain the bottleneck, and then
choose the smallest optimization that fits the evidence.

## Lesson Path

1. Re-read `curriculum/PHASE_PLAN.md` for the Phase 5 boundaries: measurement
   first, cache only after need, and derived state only with a rebuild story.
2. Read `docs/performance/baselines.md` to understand the safe baseline runner,
   local defaults, VPS limits, and result-recording format.
3. Review `docs/observability/metrics.md` so latency and status results can be
   compared with the API's existing HTTP metrics.
4. Complete `exercises/phase-5/01-measure-before-optimizing.md` by collecting
   baseline latency and error evidence before changing code.
5. Read `docs/performance/query-inspection.md`, then complete
   `exercises/phase-5/02-pagination-and-indexes.md` to connect safe
   pagination, query plans, and narrowly justified indexes.
6. Read `docs/performance/read-models.md`, then complete
   `exercises/phase-5/03-derived-read-models.md` to study explicit rebuilds,
   visible dashboard staleness, and source-of-truth ownership before cache.
7. Read `docs/performance/caching.md`, then complete
   `exercises/phase-5/04-caching-and-staleness.md` to study the one Redis
   cached endpoint, stable keys, TTL, bypass, stale-cache risk, and Redis
   outage fallback.
8. Run `scenarios/phase-5/stale-cache.md` and
   `scenarios/phase-5/redis-cache-unavailable.md` to prove cache behavior under
   failure instead of assuming it is only a speed feature.
9. Read `reviews/README.md`, `quizzes/README.md`, and
   `interviews/README.md` before assessment, then complete
   `quizzes/phase-5.md`, practice with
   `interviews/phase-5-performance-scaling.md`, and review your work with
   `reviews/checklists/phase-5-performance-review.md`.
10. Finish `exercises/phase-5/05-phase-5-capstone.md` and self-score with
    `reviews/rubrics/phase-5-capstone.md`.

## Performance Focus

Learners should be able to explain:

- Why a baseline must name the endpoint, dataset size, status mix, and latency
  shape.
- Why a tiny VPS needs bounded read-only load tests by default.
- Why write-oriented tests require explicit opt-in and disposable data.
- Why cache is not a fix for an unknown bottleneck.
- Why Postgres remains the source of truth even when a later cache or read model
  is introduced.
- What evidence would justify an index, pagination change, cache key, or
  denormalized read model.
- What new failure mode each optimization accepts.
- Why a read model can be rebuilt from authoritative tables and still be stale
  between rebuilds.
- Why the dashboard cache can be stale separately from the dashboard read
  model.
- Why Redis cache outage should not corrupt source-of-truth data.
- How to defend keeping or removing a cache based on before/after evidence and
  user impact.
