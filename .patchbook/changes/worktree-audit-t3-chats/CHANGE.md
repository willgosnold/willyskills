# worktree-audit-t3-chats

intent: LAST_CHAT finds the newest agent chat that operated in each worktree, so a worktree in recent use is never bucketed safe. In T3 the chats are the last 30 days of Claude Code transcripts and Codex rollout files, from every project folder and Codex home, not Cursor's agent-transcripts for this repo. Upstream's match is kept: a transcript counts when it names the worktree path followed by "/" or a quote, so a session that started elsewhere and worked there by absolute path counts, and glint-482 does not match glint-482-r37. Keeps upstream's 4-day recent window and its portable stat and date helpers.

edits:
- file skills/poteto-mode/scripts/worktree-audit.sh
