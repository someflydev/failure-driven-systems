# Phase 4 Operational Debugging Mock Interview

Use these prompts after the learner has completed Phase 4 exercises, run at
least one incident scenario, and written their own notes. The goal is to defend
debugging judgment from OpsLedger evidence, not to memorize polished incident
answers.

## Evidence And Timeline

### Walk me through one report job from enqueue to final state.

Strong-answer traits:

- Names the API response, report job id, and correlation ID.
- Uses durable `/reports/jobs/{id}` state as job-specific truth.
- Connects API, worker, and reporting service logs without overclaiming.
- Separates observed timestamps from inferred ordering.

### What makes a timeline trustworthy during an incident?

Strong-answer traits:

- Uses timestamped facts with evidence sources.
- Distinguishes symptoms, user impact, hypotheses, and root cause.
- Calls out ambiguity when logs are unfiltered or IDs are missing.
- Avoids filling gaps with guesses.

## Logs And Correlation

### Why are correlation IDs useful in the ambiguous logs scenario?

Strong-answer traits:

- Explains that several report jobs can run close together.
- Names `correlation_id` as the field joining HTTP, worker, reporting service,
  and durable job evidence.
- Describes what cannot be proven safely from unfiltered logs alone.
- Mentions generated IDs and caller-supplied IDs without treating either as a
  secret.

### What should never be copied into incident notes or an LLM prompt?

Strong-answer traits:

- Excludes secrets, tokens, full connection strings, request bodies, and raw
  customer data.
- Prefers focused sanitized excerpts over full environment dumps.
- Explains why enough target detail can be useful without credentials.
- Keeps evidence bounded by time window, service, ID, and question.

## Metrics And Health

### The API and reporting service readiness checks are green, but reports fail.
What do you check?

Strong-answer traits:

- Explains that readiness can prove a process is alive without proving a
  workflow meets its timeout.
- Checks report job status and `last_error`.
- Looks for worker timeout evidence and slow reporting service logs or metrics.
- Avoids declaring the system healthy from `/health/ready` alone.

### How do metrics complement logs and durable state?

Strong-answer traits:

- Uses metrics for rate, error shape, and latency trends.
- Uses logs for request-specific path and failure details.
- Uses durable state for specific report job or notification attempt truth.
- Notes current worker metric limitations after process restart.

## Incident Response

### In the worker-stalled incident, what proves work was accepted but not
progressing?

Strong-answer traits:

- Mentions `202 Accepted` and queued report job records as acceptance evidence.
- Mentions absent or stale worker logs and unchanged durable status as lack of
  progress.
- Explains why `queued` does not prove worker health.
- States the next check after worker restart if jobs remain queued.

### How should the first status update differ from the resolved update?

Strong-answer traits:

- First update names impact, current evidence, hypothesis, action now, and next
  update time.
- Avoids claiming root cause or resolution before evidence supports it.
- Resolved update cites durable status, fresh logs, and user-visible workflow
  recovery.
- Keeps language honest when data loss is not indicated.

## Postmortems And Follow-Up

### What makes a Phase 4 postmortem useful?

Strong-answer traits:

- Includes impact, detection, evidence-backed timeline, root cause,
  contributing factors, and small action items.
- Separates a failed condition from broad labels like "worker issue."
- Ties each follow-up to incident evidence.
- Keeps the document short enough to be read after a small incident.

### How do you avoid overreacting to noisy nonfatal errors?

Strong-answer traits:

- Separates report generation success from notification side-effect failure.
- Uses `/notification-attempts` as durable side-effect evidence.
- Explains why error counters alone can mislead.
- Proposes noise reduction without hiding real delivery failures.

## LLM-Assisted Debugging

### When is it appropriate to ask an LLM for help during Phase 4?

Strong-answer traits:

- Starts after the learner gathers logs, metrics, durable state, timeline, and
  hypothesis.
- Uses the assistant as incident commander, skeptical reviewer, or interviewer.
- Requests critique of unsupported claims and missing checks.
- Avoids asking for canned final incident answers.

### What should an LLM challenge in your incident analysis?

Strong-answer traits:

- Unsupported root cause claims.
- Missing user impact or next action.
- Ambiguous log correlation.
- Excessive pasted data, secrets, and action items not justified by evidence.
