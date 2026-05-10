# Phase 5 Quiz

Answer in short paragraphs or bullets. A strong answer should connect the
concept to OpsLedger behavior and name the evidence you would inspect.

## Measurement

1. Why does Phase 5 start with a baseline before indexes, read models, or cache?
2. What dataset details make a latency result interpretable?
3. Why are bounded local defaults important on a small VPS?
4. What should you record from `/metrics` before and after a performance run?
5. When is "no optimization yet" the right conclusion?

## Pagination And Indexes

1. Why does `GET /work-requests` require a stable order for pagination?
2. What query shape does `ix_work_requests_status_created_at_id` support?
3. What write-side costs does an index add?
4. Why might Postgres still choose a sequential scan on a tiny table?
5. What evidence would make you remove or change an index?

## Derived Read Models

1. Which tables own the authoritative customer and work request facts?
2. What does `customer_work_request_stats` derive?
3. Why can the dashboard be stale before a rebuild?
4. What user could be misled by stale dashboard totals?
5. Why is a read model different from a cache?

## Redis Cache

1. Why is `GET /dashboard/customer-work-request-stats` the only cached endpoint?
2. What inputs belong in the cache key?
3. What does the cache TTL control?
4. What does `bypass_cache=true` prove, and what does it not prove?
5. Why must Redis never be treated as authoritative?

## Staleness And Failure

1. How can Redis cache be stale even after the read model is correct?
2. How can the read model be stale even when Redis is bypassed?
3. What should happen when Redis is unavailable?
4. Which endpoint should a dispatcher trust for current workflow state?
5. What metrics or logs would reveal cache hit, miss, or outage behavior?

## Review Judgment

1. What claim would be unsafe after only a small local benchmark?
2. How do you explain a performance improvement and its new failure mode
   together?
3. What evidence would justify a longer dashboard cache TTL?
4. What evidence would make the cache worth removing?
5. How can an LLM help review performance work without inventing results?
