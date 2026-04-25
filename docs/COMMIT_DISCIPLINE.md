# Commit Discipline

Commits should make prompt-driven work easy to review. Prefix each commit
subject with `[PROMPT_XX]` for the prompt that was run, group related changes in
the body, and keep verification separate from the change summary.

Use `git commit -F - <<'EOF'` for multi-line messages. Avoid command-line
message strings with escaped newline sequences because they can appear
literally in commit history.

## Message Shape

Recommended structure:

```text
[PROMPT_XX] concise imperative subject

Changed:
- Grouped summary of what changed.
- Another grouped summary when useful.

Verified:
- Command or check that was run.
- Manual confirmation when appropriate.

Notes:
- Optional context, limitations, or follow-up.
```

Keep the subject concise. The body should explain what changed and how it was
checked without mixing those concerns.

## Docs-Only Example

```sh
git commit -F - <<'EOF'
[PROMPT_03] document assistant workflow discipline

Changed:
- Added assistant workflow guidance across the six curriculum phases.
- Added reusable LLM review templates for critique and interview practice.
- Updated repository navigation to include the new review materials.

Verified:
- rg "struggle first|critique second|PROMPT_|harsh implementation review"
- Confirmed templates require learner reasoning before critique.

Notes:
- Docs-only change; no application code or runtime behavior added.
EOF
```

## App-Code Example

```sh
git commit -F - <<'EOF'
[PROMPT_12] add work request status transition endpoint

Changed:
- Added the status transition handler and request validation.
- Persisted status events in the same transaction as the work request update.
- Returned explicit errors for invalid lifecycle transitions.

Verified:
- go test ./...
- Manually exercised valid and invalid transitions against local Postgres.

Notes:
- Postgres remains the source of truth for current state and event history.
EOF
```

## Tests Example

```sh
git commit -F - <<'EOF'
[PROMPT_18] cover notification retry edge cases

Changed:
- Added tests for duplicate notification attempts and retry exhaustion.
- Added coverage for poison inputs that should not be retried indefinitely.
- Documented the expected repair path for stuck notification work.

Verified:
- go test ./...
- Confirmed failing cases fail before the implementation fix.

Notes:
- Test-only change; production behavior is unchanged.
EOF
```

## Deployment Example

```sh
git commit -F - <<'EOF'
[PROMPT_27] add Dokku deployment configuration

Changed:
- Added deployment configuration for the single-service OpsLedger runtime.
- Documented required environment variables and release checks.
- Added rollback notes tied to the constrained VPS deployment model.

Verified:
- make release-check
- Confirmed deployment docs do not introduce k3s or extra services.

Notes:
- Dokku remains the deployment target for this phase.
EOF
```
