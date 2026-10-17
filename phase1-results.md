# Phase 1 results

Phase 1 adds `tools/wstack.py` (sync and build) and a committed `dist/`. Installing is left to the [`skills` CLI](https://github.com/vercel-labs/skills); see the last section. Every check ran against the same test repo as Phase 0, on the same small bug.

## Done criteria

| Criterion | Result |
| --- | --- |
| Both agents install from `dist/` | Yes, into the test repo's `.claude/skills` and `.agents/skills`. Not yet into the user folders (`~/.claude/skills`, `~/.agents/skills`), because that changes global agent config. |
| `poteto-mode` runs a bug-fix playbook in T3 on each | Yes, on the second attempt. See the checks below. |
| A build at an unchanged pin produces no diff | Yes. `build` twice leaves `git status` clean. |

Also tested:
- `sync` at the pinned commit is a no-op.
- `sync` to an older upstream commit replaced `vendor/` and matched the upstream tree hash. I reverted it afterwards.
- With a throwaway patch, a header-complete patch applied, a missing `Why:` failed, and a stale hunk failed.

## Checks

| # | Agent | Build | Result |
| --- | --- | --- | --- |
| 1 | Claude Code (Opus 5.5, medium) | `12e632b` | Fixed, PR opened and linked. It read `adapters/claude-code.md` but not the two files that file names (upstream `claude-code.md` and `t3.md`), and it used no subagents. |
| 1 | Codex (GPT-6.1-Sol, low) | `12e632b` | Fixed, 2 Claude children, PR opened and linked. It found `poteto-mode` only by searching the filesystem. |
| 2 | Claude Code | after the fix below | Read all three adapter files. Fixed it alone and said why: a one-line fix wasn't worth a brief. PR opened and linked. |
| 2 | Codex | after the fix below | `poteto-mode` was in its skill list. First command read `codex.md` and `t3.md`. 2 Claude children, PR opened and linked. |

## What check 1 found

- **T3 sends `$name` to Codex as plain text.** Codex gets no skill attachment, so it finds a skill only through the list in its system prompt. The first build wrote `allow_implicit_invocation: false` for the 53 skills upstream marks `disable-model-invocation: true`, which took them off that list. Phase 0 only worked because the list showed `pstack:Poteto Mode` and the agent opened its file.
- **Codex matches `$poteto-mode` against the skill's `name`.** Upstream's is `Poteto Mode`. The build now renames `name:` to the folder name for Codex. Only `poteto-mode` and `make-bot-ui` change.
- **A chain of pointers gets skipped.** The install note named one adapter, which named the others. Claude Code read only the first. The note now names every file directly.

The trade-off: in Codex, all 54 skills are now model-invocable, although upstream marks 53 as user-only. Codex has no way to list a skill but block it from implicit use.

## Left out of the build

- The Cursor-term denylist from the handoff. The adapter approach keeps Cursor's names in `dist/` on purpose, so every build would fail. A denylist could later check that every Cursor name in `dist/` has an adapter row.
- `rerere`. Patches are applied in a fresh temporary repo, so there is nowhere for resolutions to persist yet. Revisit when the first conflict arrives.
- `docs/guide/` (2.4 MB of images for humans). No skill reads it.

## Switch to the `skills` CLI

Will installs skills per project with the `skills` CLI (1.7.2), so `tools/wstack.py install` was removed. A local test showed three things about the CLI:

- It keeps one copy of each skill in `.agents/skills/`, which Codex reads, and symlinks `.claude/skills/<name>` to it. Both agents therefore read the same files, so `dist/` is now one agent-neutral `dist/skills/`.
- It installs only skill folders. Adapters, agent briefs and upstream's Claude Code notes now ship inside a `pstack` support skill, and every path in the install note is relative (`../pstack/...`).
- It names each folder after the skill's `name`. All names now match their folders, for both agents.

| Agent | Result |
| --- | --- |
| Claude Code (Opus 5.5, medium) | Resolved `../pstack/` and read all three adapter files. Fixed it alone with a failing test first, PR opened and linked. |
| Codex (GPT-6.1-Sol, low) | Listed `poteto-mode`, read `codex.md` and `t3.md`, delegated the fix to Claude Sonnet 5.5 with the poteto-agent brief. Then it left the change uncommitted and opened no PR, while marking "Stage the commits" and "Run Opening a PR" as completed. An agent slip at low effort, not an install problem. |

The CLI's `skills-lock.json` records a local source by relative path. Installing from a T3 worktree path is fragile. Install from a stable checkout, or from GitHub once wstack is pushed.

## Model roles

The role lines now resolve from `.agents/pstack-models.md` in the project's main checkout, then from a defaults table in `t3.md`. The defaults still encode the test budget. Two Claude checks:

- `/setup-pstack` with budget "small" wrote the project file in the main checkout, in the new line format, with every role at `medium`. Nothing went to `~/.cursor/rules/`.
- With `swarm workers: claudeAgent/claude-haiku-5-5 low` in that file, `/swarm` read it and sent both workers to Haiku 5.5 at low effort.
