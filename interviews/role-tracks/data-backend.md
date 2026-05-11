# Data/Backend Role-Track Interview

Use this guide with `paths/data-backend.md` after the learner has collected
source-of-truth, read-model, cache, and datastore-decision evidence.

## Evidence To Bring

- One transaction or migration exercise.
- Query-plan, read-model, or cache notes from Phase 5.
- One staleness or Redis outage scenario.
- A datastore decision memo or storage comparison from Phase 6.

## Prompts

### Source Of Truth

Prompt: Map customer, work request, status event, report job, notification,
read-model, and cache data. Which data is authoritative?

Strong-answer traits:

- Names Postgres-owned durable facts.
- Separates read models and Redis cache from source-of-truth data.
- Explains rebuild or fallback behavior.
- Avoids treating reporting-service payloads as owned facts.

### Query And Derived State

Prompt: Explain one measured bottleneck and why the chosen index, read model,
or cache was the right-sized response.

Strong-answer traits:

- Starts with baseline or query-plan evidence.
- Names the accepted write/storage/staleness cost.
- Explains how correctness is checked when derived state is stale.
- Does not optimize paths without evidence.

### Datastore Refusal

Prompt: Pick a datastore OpsLedger did not add. Why is refusing it currently
the better engineering decision?

Strong-answer traits:

- Ties refusal to current workload and team constraints.
- Names operational cost and failure modes.
- Explains what future evidence could change the decision.
- Avoids technology name-dropping.
