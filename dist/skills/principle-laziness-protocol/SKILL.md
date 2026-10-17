---
name: principle-laziness-protocol
description: "Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. Bias toward deletion and the smallest change that solves the problem."
disable-model-invocation: true
---

> **pstack install note.** Once per session, before following this skill, read your agent's adapter. It maps the Cursor names below to your agent. Paths are relative to this file's folder. In Claude Code, read `../pstack/docs/harness/claude-code.md`, then `../pstack/adapters/claude-code.md`. In Codex, read `../pstack/adapters/codex.md`. If the T3 Code tools are present (`delegate_task`), also read `../pstack/adapters/t3.md`. Its rows win for subagents, models, schedules, pull requests, and transcripts.

# Laziness Protocol

- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth and pass the result as a simple flag.
- **Minimize the diff.** Make the smallest change that solves the problem. Fewer lines beat "elegant" boilerplate.
