# Side Effects and Local Notifications

OpsLedger now creates a local notification attempt when a queued work request
summary report completes. This teaches side-effect boundaries without sending
real email, SMS, Slack, or any paid provider traffic.

The notification workflow is intentionally narrow: only report completion
triggers a notification. Work request status changes are left alone for now so
learners can reason about one side effect in one worker path before adding more
triggers.

## Why Report Completion

Report jobs already have durable status, bounded retries, and completed-output
duplicate protection. That makes the worker a useful place to show a separate
problem: completing the report safely does not automatically make the later
notification side effect safe.

The worker commits `result_json` and `status = succeeded` first. Then it calls
the local notification workflow. A notification failure is recorded on
`notification_attempts`; it does not rewrite the completed report as failed.

## Local Adapter

The local adapter logs a deterministic "sent" notification and writes durable
attempt state to Postgres. It does not contact an external provider.

Current channel:

```text
local_log
```

The default recipient is:

```text
operator@example.com
```

Tests can force a failed adapter path with:

```text
fail-notification@example.com
```

That failure is local and deterministic. It exists so learners can inspect the
failed attempt without needing provider credentials or spending money.

## Durable Attempt Identity

`notification_attempts` records:

- target type and target id
- channel
- recipient
- status
- idempotency key
- error, when delivery fails
- created and sent timestamps

The current idempotency key is:

```text
report_job:{report_job_id}:completed
```

Postgres enforces uniqueness on that key. If the same report completion trigger
runs twice, the workflow returns the existing attempt instead of creating a
second durable side effect.

## Not a Full Outbox Yet

This is outbox-like because it stores side-effect intent and status in a table,
but it is intentionally not a full outbox pattern.

What is simpler:

- the worker creates and delivers the local notification directly
- there is no separate dispatcher process
- there is no generic event bus
- there is no provider retry policy
- the table stores notification attempts, not arbitrary domain events

The remaining risk is the gap between report completion and notification
attempt creation. If the worker crashes after committing the report but before
creating the attempt, the duplicate-worker guard will return early and the
notification will not be created. A fuller outbox design would write the
side-effect intent in the same transaction as the state change, then let a
dispatcher send and mark delivery later.

That fuller design is deferred until the curriculum needs dispatcher recovery,
provider retries, and operational ownership for pending side effects.

## Visibility

Notification attempts are visible through:

```text
GET /notification-attempts
GET /notification-attempts?target_type=report_job&target_id={report_job_id}
```

Failed attempts remain visible instead of disappearing into logs. Logs are
supporting evidence; Postgres is the durable status surface.
