# worktree-audit-t3-chats

intent: LAST_CHAT finds the newest agent chat that ran in each worktree, so a worktree in recent use is never bucketed safe. In T3 the chats are Claude Code's session files under ~/.claude/projects and Codex's rollout files under each ~/.codex*/sessions, not Cursor's agent-transcripts. Each session counts for every worktree that one of its recorded cwd values is at or inside, compared as whole paths so glint-482 never matches glint-482-r37, with no age cutoff and paths read NUL-safe. Keeps upstream's 4-day recent window and uses the stat and date flags upstream picks once for Linux or macOS.

edits:
- file skills/poteto-mode/scripts/worktree-audit.sh
