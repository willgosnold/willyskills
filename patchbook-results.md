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

## Second round

Changes since the first checks:
- Model defaults chosen. Opus high for judgment, with Opus xhigh for `hardest tasks`. Sonnet high for code. Haiku xhigh for search, perf, reflect tooling, and swarm verification. GPT-6.1-Sol xhigh as the second runner in `arena`, `architect`, and `interrogate`.
- Reviews and verifiers run on the worker's own model unless the user names another (policy rule `same-model-review`). The judge pool is Opus alone.
- Skills name each other as "the **name** skill". Text the user types gives both `/name` and `$name`. The build fails on a `/name` without the Codex form.
- `check-plan.mjs` looks for the `schedule_task` tick. `worktree-audit.sh` reads Claude Code and Codex transcripts and works on Linux. The patchbook now patches scripts.
- `make-bot-ui` rewritten around T3 webhooks and `request_secret`.
- The build writes a top-level `skills/`. From the repo root, `npx skills add` found `vendor/`'s unpatched skills before this. It now installs all 55 patched skills.

| Check | Result |
| --- | --- |
| Claude Code (Opus 5.5, medium), `/poteto-mode` bug fix | Failing test first, fix, PR opened and linked. |
| Codex (GPT-6.1-Sol, low), `$poteto-mode` bug fix | Delegated the fix with the poteto-agent brief, ran comment-sicko, opened and linked the PR. |
| Claude Code (Opus 5.5, medium), `/arena`, project file sets runners to Sonnet 5.5 low and GPT-6.1-Sol low | Ran one candidate per provider in its own worktree, judged with the pool's entry, scored both, grafted Sol's tie and empty tests onto Sonnet's base, verified with a mutation check, committed. One Claude API error (400, credential metadata) interrupted it once; a "continue" finished it. |

## Open

- `make-bot-ui` is untested end to end. T3 returns no `webhookUrl` here, so T3 Connect remote access is off. The exact success status of a T3 webhook POST is unknown; the skill accepts any 2xx.
- Whether T3 child tasks survive a T3 restart is unverified.
- Codex lists all 55 skills, including 28 `principle-*` skills only opened by path.
