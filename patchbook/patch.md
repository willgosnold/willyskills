# Patchbook

Every change wstack makes to upstream pstack is recorded here. Upstream is written for Cursor. wstack ships it for agents running in T3 Code (Claude Code or Codex), so the build replaces each upstream block that needs a change with a patched version. Agents see only the result: never Cursor's names, an adapter, or a lookup table.

Each entry has a kind:

- **translation**: says in T3's terms what upstream says in Cursor's. The rules below define these.
- **policy**: changes what pstack does. Its intent says why, and how to tell whether it still applies.
- **keep**: a block that matches a Cursor term but needs no change (such as the word "Task" in a heading). Its intent says why.

## Entries

`entries/<upstream path>.entries` holds the entries for one upstream file, such as `entries/skills/poteto-mode/SKILL.md.entries`. (The suffix keeps the `skills` CLI from mistaking them for skills.) A block is a run of lines between blank lines, a whole fenced code block, or a file's frontmatter. Each entry:

```
=== entry <hash>
kind: translation
rules: delegate, background
intent: <what this change does, in a sentence or two>
--- upstream
<the upstream block, exactly>
--- patched
<the replacement; empty deletes the block>
```

`<hash>` is the first 12 hex digits of the SHA-256 of the upstream block. `rules` names the rules applied; policy and keep entries may leave it empty. The build replaces each block whose hash has an entry, and fails when:

- an upstream block still contains a Cursor term and has no entry (**missing**),
- an entry's upstream block no longer exists (**orphan**),
- the output contains a Cursor term, or a `{{model:…}}` or `{{snippet:…}}` placeholder it cannot fill.

`tools/wstack.py status` lists every problem (`--json` adds the block text, for agents), and `tools/wstack.py scaffold` appends a skeleton entry for each missing block. When upstream changes, status shows what moved. A missing block is rewritten from these rules. An orphan's intent decides its fate: if the change still applies to the new upstream text, rewrite it there, otherwise move it to `retired.md` with the reason.

## How to rewrite

- Change only what a rule requires. Keep upstream's wording, order, voice, and formatting everywhere else.
- Never mention Cursor, T3 "instead of" anything, an adapter, or a mapping. Write the instruction as if pstack had been written for T3.
- When a step only makes sense in Cursor (rule `cursor-only`), delete it, or the clause that holds it. Say what was dropped in the entry's `intent`.
- Use `{{model:<role>}}` wherever a model is chosen, and `{{snippet:<name>}}` for the shared sentences in `snippets.md`. Never write a model name or the project models file path by hand.
- One entry may cover a whole list or table. Rewrite every Cursor term in it.
- If no rule fits, write the closest faithful version, and explain the choice in `intent` so a reviewer can turn it into a rule.

Each rule below gives its intent, what Cursor writes, and what the patched text says instead. The intent is what to preserve when upstream rewords or restructures a block.

## Subagents

### delegate
Intent: a subagent is a T3 child task. The child starts with no conversation history, so the brief carries everything.
Cursor: `Task`, "a Task subagent", "spawn a subagent".
T3: `delegate_task`, with the whole brief in `task`. Give each spawn its own `clientRequestId`, reused only to retry that spawn. Keep the returned `taskId` and `childThreadId`. N workers in one message are N `delegate_task` calls in one message.

### agent-brief
Intent: pstack's named agents are prompt files, not agent types.
Cursor: `subagent_type: "poteto-agent"`, `subagent_type: "comment-sicko"`.
T3: no type field. The brief starts: "Read `<abs>/pstack/agents/<name>.md` and act as that agent." For poteto-agent, add "The poteto-mode skill is at `<abs>/poteto-mode/SKILL.md`." The pstack skills sit side by side, so `pstack/` is a sibling of the current skill's folder. Briefs use absolute paths.

### general-purpose
Intent: the default agent needs no field.
Cursor: `subagent_type: generalPurpose`.
T3: omit it.

### read-only
Intent: the worker must not change the repo. T3 has no read-only flag that works unattended.
Cursor: `readonly: true`.
T3: the brief says "Do not edit, create, commit, or push files.", and the parent runs `git status` in that checkout afterward. Never set `runtimeMode`: a narrower mode makes the child wait for approvals no one can give. `readonly: false` is omitted.

