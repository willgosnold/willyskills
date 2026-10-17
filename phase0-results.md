# Phase 0 results

The question: how much of the port can an adapter handle with no text edits to upstream?

## Setup

- Upstream: `vendor/pstack` at `101b274` (v0.15.25), byte-identical. Its tree hash matches upstream (`upstream.json`).
- Agents: Claude Code 2.1.301 and Codex 0.162.1 inside T3 Code 0.1.0.
- Adapters: upstream `docs/harness/claude-code.md` unchanged, `adapters/agents/codex.md`, and `adapters/hosts/t3.md`.
- Fixture: `~/Projects/pstack-phase0-sandbox`, a small Python ledger CLI with one planted bug. `--month 2026-03` includes March 2025 rows, because `in_month` ignores the year.
- Install: skills are symlinked into the fixture's `.claude/skills/` and `.agents/skills/`. `CLAUDE.md` and `AGENTS.md` there name the adapters to read. No global agent config changed.
- Remote: private GitHub repo `willgosnold/pstack-phase0-sandbox`, so PR steps run for real.

## Findings before any playbook run

These came from building the adapters and from two probe children that listed their own tools.

| # | Agent | What the skill expects | What is there | Adapter row fixes it? |
| --- | --- | --- | --- | --- |
| 1 | Claude Code | `TodoWrite`, `AskUserQuestion` | Neither exists in T3's Claude Code session. | Yes. Upstream's `claude-code.md` already falls back to a list in the reply and plain-text questions. |
| 2 | Claude Code | Tool names such as `Agent` | T3 exposes built-ins under prefixed names (`mcp__select_sight__layer_Agent`). | Unknown. The runs will show whether the agent matches by suffix. |
| 3 | Codex | `AskQuestion` | `request_user_input` works only in Plan mode. | Yes. `codex.md` says to ask in plain text in Default mode. |
| 4 | Codex | Transcripts under `~/.codex/sessions` | T3 runs Codex with `CODEX_HOME=~/.codex-vibeproxy`. | Yes. `t3.md` routes transcripts to `t3_thread_read`. |
| 5 | Both | An agent store path named in the system prompt (orchestrate, autopilot-full, multi-phase-plan) | T3 names none. | Yes. `t3.md` row added: `~/.local/state/pstack/<repo>/`. |
| 6 | Both | `bun` for `scripts/orch` and `scripts/watch-pr` | Bun is not installed. Bun-only code is confined to `bootstrap.ts` (`Bun.spawnSync`, `import.meta.dir`, which installs `commander` from `bun.lock`). Under Node 26, `watch-pr` runs once `commander` is installed. `orch` fails because it imports `bootstrap.ts` and `store.ts` uses a parameter property that Node's type stripping rejects. `tsx` gets past the syntax but not `import.meta.dir`. | No. Running without Bun needs a patch to `bootstrap.ts` and `store.ts`. Installing Bun keeps `vendor/` untouched. |
| 7 | Both | `bootstrap.ts` runs a package install inside the skill folder | With symlinks into `vendor/`, `node_modules/` would land in `vendor/`. | Mostly. Upstream's `vendor/pstack/.gitignore` already ignores it, so git stays clean. Phase 1 still builds into `dist/`, so installs land there. |
| 8 | Both | `name: Poteto Mode` and `name: Make Bot UI` in frontmatter | The folder names are `poteto-mode` and `make-bot-ui`. | Claude Code: no issue. Run 1's `/poteto-mode` loaded the skill. Codex untested. |
| 9 | Both | `deslop`, `control-ui`, `control-cli` from `cursor-team-kit`, and `/loop`, `/create-skill` from Cursor | Not installed. | Partly. `t3.md` maps `control-ui` to `preview_*` and `/loop` to `schedule_task`. `codex.md` maps `create-skill` to `skill-creator`. `deslop` has no row, so it is skipped. It is a code cleanup pass over the branch diff (needless comments, abnormal try/catch, `any` casts, deep nesting), not commit message rules. |
| 10 | Both | Each child can delegate further (orchestrate's sub-coordinators) | Both agents' children get the full T3 tool set and `canRunChildTask` for both providers. | Yes, no row needed. |

## Runs

Each run is a fresh T3 thread in the fixture project, with the prompt typed as a user would.

Budget for the first round:

- Claude only. Codex runs come later, if the Claude round justifies them.
- The run thread uses Claude Opus 5.5 at `medium` effort. Children follow the budget in `t3.md`: Claude only, `low` or `medium` effort, Sonnet 5.5 for any non-Claude slug, no fast mode.
- One run at a time, in the order below. Adapter fixes between runs are committed, and each run records the `wstack` commit it used.
- Each prompt caps subagents, so a run that misroutes costs little.

| # | Playbook | Prompt |
| --- | --- | --- |
| 1 | Bug fix | ``/poteto-mode `python -m ledger summary data/sample.csv --month 2026-03` reports rent as 1925.00. March 2026 rent was 975.00. Fix it. Use at most 3 subagents.`` |
| 2 | Feature | ``/poteto-mode Add `--format json` to `ledger summary`. It prints the category totals as one JSON object. Use at most 3 subagents.`` |
| 3 | Swarm | `/swarm Check that each of the 3 modules in ledger/ (parse.py, summary.py, __main__.py) has a unit test that would fail if its public behaviour broke. One worker per module, 3 workers total. Report PASS or ISSUES per module. Do not change any files.` |
| 4 | Autonomous run | ``/poteto-mode Move ledger from float amounts to integer pence so totals are exact. Done means `python -m unittest` passes, a new test shows summing 0.10 three times gives exactly 0.30, and `python -m ledger summary data/sample.csv --month 2026-03` prints what the fixed code prints today. Run until done, then open one PR. Use at most 3 subagents.`` |

Orchestrate is left out. It is built for multi-day programs with sub-coordinators, and a three-file fixture cannot exercise it. Autonomous run replaces it because its wake step tests the `/loop` rows in `t3.md`.

| # | Playbook | Agent | wstack commit | Thread | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | Bug fix | Claude Code | `d00e113` | `mcp:464dbd91-1fd4-4bb2-be8f-a4ed38c424f3` | Pass in 2 minutes. Failing test before fix, one child, PR [#1](https://github.com/willgosnold/pstack-phase0-sandbox/pull/1) linked. |
| 2 | Feature | Claude Code | | | not run |
| 3 | Swarm | Claude Code | | | not run |
| 4 | Autonomous run | Claude Code | | | not run |

## Failures

One row per call that went wrong: playbook, agent, what the skill asked for, what the agent did, and whether a new adapter row would fix it.

| Playbook | Agent | Skill asked for | Agent did | New adapter row? |
| --- | --- | --- | --- | --- |
| Bug fix | Claude Code | `run_in_background: true` on every Task | `delegate_task` with `mode: "wait"` | No. The row maps it to `async`. The agent chose to block because its next step needed the result. Harmless here. |
| Bug fix | Claude Code | Open a todolist of the playbook steps first | No list at the start. The steps appear only in the final reply. | No. `claude-code.md` already gives the fallback. The agent skipped it. |
| Bug fix | Claude Code | `deslop` before commit | Skipped and said so | No. Not installed, as expected. |

### What worked in run 1

- `CLAUDE.md` pointed the agent at both adapters, and it read them before starting.
- `orchestrator_capabilities` came first, then `delegate_task` with the `poteto-agent` brief line, `isolation: "worktree"`, and Claude Sonnet 5.5 at `low` in place of `grok-4.7-xhigh-fast`.
- The child committed on its own worktree branch. The parent cherry-picked the commit and verified it itself.
- `gh pr create` opened a ready PR, then `link_pull_request` linked it.

