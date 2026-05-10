# Phase 6 Storage Systems Mock Interview

Use these prompts after the learner has read `docs/storage/` and completed the
Phase 6 datastore tradeoff exercise. The goal is to compare storage paradigms
from OpsLedger evidence, not to recite generic database categories.

## Source Of Truth

### Why is Postgres still the OpsLedger source of truth?

Strong-answer traits:

- Names customers, work requests, status events, report jobs, notification
  attempts, and the dashboard read model.
- Explains transactions, constraints, migrations, inspection, and repair.
- Distinguishes authoritative facts from Redis queue/cache state.
- Names the cost: migrations, readiness, query discipline, and backups.

### What would make you move a fact out of Postgres?

Strong-answer traits:

- Starts with a specific workload Postgres cannot satisfy cleanly.
- Defines the new owner and migration or dual-read period.
- Names consistency, rollback, and repair procedures.
- Rejects moving facts for fashion or vague scale.

## Redis And Key-Value Storage

### Why is Redis acceptable in OpsLedger?

Strong-answer traits:

- Limits Redis to queue coordination and one dashboard cache.
- Says Redis can lose data without becoming the source of truth.
- Points to durable report job state and Postgres-backed read model fallback.
- Names Redis outage and stale-cache behavior.

### When would you remove Redis?

Strong-answer traits:

- Separates queue value from cache value.
- Mentions low report volume, no dashboard pressure, or operational burden.
- Explains the fallback or replacement path.
- Keeps durable records in Postgres.

## Document Stores

### Would you add MongoDB for work requests?

Strong-answer traits:

- Says current work requests are relational and constraint-heavy.
- Mentions customer foreign keys, status checks, status history, and
  transactions.
- Allows a narrow document-shaped use case such as variable intake metadata.
- Considers Postgres JSONB before a new datastore.

## Queues And Streams

### Why not start with Kafka for report generation?

Strong-answer traits:

- Says OpsLedger needs one background worker path, not a replayable event
  platform.
- Names Redis/RQ plus durable Postgres job state as sufficient today.
- Explains Kafka operational costs: brokers, partitions, offsets, retention,
  schemas, lag, and replay safety.
- Names evidence that could justify a stream later.

### What problem would an outbox solve?

Strong-answer traits:

- Describes the publish-after-commit gap.
- Keeps the authoritative event or work item in Postgres.
- Explains idempotent consumers and duplicate delivery.
- Avoids claiming an outbox removes all distributed failure.

## Search

### When would OpsLedger need a search index?

Strong-answer traits:

- Names a real workflow such as finding work requests by text across title,
  description, reasons, or report output.
- Compares Postgres filters or full-text search first.
- Treats search as derived state with staleness and rebuild risk.
- Mentions authorization and relevance failures.

## Analytics

### Why not add a warehouse for the dashboard?

Strong-answer traits:

- Says the current dashboard is a small Postgres read model.
- Names dataset size and query pressure as missing evidence.
- Explains analytical stores are for large scans and historical aggregates.
- Separates current workflow decisions from stale analytical views.

## Vector Storage

### Would vector search help OpsLedger?

Strong-answer traits:

- Names a possible retrieval feature such as similar incident or work request
  lookup.
- Says vector storage is approximate derived retrieval, not truth.
- Requires embeddings, metadata filters, evaluation, privacy review, and
  rebuilds.
- Rejects it until there is a real retrieval workflow.

## Refusal

### How do you defend not adding another datastore?

Strong-answer traits:

- Starts from current constraints: small system, VPS target, small operator
  team, Postgres source of truth, Redis only when bounded.
- Names simpler alternatives such as query changes, indexes, read models,
  cache, or an outbox.
- Explains the operational cost avoided.
- States what evidence would change the answer.
