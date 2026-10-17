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
| 8 | Both | `name: Poteto Mode` and `name: Make Bot UI` in frontmatter | The folder names are `poteto-mode` and `make-bot-ui`. | Unknown. The runs will show whether `/poteto-mode` and `$poteto-mode` resolve. Phase 1's frontmatter rewrite can fix it either way. |
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
| 4 | Orchestrate | `/poteto-mode Use the Orchestrate playbook, scaled down. Move ledger from float amounts to integer pence as exactly 2 stacked PRs: first parse.py, then summary.py and the CLI. No sub-coordinators. Use at most 4 subagents in total. Do not merge.` |

Orchestrate names its playbook because the router sends work this small to Autonomous run, which would not test Orchestrate.

| # | Playbook | Agent | wstack commit | Thread | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | Bug fix | Claude Code | | | not run |
| 2 | Feature | Claude Code | | | not run |
| 3 | Swarm | Claude Code | | | not run |
| 4 | Orchestrate | Claude Code | | | not run |

## Failures

One row per call that went wrong: playbook, agent, what the skill asked for, what the agent did, and whether a new adapter row would fix it.

| Playbook | Agent | Skill asked for | Agent did | New adapter row? |
| --- | --- | --- | --- | --- |
