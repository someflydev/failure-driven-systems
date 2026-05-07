# Phase 1 Quiz

Answer in short paragraphs or bullets. A strong answer should name the system
behavior, the evidence you would check, and the tradeoff behind the choice.

## HTTP And API Basics

1. What is the difference between `POST /customers`, `GET /customers/{id}`,
   `GET /customers`, and `PATCH /work-requests/{id}/status` in terms of intent
   and expected side effects?
2. Why should duplicate customer email return `409 Conflict` instead of a
   request validation error?
3. What should a consistent API error response help a caller or operator do?
4. Why do list endpoints need lower and upper bounds on `limit`?
5. What is the difference between a missing customer id and an invalid customer
   id shape in an HTTP request?

## Relational Modeling

1. Where does the authoritative current work request status live, and where
   does the status change history live?
2. Why does `work_requests.customer_id` need a foreign key even if the route
   checks that the customer exists?
3. What does the unique constraint on customer email protect against?
4. Why should work request statuses be constrained in the database as well as
   in request schemas?
5. What question would you ask before adding a new column to `work_requests`?

## Transactions And Migrations

1. Why should a status update and its status event insert commit together?
2. Describe one inconsistent state that could happen if status update and
   history insert used separate commits.
3. What does an Alembic migration prove that a route test does not prove?
4. Why are migrations explicit in the local and Dokku workflows?
5. What evidence would you collect before deciding whether a failed deploy is a
   code problem, migration problem, or configuration problem?

## Health Checks And Logs

1. Why should `GET /health/live` avoid checking Postgres?
2. What does `GET /health/ready` prove that liveness does not?
3. When readiness fails, which database target fields are useful to log, and
   which secret fields must not appear?
4. What log fields make a basic request useful during a Phase 1 incident?
5. Why is a broad exception handler a weak first response to database failure?

## Deployment And Operations

1. What does Dokku provide in the Phase 1 deployment path?
2. Why is linking Dokku Postgres safer than copying full database URLs into
   notes or docs?
3. What should be recorded as sanitized deployment evidence?
4. If `/health/live` returns `200` but `/health/ready` returns `503` after a
   deploy, what checks come before code changes?
5. What rollback risk appears when a deploy includes both application code and
   a schema migration?

## DB Failure And Scope Control

1. In the database unavailable scenario, what evidence proves the API process
   is still running?
2. What evidence proves Postgres is the failed dependency?
3. Why is adding a queue not the first fix for Phase 1 database unavailability?
4. Why is Redis not part of the Phase 1 default design?
5. Why should caching wait until a later measured read pressure or product need?
