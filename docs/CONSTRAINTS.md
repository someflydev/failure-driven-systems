# Constraints

Failure-Driven Systems is designed around a constrained, self-operated practice
environment. The constraints are part of the teaching method because they make
cost, complexity, reliability, and operational ownership visible.

## Target Environment

The default practice target is:

- One Linux VPS.
- 4 GB RAM.
- 3 vCPUs.
- Dokku installed for early deployments.
- Docker available.
- k3s available later, after orchestration pressure is part of the lesson.
- Modest budget.

The platform should avoid assumptions that require managed cloud services,
large clusters, paid observability stacks, or unlimited horizontal scaling.

## Deployment Assumptions

Dokku is the first deployment path. It is sufficient for learning release
discipline, environment configuration, logs, process management, database
attachment, migrations, rollback planning, and small-system operations.

k3s is a later teaching tool. It should appear only when learners have already
experienced enough deployment and operational friction to understand why a small
Kubernetes distribution might help and what complexity it introduces.

## Data Assumptions

Postgres is the source of truth unless a later prompt explicitly changes that
decision. Lessons should make durable state, transactions, constraints,
migrations, and ownership boundaries visible.

Redis is a later dependency, not an early default. It should be introduced only
after measured or observed failure makes its role defensible.

## Cloud Assumptions

The baseline curriculum assumes no managed cloud platform. That means no
managed databases, hosted queues, managed Kubernetes, proprietary deployment
platforms, or paid observability products are required for the core path.

External services may be discussed as comparisons during architecture review,
but exercises should remain runnable in the constrained VPS model until a later
prompt explicitly expands the environment.

## Design Consequences

These constraints push the platform toward:

- Simplicity before scale.
- Operational clarity before automation layers.
- Postgres-backed correctness before derived-state optimization.
- Measured need before caching.
- Modular monolith structure before service extraction.
- Explicit tradeoffs before architecture labels.
