# Incident Review Checklist

Use this checklist to critique a learner's incident drill, status updates, and
postmortem. Review the response quality, not just whether they found the
answer.

## Impact And Scope

- The review names the affected user workflow.
- Impact is stated separately from the failing component.
- Severity matches evidence and is not inflated by noisy nonfatal errors.
- The learner avoids claiming data loss, recovery, or total outage without
  proof.

## Evidence

- The timeline includes timestamps and evidence sources.
- Logs, metrics, and durable status are used for their proper purposes.
- `/reports/jobs/{id}` is treated as the job-specific source of truth.
- `/notification-attempts` is used for notification side-effect evidence.
- Metrics are used for aggregate shape, not per-job facts.
- Health endpoints are interpreted narrowly: live or ready is not the same as
  every workflow succeeding.

## Correlation And Logs

- The learner records the relevant `correlation_id`.
- API, worker, and reporting service logs are connected by correlation ID when
  the scenario supports it.
- The review challenges any timeline built from unfiltered logs alone.
- Secret-safe logging rules are followed.

## Hypothesis Discipline

- The learner states at least one hypothesis before changing anything.
- The learner records evidence that confirms or rejects the hypothesis.
- The final root cause is narrower than a vague component label.
- The response avoids speculative fixes before evidence is collected.

## Status Updates

- Updates are short enough to send during an incident.
- Each update includes impact, status, evidence, current action, and next
  update time.
- Hypotheses are labeled as hypotheses.
- The learner does not claim resolution until fresh evidence supports it.

## Postmortem

- The postmortem is written after the learner-owned timeline.
- Root cause and contributing factors are separated.
- What went well and what went poorly are concrete.
- Action items are small, assigned, and verifiable.
- Follow-ups are tied to observed evidence rather than generic maturity work.

## LLM Use

- The LLM is used after the first learner draft.
- The prompt asks for critique, missing evidence, and unsupported claims.
- The learner does not ask the LLM to invent logs, metrics, timeline, root
  cause, impact, or action items.

## Scope Control

- The response does not add production traffic, destructive actions, broad
  infrastructure, tracing, dashboards, or alerting unless a later prompt asks.
- Local/test failure injection remains local and disabled after the drill.
- The learner names what should stay out of scope for a small system.
