# System-Wide Review Checklist

Use this checklist after a learner has completed several phases, before a mock
panel, or before presenting OpsLedger as portfolio evidence. The goal is to
test whether the learner can connect decisions across phases without claiming
more than the repository actually contains.

## Evidence Package

- Names the phases, exercises, incidents, or decision memos being reviewed.
- Includes relevant files, commands, logs, metrics, database observations, and
  scenario notes.
- Separates observed facts from hypotheses and preferences.
- Includes the learner's own reasoning before reviewer critique.
- Sanitizes secrets, customer data, connection strings, tokens, and private
  deployment details.

## Source Of Truth

- Identifies which durable facts live in Postgres.
- Explains why Redis queue state, cache entries, logs, and metrics are not
  authoritative facts.
- Names which read models or cached responses may be stale.
- Describes how derived state can be rebuilt from source-of-truth tables.
- Does not move facts to another datastore without a concrete workload and
  migration or repair story.

## Backend Behavior

- Explains API status codes and user-visible behavior from concrete routes.
- Names transaction boundaries and consistency expectations.
- Covers validation, constraints, migrations, and tests.
- Connects implementation choices to failure modes and operator visibility.
- Avoids adding broad abstractions or services before a phase creates the need.

## Async And Side Effects

- Separates accepted work from completed work.
- Explains queue coordination versus durable report job state.
- Names retry limits, duplicate execution risks, and idempotency boundaries.
- Treats side effects as separate reliability problems.
- Can debug worker-down, Redis-down, retry-failure, and duplicate-execution
  scenarios from evidence.

## Boundaries And Contracts

- Explains why the reporting service is a narrow stateless extraction.
- Names ownership, contract, timeout, deployment, rollback, and debugging costs
  introduced by a process boundary.
- Distinguishes internal module boundaries from deployable service boundaries.
- Describes backward-compatible and incompatible contract changes.
- States what evidence would justify keeping, removing, or changing the
  boundary.

## Operations And Incidents

- Builds incident timelines from logs, metrics, health checks, and durable
  state.
- Separates symptoms, impact, suspected cause, confirmed cause, mitigation, and
  follow-up.
- Uses concise status updates and postmortems.
- Names what evidence proves recovery.
- Does not paste secrets or unbounded logs into review artifacts or LLM prompts.

## Performance And Scaling

- Starts with baseline evidence before proposing optimizations.
- Names dataset size, endpoint, rate, duration, latency shape, and error
  evidence.
- Explains index, read-model, and cache tradeoffs with write cost, staleness,
  rebuild, TTL, and outage behavior.
- Keeps Postgres authoritative when Redis cache or read models are used.
- Rejects generic scale claims not supported by measured OpsLedger behavior.

## Deployment And Runtime

- Explains the current local Compose and documented Dokku path accurately.
- Names what k3s teaches later and why it is not the default starting path.
- Covers health checks, migrations, config, secrets, logs, metrics access,
  rollouts, and rollback risk.
- Describes operational cost for a one-person or small-team operator on a
  constrained VPS.
- Avoids claiming deployment tooling solves schema, data, backup, or
  idempotency problems automatically.

## Interview Defense

- Can summarize the system and evolution in two minutes.
- Answers follow-ups with concrete OpsLedger evidence.
- Names tradeoffs without presenting constraints as defects.
- States at least one rejected alternative for major decisions.
- Names what evidence would change the learner's mind.

## Review Outcome

Record:

- strongest defended decision;
- weakest explanation area;
- missing evidence to collect;
- one follow-up drill or exercise;
- one interview mode to practice next.
