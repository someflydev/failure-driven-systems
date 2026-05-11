# Distributed Systems Debugging Panel

Use this panel after Phase 3 or Phase 4 work. It tests whether the learner can
debug partial failure across API, worker, Redis, Postgres, and the stateless
reporting service.

## Evidence Package

The learner should bring:

- one Phase 2, Phase 3, or Phase 4 scenario writeup;
- focused logs with request IDs or correlation IDs;
- durable report job or notification attempt observations;
- relevant metrics or health responses;
- one discarded hypothesis and why it was discarded.

## Panel Flow

### Initial Triage

Prompt: A report job is accepted but never produces a result. What do you check
first, and why?

Strong-answer traits:

- Checks durable job status before guessing.
- Separates enqueue failure, stopped worker, worker failure, Redis outage, and
  reporting-service failure.
- Names logs, health, metrics, and database evidence.
- Chooses the next smallest check.

### Queue Versus Truth

Prompt: What can Redis prove in this system, and what can it not prove?

Strong-answer traits:

- Limits Redis to queue coordination and cache behavior.
- Names Postgres report job state as durable user-visible truth.
- Explains what happens when Redis is unavailable.
- Avoids using an RQ id as the durable product handle.

### Boundary Failure

Prompt: The reporting service times out. What should the worker persist and
what should users see?

Strong-answer traits:

- Names timeout mapping, bounded failure evidence, and durable job status.
- Explains that the API should not report completed output.
- Connects correlation IDs and logs across process boundaries.
- Does not hide a partial failure behind success language.

### Incident Discipline

Prompt: Give a concise status update for the incident using only known facts.

Strong-answer traits:

- States impact, evidence, current hypothesis, current action, and next update.
- Avoids unsupported root-cause claims.
- Keeps secrets and raw customer data out of the update.
- Names what evidence would prove recovery.

### Corrective Action

Prompt: What is the smallest corrective action you would take, and what would
you explicitly avoid changing during the incident?

Strong-answer traits:

- Picks a bounded mitigation or repair step.
- Separates immediate mitigation from later prevention.
- Avoids broad rewrites during active debugging.
- Names verification after the change.

## Scoring Notes

Mark weak areas as:

- jumped to root cause without evidence;
- confused Redis with durable truth;
- ignored user impact;
- skipped correlation or durable state;
- proposed a large change before confirming failure mode.

End by assigning one scenario rerun or incident checklist review.
