# OpsLedger System Evolution

OpsLedger evolves in response to observed pressure. The system starts small,
adds moving parts only after failure makes them useful, and keeps Postgres as
the clear source of truth unless a later lesson deliberately introduces derived
state.

## Stage 1: One Synchronous Service

OpsLedger begins as one deployable service on a small Linux VPS, deployed with
Dokku and backed by Postgres. It handles customers, work requests, status
events, and operator notes directly in request/response flows.

The teaching goal is ownership of the simplest real system shape: validation,
transactions, migrations, logging, configuration, deploys, and rollback
thinking. Learners should be able to inspect data, explain a write path, and
reason about the consequences of a failed request.

This stage avoids queues, caches, orchestration, and service splits.

## Stage 2: Worker-Backed System

Report generation and notification attempts eventually make synchronous
requests painful. Some work is slow, some work involves side effects, and some
work must be retried without duplicating user-visible outcomes.

OpsLedger then adds background processing in the smallest form that addresses
the observed failure. The learner must understand the original synchronous pain
before applying terms such as retry, idempotency, dead-letter handling, or
backpressure.

Postgres remains the source of truth. Background work must be inspectable,
repairable, and explainable.

## Stage 3: One Carefully Extracted Boundary

Before any service extraction, OpsLedger is organized into clearer internal
modules: request intake, workflow state, reporting, and notifications. The
default remains one deployable service because separate deployment adds real
operational cost.

If a later failure justifies extraction, only one boundary is considered
carefully. A defensible candidate is the notification boundary, because it has
external side effects, retry behavior, and operational concerns that may differ
from core workflow writes. Extraction is not assumed. The learner must compare
the cost of a split with the cost of improving the modular monolith.

The point is to practice boundary reasoning, not to accumulate services.

## Stage 4: Observable And Performance-Aware Operation

OpsLedger becomes a system the learner can operate under pressure. Logs,
metrics, alerts, runbooks, incident reviews, and rollback decisions are tied to
real failures in requests, workers, reports, notifications, and deploys.

Performance work also arrives from evidence. Slow dashboards, expensive report
queries, or high-read work request views may justify indexes, pagination
changes, materialized views, caching, Redis, or other derived read models. Each
derived view must identify the source of truth, rebuild strategy, staleness
risk, and correction path.

This stage prepares learners to defend architecture choices with evidence from
the system they have actually built and operated.
