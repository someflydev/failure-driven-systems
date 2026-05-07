# Basic CRUD for Customers and Work Requests

## Phase

Phase 1. This exercise belongs in the first synchronous service phase because
the learner should experience direct request-response CRUD backed by Postgres
before queues, caching, workers, or service extraction appear.

## Concepts

- FastAPI route design
- Pydantic request and response schemas
- SQLAlchemy model persistence
- Primary keys, foreign keys, unique constraints, and check constraints
- Predictable API error responses
- Limit/offset pagination
- Focused API tests

## Prerequisites

- Read `docs/DOMAIN.md`.
- Read `docs/data-models/phase-1.md`.
- Inspect `services/api/opledger_api/models.py`.
- Inspect `services/api/opledger_api/schemas.py`.
- Inspect the Alembic migration under `services/api/migrations/versions/`.
- Run the existing test suite before changing behavior.

## Build/Change Task

Add the first CRUD API surface for OpsLedger customers and work requests:

- create a customer
- fetch one customer by id
- list customers with `limit` and `offset`
- create a work request for an existing customer
- fetch one work request by id
- list work requests with optional `status`, `limit`, and `offset`
- update a work request's current status

The API should return typed response bodies and clear error payloads for missing
records, duplicate customer email, validation failures, and invalid status
transitions when terminal status rules are present.

## Constraints

- Keep Postgres as the only durable source of truth.
- Do not add Redis.
- Do not add background jobs.
- Do not add caching.
- Do not extract another service.
- Do not add authentication yet.
- Do not add blanket exception handling that hides meaningful database errors.
- Keep route, schema, and helper layers small enough for a new learner to trace
  in one sitting.

## Failure Modes

- Creating orphaned work requests for missing customers.
- Returning raw database exceptions or inconsistent error shapes.
- Treating API validation as a replacement for database constraints.
- Allowing duplicate customer emails.
- Accepting invented work request statuses.
- Letting a resolved or cancelled work request move back to active work if the
  implementation has terminal status rules.
- Adding infrastructure before there is a demonstrated need.

## Expected Reasoning

The learner should be able to explain why this phase keeps the API synchronous,
why the database still owns durable constraints, why duplicate email is a
conflict rather than a validation error, and why a small helper can be useful
without turning the project into a layered architecture exercise.

## Verification

- Run `./scripts/verify.sh`.
- Confirm customer create, fetch, and list paths return successful responses.
- Confirm work request create, fetch, filtered list, and status update paths
  return successful responses.
- Confirm duplicate email returns a predictable conflict response.
- Confirm missing customer and missing work request reads return predictable
  not-found responses.
- Confirm invalid request bodies return validation failures.
- If a local database is available, run migrations and exercise the CRUD routes
  manually with curl or an HTTP client.

## Reflection Questions

- Which failures are caught by Pydantic before the database is touched?
- Which failures must still be protected by database constraints?
- Why is duplicate email a `409 Conflict` instead of a `422 Unprocessable
  Entity`?
- What would become harder to understand if this CRUD feature were split into
  repositories, services, events, and workers today?
- What evidence would justify adding caching or a derived read model later?

## LLM Usage

Use an LLM to review route behavior, ask for missing edge cases, or interview
you about why each error response has its status code. Do not ask the LLM to
generate the finished implementation until you have written your own version
and can explain the tradeoffs.

## Path-Specific Extensions

Backend path: add a focused test for each database-backed failure case and
explain which failures are enforced twice by API validation and database
constraints.

Operations path: capture manual curl commands and the response bodies for one
successful path and one failure path.

Architecture path: write a short note defending why this is still one service
and one database.

Interview path: practice explaining the difference between validation errors,
not-found errors, conflicts, and invalid state transitions.

## Deployment/Debugging Actions If Relevant

If a local database is available, run the migration and test the API against the
real database. Otherwise, rely on the fast test suite and document that manual
database CRUD remains an integration check.
