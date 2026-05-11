# Polyglot Systems

## Core Principle

A polyglot OpsLedger system is justified by constraints and team capability,
not novelty. Multiple languages can be reasonable when components have clearly
different workloads, ownership, scaling needs, or ecosystem requirements. They
are harmful when they hide weak architecture behind technology variety.

## What Polyglot Can Improve

- A stateless renderer can use a runtime better suited to its measured CPU,
  memory, or deployment profile.
- A CLI can use a language that produces a simple operator binary.
- A realtime component can use a runtime built around long-lived connections
  and supervision.
- A team with established language boundaries can let specialists own narrow
  services.

## What OpsLedger Pays

- More toolchains, dependency update paths, lockfiles, and build steps.
- More test runners and contract-test requirements.
- More container images, health endpoints, config docs, logs, metrics, and
  rollback procedures.
- More incident-debugging knowledge required from a small operator.
- More chances for duplicated models, drifted validation, and incompatible
  behavior across service boundaries.

## Boundary Requirements

Do not add another runtime unless the component is behind a stable contract or
has a very small operational surface. For OpsLedger, the best current candidate
is the stateless reporting service because `docs/contracts/report-rendering-v1.md`
already defines its input, output, compatibility expectations, and source-free
ownership model.

The API and worker are poor first polyglot candidates because they own durable
mutations, report job state, retries, notification attempts, migrations, and
most user-visible behavior.

## Failure Modes

- The second language implementation passes happy-path tests but violates the
  report contract on edge cases.
- Logs, metrics, or correlation IDs drift across runtimes and break incident
  investigation.
- Timeout behavior changes and causes report jobs to hang or fail differently.
- Build or dependency updates succeed for one runtime and break the other.
- The team cannot debug the second runtime during an outage.
- A stateless rewrite accidentally starts owning source-of-truth data.

## OpsLedger Decision Rule

Keep the main codebase Python/FastAPI. Consider a polyglot extension only when
all of these are true:

1. The component is narrow and contract-compatible.
2. The current implementation has measured pressure or a strong team/ecosystem
   reason to change.
3. The learner can explain deployment, logs, metrics, testing, and rollback.
4. The new runtime does not own Postgres facts unless a separate ADR justifies
   that migration.
5. The change can be removed without corrupting durable state.

## Interview Explanation Prompts

- What is the difference between a justified polyglot system and a showcase?
- Why is report rendering the safest OpsLedger polyglot exercise?
- Which operational checks must be identical across runtimes?
- What evidence would make the team fold a polyglot service back into Python?
