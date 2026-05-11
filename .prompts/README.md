# Prompt History

This directory records the prompt-driven development sequence for the
repository. The files are numbered in execution order and should remain
strictly monotonic:

- `PROMPT_01.txt` through `PROMPT_40.txt`

Each prompt describes one bounded repository-building phase. Future prompts
should use the next unused number, preserve earlier prompt files, and avoid
renumbering history.

Use `find .prompts -maxdepth 1 -name 'PROMPT_*.txt' | sort` to inspect the
sequence. At this release-polish pass, `PROMPT_01.txt` through
`PROMPT_40.txt` exist with no gaps.
