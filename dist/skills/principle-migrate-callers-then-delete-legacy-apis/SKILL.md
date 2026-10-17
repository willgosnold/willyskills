---
name: principle-migrate-callers-then-delete-legacy-apis
description: "Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave instead of preserving compatibility layers."
disable-model-invocation: true
---

> **pstack install note.** Once per session, before following this skill, read your agent's adapter. It maps the Cursor names below to your agent. Paths are relative to this file's folder. In Claude Code, read `../pstack/docs/harness/claude-code.md`, then `../pstack/adapters/claude-code.md`. In Codex, read `../pstack/adapters/codex.md`. If the T3 Code tools are present (`delegate_task`), also read `../pstack/adapters/t3.md`. Its rows win for subagents, models, schedules, pull requests, and transcripts.

# Migrate Callers Then Delete Legacy APIs

- Update tests to assert the new contract, and delete tests that only protect pre-refactor implementation details

**When this applies:**
- No external users depend on backward compatibility
- The project can absorb coordinated breaking changes
- The new API is part of a simplification or refactor initiative
