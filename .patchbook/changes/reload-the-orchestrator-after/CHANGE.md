# reload-the-orchestrator-after

intent: Reload the orchestrator after auto-compaction. The frontmatter PreToolUse hook records the coordinator's session id once; the project's settings.json SessionStart compact hook (a compact hook in skill frontmatter does not fire) prints a reload directive and the state file for that session only. The Orchestrate playbook names the state file the coordinator keeps current, rewritten each time a worker reports, and references/compact-reload.md holds the settings snippet and script.

edits:
- add skills/poteto-mode/references/compact-reload.md
