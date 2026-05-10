# Phase 3 Capstone: Defend The Reporting Boundary

## Phase

Phase 3: Careful Boundaries. This capstone belongs here because learners have
now practiced modular ownership, versioned contracts, one stateless extraction,
timeouts, compatibility, and partial failure. The final task is to defend
whether the extracted reporting service should stay.

## Concepts

- Modular monolith versus service boundary tradeoffs.
- Backward-compatible contract evolution.
- Durable evidence for partial failure.
- Timeout and invalid response debugging.
- Rollback and fold-back reasoning.
- LLM-assisted senior review after independent analysis.

## Prerequisites

- `lessons/phase-3/README.md`
- `docs/architecture/modular-monolith.md`
- `docs/adr/0001-report-rendering-boundary.md`
- `docs/contracts/report-rendering-v1.md`
- `docs/contracts/compatibility-playbook.md`
- `reviews/checklists/phase-3-service-boundary-review.md`
- `exercises/phase-3/01-modular-monolith-boundaries.md`
- `exercises/phase-3/02-contract-before-network.md`
- `exercises/phase-3/03-extract-reporting-service.md`
- `exercises/phase-3/04-timeouts-and-contracts.md`
- `scenarios/phase-3/reporting-timeout.md`
- `scenarios/phase-3/reporting-bad-response.md`
- `scenarios/phase-3/mixed-version-contract.md`
- The API and reporting service tests under `services/api/tests/` and
  `services/reporting/tests/`

## Build/Change Task

Complete one backward-compatible `report-rendering.v1` contract change. Choose
one small optional request or response addition, update the schema, renderer,
documentation, and tests, and prove old minimum v1 requests and responses still
work.

Run one Phase 3 failure scenario from `scenarios/phase-3/`. Capture the report
job status, result endpoint behavior, worker logs, reporting service logs, and
cleanup steps. The scenario must show a real service-boundary cost such as
timeout, malformed response, incompatible contract response, or mixed-version
drift.

Write a short decision memo, no more than one page, defending whether the
reporting service should stay extracted for OpsLedger right now. The memo must
state:

- Your recommendation: keep extracted, fold back into the monolith, or keep
  only as a learning boundary for now.
- The technical evidence from your contract change and scenario run.
- The costs of the service boundary: timeout behavior, retries, deployment,
  debugging, rollback, and local development friction.
- The benefits, if any, of keeping the boundary.
- What future evidence would change your decision.

After you write the memo, ask an LLM to act as a senior reviewer and critique
your argument. Provide it your memo and evidence. Ask it to identify weak
claims, hidden service costs, missing rollback thinking, contract compatibility
risks, and places where you confuse async work with service extraction. Revise
your memo based on the critique, but keep your own final recommendation.

## Constraints

- Do not add another extracted service.
- Do not add a database to the reporting service.
- Do not move source-of-truth ownership out of the core API and Postgres.
- Do not add k3s, service mesh, tracing, caching, or broad observability stack
  work.
- Do not add broad automatic retries across the reporting boundary.
- Do not let an LLM write the initial memo or decide your recommendation.

## Failure Modes

- Treating extraction as automatically better because it creates a service.
- Calling a contract field optional while old callers cannot ignore it.
- Storing partial or invalid report results after a bad provider response.
- Reporting success to users before `result_json` exists.
- Hiding a timeout or invalid response behind vague failure language.
- Ignoring local Compose, deploy, debug, and rollback cost in the memo.
- Asking an LLM for an answer before collecting evidence and writing your own
  defense.

## Expected Reasoning

After completing the capstone, explain why service extraction has both benefits
and costs in OpsLedger. You should be able to defend the reporting boundary in
terms of ownership, contract stability, timeout behavior, retries, deployment
cost, debugging, and rollback.

You should also be able to argue the opposite side: why the same stateless
renderer may be cheaper and clearer as an in-process module for a small system
without independent scaling, team ownership, or runtime isolation pressure.

## Verification

- Run `./scripts/verify.sh`.
- Run the focused contract/client tests relevant to your change, for example:

```sh
uv run pytest services/api/tests/test_report_rendering_contract.py services/api/tests/test_reporting_client.py services/reporting/tests/test_reporting_service.py
```

- Confirm the old minimum valid render request still validates.
- Confirm your new optional contract field is backward-compatible.
- Run one Phase 3 failure scenario and record the inspected job status, result
  endpoint behavior, logs, and cleanup.
- Confirm the capstone memo includes both technical verification and an
  explanation of whether the extraction should stay.

## Reflection Questions

- What problem did the extracted reporting service solve that the modular
  monolith did not?
- Which costs appeared only after the renderer crossed an HTTP boundary?
- Which Phase 2 problems were solved by async work rather than service
  extraction?
- What would make the service boundary worth keeping in production?
- What would make the in-process renderer the better production choice?
- How did the LLM critique change your memo, and what did you reject?

## LLM Usage

Use an LLM only after you have implemented the contract change, run the
scenario, and written the first decision memo. Ask for a senior-review critique
of your reasoning, not a replacement memo.

Suggested prompt:

```text
Act as a senior backend architect reviewing my Phase 3 OpsLedger boundary
decision. I will provide my memo and evidence. Critique hidden costs, weak
evidence, rollback risk, contract compatibility risk, timeout/retry reasoning,
and any place where I confuse async work with service extraction. Do not rewrite
the memo for me; give actionable critique I can use to revise it.
```

## Path-Specific Extensions

Backend: add one focused test proving a mixed-version additive response still
works or an incompatible response fails clearly.

Operations: write a rollback note for returning the worker to the in-process
renderer by removing `OPLEDGER_REPORT_RENDERING_SERVICE_URL`.

Architecture: compare report rendering with notification extraction and
explain why notification ownership is less safe to split in Phase 3.

Interview: answer "Should this service stay extracted?" twice, once arguing for
keeping it and once arguing for folding it back.

## Deployment/Debugging Actions If Relevant

Run the selected local scenario with Docker Compose if your environment
supports it. If local Docker is unavailable, document the blocker and use
focused tests plus the scenario guide to explain exactly which runtime evidence
you could not collect.
