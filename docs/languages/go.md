# Go

## Problem This Runtime Often Solves

Go fits small operational services, CLIs, network daemons, and
concurrency-heavy components where simple deployment, fast startup, and
predictable resource use matter. It is often a practical choice for one
stateless service or infrastructure-facing tool.

## Strengths

- Produces straightforward static binaries and small container images.
- Strong standard library for HTTP, concurrency, profiling, and operational
  tooling.
- Goroutines and channels can model many concurrent network operations without
  a large framework.
- Compile-time types catch many integration mistakes before runtime.

## Weaknesses

- Less expressive for highly dynamic data shaping than Python.
- Error handling and boilerplate can become repetitive without local
  discipline.
- Framework and ORM choices vary; teams need conventions for migrations,
  validation, testing, and observability.
- Adding Go creates a second build, dependency, lint, test, and deploy surface.

## Runtime And Deployment Implications

A Go service can be built into a single binary and containerized separately
from the Python API. That can simplify runtime dependencies for a narrow
stateless component, but it also means OpsLedger must add Go toolchain setup,
module management, CI checks, image build steps, config documentation, logs,
metrics, and rollback procedures.

## Team Productivity

Go can be productive when the team already knows it or when the component is
small and contract-driven. It is a poor fit if the team cannot debug goroutine
leaks, context cancellation, HTTP timeouts, or dependency updates under
incident pressure.

## Operability

Go gives useful primitives for health checks, context deadlines, pprof, and
low-overhead services. OpsLedger would still need consistent JSON logs,
request or correlation ID propagation, Prometheus-compatible metrics, and
contract tests matching the existing report-rendering behavior.

## OpsLedger Fit

Go might fit an optional rewrite of the stateless reporting service or a future
operator CLI. It is less compelling for the core API because the API owns
transactions, migrations, source-of-truth writes, and most existing tests.

For OpsLedger today, Go is a candidate only behind a stable boundary such as
`report-rendering.v1`, and only when profiling, release ownership, or team
capability makes a second runtime worth operating.

## Interview Explanation Prompts

- Why might Go fit the reporting service better than the API?
- What would OpsLedger have to add to verify Go contract compatibility?
- How would timeouts and correlation IDs work across a Go reporting service?
- What evidence would make the Go rewrite unnecessary?
