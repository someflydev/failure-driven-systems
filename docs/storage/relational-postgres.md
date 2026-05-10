# Relational Postgres

## Problem This Paradigm Solves

Relational databases solve durable fact ownership where records have identity,
relationships, constraints, transactions, migrations, and inspection needs. For
OpsLedger, this matches customers, work requests, status events, report jobs,
notification attempts, and the dashboard read model.

## What OpsLedger Gains

OpsLedger gains one authoritative place for facts. Postgres can enforce unique
customer emails, work request foreign keys, allowed status values, report job
identity, and transactional updates such as changing current status while
recording status history.

It also gives learners practical surfaces for migrations, readiness checks,
query inspection, indexes, read-model rebuilds, and incident debugging. A small
operator can inspect the database directly instead of reconciling truth across
several systems.

## What OpsLedger Pays Operationally

Postgres is a hard dependency for durable API behavior. OpsLedger must run
migrations carefully, manage connection strings, watch readiness, avoid
connection exhaustion, understand query plans, and treat rollback as a data
decision.

Postgres also makes schema design visible. Bad constraints, missing indexes,
unsafe migrations, or unbounded queries can hurt the whole system.

## Failure Modes

- Postgres unavailable: readiness fails and durable reads or writes stop.
- Bad migration: deployed code and schema disagree.
- Weak constraints: invalid or duplicate facts become durable.
- Slow query: API latency rises until query shape, index, pagination, or a read
  model is justified by evidence.
- Overloaded connection pool: healthy code can still fail under too many
  concurrent database users.

## Interview Explanation Prompts

- Why is Postgres the source of truth for OpsLedger?
- Which OpsLedger facts need relational constraints rather than flexible
  documents?
- What does Redis currently do that Postgres deliberately does not own?
- When would a read model be enough instead of another datastore?
- What evidence would make you revisit the Postgres-first decision?
