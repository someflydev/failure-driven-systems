# Noisy Nonfatal Errors

Use this scenario to practice separating noisy side-effect failures from the
core user workflow.

## Goal

Inspect notification failure evidence without incorrectly declaring report
generation down.

## Preconditions

- Local tests can run.
- You understand `docs/async/side-effects-and-outbox.md`.
- You understand `docs/observability/metrics.md`.

## Steps

Run the deterministic notification failure test:

```sh
uv run pytest services/api/tests/test_notifications.py::test_failed_local_notification_adapter_path_is_visible
```

For manual inspection against a migrated local stack, create a failed local
notification attempt and inspect it through the API:

```sh
uv run python -c 'from opledger_api.db import get_session; from opledger_api.models import ReportJob; from opledger_api.notifications import LOCAL_NOTIFICATION_FAILURE_RECIPIENT, notify_report_completed; s=get_session(); j=ReportJob(report_type="work_request_summary", status="succeeded"); s.add(j); s.commit(); s.refresh(j); a=notify_report_completed(s, j, recipient=LOCAL_NOTIFICATION_FAILURE_RECIPIENT); print(j.id, a.status, a.error); s.close()'
curl -sS http://localhost:18080/notification-attempts?target_type=report_job\&target_id={id}
```

Use the same local database environment you use for migrations, but do not copy
the full connection string into incident notes.

Inspect logs if the stack is running:

```sh
docker compose logs --tail=100 api
docker compose logs --tail=100 worker
```

## Expected Observations

- A notification attempt can be `failed` while the related report job remains
  `succeeded`.
- Logs may include `event=notification_failed` with
  `error=LocalNotificationDeliveryError`.
- `/notification-attempts` is the durable surface for the side-effect failure.
- Notification failure counters can move inside the process that records them,
  but `/notification-attempts` is the durable evidence that survives process
  boundaries in the current local setup.

## Status Update Practice

Write one update that reports the notification side-effect issue without
claiming the report job failed. Include the evidence you would still check
before escalating the severity.

## Explain What Happened

- Which workflow was still successful?
- Which side effect failed?
- Which endpoint shows durable notification evidence?
- Why would a dashboard showing only error counts be misleading here?
- What follow-up would reduce noise without hiding real notification failures?
