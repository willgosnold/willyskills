# worktree-audit-t3-chats

intent: LAST_CHAT finds the newest agent chat that ran in each worktree, so a worktree in recent use is never bucketed safe. In T3 the chats are Claude Code's per-directory transcripts and Codex's rollout files (any cwd at or inside the worktree), not Cursor's agent-transcripts. Keeps upstream's 4-day recent window and its guard against prefix matches (glint-482 vs glint-482-r37). stat and date are called so they work on Linux and macOS.

edits:
- file skills/poteto-mode/scripts/worktree-audit.sh
