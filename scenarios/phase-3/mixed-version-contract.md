# Mixed-Version Contract Scenario

Use this scenario to reason about backward-compatible additions and incompatible
contract drift across the reporting service boundary.

## Goal

Compare a safe additive `report-rendering.v1` response with an incompatible
response shape, then explain why versioned contracts matter during deploys.

## Preconditions

- You have read `docs/contracts/report-rendering-v1.md`.
- You have read `docs/contracts/compatibility-playbook.md`.
- Local `uv` tooling is available.

## Steps

Run the focused compatibility tests:

```sh
uv run pytest services/api/tests/test_report_rendering_contract.py services/api/tests/test_reporting_client.py
```

Before changing code, inspect what those tests prove:

- v1 requests still require required fields.
- Optional request additions such as `requested_by` are accepted.
- Additive response fields from a newer renderer are ignored by the v1 client.
- Missing required fields or wrong contract literals fail validation.

Now run the reporting service bad-response scenario with:

```sh
OPLEDGER_REPORTING_FAILURE_MODE=incompatible_response
```

Observe the failed report job and worker logs before making any fix.

Expected observations:

- A newer additive field is safe only when old consumers can ignore it.
- A different `contract_version` is not a v1 additive change.
- The worker should make invalid contract responses visible in durable job
  state.

## Explain What Happened

- Which changes are safe for old workers?
- Which changes require a new version or coordinated deploy?
- Why does persisted report result JSON make compatibility more than a runtime
  concern?
- What consumer expectation would you write before changing the provider?

## Cleanup

```sh
./scripts/dev-down.sh
```
