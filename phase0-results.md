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
| 8 | Both | `name: Poteto Mode` and `name: Make Bot UI` in frontmatter | The folder names are `poteto-mode` and `make-bot-ui`. | No issue on either agent. `/poteto-mode` (run 1) and `$poteto-mode` (run 6) both loaded the skill. |
| 9 | Both | `deslop`, `control-ui`, `control-cli` from `cursor-team-kit`, and `/loop`, `/create-skill` from Cursor | Not installed. | Partly. `t3.md` maps `control-ui` to `preview_*` and `/loop` to `schedule_task`. `codex.md` maps `create-skill` to `skill-creator`. `deslop` has no row, so it is skipped. It is a code cleanup pass over the branch diff (needless comments, abnormal try/catch, `any` casts, deep nesting), not commit message rules. |
| 10 | Both | Each child can delegate further (orchestrate's sub-coordinators) | Both agents' children get the full T3 tool set and `canRunChildTask` for both providers. | Yes, no row needed. |

## Runs

Each run is a fresh T3 thread in the fixture project, with the prompt typed as a user would.

Budget for the first round:

- Claude only. Codex runs come later, if the Claude round justifies them.
- The run thread uses Claude Opus 5.5 at `medium` effort. Children follow the budget in `t3.md`: Claude only, `low` or `medium` effort, Sonnet 5.5 for any non-Claude slug, no fast mode.
- One run at a time, in the order below. Adapter fixes between runs are committed, and each run records the `willyskills` commit it used.
- Each prompt caps subagents, so a run that misroutes costs little.

| # | Playbook | Prompt |
| --- | --- | --- |
| 1 | Bug fix | ``/poteto-mode `python -m ledger summary data/sample.csv --month 2026-03` reports rent as 1925.00. March 2026 rent was 975.00. Fix it. Use at most 3 subagents.`` |
| 2 | Feature | ``/poteto-mode Add `--format json` to `ledger summary`. It prints the category totals as one JSON object. Use at most 3 subagents.`` |
| 3 | Swarm | `/swarm Check that each of the 3 modules in ledger/ (parse.py, summary.py, __main__.py) has a unit test that would fail if its public behaviour broke. One worker per module, 3 workers total. Report PASS or ISSUES per module. Do not change any files.` |
| 4 | Autonomous run | ``/poteto-mode Move ledger from float amounts to integer pence so totals are exact. Done means `python -m unittest` passes, a new test shows summing 0.10 three times gives exactly 0.30, and `python -m ledger summary data/sample.csv --month 2026-03` prints what the fixed code prints today. Run until done, then open one PR. Use at most 3 subagents.`` |

Orchestrate is left out. It is built for multi-day programs with sub-coordinators, and a three-file fixture cannot exercise it. Autonomous run replaces it because its wake step tests the `/loop` rows in `t3.md`.

| # | Playbook | Agent | willyskills commit | Thread | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | Bug fix | Claude Code | `d00e113` | `mcp:464dbd91-1fd4-4bb2-be8f-a4ed38c424f3` | Pass in 2 minutes. Failing test before fix, one child, PR [#1](https://github.com/willgosnold/pstack-phase0-sandbox/pull/1) linked. |
| 2 | Feature | Claude Code | `4d03959` | `mcp:04058359-5983-484d-b1ce-703ea55c611d` | Pass in 3 minutes over two turns. Async child woke the parent. Parent caught a regression the child missed. PR [#2](https://github.com/willgosnold/pstack-phase0-sandbox/pull/2) linked. |
| 3 | Swarm | Claude Code | `6d1362f` | `mcp:3995690b-f17b-42fd-8090-dea5104156e8` | Pass in 2 minutes over three turns. 3 parallel read-only workers, all ISSUES with evidence. Found the planted bug independently. |
| 4 | Autonomous run | Claude Code | `07144e0` | `mcp:b45f5a4c-2916-4b77-8300-372e2181cc34` | Task passed in 2 minutes, PR [#3](https://github.com/willgosnold/pstack-phase0-sandbox/pull/3) linked. Wake rows untested: one iteration met the predicate, so it never needed `/loop`. |

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
| Feature | Claude Code | `how` explainer and `architect` runners as subagents | Did both inline and said so | No. The prompt's 3-subagent cap caused it. |

### What worked in run 2

- The implementer ran with `mode: "async"`. The parent ended its turn, T3 woke it with "Delegated task finished", and it read the result with `task_status`. This is the `run_in_background` row working end to end.
- `comment-sicko` ran from the brief line with "Do not edit, create, commit, or push files", and reported without editing.
- The parent reviewed the child's diff, found a blank-line regression on empty months, fixed it, and checked table output against the old code.
- It listed the playbook steps mid-run this time.
| Swarm | Claude Code | `environment: "cloud"` workers | Read-only workers with no `isolation`, sharing the checkout and mutating copies in `/tmp` | Yes, a clarification. The `cloud` row said worktree for every worker. It now says read-only workers share the checkout, matching the `local` row. Fixed after run 3. |

### What worked in run 3

- Three `delegate_task` calls in one message, each with its own `clientRequestId`, on Sonnet 5.5 at `medium`.
- T3 woke the parent once for the first result and once for the other two, batched into one notification.
- The parent checked each result named the commit and method its brief asked for, then ran `git status` to confirm the read-only workers left the tree clean.
| Autonomous run | Claude Code | Pick a wake mechanism with `/loop` (step 2) | Never reached it. One iteration met the predicate. | Untested. Needs a task whose predicate depends on something outside the agent, such as CI or a merge. |
| Autonomous run | Claude Code | Delegate code to subagents | Wrote the change itself, used 0 of 3 subagents | No. The change was a few lines, and Autonomous run does not require delegation. |
| Autonomous run | Claude Code | (Prompt flaw, mine) "what the fixed code prints today" | `main` still has the year bug, because PR #1 is unmerged. The agent saw the ambiguity, kept today's buggy output, and flagged the bug. | No. Fix the prompt if this run is repeated. |

## Round 1 summary (Claude Code)

All four tasks finished and verified their own work. Rows exercised and working: the adapter pointers in `CLAUDE.md`, `orchestrator_capabilities`, `delegate_task` with the agent-file brief, `isolation: "worktree"` for writers, shared checkout for readers, `mode: "async"` with T3 waking the parent, parallel fan-out, `task_status`, the read-only brief plus `git status`, the Claude-only model budget, `gh pr create`, and `link_pull_request`.

One adapter row changed (`environment: "cloud"` for read-only workers). No upstream text edits were needed.

Untested so far: `schedule_task` for `/loop`, `watch_pull_request`, `task_cancel`, `t3_thread_send` for resume, the transcript rows, the agent store path, `preview_*`, and everything on Codex.

## Round 2

| # | Playbook | Agent | willyskills commit | Thread | Result |
| --- | --- | --- | --- | --- | --- |
| 5 | Babysit | Claude Code | `9c212e7` | `mcp:21f283b9-95a5-431f-b3c9-c67ac5ab2cda` | Pass over two turns. `watch-pr` ran under Bun in a background shell, its `READY` verdict woke the thread when CI finished, and it did not merge. |
| 6 | Bug fix | Codex (GPT-6.1-Sol, low) | `9c212e7` | `mcp:83c55533-6210-4479-b7bc-259008be2eaf` | Pass in 2 minutes. 3 Claude children, failing test first, PR [#4](https://github.com/willgosnold/pstack-phase0-sandbox/pull/4) linked. |

The fixture gained a CI workflow on `main` that sleeps 180 seconds before running the tests, so Babysit has something to wait for. PR #3 was updated from `main` to start CI.

### What worked in run 6 (Codex)

- `AGENTS.md` led it to `codex.md`, then to `t3.md`. It read both before starting.
- `update_plan` held the bug-fix steps, as `codex.md` maps.
- `orchestrator_capabilities`, then three `delegate_task` calls, all with Claude targets under the budget: a worktree implementer on Sonnet 5.5, a read-only explainer, and `comment-sicko` from its agent file.
- Codex kept working while children ran. T3 delivered each completion as a notification inside the turn, and Codex read each with `task_status`.
- `gh pr create`, then `link_pull_request`, then `list_thread_pull_requests` to confirm.

| Playbook | Agent | Skill asked for | Agent did | New adapter row? |
| --- | --- | --- | --- | --- |
| Bug fix | Codex | Read-only explainer | Shared the checkout while the parent cherry-picked the fix, so the explainer saw the code change mid-read and said so | No. Harmless here. A read-only worker that needs a stable tree could be pinned to a commit in its brief. |
| Babysit | Claude Code | Wait for CI, then report the forge verdict | Ran `watch-pr` (Bun) in a Claude Code background shell and ended its turn. The shell's exit woke the thread 2 minutes later. It never called `watch_pull_request`. | Yes, a clarification. Both work. The row now says a background shell wakes Claude Code only while its session lives, and to use `watch_pull_request` for longer waits. Codex has no equivalent. Fixed after run 5. |
| Babysit | Claude Code | `scripts/watch-pr/watch-pr` | Looked for it under `<pstack>/scripts/` first, then found it under `skills/poteto-mode/scripts/`. Its reply calls this a pstack docs bug. | No. The playbook path is relative to the skill folder. The agent's bug claim looks wrong. |

### What worked in run 5

- `watch-pr` ran under Bun with no setup beyond the mise install. Finding 6 is closed.
- A T3 thread woke from a Claude Code background command's exit after its turn had ended.
- `t3_thread_search` looked for another babysitter on the PR before starting, which the playbook asks for.
- `link_pull_request` on the PR it was given.

## Round 2 summary

Codex follows the same adapters through `AGENTS.md`, `codex.md`, and `t3.md` with no extra rows. Babysit's waiting worked, through a Claude Code mechanism rather than the T3 one. Still untested: `schedule_task`, `watch_pull_request`, `task_cancel`, resume through `t3_thread_send`, the agent store path, and `preview_*`.

