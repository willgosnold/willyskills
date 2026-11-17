# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## reload-the-orchestrator-after

Retired at pstack e1cc031, with its frontmatter `PreToolUse` hook in poteto-mode's `SKILL.md` (entry 9ab9dbbc3978) and its state-file bullet in the Orchestrate playbook (entry 46658be16fff). Upstream deleted the Orchestrate playbook and its coordinator, so no playbook keeps the state file this hook reloads, and `references/compact-reload.md` would point at `playbooks/orchestrate.md`, which no longer exists.

Intent: Reload the orchestrator after auto-compaction. The frontmatter PreToolUse hook records the coordinator's session id once; the project's settings.json SessionStart compact hook (a compact hook in skill frontmatter does not fire) prints a reload directive and the state file for that session only. The Orchestrate playbook names the state file the coordinator keeps current, and references/compact-reload.md holds the settings snippet and script.

## check-plan-hourly-tick

Retired at pstack e1cc031. Upstream deleted `skills/poteto-mode/scripts/check-plan.mjs` and its test, and the Multi-phase plan playbook no longer has a plan skeleton with a Program checklist or an audit tick. Nothing is left to check.

Intent: The Program checklist must arm an hourly audit tick. The patched plan skeleton arms it with schedule_task and everyMs: 3600000, so check-plan.mjs looks for that instead of /loop 1h. The test's valid-plan fixture keeps in step, in a code span as in a real plan, because the checker rejects a mid-sentence colon in prose.
