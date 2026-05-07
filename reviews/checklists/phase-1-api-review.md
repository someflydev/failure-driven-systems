# Phase 1 API Review Checklist

Use this checklist when reviewing the implemented Phase 1 OpsLedger API. Keep
feedback tied to behavior that exists now: customers, work requests, status
updates, status history, liveness, and readiness.

## Validation

- Customer names are non-empty and customer emails use the current schema email
  pattern.
- Work request titles and descriptions are non-empty.
- Work request status accepts only `open`, `in_progress`, `resolved`, and
  `cancelled`.
- List endpoints reject `limit` below 1, `limit` above 100, and negative
  offsets.
- Validation failures return the API's consistent `validation_failed` error
  shape.

## Database Constraints

- `customers.email` is unique through `uq_customers_email`.
- `work_requests.customer_id` has a foreign key to `customers.id`.
- Work request status values have database check constraints.
- Status event old and new status values have database check constraints.
- Status events have a foreign key to `work_requests.id`.
- Route validation is not treated as a replacement for database constraints.

## Transaction Boundaries

- Work request creation verifies the customer exists before inserting the work
  request.
- Status updates change the current work request status and insert the status
  event in one commit.
- Failed status updates do not create orphan status events.
- Duplicate email conflicts roll back the failed transaction before returning
  `409 Conflict`.

## Error Shape

- Missing customers return `customer_not_found`.
- Missing work requests return `work_request_not_found`.
- Duplicate customer emails return `duplicate_customer_email`.
- Invalid terminal status transitions return `invalid_status_transition` with
  the attempted `from` and `to` values.
- Error responses use `{ "error": { "code", "message", "details" } }`.

## Logs And Operational Signals

- `GET /health/live` stays dependency-free and does not check the database.
- `GET /health/ready` checks database reachability.
- Readiness failures expose the error class and sanitized database target, not
  credentials.
- Manual operational checks use the current health endpoints and one CRUD path.

## Tests

- Shared fixtures provide the API client, isolated test database, and seed data.
- Tests cover duplicate customer email conflict.
- Tests cover work request creation for a missing customer.
- Tests cover status filter behavior.
- Tests cover pagination bounds for list endpoints.
- Tests cover liveness/readiness separation.
- Tests cover status history creation and missing work request failures.
- Local verification is run through `./scripts/verify.sh`.

## No Premature Complexity

- Do not add Redis, queues, workers, service extraction, Docker Compose, k3s, or
  caching for Phase 1 API review findings.
- Do not add repositories or service layers unless the current code becomes
  harder to reason about without them.
- Do not broaden tests into slow integration suites before deployment or
  scenario infrastructure exists.
- Keep feedback focused on correctness, consistency, and learner reasoning.
