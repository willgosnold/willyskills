---
name: principle-prove-it-works
description: "Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.'"
disable-model-invocation: true
---

> **pstack install note.** Once per session, before following this skill, read your agent's adapter. It maps the Cursor names below to your agent. Paths are relative to this file's folder. In Claude Code, read `../pstack/docs/harness/claude-code.md`, then `../pstack/adapters/claude-code.md`. In Codex, read `../pstack/adapters/codex.md`. If the T3 Code tools are present (`delegate_task`), also read `../pstack/adapters/t3.md`. Its rows win for subagents, models, schedules, pull requests, and transcripts.

# Prove It Works

Verify every task output by checking the real thing directly. Do not infer from proxies, self-reports, or "it compiles."

**Why:** Unverified work has unknown correctness. Indirect verification (file mtimes, output freshness, agent self-reports, cached screenshots) feels cheaper than direct observation. Acting on a wrong inference costs far more than checking the source.

Check the real thing, not a proxy:
- Check process liveness directly, not indirectly through derived state
- Read the actual value, not a cached or derived representation
- When verification fails, suspect the observation method before suspecting the system

## Script the check when you can

The strongest proof is a deterministic script that re-runs the same comparison, not a one-time eyeball. Write the script, run it, and keep its output as an artifact a reviewer can re-run instead of trusting your word.

Keep the artifact visible for the human. Commit it only for large or complex work where the trail has to be auditable later, like a big port or migration (the **show-me-your-work** skill).
