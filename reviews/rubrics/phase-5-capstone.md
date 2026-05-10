# Phase 5 Capstone Rubric

Score each category from 1 to 4. A passing capstone should have no category
below 3 unless the learner documents a real environment blocker and still
demonstrates the reasoning with sanitized evidence from tests, metrics,
scenario notes, or written review notes.

## Measurement Evidence

1. Baseline evidence is missing or only lists intended commands.
2. A run is recorded, but dataset, rate, status mix, or latency details are
   incomplete.
3. The learner records endpoint, command, dataset, status mix, latency shape,
   and relevant `/metrics` evidence.
4. The learner also explains uncertainty and names the next measurement that
   would improve confidence.

## Query And Index Reasoning

1. The learner says an index makes things faster without naming the query.
2. The learner names the query but gives weak reasoning about ordering or
   write-side costs.
3. The learner ties the index to status filtering, stable ordering, bounded
   pagination, and write/storage costs.
4. The learner also interprets why the planner may choose differently on small
   or skewed datasets.

## Read-Model Ownership

1. The learner treats the dashboard projection as authoritative.
2. Source tables and projection are named but ownership is blurry.
3. The learner clearly separates source-of-truth tables from rebuildable
   dashboard state.
4. The learner also demonstrates stale-before-rebuild behavior and explains
   user impact.

## Cache Behavior

1. Cache behavior is asserted without tests, metrics, or scenario evidence.
2. Hit or miss behavior is shown, but TTL, bypass, or key shape is missing.
3. Hit, miss, TTL, bypass, key shape, and invalidation behavior are explained
   with evidence.
4. The learner also identifies removal or rollback criteria if the cache is not
   earning its complexity.

## Staleness And Failure Modes

1. Staleness is ignored or treated as a bug to hide.
2. Staleness is mentioned but not tied to user impact or source endpoints.
3. Cache staleness, read-model staleness, and source-of-truth correctness are
   distinguished.
4. The learner also names concrete monitoring or review signals for stale data
   becoming harmful.

## Redis Outage Reasoning

1. Redis outage is not tested or discussed.
2. Redis outage is described generally without source-of-truth evidence.
3. The learner shows fallback to the read model and confirms source data is not
   corrupted.
4. The learner also distinguishes dashboard cache outage from Redis queue
   outage behavior elsewhere in OpsLedger.

## Review And Communication

1. The final writeup is a feature summary with broad performance claims.
2. The writeup includes evidence but weakly explains tradeoffs.
3. The writeup names measured behavior, chosen optimization, accepted failure
   mode, and verification.
4. The learner also uses checklist or LLM critique to remove unsupported claims
   and sharpen the decision memo.
