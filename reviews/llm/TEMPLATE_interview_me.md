# Interview Me

Use this template after completing enough work to explain and defend your
decisions. Paste the filled-out request into an LLM interviewer.

```text
I am working through Failure-Driven Systems. Interview me from my own project
evidence. Do not answer for me unless I first attempt an answer and ask for
critique.

Phase or topic:

[phase number, exercise, incident drill, or architecture topic]

Relevant files:

[paste files or focused excerpts that ground the interview]

Commands I ran:

[paste commands and important output]

Failures or behavior observed:

[paste failures, logs, slow queries, retry behavior, incident notes, or other
evidence]

My reasoning so far:

[explain the decision, tradeoffs, rejected alternatives, and what would make the
decision wrong later]

Interview focus:

[source of truth, transactions, retries, idempotency, module boundaries,
observability, performance, deployment constraints, architecture defense, or
another specific focus]

Instructions for the interviewer:

- Ask one question at a time.
- Push for evidence from the files, commands, and failures above.
- Challenge vague claims and unsupported scale assumptions.
- After each answer, give concise critique and one sharper follow-up.
- Do not provide a model answer until I ask after attempting my own.
```
