# Test Matrix and Edge Cases

## Phase

Phase 1. This exercise belongs in the first synchronous service phase because
the learner should practice designing useful checks for one API and one
database before adding workers, containers, or distributed failure modes.

## Concepts

- Test matrix design
- Unit tests, API tests, migration checks, and manual operational checks
- Boundary values for pagination
- Conflict, not-found, validation, and invalid-state failures
- LLMs as test reviewers instead of answer generators

## Prerequisites

- Complete `exercises/phase-1/01-basic-crud.md`.
- Complete `exercises/phase-1/02-transactions-and-history.md`.
- Read `docs/TESTING_STRATEGY.md`.
- Inspect `services/api/tests/conftest.py`.
- Inspect the tests under `services/api/tests/`.
- Inspect `services/api/opledger_api/routes.py`.
- Run `./scripts/verify.sh` before changing tests.

## Build/Change Task

Design a test matrix for the current Phase 1 OpsLedger API before asking an LLM
for additional cases. Your matrix should name the behavior, test layer,
expected result, and why the case matters.

Cover at least:

- customer creation and duplicate email conflict
- work request creation for an existing customer and a missing customer
- work request status filtering
- pagination lower and upper bounds for list endpoints
- status update transaction behavior and status history
- missing work request status updates
- liveness behavior without database access
- readiness behavior when the database is available and unavailable
- one manual migration or operational check when a local database is available

After writing your own matrix, ask an LLM to review it for missing edge cases.
Add only cases you understand and can connect to implemented API behavior.

## Constraints

- Keep tests fast enough to run frequently through `./scripts/verify.sh`.
- Do not add Redis, queues, Docker Compose, k3s, or external services.
- Do not add property-based testing unless you can name a small invariant that
  is clearer than hand-written examples.
- Do not use an LLM to generate the first version of the matrix.
- Keep new tests tied to behavior that exists in Phase 1.

## Failure Modes

- Testing only happy paths.
- Duplicating fixture setup instead of using shared test fixtures.
- Treating Pydantic validation tests as proof that database constraints exist.
- Treating API tests as proof that migrations ran correctly against Postgres.
- Mixing liveness and readiness responsibilities.
- Adding slow or brittle tests that learners stop running.
- Accepting LLM-suggested cases that do not match the implemented API.

## Expected Reasoning

The learner should be able to explain which checks belong in unit-style schema
or model tests, which need API tests, which need migration inspection, and which
remain manual operational checks. The learner should also be able to explain why
the same failure can deserve both an API check and a database constraint.

## Verification

- Run `./scripts/verify.sh`.
- Confirm each new or revised test maps to a row in your matrix.
- Confirm duplicate email returns `409 Conflict`.
- Confirm missing customer work request creation returns a not-found error.
- Confirm status filters return only matching work requests.
- Confirm pagination rejects `limit=0`, `limit=101`, and negative offsets.
- Confirm liveness does not depend on database readiness.
- Confirm readiness reports both available and unavailable database states.

## Reflection Questions

- Which cases prove API behavior, and which cases prove database behavior?
- Where does the current SQLite-backed test database differ from Postgres?
- Why should liveness ignore the database while readiness checks it?
- What makes a test useful enough to keep in a frequent verification gate?
- Which LLM-suggested cases did you reject because they did not fit Phase 1?

## LLM Usage

Write your own test matrix first. Then ask an LLM to review it for missing edge
cases, unclear expected results, or tests placed in the wrong layer. Do not ask
the LLM to replace your matrix or generate tests you cannot explain.

## Path-Specific Extensions

Backend path: add one focused API test for a matrix row that is not already
covered, then explain why it belongs at the API layer.

Operations path: write the manual commands you would run to distinguish a live
service from a ready service.

Architecture path: explain which test layers should appear only after Docker,
deployment, scenarios, queues, or workers exist.

Interview path: practice explaining the difference between validation,
conflict, not-found, and readiness failures.

## Deployment/Debugging Actions If Relevant

If a local database is available, run the migration and inspect the Phase 1
tables and constraints. If no local database is available, record that migration
verification remains a deferred manual integration check and rely on
`./scripts/verify.sh` for local verification.
