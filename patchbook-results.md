# Patchbook build: results

The build now rewrites upstream instead of shipping adapters. Each upstream block that uses a Cursor name is replaced from `patchbook/entries/`, and agents read only the finished skills: no install note, adapter, or lookup table.

## First batch (upstream 101b274)

- 136 entries in 46 files: 132 translations, 4 keeps.
- Drafted by 7 parallel Opus subagents from `patchbook/patch.md`, then a fix-up pass after the term check was widened. `status` reports no problems.
- The term check found three Cursor-isms the first list missed: `create-skill`, "fast or standard speed", and links to unshipped `docs/guide/` pages. Each became a rule.
- No `.md` file in the installed skills mentions Cursor.

## Checks in the sandbox (installed with the `skills` CLI)

| Check | Result |
| --- | --- |
| Claude Code (Opus 5.5, medium), `/poteto-mode` bug fix | Failing test first, fix, PR opened and linked. Fixed the one-line bug itself instead of delegating, and said so. |
| Claude Code (Opus 5.5, medium), `/swarm`, project file sets `swarm workers: claudeAgent/claude-haiku-5-5 low` | Read the project file from the main checkout, sent two read-only async workers to Haiku 5.5 low, kept its step list in the reply, and reported when both woke it. |
| Codex (GPT-6.1-Sol, low), `$poteto-mode` bug fix | Kept its plan with `update_plan`, called `orchestrator_capabilities`, delegated the fix to Sonnet 5.5 (`bug-fix` role) asynchronously, ran a comment-sicko review, then committed, pushed, and opened and linked the PR. In Phase 1 it skipped the commit and PR. |

## Open

- `poteto-mode/scripts/check-plan.mjs` requires `/loop 1h` in a plan, which the patched skeleton no longer writes. Plans will fail that check.
- `poteto-mode/scripts/worktree-audit.sh` reads only Cursor transcripts, so its `LAST_CHAT` column is always empty in T3. The patched playbook says so and checks T3 threads instead.
- `make-bot-ui` is built on Cursor routines. Most of it passes the term check, but it won't work in T3.
- `/name` references in skills are not rewritten, so Codex sees `/how` where it would type `$how`.
- Whether T3 child tasks survive a T3 restart is unverified.
