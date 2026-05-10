# Phase 5 Lesson Path

Phase 5 teaches performance work as an evidence discipline. OpsLedger now has
enough source-of-truth tables, derived reports, async job state, metrics, and a
small VPS deployment target for performance questions to be real. The lesson is
not to add cache first; it is to measure, explain the bottleneck, and then
choose the smallest optimization that fits the evidence.

## Initial Path

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
6. Revisit the Phase 2 report exercises and Phase 4 metrics exercise to connect
   request latency, durable report job state, and derived report behavior.
7. Write a bottleneck hypothesis from measured data. The hypothesis may be that
   the current dataset does not justify optimization yet.

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

Future Phase 5 lessons may add caching and read models. They should cite
baseline evidence before changing system behavior and account for the new
failure modes they introduce.
