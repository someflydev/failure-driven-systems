# Debug Timeouts and Contract Drift

## Phase

Phase 3. This work belongs here because the report renderer now crosses a real
service boundary where slow responses, non-2xx responses, and mixed contract
versions are normal operational risks.

## Concepts

- Partial failure across HTTP boundaries
- Bounded timeouts
- Invalid response handling
- Backward-compatible contract changes
- Durable async job evidence
- User-visible impact of failed background work

## Prerequisites

- `exercises/phase-3/03-extract-reporting-service.md`
- `docs/contracts/report-rendering-v1.md`
- `docs/contracts/compatibility-playbook.md`
- `scenarios/phase-3/reporting-timeout.md`
- `scenarios/phase-3/reporting-bad-response.md`
- `services/api/opledger_api/reporting_client.py`
- `services/api/opledger_api/report_jobs.py`
- `services/reporting/reporting_service/main.py`
- Docker Compose and the repo-root `uv` workflow

## Build/Change Task

Run the timeout scenario for the extracted reporting service. Enqueue a report,
inspect the report job status, inspect worker and reporting service logs, and
write down the user-visible impact before changing any implementation.

Then review the client and contract tests. Ensure timeout, non-2xx response,
malformed JSON, and incompatible contract responses are distinguishable enough
for debugging. Confirm at least one additive v1 field remains
backward-compatible.

## Constraints

- Do not add broad automatic retries across the reporting boundary.
- Do not add a circuit breaker library yet.
- Do not add tracing yet.
- Do not add another service.
- Keep Postgres as the source of truth for report job state.
- Keep reporting service failure injection disabled by default and local/test
  only.

## Failure Modes

- Treating a timeout, a 500, and invalid JSON as the same failure.
- Storing a partial or incompatible report result.
- Reporting success to the user before `result_json` exists.
- Making a contract addition that old consumers cannot ignore.
- Fixing the provider without first observing consumer-visible evidence.
- Enabling failure injection in production-like settings.

## Expected Reasoning

After completing this exercise, you should be able to explain what changed when
report rendering moved from a function call to an HTTP call. Name which service
was slow or wrong, which timeout bounded the wait, what durable evidence the
worker stored, and what a user can honestly be told while the report is not
available.

You should also be able to classify contract changes as safe additions,
breaking changes, or changes that need a new version.

## Verification

- Run `./scripts/verify.sh`.
- Run `scenarios/phase-3/reporting-timeout.md`.
- Inspect `GET /reports/jobs/{id}` after the timeout.
- Inspect worker logs and reporting service logs.
- Confirm `GET /reports/jobs/{id}/result` does not return report output for a
  failed or unfinished job.
- Run the focused compatibility tests:

```sh
uv run pytest services/api/tests/test_report_rendering_contract.py services/api/tests/test_reporting_client.py
```

## Reflection Questions

- What did the API promise when it accepted the report job?
- What should the caller see while the report is not ready?
- How can an operator tell timeout apart from an invalid response?
- Which additive field is safe for v1 consumers, and why?
- Which contract change would force a v2?
- Why are retries not automatically safe just because the work is a report?

## LLM Usage

Use an LLM as a debugging interviewer after you have captured the timeout
evidence. Ask it to challenge whether your explanation distinguishes timeout,
non-2xx, malformed JSON, and incompatible contract responses. Do not ask it to
invent the observations you should collect from logs and job status.

## Path-Specific Extensions

Backend: add one focused test for an incompatible response that is valid JSON
but not valid `report-rendering.v1`.

Operations: write a short incident note with the report job id, timeout
configuration, worker log evidence, and user impact.

Architecture: propose when a circuit breaker would become useful and what
evidence would justify adding it later.

Interview: explain why contract compatibility is a deployment concern, not
only a schema concern.

## Deployment/Debugging Actions If Relevant

Start the Compose stack with reporting service failure injection enabled only
for the scenario. After the drill, stop the stack and restart it without the
failure injection variables so normal local development is healthy again.
