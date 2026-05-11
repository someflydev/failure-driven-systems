# Generalist Backend Role-Track Interview

Use this guide with `paths/generalist-backend.md` after the learner has one
feature, one debugging scenario, one review, and one system explanation.

## Evidence To Bring

- One feature walkthrough with tests.
- One local container or deployment note.
- One incident or debugging note.
- One performance or cache observation.
- Output from `./scripts/verify.sh`.

## Prompts

### End-To-End Ownership

Prompt: Walk through one change from requirement to implementation, tests,
runtime checks, and review.

Strong-answer traits:

- Names files, commands, and observed behavior.
- Explains one tradeoff and one rejected alternative.
- Uses the narrowest relevant review checklist.
- Does not outsource reasoning to an LLM.

### Operational Debugging

Prompt: Pick one failure scenario. What evidence did you collect, what
hypothesis did you discard, and what would you do next in production?

Strong-answer traits:

- Uses logs, health, metrics, database state, or durable job status.
- Separates immediate mitigation from follow-up fix.
- Communicates user impact.
- Avoids vague "check everything" answers.

### Breadth With Restraint

Prompt: What did you deliberately not add to OpsLedger, and why?

Strong-answer traits:

- Names one deferred service, datastore, platform, or observability tool.
- Connects the refusal to constraints and current evidence.
- Explains what signal would justify revisiting the decision.
- Shows breadth without overbuilding.
