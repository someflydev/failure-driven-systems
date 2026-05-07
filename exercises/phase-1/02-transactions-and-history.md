# Transactions and Status History

## Phase

Phase 1. This exercise belongs in the single synchronous service phase because
the learner should see how one relational database transaction protects related
facts before adding slower or more distributed patterns.

## Concepts

- Transaction boundaries
- Source-of-truth ownership
- Status history tables
- Foreign keys and check constraints
- Clear API failure responses
- Focused tests for consistency failures

## Prerequisites

- Complete `exercises/phase-1/01-basic-crud.md`.
- Read `docs/data-models/phase-1.md`.
- Inspect `services/api/opledger_api/models.py`.
- Inspect `services/api/opledger_api/routes.py`.
- Inspect `services/api/opledger_api/schemas.py`.
- Inspect the Alembic migrations under `services/api/migrations/versions/`.
- Run the existing API tests before changing behavior.

## Build/Change Task

Add status history for OpsLedger work requests:

- create a `work_request_status_events` table
- record `work_request_id`, `old_status`, `new_status`, `reason`, and
  `created_at`
- update the status update route so the work request's current status and the
  status event are committed together
- add a route that lists status events for one work request
- return predictable errors for missing work requests

Before building, write down what could go wrong if the status update and the
history insert were two separate operations. Include at least one failure after
the status row changes but before the history row is written, and one failure
where history could point at work that does not exist.

## Constraints

- Keep Postgres as the only durable source of truth.
- Keep this as one synchronous API and one local database transaction.
- Do not add queues.
- Do not add background workers.
- Do not add external audit logging.
- Do not introduce a separate service.
- Do not make status history the only source for current status.
- Do not use event sourcing terminology as the default explanation.

## Failure Modes

- Updating the current status without recording why it changed.
- Recording a status event when the status update failed.
- Creating orphan status events for missing work requests.
- Letting status history accept statuses that `work_requests.status` rejects.
- Treating API validation as a replacement for database constraints.
- Splitting related writes across separate commits.

## Expected Reasoning

The learner should be able to explain which fact is authoritative for current
status, which fact is authoritative for status history, and why both facts must
be changed in one transaction. The learner should also be able to explain how a
foreign key prevents orphan history and why the API should still return a clean
not-found error before relying on the database to reject bad writes.

## Verification

- Run the migration against a local database when one is available.
- Run `./scripts/verify.sh`.
- Confirm a status update creates exactly one status event with the old status,
  new status, reason, and work request id.
- Confirm updating a missing work request returns the expected error shape.
- Confirm no status event can be created for a missing work request.
- Inspect the generated migration for the status event foreign key, non-null
  columns, and status check constraints.

## Reflection Questions

- Why is the current status still stored on `work_requests`?
- Why is status history stored in a separate table?
- What inconsistent states become possible if the two writes use separate
  commits?
- Which problems are prevented by route code, and which are prevented by
  database constraints?
- What would make this change harder to understand if it were moved out of the
  local request-response path today?

## LLM Usage

Use an LLM to review your transaction reasoning, ask for missing consistency
tests, or challenge your explanation of authoritative facts. Do not ask the LLM
to skip the pre-pattern reasoning step or produce the finished implementation
before you can explain the failure modes yourself.

## Path-Specific Extensions

Backend path: add tests for repeated status changes and verify event ordering.

Operations path: capture the SQL query you would run during an incident to
explain a work request's status timeline.

Architecture path: write a short note explaining why this lesson stays inside
one service and one database transaction.

Interview path: practice explaining atomicity and foreign keys without naming
larger architecture patterns.

## Deployment/Debugging Actions If Relevant

If a local database is available, run the migration, perform one status update
through the API, and query `work_request_status_events` to confirm the stored
history. If no local database is available, rely on the fast test suite and
document that the migration remains the integration check.