### isolation
Intent: a worker that writes gets its own checkout. A worker that only reads shares the parent's.
Cursor: `environment: "cloud"`, `environment: "local"`, `cloud_base_branch: <b>`.
T3: a writer gets `isolation: "worktree"`, a checkout of the parent's current local commit. Uncommitted edits are not copied, so commit first or name a pushed branch. A reader gets no `isolation` and shares the checkout, with scratch copies in `/tmp`. For a base branch, the brief tells the worker to check out `<b>` first. Every child runs on this machine.

### background
Intent: the parent keeps working, or ends its turn, while the child runs, and is woken when it finishes.
Cursor: `run_in_background: true` / `false`, `is_background: true`.
T3: `mode: "async"`. The child's completion wakes this thread, so end the turn instead of polling. Use `task_status` only for a result needed mid-turn. Blocking is `mode: "wait"`; on `waitTimedOut`, keep the `taskId` and check `task_status` later. `is_background` is dropped.

### resume
Intent: continue an agent's own conversation, as opposed to starting a fresh one.
Cursor: `resume` an agent.
T3: `t3_thread_send` to its `childThreadId`. A finished task then runs a follow-up with its own `taskId`. A fresh review round is a new `delegate_task` with the consolidated brief.

### stop
Intent: halt an agent and everything it started.
Cursor: stop an agent, the agents dashboard.
T3: `task_cancel`, then confirm with `task_status`. Cancelling stops the tasks it delegated too. `task_status` reads state without waking the agent.

### child-question
Intent: a child can block on a question.
T3: `t3_pending_request_read` and `t3_pending_request_respond` with `threadId: <childThreadId>`, or ask the user.

## Models

### model-role
Intent: every spawn's model comes from one place the user controls: per-project lines first, then wstack's defaults. Skills never hard-code a model.
Cursor: a slug such as `grok-4.7-xhigh-fast` or `claude-opus-5-5-xhigh`; "the `<role>` line in `~/.cursor/rules/pstack-models.mdc`"; "default X if the rule or line is missing"; `auto` / `inherit-parent`; Task `model`.
T3: "the `<role>` line in {{snippet:models-file}}, else {{model:<role>}}". Where a skill explains how to apply a line, use {{snippet:model-entry}}. Roles are the names in `models.json`. Drop fallbacks for a rejected slug and the family-prefix rules (`claude-*`, `grok-*`, `composer-*`); `orchestrator_capabilities` lists what exists.

### model-effort
Intent: the user's line sets the budget.
Cursor: "pick the reasoning level and fast or standard speed", raise for hard work, lower for routine, fast only when urgent.
T3: the line's effort is a ceiling. Lower it for routine work, never raise it. Never set `fastMode`. Where upstream says "Pick each subagent's reasoning level and fast or standard speed for the job", write "Set each subagent's effort for the job, lowering its line's effort for routine work and never raising it.".

### model-unnamed
Intent: spawns that name no role still get a deliberate model.
T3: "fast code model" / trivial mechanical edits → `feature, refactoring`. "Strongest judgment model" / hardest changes → `hardest tasks`. "Fast, cheap model" → `how explorer`. A reviewer, judge, or verifier "on a different model family" → the first `arena cross-judge pool` entry whose provider differs from the worker's, else the first entry, saying so. Anything else → `judgment and prose`.

### setup-pstack
Intent: `/setup-pstack` writes the project models file.
T3: detect models with `orchestrator_capabilities`. Write {{snippet:models-file}} with one line per role and a `# budget:` line. A budget sets each entry's effort to its level, or the highest that model offers below it. Tell the user to commit the file if worktrees and other people should see it.

## Tools the agent uses

### ask
Intent: a question to the user ends the turn.
Cursor: `AskQuestion`.
T3: ask in plain text, then end the turn.

### todolist
Intent: a visible step list kept current at each phase.
Cursor: "open a todolist".
T3: Codex keeps it with `update_plan`. Claude Code keeps it in the reply and updates it at each phase.

### invoke
Intent: tell the user how to start a skill.
Cursor: "type `/name`".
T3: "`/name` (`$name` in Codex)".

### capabilities
Intent: know which providers and models exist, and this thread's ID.
T3: call `orchestrator_capabilities` once before the first spawn. It returns `parentThreadId`.

## Waiting and schedules

