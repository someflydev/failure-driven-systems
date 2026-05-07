# Phase 1 Data Model

Phase 1 introduces the first durable OpsLedger relational model: customers and
work requests. Postgres is the source of truth for these records. Application
schemas validate request and response shapes, but the database owns the
constraints that protect persisted data.

## Tables

### customers

`customers` stores the account or contact that work belongs to.

| Column | Purpose |
| --- | --- |
| `id` | Surrogate primary key used by related tables. |
| `name` | Human-readable customer name. |
| `email` | Contact email, unique across customers. |
| `created_at` | Database timestamp for record creation. |
| `updated_at` | Database timestamp for the latest row update. |

### work_requests

`work_requests` stores the operational work item tracked by the team.

| Column | Purpose |
| --- | --- |
| `id` | Surrogate primary key for the work request. |
| `customer_id` | Required foreign key to `customers.id`. |
| `title` | Short summary used in lists and operator views. |
| `description` | Required details for the requested work. |
| `status` | Current lifecycle state. |
| `created_at` | Database timestamp for record creation. |
| `updated_at` | Database timestamp for the latest row update. |

Allowed work request statuses are `open`, `in_progress`, `resolved`, and
`cancelled`.

## Relational Choices

Customer data is normalized into its own table because multiple work requests
can belong to the same customer. A work request stores `customer_id` instead of
duplicating customer name or email, which keeps customer identity in one place.

The work request keeps only its current status in Phase 1. Status event history
is deliberately not modeled yet; it is introduced later as the transaction
lesson. This keeps the first model focused on primary keys, foreign keys,
uniqueness, and check constraints before adding history tables.

## Deliberately Not Modeled Yet

The model does not include status events, operator notes, generated reports,
notification attempts, derived dashboard tables, queues, or caches. Those
concepts appear only after prompts create the failure pressure that justifies
them.

The model also avoids denormalized read tables. Reads should query the source
tables until measurement proves that a derived model is needed and a rebuild
path is defined.

## Failures Prevented By Constraints

The unique customer email constraint prevents two customer rows from claiming
the same contact address.

The work request foreign key prevents orphaned work that points at a missing
customer.

The work request status check prevents misspelled or invented lifecycle states
from becoming durable truth. API validation should catch bad input early, but
Postgres still rejects invalid persisted state if application code has a bug.
