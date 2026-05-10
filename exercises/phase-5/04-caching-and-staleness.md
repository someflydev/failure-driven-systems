# Caching And Staleness

## Phase

Phase 5: Performance, Caching, And Read Models. This work belongs here because
learners have measured read behavior, inspected indexes, and studied a derived
read model before adding Redis cache to one bounded endpoint.

## Concepts

- Redis response caching
- Stable cache keys
- TTL selection
- Cache hit and miss metrics
- Bypass and invalidation behavior
- Stale reads and source-of-truth ownership
- Graceful cache outage fallback

## Prerequisites

Read these first:

- `docs/performance/baselines.md`
- `docs/performance/query-inspection.md`
- `docs/performance/read-models.md`
- `docs/performance/caching.md`
- `docs/observability/metrics.md`
- `exercises/phase-5/01-measure-before-optimizing.md`
- `exercises/phase-5/02-pagination-and-indexes.md`
- `exercises/phase-5/03-derived-read-models.md`
- `exercises/TEMPLATE.md`

You should be able to run the local stack, rebuild read models, query
`/metrics`, and compare dashboard output with source-of-truth work request
output.

## Build/Change Task

Use the cached dashboard endpoint:

```http
GET /dashboard/customer-work-request-stats
```

Complete the exercise by collecting evidence, not by adding another cache:

1. Create or reuse a local dataset with at least two customers and several work
   requests.
2. Rebuild `customer_work_request_stats`.
3. Capture a baseline dashboard response and `/metrics`.
4. Read the dashboard endpoint twice and identify one miss and one hit in
   `opledger_cache_access_total`.
5. Read the dashboard with `bypass_cache=true` and explain what it bypasses.
6. Change source data without rebuilding, then prove the dashboard can be
   stale while `GET /work-requests` is current.
7. Rebuild the read model and confirm the dashboard catches up.
8. Stop Redis and confirm the endpoint falls back to the read model without
   corrupting source tables.

Write a short note explaining why this endpoint was cached and why no
source-of-truth endpoint was cached.

## Constraints

- Cache exactly one endpoint.
- Do not cache work request detail or status-event endpoints.
- Do not increase TTL without naming user impact.
- Do not treat Redis as authoritative.
- Do not use cache to hide a slow or incorrect source query.
- Do not add a new datastore, cache cluster, or observability stack.
- Keep metrics labels bounded and free of customer data.

## Failure Modes

- A cached dashboard response outlives a source-table change.
- A read-model rebuild fails to invalidate cache.
- A learner mistakes `bypass_cache=true` for source-of-truth freshness.
- Redis is down and cache reads or writes fail.
- Cache keys omit pagination inputs and return the wrong page.
- A long TTL makes stale dashboard data operationally misleading.
- Hit-rate metrics look good while users need current workflow state.

## Expected Reasoning

After completing the work, explain:

- Why the dashboard endpoint is a better cache candidate than work request
  detail.
- What the cache key includes and why.
- What the TTL allows and risks.
- Which stale interval comes from Redis and which comes from the read model.
- Why Postgres remains authoritative.
- What Redis outage changes for users and operators.
- Which before/after evidence would be needed before claiming a performance
  improvement.

## Verification

Run:

```sh
./scripts/verify.sh
```

Manual checks:

```sh
curl -s "http://127.0.0.1:18080/dashboard/customer-work-request-stats?limit=50&offset=0"
curl -s "http://127.0.0.1:18080/dashboard/customer-work-request-stats?limit=50&offset=0"
curl -s "http://127.0.0.1:18080/dashboard/customer-work-request-stats?bypass_cache=true"
curl -s http://127.0.0.1:18080/metrics
```

Scenario checks:

```sh
scenarios/phase-5/stale-cache.md
scenarios/phase-5/redis-cache-unavailable.md
```

Your submitted evidence should include:

- Cache miss and hit metrics.
- One stale dashboard example.
- One source-of-truth response proving current state.
- Redis outage behavior.
- A short note on whether the measured improvement justifies the cache.

## Reflection Questions

- What would make this cache harmful even if it improves latency?
- What does `bypass_cache=true` prove, and what does it not prove?
- Why is Redis allowed to lose this data?
- How would you detect a cache that is always missing?
- How would you detect a cache that is serving stale data for too long?
- When would removing the cache be the right decision?

## LLM Usage

Use an LLM after you have gathered evidence. Ask it to critique whether your
cache choice, TTL, stale-data explanation, and Redis outage conclusion are
supported by the facts. Do not ask it to invent benchmark results or stale
cache output.

## Path-Specific Extensions

Backend: review or add tests for hit, miss, TTL, bypass, invalidation, stale
read risk, and Redis outage fallback.

Operations: write an alert note for a sudden rise in
`opledger_cache_access_total{outcome="unavailable"}`.

Architecture: compare this cache with the read model and explain why both are
derived state but have different failure modes.

Interview: practice defending a short TTL and explaining when not to cache.

## Deployment/Debugging Actions If Relevant

On a deployed environment, verify Redis URL configuration, keep `/metrics`
internal, run a bounded baseline before and after cache warmup, and document
whether Redis outage returns dashboard data from Postgres or a service error.
