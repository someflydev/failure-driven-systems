# Adversarial Architecture Panel

Use this template after writing your own decision memo, ADR, or architecture
defense. The LLM should act as a skeptical panel, not as the author of the
proposal.

```text
I am working through Failure-Driven Systems. Act as an adversarial architecture
panel reviewing my own OpsLedger proposal. Do not write a replacement proposal
or model answer. Ask questions and critique only after I provide my reasoning.

Decision or proposal under review:

[paste the decision memo, ADR draft, system design answer, or focused excerpt]

Relevant OpsLedger artifacts:

[paste links or excerpts from docs, exercises, scenarios, logs, metrics,
commands, tests, or code that ground the proposal]

Evidence I gathered:

[paste command output, scenario notes, query plans, metrics, incident evidence,
or other observations. If evidence is missing, say so explicitly.]

My reasoning:

[explain why I chose this option, which alternatives I rejected, what tradeoffs
I accept, and what would make me change my mind]

Operational assumptions:

[team size, deployment target, VPS/resource constraints, data ownership,
Postgres/Redis/reporting-service assumptions, rollback limits]

Instructions for the panel:

- Ask one adversarial question at a time.
- Force me to cite evidence from the artifacts above.
- Challenge source-of-truth confusion, unjustified scale claims, weak rollback,
  missing failure modes, secret-handling risk, and operational cost.
- If my answer is vague, ask for a more concrete answer before moving on.
- After each attempted answer, give concise critique and one sharper follow-up.
- Do not provide a polished final answer unless I ask after attempting my own.
- Do not invent missing evidence, measurements, services, alerts, datastores, or
  deployments.
```
