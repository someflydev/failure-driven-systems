# OpsLedger Domain

OpsLedger is the single evolving system domain for Failure-Driven Systems. It
is a small internal operations workflow platform used to track customer work
requests, status changes, operational notes, generated reports, and later
notifications.

The domain is intentionally ordinary. It gives learners enough real workflow
pressure to encounter backend, data, operational, and architecture tradeoffs
without requiring specialized business knowledge.

## Purpose

OpsLedger exists to teach engineering judgment through one system that changes
over time. Early lessons begin with a simple synchronous service backed by
Postgres. Later lessons add background work, clearer internal boundaries,
operational evidence, performance work, and architecture defense only after the
learner has experienced the failure or friction that motivates each step.

## Boundaries

OpsLedger includes:

- Customer records needed to associate work with a real account or contact.
- Work requests that represent operational tasks the team must track.
- Status events that record how a work request moves through its lifecycle.
- Operator notes that capture human context during handling.
- Reports generated from operational data.
- Notification attempts for later delivery of status changes or report
  availability.
- Derived read models for dashboards, summaries, and query-heavy views once
  measurement justifies them.

OpsLedger avoids:

- General-purpose project management.
- Full customer relationship management.
- Billing, payments, shopping carts, and ecommerce order flows.
- Deep operations-industry modeling.
- Early microservice design, event-driven design, or Kubernetes-centered
  architecture.
- Artificial domain complexity that distracts from backend and systems
  tradeoffs.

## Conceptual Entities

These entities are conceptual teaching anchors, not implementation schemas.
They should not be treated as table definitions, API resources, or service
boundaries until later prompts create that need.

| Entity | Role in the domain | First phase where it matters |
| --- | --- | --- |
| Customers | Identify the organization or person associated with work. | Phase 1 |
| Work requests | The central unit of operational work being created, viewed, updated, and completed. | Phase 1 |
| Status events | A durable history of meaningful state changes on a work request. | Phase 1 |
| Operator notes | Human-authored context attached while handling work. | Phase 1 |
| Reports | Generated summaries or exports based on operational data. | Phase 2 |
| Notification attempts | Records of attempts to notify people about status changes or report readiness. | Phase 2 |
| Derived read models | Rebuilt or refreshed views optimized for dashboards, summaries, or expensive reads. | Phase 5 |

## Phase Fit

In Phase 1, OpsLedger is one synchronous service. Learners handle customers,
work requests, status events, and notes through direct request/response flows
and a clear Postgres source of truth.

In Phase 2, report generation and notification attempts create pressure that
does not fit well inside user-facing requests. Learners experience latency,
retry hazards, and partial failure before introducing background work.

In Phase 3, the same system is reorganized around explicit internal boundaries:
request intake, workflow state, reporting, and notification concerns. These are
module boundaries first, not separate services by default.

In Phase 4, OpsLedger becomes an operational system. Learners investigate bad
deploys, confusing logs, stuck work, failed notifications, and incomplete
reports using evidence from the running service and database.

In Phase 5, dashboards and reporting queries create measured read pressure.
Learners introduce indexes, pagination, caching, and derived read models only
after proving the bottleneck and naming the source of truth.

In Phase 6, OpsLedger becomes the concrete project history learners use to
defend architecture decisions, compare alternatives, and answer system design
questions without relying on memorized diagrams.
