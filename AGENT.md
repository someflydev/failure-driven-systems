# Agent Routing

This repository is developed through prompt-driven coding-assistant sessions.
Future agents should treat the repository as a public-quality learning artifact,
not a scratchpad.

## Session Start

At the start of each session:

1. Inspect the current directory with `pwd`.
2. Inspect worktree state with `git status --short`.
3. Inspect available files with `rg --files`.
4. Read the active prompt file before making changes.
5. Read any existing files that the prompt may affect.

## Working Rules

- Preserve existing human and agent work unless the active prompt explicitly
  asks for replacement.
- Follow prompt files as the source of truth for the current task.
- Keep changes scoped to the requested phase.
- Do not add application code, services, infrastructure manifests, dependencies,
  or generated artifacts before a prompt creates that need.
- Keep files ASCII unless a file already uses another character set for a clear
  reason.
- Do not claim that planned features, services, databases, queues, deployments,
  or tests already exist.

## Verification

Before the final response:

- Run the verification commands requested by the prompt.
- Check that the repository map still reflects reality.
- Confirm that new docs are durable guidance, not vague placeholders.
- Report what changed and what verification was run.
