# Phase 3 Distributed Boundaries Mock Interview

Use these prompts after the learner has completed the Phase 3 exercises,
scenario notes, and capstone memo draft. The goal is defensible reasoning from
OpsLedger evidence, not memorized microservice talking points.

## Boundary Design

### Why did OpsLedger start Phase 3 with modular monolith boundaries?

Strong-answer traits:

- Names ownership of customers, work requests, report jobs, rendering, and
  notification attempts.
- Explains that internal boundaries improve reasoning before deployment is
  split.
- States that service boundaries add cost.
- Avoids presenting extraction as the default end state.

### Which facts cross the reporting boundary?

Strong-answer traits:

- Says the worker sends a complete report snapshot.
- Explains that the renderer returns derived output.
- Names Postgres as the owner of source-of-truth facts.
- Does not claim the reporting service owns work requests or report jobs.

## Extraction Decision

### Why was report rendering the safest Phase 3 extraction candidate?

Strong-answer traits:

- Describes rendering as pure computation over caller-provided input.
- Contrasts it with workflow state, notifications, or customer identity.
- Mentions the educational value of HTTP contracts and partial failure.
- Also names the extra service, timeout, deployment, and debugging costs.

### Should the reporting extraction stay?

Strong-answer traits:

- Gives a conditional answer based on evidence.
- Weighs isolation or independent runtime needs against operational cost.
- Considers folding back to the in-process renderer if benefits are weak.
- Does not argue from architecture fashion.

## Contracts

### What makes a `report-rendering.v1` change backward-compatible?

Strong-answer traits:

- Uses optional additive fields as the safe example.
- Explains old caller and old provider behavior.
- Preserves required fields, types, literals, and semantics.
- Mentions tests that prove old and new shapes still work.

### How do you handle mixed versions during deployment?

Strong-answer traits:

- Starts with consumer expectations.
- Explains why additive response metadata can be ignored.
- Rejects wrong contract versions or missing required fields.
- Names persisted report results as a reason compatibility matters after
  runtime calls finish.

## Failure And Debugging

### A report job failed after the reporting service was slow. What do you check?

Strong-answer traits:

- Checks report job status and attempt evidence first.
- Inspects worker and reporting service logs.
- Names the configured timeout.
- Separates accepted work from completed work.

### Why not retry every failed rendering call automatically?

Strong-answer traits:

- Explains bounded retry design and idempotency reasoning.
- Distinguishes timeout, provider error, malformed JSON, and invalid contract.
- Avoids masking contract drift with retries.
- Names durable evidence as more useful than blind repetition.

## Operations

### What did extraction add for operators?

Strong-answer traits:

- Names a new process, health endpoint, configuration, logs, deploy order, and
  rollback decision.
- Explains local Compose friction as a real cost.
- States how to fall back to the in-process renderer when configured that way.
- Keeps observability claims limited to current logs and status endpoints.

### What would justify extracting another OpsLedger module?

Strong-answer traits:

- Requires concrete operational, scaling, ownership, or reliability evidence.
- Names source-of-truth and transaction questions before technology choices.
- Rejects database-per-service as a default.
- Keeps k3s, caching, and another service out of Phase 3.
