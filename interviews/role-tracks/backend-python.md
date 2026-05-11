# Backend/Python Role-Track Interview

Use this guide with `paths/backend-python.md` after the learner has completed
the required implementation, debugging, review, and explanation milestones.

## Evidence To Bring

- One API implementation exercise and relevant route, schema, model, migration,
  and test files.
- One async job or idempotency exercise.
- One debugging scenario involving Postgres, Redis, worker, or reporting.
- Output from `./scripts/verify.sh`.

## Prompts

### API And Data Integrity

Prompt: Walk through one OpsLedger write path. Where is validation enforced,
where is truth stored, and what test would fail if the transaction were wrong?

Strong-answer traits:

- Names concrete files and behavior.
- Separates request validation from database constraints.
- Explains status history or report job state atomically.
- Identifies one missing edge case honestly.

### Async Backend Behavior

Prompt: Why does report generation use a worker, and what must remain durable
if Redis or the worker fails?

Strong-answer traits:

- Starts from synchronous pain.
- Separates API acceptance, Redis queue coordination, worker execution, and
  Postgres status.
- Mentions retries, idempotency, and duplicate side effects.
- Avoids claiming async completion from a `202 Accepted` response.

### Python Runtime Defense

Prompt: Defend Python/FastAPI for this system and name evidence that would make
you reconsider.

Strong-answer traits:

- Cites team fit, repo tooling, API speed of development, and tests.
- Names operational and performance limits.
- Compares against `docs/languages/go.md` or another runtime only in context.
- Avoids generic language ranking.
