# Phase 1 Data Model

Phase 1 introduces the first durable OpsLedger relational model: customers,
work requests, and local status history. Postgres is the source of truth for
these records. Application schemas validate request and response shapes, but the
database owns the constraints that protect persisted data.

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

### work_request_status_events

`work_request_status_events` stores the local history of status changes for a
work request.

| Column | Purpose |
| --- | --- |
| `id` | Surrogate primary key for the status event. |
| `work_request_id` | Required foreign key to `work_requests.id`. |
| `old_status` | Status before the API accepted the change. |
| `new_status` | Status after the API accepted the change. |
| `reason` | Human-readable reason recorded by the status update request. |
| `created_at` | Database timestamp for when the status event was recorded. |

## Relational Choices

Customer data is normalized into its own table because multiple work requests
can belong to the same customer. A work request stores `customer_id` instead of
duplicating customer name or email, which keeps customer identity in one place.

The work request row stores the current status because that is the authoritative
fact for the current lifecycle state. The status event row stores the history of
one accepted status change because that is the authoritative fact for explaining
what happened. This is the phase 1 version of one owner per authoritative fact:
do not make callers infer history from the current row, and do not make callers
infer the current status from the history table.

The status update API changes `work_requests.status` and inserts a
`work_request_status_events` row in one database transaction. If either write
fails, neither fact should be committed. That transaction boundary matters
because the system would otherwise be able to say that a request is
`in_progress` while having no durable explanation for how it got there, or it
could record a status event for a status change that did not actually happen.

## Deliberately Not Modeled Yet

The model does not include operator notes, generated reports, notification
attempts, derived dashboard tables, queues, or caches. Those concepts appear
only after prompts create the failure pressure that justifies them.

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

The status event foreign key prevents orphaned history that points at a missing
work request.

The old and new status checks prevent status history from accepting lifecycle
states that the current work request row would reject.
