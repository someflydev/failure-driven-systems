# Report Rendering Contract v1

## Scope

`report-rendering.v1` is the contract for rendering the work request summary
report from a caller-provided snapshot. It began as an internal module contract
and is now also implemented by the stateless reporting service under
`services/reporting/`. The contract makes the data passed into report rendering
explicit so the API route, background job worker, and extracted renderer share
the same schema deliberately.

Postgres remains the source of truth for customers, work requests, status
events, report jobs, and persisted report results. The renderer receives a
snapshot of facts and returns a derived report. It does not own or mutate
source-of-truth facts.

## Request Schema

The request schema is implemented as
`opledger_api.report_contracts.WorkRequestSummaryRenderRequest`.

Required fields:

- `contract_version`: literal `report-rendering.v1`.
- `report_type`: literal `work_request_summary`.
- `generated_at`: timestamp chosen by the caller for deterministic output.
- `total_work_requests`: non-negative integer.
- `by_status`: counts for every work request status: `open`, `in_progress`,
  `resolved`, and `cancelled`.
- `status_event_count`: non-negative integer.

Optional fields:

- `requested_by`: optional caller identity or operator label. Current rendering
  ignores it, which makes it a backward-compatible input addition.

Validation rules:

- Unknown request fields are ignored. This allows a newer caller to send a
  backward-compatible optional field to an older renderer, but safe additions
  must not change required rendering behavior.
- Status counts must include every known work request status.
- Status count values cannot be negative.
- Status counts must add up to `total_work_requests`.

## Response Schema

The response schema is implemented as
`opledger_api.report_contracts.WorkRequestSummaryReport`.

Required fields:

- `contract_version`: literal `report-rendering.v1`.
- `report_type`: literal `work_request_summary`.
- `generated_at`: timestamp copied from the render request.
- `total_work_requests`: non-negative integer.
- `by_status`: counts for every work request status.
- `status_event_count`: non-negative integer.

Optional fields:

- `warnings`: list of non-fatal rendering warnings. It defaults to an empty
  list so older callers do not need to send or store it.

Validation rules:

- Unknown response fields are ignored by current consumers. This allows a newer
  renderer to return additive metadata to an older worker while required v1
  fields still validate strictly.
- Status count completeness and total consistency match the request rules.

## Compatibility Rules

Backward-compatible changes:

- Add an optional request field with a default or nullable value.
- Add an optional response field with a default.
- Add response metadata that old consumers may ignore without changing the
  meaning of required fields.
- Widen documentation around field meaning without changing field names,
  requiredness, types, or semantics.
- Add renderer behavior that preserves the same output for the same v1 input
  unless a new optional field explicitly changes behavior.

Breaking changes:

- Remove or rename a required field.
- Make an optional field required.
- Change a field type, allowed literal, timestamp format, or status name.
- Allow partial `by_status` maps or negative counts.
- Move source-of-truth ownership for work requests or status events out of
  Postgres as part of rendering.
- Add network calls or persistence writes to the renderer and still claim it is
  the same stateless contract.

## HTTP Boundary

The extracted service implements:

- `GET /health/live`: dependency-free liveness.
- `GET /health/ready`: stateless readiness.
- `POST /reports/work-requests/summary/render`: accepts
  `WorkRequestSummaryRenderRequest` and returns `WorkRequestSummaryReport`.

The service must not connect to the core database. The worker assembles the
snapshot from Postgres, calls the service only when
`OPLEDGER_REPORT_RENDERING_SERVICE_URL` is configured, and uses
`OPLEDGER_REPORT_RENDERING_SERVICE_TIMEOUT_SECONDS` for an explicit bounded
timeout. There are no unbounded retries in the HTTP client.

## Versioning Approach

The `contract_version` field is required even while the boundary is in-process.
If a future change cannot be made backward-compatible, introduce a new contract
version such as `report-rendering.v2` and keep v1 contract tests until all v1
callers and persisted results are retired or migrated.

Versioning this contract does not make the service own report data.
