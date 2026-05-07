# Phase 1 Backend Mock Interview

Use these prompts after the learner has completed the Phase 1 exercises and
written their own notes. The goal is to test reasoning from concrete OpsLedger
evidence, not to memorize canned answers.

## API Design

### Explain the customer and work request API surface.

Strong-answer traits:

- Names the implemented customer and work request routes.
- Distinguishes create, read, list, and status update behavior.
- Explains validation, not-found, conflict, and invalid-state failures.
- Keeps the explanation tied to one synchronous API.

### Why is duplicate customer email a conflict?

Strong-answer traits:

- Connects the response to an existing durable record.
- Mentions the database unique constraint as the final guard.
- Separates request shape validation from state conflict.
- Describes what a client can do next.

## Relational Modeling

### Walk through the Phase 1 data model.

Strong-answer traits:

- Identifies customers, work requests, and status events.
- Explains primary keys, foreign keys, uniqueness, and status constraints.
- Names Postgres as the source of truth.
- Avoids treating route validation as enough for durable integrity.

### Why keep current status on `work_requests` and history in a separate table?

Strong-answer traits:

- Separates the current operational fact from the timeline.
- Explains why list and read routes need the current status directly.
- Explains how history supports audit and debugging.
- Notes that both facts must stay consistent.

## Transactions

### Explain the status update transaction.

Strong-answer traits:

- Describes changing the current status and inserting the status event.
- Explains why one commit protects consistency.
- Names a failure that could happen with separate commits.
- Mentions foreign keys and check constraints as additional protection.

### How would you test transaction behavior?

Strong-answer traits:

- Starts with API tests for the visible behavior.
- Checks status history creation and missing work request errors.
- Mentions migration or database inspection for constraints.
- Keeps the test strategy fast enough for frequent verification.

## Health, Logs, And Debugging

### The API is live but not ready. What does that mean?

Strong-answer traits:

- Explains liveness as process responsiveness.
- Explains readiness as dependency availability.
- Names Postgres as the Phase 1 readiness dependency.
- Describes checking health responses and logs before changing code.

### What should database readiness failure logs include?

Strong-answer traits:

- Includes event name, error class, driver, host, port, and database.
- Excludes credentials, full URLs, and secret environment values.
- Explains why sanitized target details are enough for diagnosis.
- Connects logs to an incident note or deploy check.

## Deployment

### Walk through the Dokku deployment path.

Strong-answer traits:

- Mentions the root `Dockerfile`, one Dokku app, and one Dokku Postgres service.
- Explains Postgres linking and `DATABASE_URL`.
- Runs migrations explicitly after deploy.
- Checks liveness, readiness, logs, and one database-backed API path.

### A deploy succeeds but CRUD routes fail. How do you reason about it?

Strong-answer traits:

- Separates build success from runtime correctness.
- Checks readiness, logs, config, and migration state.
- Considers schema mismatch before editing route code.
- Discusses rollback risk if migrations already changed the database.

## Scope Control

### Why is Phase 1 still one service?

Strong-answer traits:

- Grounds the answer in current behavior and failure modes.
- Explains that one service keeps transactions and debugging visible.
- Names the costs of service extraction before there is a concrete need.
- Avoids presenting service count as a maturity signal.

### Why not add Redis, caching, or a queue yet?

Strong-answer traits:

- Connects each tool to a later kind of measured pain.
- Explains that Phase 1 failures are direct request, database, deploy, and log
  failures.
- Avoids using technology names as proof of architecture.
- States what evidence could justify revisiting the decision later.
