# Doctrine

Failure-Driven Systems teaches judgment by making learners encounter pressure
before giving them vocabulary, tools, or abstractions. The goal is not to finish
checklists of technologies. The goal is to build the habit of making small,
defensible decisions under realistic constraints.

## Failure Before Abstraction

A learner should feel a problem before receiving the abstraction that solves it.
Abstractions introduced too early become labels without judgment. A queue is not
introduced because queues are common. It is introduced after synchronous work
creates latency, retries, user-visible delay, or operational coupling that the
learner can observe and explain.

Each major concept should follow this sequence:

1. Experience the system directly.
2. Encounter failure or friction.
3. Name the problem precisely.
4. Identify the pattern that addresses it.
5. Apply the pattern in a small way.
6. Vary the scenario and observe what changes.
7. Explain and defend the decision under questioning.

## Friction Before Naming

Terminology should arrive after the learner can point to the pain. Terms like
idempotency, backpressure, fanout, read model, source of truth, consistency
boundary, and blast radius should be attached to concrete failures.

This prevents shallow vocabulary. A learner should be able to say what broke,
why the current design made it likely, what changed, what tradeoff was accepted,
and what would make the decision wrong later.

## Simple Deployment First

The first deployment target is one Linux VPS. Dokku comes before k3s because
the early goal is to learn ownership, release shape, logs, configuration,
migrations, rollback thinking, and operational limits without prematurely
adding cluster complexity.

k3s is reserved for later lessons where orchestration itself becomes part of
the failure being studied. The platform should not introduce Kubernetes language
or manifests before learners have enough deployment and operational experience
to recognize the problems orchestration is meant to address.

## Source-of-Truth Clarity

Postgres is the default source of truth. Early systems should make writes,
transactions, constraints, migrations, and data ownership explicit. If data is
derived, cached, denormalized, indexed elsewhere, or delivered asynchronously,
the docs and exercises must explain where truth lives and how derived state is
rebuilt or corrected.

Redis is not a default dependency. It appears only when a later failure creates
a concrete need such as measured hot reads, coordination pressure, ephemeral
state, or queue-like behavior that Postgres should no longer carry alone.

## Operational Judgment

Operational work is part of the curriculum, not an appendix. Learners should
practice reading logs, inspecting database state, running migrations, recovering
from bad deploys, handling partial failure, and explaining incident timelines.

The platform should teach questions such as:

- What is the smallest change that reduces the failure?
- What state is durable, derived, or disposable?
- What can be retried safely?
- What would alert a human before users report the issue?
- What evidence supports the architecture decision?
- What failure would force this design to evolve?

## LLM Boundaries

LLMs may be used as reviewers, interviewers, critics, and scenario generators.
They should challenge reasoning, ask follow-up questions, find weak assumptions,
and help learners practice explanations.

LLMs should not be used as ghostwriters for the learner's understanding. A
learner who cannot explain, modify, debug, or defend generated work has not
completed the lesson. The platform should prefer prompts that force the learner
to reason from observed system behavior.

## Constrained VPS Philosophy

The target environment is intentionally modest: one Linux VPS with 4 GB RAM,
3 vCPUs, Dokku installed, Docker available, and k3s available later. This
constraint keeps tradeoffs visible. Memory, CPU, disk, network, deploy shape,
and operational complexity all matter.

The platform should use the constraint to teach good defaults:

- Start with one service when one service is enough.
- Use a modular monolith before service sprawl.
- Prefer boring, observable components.
- Add infrastructure only when a failure justifies it.
- Treat cost and operational burden as design inputs.
- Make every new moving part earn its place.
