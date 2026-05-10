# Datastore Tradeoff Defense

## Phase

Phase 6: architecture defense, system design, and interview readiness.

This exercise belongs here because the learner can now compare storage
paradigms against the actual OpsLedger implementation instead of inventing a
generic system design diagram.

## Concepts

- Source-of-truth ownership.
- Relational, document, key-value, queue, search, analytical, and vector
  storage tradeoffs.
- Derived state and staleness.
- Operational cost for a small team.
- Evidence-based refusal to add infrastructure.
- Interview defense under follow-up questions.

## Prerequisites

Read these before starting:

- `docs/architecture/current-system.md`
- `docs/adr/0003-postgres-source-of-truth.md`
- `docs/adr/0004-redis-queue-cache-postgres-durability.md`
- `docs/data-models/phase-1.md`
- `docs/performance/read-models.md`
- `docs/performance/caching.md`
- `docs/storage/README.md`
- every comparison doc in `docs/storage/`
- `exercises/phase-6/01-decision-memo-defense.md`

You should also understand report jobs, notification attempts, the dashboard
read model, the Redis queue, and the reporting service boundary.

## Build/Change Task

Write a short datastore tradeoff defense for one proposed OpsLedger change:

- add a document store for flexible work request metadata;
- add a search index for work request discovery;
- add an analytical store for long-range reporting;
- add a durable stream for work request events;
- add vector storage for similar incident or work request retrieval;
- remove or narrow Redis usage.

Your defense must include:

- the current OpsLedger workload and user workflow;
- the current source-of-truth owner;
- the proposed store and exactly what it would own;
- what OpsLedger would gain;
- what OpsLedger would pay operationally;
- at least four failure modes;
- the simpler alternative you would try first;
- the evidence that would make you accept or reject the proposal;
- a two-minute interview answer.

## Constraints

- Do not implement the proposed datastore.
- Do not add MongoDB, Elasticsearch, ClickHouse, Kafka, vector databases,
  managed cloud queues, or cloud-managed services.
- Do not imply every paradigm belongs in OpsLedger.
- Do not make Redis, cache, search, analytics, or vector retrieval
  authoritative for current workflow state.
- Do not use generic scale claims without OpsLedger-specific workload evidence.

## Failure Modes

- The defense recommends a datastore because it is common, not because
  OpsLedger has the workload.
- The proposed store duplicates Postgres facts without a reconciliation plan.
- The answer ignores stale derived state.
- The answer cannot explain backup, restore, monitoring, security, or rollback.
- The answer confuses queue transport, event history, and source of truth.
- The interview answer cannot say when not to add another datastore.

## Expected Reasoning

After completing the exercise, you should be able to defend why OpsLedger uses
Postgres and Redis today, compare a specialized datastore against that baseline,
and explain why the responsible decision may be to keep the architecture
smaller.

## Verification

- Run `./scripts/verify.sh`.
- Confirm your defense cites at least three concrete OpsLedger artifacts.
- Confirm it names a current source-of-truth owner for every affected fact.
- Confirm it includes a "do not add this yet" argument.
- Confirm no runtime code, dependencies, service manifests, or generated
  artifacts were added.

## Reflection Questions

- Which current OpsLedger failure mode would the new store improve?
- Which new failure mode would be hardest for a small operator to debug?
- What data could become stale, duplicated, or missing?
- Which simpler Postgres or Redis change should be tried first?
- What evidence would change your answer six months later?

## LLM Usage

Use an LLM only after writing your own defense. Ask it to challenge weak
evidence, ownership ambiguity, missing failure modes, and operational blind
spots. Do not ask it to choose the datastore for you.

## Path-Specific Extensions

Backend path: include schema, query, transaction, idempotency, or consistency
implications.

Operations path: include deployment, health checks, backup, restore, metrics,
logs, and incident response.

Architecture path: compare at least three paradigms and explain why two are
rejected for the current OpsLedger workload.

Interview path: answer five follow-up questions from
`interviews/phase-6-storage-systems.md` without notes.

## Deployment/Debugging Actions If Relevant

No deployment is required. If your defense depends on runtime evidence, cite
the specific scenario, baseline, metric, log event, health check, or durable
database row you inspected.
