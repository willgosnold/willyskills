# pstack in Codex

pstack skills use Cursor names. In Codex, read this file once per session, then map each Cursor name in a skill with the tables below. `<pstack>` means the folder that holds `skills/`, `agents/`, and `docs/`. If the T3 Code MCP tools are present (`mcp__t3_code__delegate_task`), also read the T3 host adapter that `AGENTS.md` names. Its rows replace this file's rows for subagents, scheduling, pull requests, transcripts, and models. If a Cursor field has no row, drop it and say so. Never pass a field or value the tool schema rejects.

## Tools

| Cursor | Codex |
| --- | --- |
| `AskQuestion` | `request_user_input` works only in Plan mode. In Default mode, ask in plain text and end your turn. |
| Open a todolist | `update_plan`. Update it at each phase. |
| Run another pstack skill (`/name` or "the **name** skill") | Read `<pstack>/skills/<name>/SKILL.md` and follow it. When you tell the user to type it, write `$<name>`. |
| `Read`, `Grep`, `Glob` | `exec_command` with `sed -n`, `rg`, or `rg --files`. |
| Editing a file | `apply_patch`. |
| `create-skill` (Cursor's built-in skill-authoring skill) | Codex's `skill-creator` skill. |

## Subagents outside T3

Use these rows only when the T3 tools are absent. These rows are unverified.

| Cursor | Codex |
| --- | --- |
| `Task` | `spawn_agent`. Wait for it with `wait_agent`. |
| `poteto-agent`, `comment-sicko` | No agent types. Start the brief with "Read `<pstack>/agents/<name>.md` and act as that agent", using an absolute path. |
| `readonly: true` | The brief says "Do not edit, create, commit, or push files." Run `git status` afterward. |
| `environment: "cloud"` | Create a worktree with `git worktree add` and name its path in the brief. |
| `run_in_background: true` | Spawn, keep working, and call `wait_agent` when you need the result. |
| `resume` | `followup_task`. |
| Stop an agent | `interrupt_agent`. |
| A model slug | Omit the model so the agent runs on the session model, and say so. |

## Paths

| Cursor | Codex |
| --- | --- |
| `.cursor/skills/`, `~/.cursor/skills/` | `.agents/skills/`, `~/.agents/skills/` |
| `~/.cursor/plugins/` (where `poteto-agent` searches for `poteto-mode`) | Your parent gives you the absolute path. If it didn't, stop and say so. |
| `.cursor/rules/*.mdc`, always-applied rules | `AGENTS.md`. Codex never reads `.mdc` files. |
| Transcripts in `~/.cursor/projects/<slug>/agent-transcripts/` | `$CODEX_HOME/sessions/<yyyy>/<mm>/<dd>/rollout-*.jsonl`. `CODEX_HOME` defaults to `~/.codex`, and T3 sets it to another folder. Under T3, use the transcript rows in `t3.md`. |

## Cursor-only features

Automations, Bugbot, Cursor cloud agents, and Cursor's pull request tool have no Codex equivalent. Say so, skip that step, and continue.
