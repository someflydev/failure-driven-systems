# Decision Memo Defense

## Phase

Phase 6: architecture defense, system design, and interview readiness.

This exercise belongs here because the learner has already built and operated
enough of OpsLedger to defend decisions from evidence instead of diagrams.

## Concepts

- Architecture decision records.
- Workload- and team-specific tradeoffs.
- Source-of-truth ownership.
- Operational cost.
- Failure modes and rollback.
- Interview defense under follow-up questions.

## Prerequisites

Read these before starting:

- `docs/architecture/current-system.md`
- `docs/adr/TEMPLATE.md`
- `docs/adr/0001-report-rendering-boundary.md`
- `docs/adr/0002-fastapi-python-primary-stack.md`
- `docs/adr/0003-postgres-source-of-truth.md`
- `docs/adr/0004-redis-queue-cache-postgres-durability.md`
- `docs/adr/0005-dokku-first-deployment.md`
- `docs/CONSTRAINTS.md`
- `docs/performance/baselines.md`
- `reviews/checklists/architecture-review.md`

You should also understand the API, worker, Redis, Postgres, reporting service,
logs, metrics, and Dokku deployment docs from earlier phases.

## Build/Change Task

Write a small decision memo for one proposed change to OpsLedger. Choose one:

- keep or remove the stateless reporting service;
- add a second worker process;
- keep Redis cache for the dashboard or remove it;
- move beyond Dokku for the current system;
- add one new index or read model after measured evidence.

Your memo must include:

- the current workload and dataset assumption;
- the team and operator assumption;
- the specific pain, measurement, incident, or learning need;
- the decision;
- at least two alternatives;
- consequences and tradeoffs;
- failure modes;
- operational cost;
- rollback or reversal plan;
- a short interview defense.

Then defend the memo in a short Q&A. Ask a reviewer or LLM to challenge your
assumptions only after you have written your own reasoning.

## Constraints

- Do not implement the proposed architecture change during this exercise.
- Do not propose k3s manifests yet.
- Do not claim a tool is better without naming workload, team, operational
  cost, and failure modes.
- Do not use generic cloud scale arguments unless they match OpsLedger's
  constrained VPS target.
- Do not let an LLM write the first draft.

## Failure Modes

- The memo recommends a fashionable architecture without evidence.
- The memo treats Redis, cache, or read models as authoritative data.
- The memo ignores how a small team would deploy, monitor, debug, and roll
  back the change.
- The memo assumes the local Compose shape and current Dokku deployment docs
  are identical.
- The interview defense cannot explain what evidence would change the decision.

## Expected Reasoning

After completing the exercise, you should be able to explain why a decision
fits this system now, what it costs, how it fails, and what future evidence
would cause you to reverse it.

## Verification

- Run `./scripts/verify.sh`.
- Confirm the memo cites at least three concrete repo artifacts.
- Review the memo against `reviews/checklists/architecture-review.md`.
- Confirm the memo has explicit alternatives, consequences, failure modes,
  operational cost, and rollback sections.
- Confirm no runtime code, manifests, dependencies, or generated artifacts were
  added.

## Reflection Questions

- What exact evidence made this decision worth considering?
- Which part of the system owns the durable facts affected by the decision?
- What operational task becomes harder if this decision is accepted?
- How would the answer change for a larger team or a managed cloud platform?
- What would make you reverse the decision six months later?

## LLM Usage

Use an LLM as a skeptical reviewer or interviewer after your first draft. Ask
it to identify missing evidence, weak assumptions, hidden failure modes, and
unclear rollback steps. Do not ask it to generate the decision for you.

## Path-Specific Extensions

Backend path: tie the memo to request latency, transactions, retry behavior,
or source-of-truth data ownership.

Operations path: tie the memo to deploy steps, runbooks, health checks, logs,
metrics, and rollback.

Architecture path: compare at least three alternatives and state what evidence
would make each alternative reasonable.

Interview path: prepare a two-minute verbal defense and five follow-up answers.

## Deployment/Debugging Actions If Relevant

No deployment is required. If your memo depends on runtime evidence, cite the
specific scenario, baseline, health check, log event, metric, or durable
database state you used.
