---
name: principle-guard-the-context-window
description: "Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads."
disable-model-invocation: true
---

> **pstack install note.** `<pstack>` is `{{PSTACK_ROOT}}`. Once per session, before following this skill, read `{{PSTACK_ROOT}}/adapters/codex.md`. It maps the Cursor names below to this agent. If the T3 Code tools are present (`delegate_task`), also read `{{PSTACK_ROOT}}/adapters/t3.md`. Its rows win for subagents, models, schedules, pull requests, and transcripts.

# Guard the Context Window

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
