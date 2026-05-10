# Postmortem Critique

Use this template only after writing your own postmortem draft from observed
logs, metrics, durable state, and operator notes.

```text
I am working through Failure-Driven Systems. Critique my postmortem as a
skeptical reviewer. Do not rewrite it for me.

Scenario:

[paste the scenario name]

Postmortem draft:

[paste my draft]

Evidence package:

[paste bounded sanitized evidence: status updates, timeline sources, logs,
metrics, health checks, durable job status, notification attempts, and commands]

My hypothesis for root cause:

[explain the root cause I believe the evidence supports]

Known uncertainty:

[name facts I could not prove or checks I could not run]

Instructions for the reviewer:

- Findings first, ordered by severity.
- Identify unsupported claims, missing timestamps, vague impact, weak root
  cause language, and action items not tied to evidence.
- Check that symptoms, contributing factors, root cause, mitigation, and
  follow-up are separated.
- Challenge overbroad platform work that the incident does not justify.
- Flag any secret-handling risk or excessive pasted data.
- Ask follow-up questions where the draft needs more evidence.
- Do not write the final postmortem or invent incident facts.
```
