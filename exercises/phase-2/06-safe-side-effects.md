# Safe Side Effects

## Phase

Phase 2: Async After Synchronous Pain. This exercise belongs here because the
learner has already seen queued report work, retries, idempotent job execution,
and the difference between durable state and queue coordination.

## Concepts

- Side effects after durable state changes.
- Dual writes and crash windows.
- Local fake adapters versus real providers.
- Durable side-effect identity.
- Failed side-effect visibility.
- The difference between outbox-like records and a full outbox dispatcher.

## Prerequisites

- `exercises/phase-2/01-synchronous-report-pain.md`
- `exercises/phase-2/02-background-report-worker.md`
- `exercises/phase-2/03-job-status-and-eventual-consistency.md`
- `exercises/phase-2/04-retries-before-idempotency.md`
- `exercises/phase-2/05-idempotent-report-jobs.md`
- `docs/async/idempotency.md`
- `docs/async/side-effects-and-outbox.md`
- `services/api/opledger_api/report_jobs.py`
- `services/api/opledger_api/notifications.py`
- `services/api/opledger_api/models.py`
- `services/api/tests/test_notifications.py`
- Alembic migration workflow.

## Build/Change Task

Review or build the local notification workflow for completed report jobs. When
a work request summary report job reaches `succeeded`, the worker should create
one durable notification attempt for the completed report.

Use the local adapter only. Confirm that the notification attempt is visible
through the API, that duplicate triggers do not create duplicate attempts, and
that a failed local adapter path records a failed attempt.

Then write a short explanation of the dual-write boundary: the report result
and the notification attempt are separate durable facts, and committing one does
not automatically commit the other.

## Constraints

- Do not integrate real email, SMS, Slack, or paid APIs.
- Do not add a separate notification service.
- Do not add a generic event bus.
- Do not hide failed notification attempts.
- Do not claim the current table is a full outbox dispatcher.
- Do not make notification success required for report success.
- Keep the trigger scoped to report completion.

## Failure Modes

- Sending a real provider notification from tests or local exercises.
- Creating duplicate notification attempts during worker redelivery.
- Treating report job idempotency as if it also solves side-effect
  idempotency.
- Marking a completed report as failed because the later notification failed.
- Recording only logs with no database-visible failed attempt.
- Ignoring the crash window between report completion and attempt creation.
- Naming the pattern "outbox" without explaining which outbox guarantees are
  still missing.

## Expected Reasoning

After completing this exercise, explain why side effects need their own durable
identity. Be precise about which key prevents duplicate notification attempts
and why the notification status must be inspectable separately from report job
status.

You should also be able to explain what would change with a real email
provider: provider credentials, external idempotency support, delivery retries,
bounce or rejection handling, rate limits, observability, and a dispatcher that
can recover pending work after a process crash.

## Verification

- Run `./scripts/verify.sh`.
- Start the local stack with `./scripts/dev-up.sh`.
- Apply migrations with `./scripts/migrate.sh --compose`.
- Enqueue a work request summary report job.
- Run the worker and wait for the report job to reach `succeeded`.
- Call `GET /notification-attempts?target_type=report_job&target_id={id}` and
  confirm one `sent` attempt exists.
- Trigger the same completed report notification path again in a test or local
  shell and confirm a second attempt is not created.
- Force the local failed-adapter path in a test and confirm a `failed` attempt
  remains visible with an error.

## Reflection Questions

- What durable fact proves the report completed?
- What durable fact proves notification delivery was attempted?
- Why is the notification idempotency key not the same as the report enqueue
  idempotency key?
- What crash window remains in the intentionally simple design?
- Which parts would need to change before using a real email provider?

## LLM Usage

Use an LLM as a reviewer after you can explain the boundary yourself. Ask it to
look for duplicate side effects, hidden failures, and places where report job
status and notification status are incorrectly coupled. Do not ask it to design
a full notification platform before you have identified the current failure
mode.

## Path-Specific Extensions

Backend: add a focused test for a duplicate worker delivery after report
success and explain why no second notification attempt appears.

Operations: inspect application logs and the `notification_attempts` table for
the same report completion, then decide which evidence would help during an
incident.

Architecture: sketch the minimal changes required to turn this into a full
outbox dispatcher while keeping Postgres as the source of truth.

Interview: defend why the exercise uses a local fake adapter before a real
provider.

## Deployment/Debugging Actions If Relevant

Use local or VPS logs to confirm the `local_log` adapter emitted a notification
event. Inspect the database row to confirm durable status instead of relying on
logs alone.
