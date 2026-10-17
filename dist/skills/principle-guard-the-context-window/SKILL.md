---
name: principle-guard-the-context-window
description: "Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads."
disable-model-invocation: true
---

> **pstack install note.** Once per session, before following this skill, read your agent's adapter. It maps the Cursor names below to your agent. Paths are relative to this file's folder. In Claude Code, read `../pstack/docs/harness/claude-code.md`, then `../pstack/adapters/claude-code.md`. In Codex, read `../pstack/adapters/codex.md`. If the T3 Code tools are present (`delegate_task`), also read `../pstack/adapters/t3.md`. Its rows win for subagents, models, schedules, pull requests, and transcripts.

# Guard the Context Window

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
