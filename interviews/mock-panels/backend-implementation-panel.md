# Backend Implementation Panel

Use this panel after the learner has completed Phase 1 and Phase 2 work, or as
a backend-focused review before a larger mock interview.

## Evidence Package

The learner should bring:

- one completed backend exercise or capstone;
- relevant route, schema, model, migration, and test files;
- command output from `./scripts/verify.sh`;
- database or API observations from at least one failure scenario;
- notes on one decision they made and one alternative they rejected.

## Panel Flow

### System Walkthrough

Prompt: Walk through the current OpsLedger request path for creating or
updating a work request. Where is truth stored?

Strong-answer traits:

- Names the route, schema, model, migration, and tests involved.
- Explains Postgres as the durable owner of workflow facts.
- Mentions transaction boundaries and status history when relevant.
- Avoids claiming logs or API responses are the source of truth.

### Data Integrity

Prompt: What bug would you expect if status changes and status history were not
written atomically?

Strong-answer traits:

- Describes current state and history diverging.
- Names how a test or database inspection would reveal the problem.
- Explains user or operator confusion.
- Gives a small fix direction without hand-waving.

### API Semantics

Prompt: Pick one endpoint and defend its status codes and error behavior.

Strong-answer traits:

- Names what the caller can safely assume.
- Separates validation errors, missing resources, and successful state changes.
- Ties behavior to tests or observed responses.
- Does not overpromise background completion from synchronous responses.

### Async Extension

Prompt: Why did report generation move behind a worker, and what did that not
solve?

Strong-answer traits:

- Starts from synchronous report pain.
- Separates API acceptance, Redis queue coordination, worker execution, and
  durable Postgres status.
- Names retries, stuck jobs, and duplicate side effects as remaining concerns.
- Avoids treating async work as a service extraction.

### Test Judgment

Prompt: Which test in your attempt catches the most important regression, and
which case is still weak?

Strong-answer traits:

- Names a concrete test and behavior.
- Explains why that behavior is high-risk.
- Names a missing edge case or scenario.
- Avoids claiming full confidence from happy-path tests.

## Scoring Notes

Mark weak areas as:

- implementation detail unclear;
- source-of-truth confusion;
- missing failure evidence;
- weak test explanation;
- overbroad architecture claim.

End by assigning one checklist or quiz section to revisit.
