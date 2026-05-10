# Phase 5 Performance Review Checklist

Use this checklist when reviewing Phase 5 work. Keep feedback tied to measured
OpsLedger behavior, not generic scaling advice.

## Baseline Evidence

- The reviewed work names the endpoint, command, dataset size, rate, duration,
  status mix, and latency shape.
- `/metrics` is checked before and after the run.
- The evidence separates observed results from hypotheses.
- The review does not claim production scalability from a small local dataset.

## Query And Pagination

- `GET /work-requests` uses bounded `limit` and `offset`.
- Recent-first ordering includes a stable tie breaker.
- Query-plan notes identify whether the index fits the access pattern.
- Index costs for writes, storage, and migrations are named.
- Extra indexes are not added without measured access patterns.

## Derived Read Model

- `customer_work_request_stats` is described as rebuildable derived state.
- Source-of-truth ownership remains with `customers`, `work_requests`, and
  `work_request_status_events`.
- The review includes stale-before-rebuild evidence.
- Source-of-truth endpoints remain correct during dashboard staleness.
- Rebuild behavior is explicit and repeatable.

## Redis Cache

- Exactly one endpoint is cached:
  `GET /dashboard/customer-work-request-stats`.
- Cache keys include endpoint version and pagination inputs.
- TTL is explicit and justified.
- `bypass_cache=true` behavior is tested and explained.
- Rebuild invalidation is best-effort and does not replace TTL.
- Hit, miss, bypass, and unavailable outcomes are visible in metrics or logs.

## Staleness

- The review distinguishes cache staleness from read-model staleness.
- User impact is named in product terms.
- The learner states which endpoint should be trusted for current workflow
  truth.
- Longer stale intervals require explicit evidence and acceptance.
- Cache is not used to hide incorrect source data.

## Redis Outage

- Redis outage behavior is tested or documented.
- The dashboard falls back to the Postgres-backed read model when possible.
- Source-of-truth data is not corrupted, repaired, or mutated by cache failure.
- Queue-related Redis behavior is not confused with dashboard cache behavior.
- Logs or metrics make cache unavailability visible.

## Scope Control

- No new datastore, cache cluster, service, or observability stack is added.
- Performance claims are limited to measured evidence.
- Docs and exercises teach tradeoffs instead of "cache makes it faster."
- LLM usage is review-oriented and does not invent benchmark or scenario
  results.
