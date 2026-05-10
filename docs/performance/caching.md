# Redis Caching

Phase 5 adds one deliberate Redis cache after baselines, pagination/index work,
and the derived read-model lesson. Redis already exists for report queues, but
queue transport does not automatically justify cache usage. A cache is accepted
only when the read path, stale-data risk, key shape, TTL, and fallback behavior
are explicit.

## Cached Endpoint

The only cached endpoint is:

```http
GET /dashboard/customer-work-request-stats
```

This endpoint is a good first cache candidate because it already serves a
dashboard projection from `customer_work_request_stats`. The endpoint is
read-heavy in the lesson path, the response is bounded by `limit` and `offset`,
and short staleness is acceptable for a summary dashboard. It is not used to
drive a workflow decision that requires current source-of-truth state.

Do not copy this cache pattern to source-of-truth endpoints such as:

```http
GET /work-requests/{work_request_id}
GET /work-requests/{work_request_id}/status-events
```

Those endpoints should continue to read authoritative tables when correctness
matters more than dashboard latency.

## Key And TTL

Cache keys include a version, endpoint name, and pagination inputs:

```text
opledger:v1:dashboard:customer-work-request-stats:limit=50:offset=0
```

The default TTL is `30` seconds and can be changed with:

```text
OPLEDGER_DASHBOARD_CUSTOMER_WORK_REQUEST_STATS_CACHE_TTL_SECONDS
```

The TTL is intentionally short. It lets learners observe a stale cache without
turning Redis into an unofficial database. Raising the TTL requires evidence
that the dashboard can safely tolerate a longer stale interval.

## Bypass And Invalidation

The endpoint accepts:

```http
GET /dashboard/customer-work-request-stats?bypass_cache=true
```

Bypass reads the derived table directly and does not refresh Redis. It is a
debugging and comparison tool, not a user-facing correctness guarantee. If the
derived table itself is stale, bypassing cache will still return stale
projection data.

Running the read-model rebuild attempts best-effort invalidation for keys with
the dashboard cache prefix. If Redis is unavailable, invalidation failure is
logged and source-of-truth data remains unchanged. The next cache miss or TTL
expiration can repopulate Redis from the read model.

## What Can Go Stale

There are two separate stale intervals:

- The read model can lag source tables until `scripts/rebuild-read-models.sh`
  runs.
- Redis can keep an older dashboard response until TTL expiration or rebuild
  invalidation.

That means a new work request can be visible in `GET /work-requests` while the
dashboard still shows an older total. A dispatcher should trust the work
request detail and list endpoints for current workflow decisions. The dashboard
is useful for operational shape, not authoritative current state.

## Redis Is Not Authoritative

Redis stores a serialized response for one dashboard endpoint. It does not own
customer identity, work request state, status event history, or the derived
projection. Postgres remains authoritative:

- `customers` owns customer identity.
- `work_requests` owns current work request state.
- `work_request_status_events` owns transition history.
- `customer_work_request_stats` is rebuildable derived state.
- Redis owns only a disposable response copy.

If Redis is down, the endpoint falls back to the derived table, records/logs the
cache-unavailable outcome, and still returns data if Postgres is available.
Redis outage must not mutate source tables, hide failed writes, or change the
meaning of source-of-truth endpoints.

## Metrics And Logs

The cache records:

```text
opledger_cache_access_total{endpoint="dashboard_customer_work_request_stats",outcome="hit"}
opledger_cache_access_total{endpoint="dashboard_customer_work_request_stats",outcome="miss"}
opledger_cache_access_total{endpoint="dashboard_customer_work_request_stats",outcome="bypass"}
opledger_cache_access_total{endpoint="dashboard_customer_work_request_stats",outcome="unavailable"}
opledger_cache_access_total{endpoint="dashboard_customer_work_request_stats",outcome="write_failed"}
```

The endpoint label is bounded and contains no customer data. Logs include cache
events for unavailable Redis, failed writes, and failed invalidation with the
exception class only.

## Evidence To Capture

Before claiming the cache helped, record:

- Baseline command and dataset size.
- Before/after latency for the dashboard endpoint.
- Cache hit and miss counts from `/metrics`.
- A stale-cache example and the source-of-truth endpoint that proves current
  state.
- Redis outage behavior showing no source-of-truth corruption.

If there is no measured pressure on the dashboard endpoint, the correct
production decision may be to remove the cache and keep the read model only.
