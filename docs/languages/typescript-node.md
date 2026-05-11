# TypeScript And Node.js

## Problem This Runtime Often Solves

TypeScript with Node.js fits teams that want one language across frontend,
backend, and tooling, or systems centered on I/O-heavy HTTP, WebSocket, and
event-driven product surfaces. TypeScript adds static checking to JavaScript's
large ecosystem.

## Strengths

- Product teams can share language knowledge between UI, API clients, scripts,
  and services.
- Node handles many concurrent I/O-bound requests with an event loop model.
- TypeScript, schema validators, and generated API clients can create useful
  contract discipline.
- The ecosystem is broad for HTTP APIs, integration clients, build tools, and
  developer automation.

## Weaknesses

- Dependency volume and supply-chain churn can be high.
- Runtime behavior still depends on JavaScript semantics and careful async
  error handling.
- CPU-heavy report rendering can block the event loop unless moved to workers
  or another process.
- Multiple package managers and build configurations can create tool drift.

## Runtime And Deployment Implications

Adding Node means adding `package.json`, lockfiles, TypeScript compilation,
linting, test tooling, and a separate container or process. A Node service also
needs explicit startup, health, logging, metrics, timeout, and graceful
shutdown behavior.

OpsLedger would gain little by moving the source-of-truth API to Node unless
the team or product surface strongly depends on TypeScript. A stateless
contract-compatible renderer is a safer experiment.

## Team Productivity

TypeScript can improve productivity for full-stack teams and API-client-heavy
workflows. It can slow a small backend-only curriculum if learners now have to
reason about Python and Node packaging, testing, and runtime behavior at the
same time.

## Operability

Node services need event-loop health awareness, bounded request timeouts,
structured logging, dependency update discipline, and memory monitoring.
OpsLedger would also need contract tests proving the TypeScript implementation
matches `docs/contracts/report-rendering-v1.md`.

## OpsLedger Fit

TypeScript might fit an optional report-rendering exercise if the learner wants
to practice a contract-compatible rewrite or if a future UI-heavy team wants
shared schema tooling. It does not currently fit the main API path better than
Python because the system's central work is durable backend coordination, not
shared frontend/backend product iteration.

## Interview Explanation Prompts

- When would TypeScript be a team-productivity choice rather than a
  performance choice?
- What Node failure modes matter for report rendering?
- Why is the stateless renderer a safer TypeScript candidate than the API?
- How would you prevent package and contract drift?
