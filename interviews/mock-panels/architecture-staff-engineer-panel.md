# Architecture And Staff Engineer Panel

Use this panel during Phase 6 after the learner has written at least one
decision memo or ADR-style defense. It tests judgment, sequencing, operational
cost, and the ability to refuse unnecessary complexity.

## Evidence Package

The learner should bring:

- one decision memo, ADR, or architecture defense exercise;
- relevant docs from `docs/architecture/`, `docs/storage/`,
  `docs/languages/`, or `docs/deployment/`;
- at least one performance, incident, or failure scenario observation;
- one rejected alternative;
- a rollback or reversal plan.

## Panel Flow

### Current System

Prompt: Describe the current OpsLedger architecture in two minutes. Include
what is real today and what is intentionally out of scope.

Strong-answer traits:

- Names API, worker, reporting service, Postgres, Redis, logs, metrics, and
  deployment docs accurately.
- Distinguishes implemented behavior from planned or optional work.
- Explains the phase sequence.
- Avoids inventing scale, alerts, managed services, or extra datastores.

### Decision Defense

Prompt: Pick one decision and defend why it fits the current constraints.

Strong-answer traits:

- States context, decision, alternatives, consequences, and failure modes.
- Ties the decision to OpsLedger evidence.
- Names one-person or small-team operational cost.
- Says what evidence would reverse the decision.

### Datastore Pressure

Prompt: A stakeholder asks for another datastore. How do you evaluate the
request?

Strong-answer traits:

- Starts from workload and source-of-truth ownership.
- Considers Postgres changes, indexes, read models, cache, or outbox first.
- Names migration, consistency, backups, repair, observability, and rollback.
- Rejects vague scale or fashion arguments.

### Runtime Or Platform Change

Prompt: When would you choose a different runtime or move from Dokku to k3s?

Strong-answer traits:

- Compares component fit, team skill, local workflow, deployment, operations,
  and rollback.
- Treats k3s as a later orchestration lesson, not the default starting point.
- Names resource constraints on the small VPS.
- Avoids turning role tracks or runtime experiments into separate main
  codebases.

### Tradeoff Under Pressure

Prompt: What compromise in OpsLedger are you most willing to defend, and what
is the strongest argument against it?

Strong-answer traits:

- Names a real compromise from the repository.
- Gives the strongest opposing argument fairly.
- Explains why the current decision still fits.
- Names evidence that would change the recommendation.

## Scoring Notes

Mark weak areas as:

- generic architecture vocabulary without evidence;
- no rollback or reversal plan;
- operational cost omitted;
- constraints treated as embarrassing instead of intentional;
- proposed complexity without a concrete failure.

End by assigning `reviews/checklists/architecture-review.md`,
`reviews/checklists/system-wide-review.md`, or another focused defense drill.
