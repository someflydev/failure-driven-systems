# Log Analysis Helper

Use this template after collecting a bounded log excerpt and related evidence.
The assistant should help analyze what the evidence can and cannot prove.

```text
I am working through Failure-Driven Systems. Help analyze this bounded evidence
as a skeptical reviewer.

Scenario:

[paste the exact scenario or exercise name]

Question I am trying to answer:

[one concrete question, such as whether a report job reached the worker]

Bounded log excerpt:

[paste only the relevant sanitized log lines, preferably filtered by
correlation_id, job id, service, and time window]

Metrics snapshot:

[paste a small sanitized before/after metrics snippet, or "not collected"]

Durable status snapshot:

[paste relevant /reports/jobs, /reports/jobs/{id}, /reports/jobs/{id}/result,
or /notification-attempts output]

Commands I ran:

[paste commands and important output, not full terminal history]

My hypothesis:

[explain what I think the evidence shows before asking for analysis]

What I already ruled out:

[name any discarded hypotheses and the evidence]

Instructions for the helper:

- First state what the evidence directly supports.
- Then state what remains ambiguous.
- Challenge my hypothesis if the evidence is too thin.
- Suggest the next smallest check that would reduce uncertainty.
- Keep analysis bounded to the pasted evidence and named scenario.
- Do not request unlimited logs, full environment dumps, secrets, tokens, full
  connection strings, request bodies, or raw customer data.
- Do not provide a final incident answer unless the evidence is sufficient.
```