### loop
Intent: repeat work on a timer, or until a condition holds.
Cursor: `/loop <interval> <prompt>`, `/loop until <predicate>`.
T3: an interval is `schedule_task` with `schedule: {type: "interval", everyMs: <ms>}` (minimum 60000); report `nextRunAt`, and `delete_scheduled_task` once the predicate holds. "Until" wakes on the event when T3 can see it (an async child finishing, `watch_pull_request`), plus a `schedule_task` heartbeat of 20 to 30 minutes; each wake re-checks the predicate.

## Pull requests

### pr-tool
Intent: open and track PRs from the shell.
Cursor: Cursor's pull request tool.
T3: `gh` (or `origin` where the skill says so), then `link_pull_request` with the URL right after creating it, once per stack layer. Before finishing, check `list_thread_pull_requests`.

### pr-wait
Intent: wait for CI, reviews, or comments without polling.
T3: `watch_pull_request`, then end the turn. It wakes on a failed check, required checks passing, another person's comment or review, or a new conflict. A merge ends the watch without a wake, so pair it with a `schedule_task` heartbeat when waiting for a merge. `scripts/watch-pr` stays the source of the verdict. Call `unwatch_pull_request` before handing work back.

## Transcripts and state

### transcripts
Intent: read this chat, a subagent's chat, or past chats.
Cursor: `~/.cursor/projects/<slug>/agent-transcripts/`.
T3: `t3_thread_read` with `threadId: <parentThreadId>` (page with `afterPosition`, `view: "activity"` for tool calls), or a child's `childThreadId`. Search with `t3_thread_search`, without a `projectId`.

### store
Intent: a scratch folder shared by a coordinator and its worktree children.
Cursor: the agent's store, given in the system prompt.
T3: `~/.local/state/pstack/<repo>/`, where `<repo>` is `basename "$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"`. Create it if missing.

### paths
Intent: where skills and always-on rules live.
Cursor: `.cursor/skills/`, `~/.cursor/skills/`, `~/.cursor/plugins/`, `.cursor/rules/*.mdc`.
T3: project skills are `.agents/skills/` (Claude Code reads them through `.claude/skills/`). Always-on project rules go in `AGENTS.md` (Claude Code: `CLAUDE.md`).

## Verification surfaces

### verify-surface
Intent: drive the real app to prove a change.
Cursor: `control-ui`, `control-cli` (from cursor-team-kit), Cursor's `mcps/` folder.
T3: the project's own verification skill if it has one. Otherwise, for a UI, T3's `preview_*` tools (`preview_open`, `preview_navigate`, `preview_snapshot`, `preview_click`, `preview_type`, `preview_evaluate`; `preview_snapshot` with `save: true` for a screenshot the user can see). For a CLI, drive it from the shell. MCP servers are whatever is in your tool list.

### team-kit
Intent: some steps use skills from Cursor's separate `cursor-team-kit` plugin. They may not be installed.
Cursor: "the `deslop` skill from the `cursor-team-kit` plugin", "`control-ui` from `cursor-team-kit`".
T3: drop the plugin name. `deslop` becomes "`/deslop`, if it is installed". `control-ui` and `control-cli` follow rule `verify-surface`.

### create-skill
Intent: authoring a skill uses the skill-writing skill the agent has.
Cursor: `create-skill` (Cursor's built-in skill-authoring skill), `/create-skill`.
T3: "the `skill-creator` skill, if it is installed". Codex bundles it, and Claude Code gets it as a plugin. Labels and templates that name `create-skill` name `skill-creator`.

### unshipped-link
Intent: don't point agents or users at files that aren't installed.
Cursor: relative links to `docs/guide/` pages or pstack's `README.md`.
T3: drop the link and keep the sentence if it still says something on its own; otherwise drop the sentence.

## Cursor-only

### cursor-only
Intent: remove steps that cannot happen here, so they don't distract.
Cursor: automations, cloud agents and their VMs, the agents dashboard, Ask mode and `allow_multiple` question options, workspace-scoped transcript paths, a Cursor restart, Cursor's pull request tool, skill frontmatter keys only Cursor reads.
T3: delete the step or clause. Bugbot is a GitHub app, so its PR comments can still appear: keep Bugbot triage, but call it Bugbot, not Cursor Bugbot.
