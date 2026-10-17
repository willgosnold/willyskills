# pstack in Claude Code (this install)

Read `<pstack>/docs/harness/claude-code.md` once per session and map Cursor names with its tables. If the T3 Code MCP tools are present (`delegate_task`), also read `t3.md` in the same folder as this file. Its rows replace both files' rows for subagents, scheduling, pull requests, transcripts, and models.

That upstream file assumes pstack is installed as a Claude Code plugin. This install puts each skill straight into a skills folder, so these rows replace its rows.

| Upstream `claude-code.md` says | This install |
| --- | --- |
| Tell the user to type `/pstack:<name>` | `/<name>`. Skills have no plugin namespace. |
| `subagent_type: "pstack:poteto-agent"` or `"pstack:comment-sicko"` | No such agent types. Use `general-purpose` and start the brief with "Read `<pstack>/agents/<name>.md` and act as that agent", using an absolute path. |
| `~/.claude/plugins/` (where `poteto-agent` searches for `poteto-mode`) | Your parent gives you the absolute path. If it didn't, stop and say so. |
