# LLM Review Prompts

These reusable patterns keep LLM help aligned with the doctrine: struggle
first, critique second, explanation third, and solution comparison only after a
serious attempt. Paste relevant files, commands, failures, and your own
reasoning before using any pattern.

## Harsh Implementation Review

Use after completing an implementation attempt.

```text
Act as a harsh implementation reviewer for this Failure-Driven Systems task.

Context:
- Prompt or exercise:
- Relevant files:
- Commands I ran:
- Failures or confusing behavior:
- My reasoning and tradeoffs:

Review for correctness, missing validation, weak transactions, source-of-truth
confusion, operational blind spots, and tests I should add. Do not rewrite the
solution. Give findings first, ordered by severity, then ask follow-up
questions I should answer.
```

## Missed Edge Cases

Use when the implementation works on the happy path.

```text
Find missed edge cases in my attempt.

Context:
- Prompt or exercise:
- Relevant files:
- Commands I ran:
- Known passing cases:
- Known failing cases:
- My reasoning about the design:

Focus on inputs, state transitions, concurrency, persistence, retries, partial
failure, and user-visible confusion. Do not provide a full replacement
implementation. Give me a test matrix and explain why each case matters.
```

## Retry/Idempotency Critique

Use after designing retry-prone work.

```text
Critique my retry and idempotency design.

Context:
- Prompt or exercise:
- Relevant files:
- Commands I ran:
- Side effects involved:
- Failure modes I observed:
- My reasoning about what can be retried safely:

Challenge duplicate side effects, retry limits, stuck work, poison inputs,
dead-letter handling, observability, and repair steps. Do not solve it for me.
Ask questions that force me to defend the design.
```

## Architecture Skeptic

Use before committing to a boundary or architecture change.

```text
Act as an architecture skeptic.

Context:
- Prompt or exercise:
- Relevant files or diagrams:
- Commands or evidence gathered:
- Problem the design is supposed to solve:
- My reasoning and rejected alternatives:

Challenge ownership, coupling, source-of-truth boundaries, operational cost,
failure modes, and whether the change is justified by evidence. Do not invent a
larger architecture. Tell me what would make my decision wrong later.
```

## Incident Commander

Use during or after an operational drill.

```text
Act as an incident commander for this debugging drill.

Context:
- Scenario or prompt:
- Relevant files:
- Commands I ran:
- Logs, metrics, database observations, or deploy output:
- What I think happened:
- What users experienced, if known:

Help me build an evidence-based timeline. Separate symptoms from causes, point
out missing evidence, ask what I should check next, and require a small
corrective action. Do not skip directly to a final answer.
```

## Mock Backend Interview

Use after finishing enough work to defend decisions from evidence.

```text
Mock interview me as a backend systems candidate.

Context:
- Phase or project history:
- Relevant files:
- Commands or evidence I can cite:
- Failures I encountered:
- My current architecture reasoning:

Ask one question at a time. Press me on source of truth, transactions,
idempotency, consistency, observability, performance, deployment constraints,
and tradeoffs. Do not answer for me unless I ask for critique after attempting
an answer.
```
