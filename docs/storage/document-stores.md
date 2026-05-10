# Document Stores

## Problem This Paradigm Solves

Document stores solve flexible aggregate storage when records vary in shape,
are commonly read as whole documents, and do not need many cross-document joins
or relational constraints. They can fit catalogs, event payload archives,
profile blobs, forms, or integration-specific records whose fields change often.

## What OpsLedger Would Gain

OpsLedger might gain easier storage for highly variable customer intake forms,
third-party webhook payloads, or report snapshots where each record is usually
retrieved as one object. A document store could reduce schema churn if the
payload shape changed frequently and did not drive core workflow correctness.

For the current OpsLedger workload, that gain is limited. Customers, work
requests, status history, report jobs, and notification attempts are connected
facts with constraints. Postgres already stores structured records and can hold
bounded JSON payloads when a small flexible field is enough.

## What OpsLedger Would Pay Operationally

OpsLedger would add another database to deploy, secure, back up, monitor,
upgrade, and debug. The team would also need to define which facts live in
Postgres and which live in the document store, then handle duplication,
consistency, migration, and repair across both.

If documents become authoritative for workflow state, OpsLedger loses some of
the relational guarantees the curriculum intentionally teaches.

## Failure Modes

- Split-brain facts: customer or work request state diverges between Postgres
  and the document store.
- Weak uniqueness or relationship enforcement: duplicate customer identities
  or orphaned work records become easier to create.
- Query drift: flexible documents accumulate inconsistent field names and
  shapes that make reporting unreliable.
- Migration blind spots: old documents keep stale structures that new code does
  not handle.
- Backup mismatch: restoring one database without the other corrupts the
  business timeline.

## Interview Explanation Prompts

- Which OpsLedger data, if any, is document-shaped rather than relational?
- Why is "flexible schema" not automatically a win for work request state?
- How would you prevent Postgres and a document store from disagreeing?
- Could Postgres JSONB solve the narrow need without adding a new datastore?
- What operational evidence would justify this extra database?
