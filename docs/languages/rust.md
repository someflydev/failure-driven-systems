# Rust

## Problem This Runtime Often Solves

Rust fits performance-sensitive, memory-sensitive, security-sensitive, or
systems-level components where predictable resource use and compile-time safety
justify a steeper learning curve. It can be excellent for narrow libraries,
CLIs, parsers, and services with strict efficiency requirements.

## Strengths

- Strong compile-time guarantees around ownership, memory safety, and data
  races.
- Predictable performance without a garbage collector.
- Good fit for CPU-heavy or resource-constrained components after profiling
  proves the need.
- Produces deployable binaries and has strong tooling through Cargo.

## Weaknesses

- Higher learning curve and slower iteration for teams without Rust fluency.
- Web-service ecosystem choices require deliberate conventions.
- Compile-time safety does not remove distributed-system risks such as stale
  data, bad contracts, retries, or timeouts.
- A Rust component adds another toolchain and review discipline.

## Runtime And Deployment Implications

A Rust service can ship as a small binary in a container, but OpsLedger would
need Cargo setup, dependency review, linting, tests, contract tests,
observability libraries, image builds, and rollback guidance. Build times and
cross-compilation may also become part of the workflow.

## Team Productivity

Rust can pay off when correctness and efficiency matter enough for the team to
invest in the language. It can be a poor fit for learner-facing application
code where the main lesson is source-of-truth ownership, transactions,
timeouts, and architecture defense.

## Operability

Rust services still need the same operational surfaces as any service:
readiness, logs, metrics, config, request deadlines, graceful shutdown, and
contract compatibility. Memory safety does not make report job state durable or
Redis authoritative.

## OpsLedger Fit

Rust might fit a future CPU-heavy report transformation library or a small
high-performance utility after profiling shows Python rendering is the real
bottleneck. It is not a current fit for the core API or worker because their
main risks are database correctness, operational visibility, and workflow
semantics rather than memory safety.

## Interview Explanation Prompts

- What measured OpsLedger problem would make Rust worth considering?
- Why is Rust not a substitute for contract tests or timeout handling?
- Which component is narrow enough for a Rust experiment?
- What would a small team lose in review speed and incident debugging?
