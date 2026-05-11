# Release Checklist

Use this before presenting the repository publicly or tagging a learning
milestone.

## Verification

- Run `./scripts/verify.sh`.
- Run any repo-provided docs or link check.
- Run `find .prompts -maxdepth 1 -name 'PROMPT_*.txt' | sort` and confirm
  `PROMPT_01.txt` through `PROMPT_40.txt` exist with no gaps.
- Confirm exercise files still follow `exercises/TEMPLATE.md`.
- Confirm `README.md` is concise and points to durable navigation docs.

## Documentation Links

- Check local Markdown links and inline paths for broken references.
- Confirm `docs/NAVIGATION.md` lists major artifact groups.
- Confirm `docs/REPO_MAP.md` reflects current files, not future claims.
- Confirm phase lesson indexes point to the matching exercises, scenarios,
  reviews, quizzes, and interviews.
- Confirm role paths point to existing artifacts.

## Runtime And Deployment Docs

- Confirm `Dockerfile`, `docker-compose.yml`, `.env.example`, and
  `scripts/dev-*.sh` match the documented local workflow.
- Confirm `deploy/dokku/README.md` and `deploy/dokku/checklist.md` remain the
  first deployment path.
- Confirm `deploy/k3s/README.md`, `deploy/k3s/checklist.md`, and manifests are
  described as later orchestration learning materials, not early defaults.
- Confirm migration commands and health checks are documented.

## Secrets And Safety

- Confirm no real `.env` file is committed.
- Search for likely secret patterns, tokens, private keys, passwords, and real
  service credentials.
- Keep `.env.example` values local placeholders only.
- Confirm failure-injection settings are disabled by default and described as
  local/test tools.
- Confirm destructive scenario steps are scoped to local or disposable
  environments.

## Metrics And Debug Exposure

- Confirm `/metrics`, worker metrics, logs, dashboards, and debug-style
  surfaces are documented as internal-only.
- Confirm metrics labels avoid user IDs, free-form text, secrets, and
  high-cardinality values.
- Confirm incident and dashboard docs do not suggest exposing operational
  internals publicly.

## Public Readability

- Remove wording that implies Kubernetes, microservices, Redis, caching, extra
  datastores, or broad observability stacks are defaults.
- Avoid unsupported scale or production-readiness claims.
- Keep LLM guidance framed around review, critique, interviews, and debugging,
  not answer generation.
- Leave known verification gaps visible.
