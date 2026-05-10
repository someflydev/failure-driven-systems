# Phase 5 Capstone

## Phase

Phase 5: Performance, Caching, And Read Models. This capstone asks learners to
defend one measured performance improvement and its new failure mode across
measurement, query shape, derived state, cache behavior, and review.

## Concepts

- Evidence-first performance work
- Bounded load testing
- Pagination and query-plan reasoning
- Index tradeoffs
- Derived read models
- Redis cache keys, TTL, bypass, and invalidation
- Staleness and source-of-truth ownership
- Performance review communication

## Prerequisites

Complete:

- `exercises/phase-5/01-measure-before-optimizing.md`
- `exercises/phase-5/02-pagination-and-indexes.md`
- `exercises/phase-5/03-derived-read-models.md`
- `exercises/phase-5/04-caching-and-staleness.md`

Read:

- `docs/performance/baselines.md`
- `docs/performance/query-inspection.md`
- `docs/performance/read-models.md`
- `docs/performance/caching.md`
- `reviews/checklists/phase-5-performance-review.md`
- `reviews/rubrics/phase-5-capstone.md`
- `exercises/TEMPLATE.md`

## Build/Change Task

Prepare a short Phase 5 performance review packet:

1. Record a baseline for one read path.
2. Inspect or explain the query shape for the measured path.
3. Explain the Phase 5 index and its write-side cost.
4. Rebuild and inspect the customer dashboard read model.
5. Demonstrate read-model staleness.
6. Demonstrate dashboard cache hit, miss, bypass, TTL, and stale-read risk.
7. Demonstrate Redis cache outage fallback.
8. Write a decision memo defending whether the cache should remain.
9. Complete the Phase 5 quiz and one mock interview pass.
10. Review your packet against the Phase 5 checklist and rubric.

The memo should be specific: name endpoints, commands, dataset size, metric
snippets, stale-data examples, and the accepted tradeoff.

## Constraints

- Do not add another cache or read model.
- Do not claim scalability from local-only evidence.
- Do not run unbounded load tests against a small VPS.
- Do not treat Redis or `customer_work_request_stats` as authoritative.
- Do not hide stale data in the write path or source-of-truth endpoints.
- Do not ask an LLM to write the final packet before you have evidence.

## Failure Modes

- Baseline evidence is missing or not reproducible.
- The optimization is described generically instead of tied to an endpoint.
- The learner ignores write-side index cost.
- Dashboard speed is confused with workflow correctness.
- Redis outage behavior is not tested.
- Stale cache and stale read-model intervals are blurred together.
- The review claims production scale without measured before/after evidence.

## Expected Reasoning

After completing the capstone, explain:

- What was slow or worth inspecting and how you measured it.
- Why each optimization was introduced in this order.
- What new cost or failure mode each optimization adds.
- Which data remains authoritative.
- What stale data can mislead a user or operator.
- What evidence would make you remove, keep, or change the cache.
- How you would present this tradeoff in an interview.

## Verification

Run:

```sh
./scripts/verify.sh
```

If practical, run a bounded local performance smoke before and after cache
warmup and record the results using the format in
`docs/performance/baselines.md`.

Manual evidence should include:

- Baseline command and result.
- Query-plan or index reasoning note.
- Read-model rebuild output.
- Stale read-model example.
- Cache hit/miss/bypass metrics.
- Redis outage fallback result.
- Completed checklist and rubric self-score.

## Reflection Questions

- Which performance change was most justified by evidence?
- Which change added the most operational risk?
- What would you monitor after deploying the cache?
- What user workflow must never depend on stale dashboard data?
- What evidence would justify a longer TTL?
- What evidence would make the cache unnecessary?

## LLM Usage

Use an LLM as a senior reviewer or interviewer after your memo is drafted. Ask
it to find unsupported claims, missing evidence, hidden correctness risks, and
weak tradeoff explanations. Do not ask it to invent measurements or write the
memo from scratch.

## Path-Specific Extensions

Backend: tighten one test that proves cache or read-model behavior under a
failure mode.

Operations: write a one-page deploy and rollback note for the cache setting.

Architecture: compare cache, read model, and source table responsibilities in
a diagram or table.

Interview: answer the Phase 5 mock interview prompts without notes, then revise
based on gaps.

## Deployment/Debugging Actions If Relevant

For a real deployment, keep load tests bounded, keep `/metrics` internal,
confirm Redis and Postgres health separately, and document rollback by disabling
or ignoring cache while continuing to serve the read model from Postgres.
