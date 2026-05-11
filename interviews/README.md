# Interviews

Interview materials turn completed learner work into spoken defense practice.
They can be used alone, with a peer, with a mentor, or with an LLM interviewer.

Do not memorize answers from these files. Use the prompts to practice explaining
what happened in OpsLedger, what decision was made, what evidence supports it,
what failed, and what would make the decision wrong later.

## Modes

### Backend Feature Deep Dive

Use this mode for endpoint behavior, transactions, schemas, migrations, tests,
status transitions, idempotency, and user-visible API semantics. The
interviewer should press for concrete code paths and evidence from tests or
database state.

Best starting files:

- `interviews/phase-1-backend.md`
- `interviews/phase-2-backend-distributed.md`
- `interviews/mock-panels/backend-implementation-panel.md`

### Distributed Failure Debugging

Use this mode for queues, workers, retries, Redis outages, service timeouts,
contract failures, correlation IDs, and durable status. The interviewer should
ask the learner to separate symptoms, causes, next checks, and repair actions.

Best starting files:

- `interviews/phase-2-backend-distributed.md`
- `interviews/phase-3-distributed-boundaries.md`
- `interviews/mock-panels/distributed-systems-debugging-panel.md`

### Operational Incident

Use this mode for incident timelines, status updates, logs, metrics, health
checks, postmortems, and secret-safe evidence handling. The interviewer should
make the learner prove user impact and resolution from bounded evidence.

Best starting files:

- `interviews/phase-4-operational-debugging.md`
- `reviews/checklists/incident-review.md`
- `ops/incidents/TEMPLATE_postmortem.md`

### Architecture Decision Defense

Use this mode for ADRs, decision memos, source-of-truth boundaries, deployment
platform choices, runtime choices, datastore decisions, rollback, and
operational cost. The interviewer should challenge assumptions without asking
for a larger architecture by default.

Best starting files:

- `interviews/phase-6-storage-systems.md`
- `interviews/phase-6-language-runtime.md`
- `interviews/phase-6-deployment-platforms.md`
- `interviews/mock-panels/architecture-staff-engineer-panel.md`

### Role-Track-Specific Interview

Use this mode to bias the same OpsLedger evidence toward a target role without
turning role tracks into separate codebases.

- Backend track: API behavior, data integrity, transactions, tests,
  idempotency, and service boundaries.
- Data/backend track: source of truth, derived state, rebuilds, staleness,
  query shape, and datastore refusal.
- Platform/operations track: deployment, health checks, logs, metrics,
  incidents, runbooks, and rollback.
- Architecture/staff track: constraints, tradeoffs, sequencing, operational
  cost, and decision reversibility.

## Human, Self, And LLM Use

Human interviewer: ask one question at a time, interrupt vague claims, and ask
for evidence before giving feedback.

Self-review: record or write answers, then compare them to the strong-answer
traits. Mark weak areas to revisit.

LLM interviewer: use `reviews/llm/TEMPLATE_interview_me.md` or
`reviews/llm/TEMPLATE_adversarial_architecture_panel.md` after providing
learner artifacts and reasoning. Require critique after attempted answers, not
model answers first.
