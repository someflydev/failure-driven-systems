# Architecture Decisions Role-Track Interview

Use this guide with `paths/architecture-decisions.md` after the learner has
completed decision memo, service-boundary, datastore, runtime, and deployment
defense work.

## Evidence To Bring

- Current-system narrative from `docs/architecture/current-system.md`.
- One ADR or decision memo.
- One incident or performance artifact that shaped the decision.
- Completed `reviews/checklists/architecture-review.md` or
  `reviews/checklists/system-wide-review.md`.

## Prompts

### Current Architecture

Prompt: Explain the current OpsLedger architecture in two minutes. What owns
truth, what is derived, and what is disposable?

Strong-answer traits:

- Names API, Postgres, Redis, worker, reporting service, logs, and metrics.
- Separates source-of-truth facts from queue, cache, and derived state.
- Mentions constrained VPS and small-team operation.
- Avoids claiming planned features already exist.

### Decision Defense

Prompt: Defend one decision you made or accepted. What alternatives did you
reject, what did it cost, and how would you roll it back?

Strong-answer traits:

- Uses context, evidence, alternatives, consequences, failure modes, and
  rollback.
- Names operational cost and ownership impact.
- Includes evidence that would change the decision.
- Does not rely on generic system-design labels.

### Built Artifact Pressure

Prompt: Which built artifact most changed your architecture judgment?

Strong-answer traits:

- Points to an exercise, scenario, review, ADR, or measured result.
- Explains how implementation or incident evidence constrained the proposal.
- Connects local evidence to interview-ready tradeoff language.
- Keeps the architecture path grounded in the built system.
