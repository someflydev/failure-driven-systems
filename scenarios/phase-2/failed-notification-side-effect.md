# Failed Notification Side Effect Scenario

Use this scenario to inspect a failed local notification attempt without
calling any external provider.

## Goal

Force the local adapter failure path, confirm the report can remain succeeded,
and inspect the durable failed notification attempt.

## Preconditions

- Local tests can run.
- You understand `docs/async/side-effects-and-outbox.md`.
- No real email, SMS, Slack, or paid provider is configured.

## Fast Test Path

Run the focused notification test:

```sh
uv run pytest services/api/tests/test_notifications.py::test_failed_local_notification_adapter_path_is_visible
```

The test creates a succeeded report job, calls the local notification workflow
with `fail-notification@example.com`, and verifies that the attempt is marked
`failed` with `LocalNotificationDeliveryError`.

## Manual Inspection Path

Use a local shell against a migrated database:

```sh
DATABASE_URL=postgresql+psycopg://opledger:opledger_local_password@localhost:55432/opledger \
uv run python -c 'from opledger_api.db import get_session; from opledger_api.models import ReportJob; from opledger_api.notifications import LOCAL_NOTIFICATION_FAILURE_RECIPIENT, notify_report_completed; s=get_session(); j=ReportJob(report_type="work_request_summary", status="succeeded"); s.add(j); s.commit(); s.refresh(j); a=notify_report_completed(s, j, recipient=LOCAL_NOTIFICATION_FAILURE_RECIPIENT); print(j.id, a.status, a.error); s.close()'
```

Then inspect attempts through the API:

```sh
curl -sS http://localhost:18080/notification-attempts?target_type=report_job\&target_id={id}
```

Expected observations:

- The notification attempt is durable and visible.
- The attempt status is `failed`.
- The report status does not need to become `failed` just because the later
  side effect failed.

## Explain What Happened

- Why is a failed notification attempt separate from report job status?
- What evidence would an operator inspect first?
- What would a full outbox dispatcher add that this local workflow does not?
- Why is a local deterministic adapter safer for this phase than a real
  provider?
