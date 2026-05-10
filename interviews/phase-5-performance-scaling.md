# Phase 5 Performance And Scaling Mock Interview

Use these prompts after the learner has completed Phase 5 exercises and
captured their own measurements. The goal is to defend performance judgment
from OpsLedger evidence, not to recite generic scaling patterns.

## Measurement

### Walk me through your first performance baseline.

Strong-answer traits:

- Names the endpoint, command, dataset size, duration, rate, and status mix.
- Compares latency with `/metrics` instead of relying on one tool only.
- Separates observed results from hypotheses.
- Avoids production-scale claims from a tiny local run.

### When would you decide not to optimize?

Strong-answer traits:

- Says small datasets and low latency may not justify complexity.
- Names the next measurement that would reduce uncertainty.
- Explains the maintenance cost of speculative indexes or cache.
- Keeps the source-of-truth design simple until pressure is real.

## Query Shape And Indexes

### Why was the work request list index narrow?

Strong-answer traits:

- Connects it to `status`, `created_at`, `id`, bounded pagination, and stable
  ordering.
- Explains that it supports one measured access pattern.
- Names write-side insert, update, storage, and migration costs.
- Notes that planner behavior depends on dataset shape.

### How would you investigate pagination drift?

Strong-answer traits:

- Checks ordering fields and tie breakers.
- Uses deterministic pages with `limit` and `offset`.
- Looks at concurrent writes as a source of user-visible movement.
- Avoids solving the issue with cache before understanding the query.

## Read Models

### What does the customer dashboard read model own?

Strong-answer traits:

- Says it owns no authoritative facts.
- Names source tables for customer identity, work request state, and status
  event history.
- Describes the read model as rebuildable derived state.
- Explains why source endpoints remain trusted for workflow decisions.

### How do you explain read-model staleness to a product stakeholder?

Strong-answer traits:

- Uses product terms such as understated open work or outdated totals.
- Names which user could be misled.
- Separates dashboard summary from current work request state.
- Suggests a rebuild or freshness indicator only if evidence justifies it.

## Redis Cache

### Why cache only the dashboard endpoint?

Strong-answer traits:

- Points to measured or plausible hot dashboard reads after earlier Phase 5
  work.
- Explains that the endpoint is already derived and can tolerate short
  staleness.
- Rejects caching source-of-truth detail endpoints.
- Names the cache key and TTL.

### What happens when Redis is unavailable?

Strong-answer traits:

- Describes fallback to the Postgres-backed read model.
- Mentions cache-unavailable metrics/logs.
- Says source tables are not mutated or repaired by cache logic.
- Distinguishes dashboard degradation from queue behavior elsewhere in the
  system.

### What does `bypass_cache=true` prove?

Strong-answer traits:

- It proves the response from the derived table without using Redis.
- It does not prove source tables are current.
- It helps compare cache staleness with read-model staleness.
- It should not become a hidden correctness dependency.

## Tradeoffs

### A cache improved p95 latency. What question do you ask next?

Strong-answer traits:

- Asks whether stale data is acceptable for the user workflow.
- Checks hit rate, miss rate, Redis failures, and source load.
- Compares operational complexity with measured benefit.
- Names rollback or removal criteria.

### How would you defend this Phase 5 design in a system design interview?

Strong-answer traits:

- Starts with constraints and measured evidence.
- Keeps Postgres as source of truth.
- Adds indexes, read models, and cache in order of justified complexity.
- States new failure modes plainly instead of claiming free speed.

## LLM-Assisted Review

### What should an LLM challenge in your performance memo?

Strong-answer traits:

- Unsupported scale claims.
- Missing dataset and command details.
- Confusion between cache, read model, and source tables.
- Staleness or Redis outage risks not backed by evidence.
