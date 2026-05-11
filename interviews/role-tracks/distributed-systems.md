# Distributed Systems Role-Track Interview

Use this guide with `paths/distributed-systems.md` after the learner has
completed async, service-boundary, and incident debugging evidence.

## Evidence To Bring

- One report job lifecycle exercise.
- One reporting-service timeout or bad-response scenario.
- One incident timeline with logs, metrics, and durable status.
- A service-boundary review checklist.

## Prompts

### Partial Failure

Prompt: A report request was accepted but never completes. Walk through your
first checks and what each result would imply.

Strong-answer traits:

- Checks API response, durable report job status, Redis, worker logs, reporting
  service health, and correlation IDs.
- Separates symptom, hypothesis, and next action.
- Names user-visible impact.
- Avoids guessing before inspecting durable state.

### Boundary Failure

Prompt: The reporting service returns an invalid response. What fails, what
should remain correct, and how would you prove it?

Strong-answer traits:

- Names the report-rendering contract.
- Explains bounded worker failure and durable job status.
- Uses logs or metrics to locate the boundary.
- Does not corrupt source-of-truth work request data.

### System Size

Prompt: Why is this not automatically a microservices system?

Strong-answer traits:

- Names the modular monolith baseline.
- Defends the narrow stateless extraction as a learning boundary.
- Lists deployment, debugging, rollback, and contract costs.
- States what evidence could justify another split.
