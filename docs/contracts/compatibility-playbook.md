# Contract Compatibility Playbook

Service boundaries make mixed versions normal. During a deploy, the OpsLedger
worker may call an older or newer reporting service than the one it was tested
with locally. The `report-rendering.v1` contract exists so both sides can tell
the difference between safe drift and a broken contract.

## Backward-Compatible Changes

A change is backward-compatible when old consumers and new consumers can both
keep using the contract without coordinated deployment.

Safe examples:

- Add optional request metadata such as `requested_by` that the renderer may
  ignore.
- Add optional response metadata such as `renderer_build` that old consumers
  can ignore.
- Add a response field with a default value, such as the existing `warnings`
  list.
- Clarify documentation without changing field names, types, requiredness, or
  meaning.

These additions must not change what existing required fields mean. If a new
optional field is required to calculate the report correctly, it is not really
optional and should not be hidden inside v1.

## Breaking Changes

A change is breaking when an old caller, old renderer, or old persisted result
can no longer be handled correctly.

Unsafe examples:

- Rename `total_work_requests` to `total`.
- Remove `status_event_count`.
- Make `requested_by` required.
- Change `generated_at` from an ISO timestamp to a Unix integer.
- Add a new required work request status without a v2 migration plan.
- Return `report-rendering.v2` while the consumer expects
  `report-rendering.v1`.
- Return partial `by_status` counts or counts that do not add up to
  `total_work_requests`.

Breaking changes need a new version, a migration plan, or both.

## Consumer-Driven Thinking

The provider is the reporting service. The consumers are the API routes, worker,
tests, and persisted report readers that depend on the response shape.

Before changing the contract, ask:

- Which fields does each consumer read?
- Which fields are persisted and may outlive the deploy?
- Can old consumers ignore this addition safely?
- Can old providers ignore this addition safely?
- What exact error should the worker record if the response is not v1?

Compatibility tests should be written from consumer expectations first. A
provider test that only proves the service returns JSON is not enough.

## Why Versioned Contracts Matter

The `contract_version` field gives debugging a stable reference point. When a
job fails because the renderer returned a v2-shaped response to a v1 worker, the
worker can record an invalid contract response instead of hiding it as a generic
failure.

Versioning also protects persisted data. Report job results may be stored long
after the renderer changes. Keeping v1 validation around until v1 data is
retired prevents newer code from silently misreading older results.

## Local Debugging Checklist

- Confirm the request includes `contract_version: report-rendering.v1`.
- Confirm the response includes all required v1 fields.
- Confirm additive fields are optional and safe to ignore.
- Confirm missing fields, wrong literals, malformed JSON, and non-2xx responses
  fail distinctly in the reporting client.
- Do not add broad automatic retries until the operation is proven safe to
  repeat across this boundary.
