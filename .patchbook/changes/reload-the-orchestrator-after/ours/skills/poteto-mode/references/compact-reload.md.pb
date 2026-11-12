# Reloading the orchestrator after compaction

Auto-compaction truncates long skills, so the coordinator loses `SKILL.md`, the Orchestrate playbook, and its live state. This restores them for the coordinator session only.

Two hooks do it. The `PreToolUse` hook in this skill's frontmatter records the session id the first time the skill runs a tool, in `$CLAUDE_PROJECT_DIR/.claude/orchestrator-session`. A `SessionStart` hook for `compact` must live in the project's `.claude/settings.json`, because a `compact` hook in skill frontmatter never fires. It reads the session id and prints a reload directive only when it matches. Another session on the project gets nothing. A later session that runs this skill overwrites the id, so one orchestrator per project.

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/orchestrator-reload.sh 2>/dev/null || true",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

Save as `.claude/hooks/orchestrator-reload.sh`. Hook stdout is capped at 10,000 characters, so the script prints paths and an order to Read them, then as much of the state file as fits:

```bash
#!/usr/bin/env bash
set -u
dir=${CLAUDE_PROJECT_DIR:-$PWD}
id=$(jq -r '.session_id // empty' 2>/dev/null)
[ -n "$id" ] && [ "$id" = "$(cat "$dir/.claude/orchestrator-session" 2>/dev/null)" ] || exit 0

skill=$dir/.claude/skills/poteto-mode
state=$dir/.claude/orchestrator-state.md
budget=9500
out=
if [ -f "$skill/SKILL.md" ]; then
  out="You are the poteto-mode orchestrator and your context was just compacted. Before any other tool call, Read these two files in full:
$skill/SKILL.md
$skill/playbooks/orchestrate.md
"
fi
if [ -s "$state" ]; then
  body=$(cat "$state")
  room=$((budget - ${#out} - 200))
  head="Your live state follows, from $state:
"
  if [ "${#body}" -gt "$room" ]; then
    body="${body:0:$room}"
    head="Your live state follows, from $state. TRUNCATED to $room characters; Read the file for the rest:
"
  fi
  out="$out
$head$body
"
fi
[ -n "$out" ] && printf '%s' "$out"
exit 0
```

The coordinator rewrites `.claude/orchestrator-state.md` whenever the program's state changes. Gitignore it and `.claude/orchestrator-session`.
