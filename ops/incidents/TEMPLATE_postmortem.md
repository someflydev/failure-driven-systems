# Incident Postmortem Template

Use this after the learner has built their own timeline from logs, metrics,
durable status, and operator notes. Keep it short enough that the useful parts
would still be read after a small incident.

## Summary

- What happened:
- When it started:
- When it ended:
- Current state:

## Impact

- Affected users or workflows:
- User-visible symptoms:
- Scope estimate:
- Data loss or correctness concern:

## Timeline

List observed facts in timestamp order. Include the evidence source for each
entry.

- `HH:MM`: Observation and source.
- `HH:MM`: Observation and source.
- `HH:MM`: Observation and source.

## Detection

- First signal noticed:
- Signal source:
- Why this signal mattered:
- Signal that was noisy or misleading:

## Root Cause

Name the specific failed condition. Avoid broad labels such as "worker issue"
unless the evidence supports no finer conclusion yet.

## Contributing Factors

- Missing or ambiguous signal:
- Slow or manual step:
- Configuration, deployment, contract, or process factor:

## What Went Well

- Evidence that was easy to find:
- Runbook or status surface that helped:
- Decision that reduced impact:

## What Went Poorly

- Evidence that was missing, delayed, or hard to connect:
- Status update that was unclear:
- Manual step that created avoidable risk:

## Action Items

| Action | Owner | Due | Verification |
| --- | --- | --- | --- |
|  |  |  |  |

Each action should be small, observable, and tied to evidence from this
incident. Do not add broad platform work unless the incident proves the need.

## Interview Explanation

In five sentences or fewer, explain the incident to an interviewer. Include
impact, root cause, evidence used, mitigation, and one follow-up.
