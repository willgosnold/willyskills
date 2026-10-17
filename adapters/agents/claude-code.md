# pstack in Claude Code (this install)

`<pstack>` means the `pstack` skill folder, which holds `adapters/`, `agents/`, and `docs/`. The other pstack skills are installed beside it, so `<skills>/<name>/SKILL.md` is the skill called `<name>`, where `<skills>` is the parent of `<pstack>`. Give subagents absolute paths. Read `<pstack>/docs/harness/claude-code.md` once per session and map Cursor names with its tables. If the T3 Code MCP tools are present (`delegate_task`), also read `<pstack>/adapters/t3.md`. Its rows replace both files' rows for subagents, scheduling, pull requests, transcripts, and models.

That upstream file assumes pstack is installed as a Claude Code plugin. The `skills` CLI installs each skill as its own folder instead, so these rows replace its rows.

| Upstream `claude-code.md` says | This install |
| --- | --- |
| Tell the user to type `/pstack:<name>` | `/<name>`. Skills have no plugin namespace. |
| `subagent_type: "pstack:poteto-agent"` or `"pstack:comment-sicko"` | No such agent types. Use `general-purpose` and start the brief with "Read `<pstack>/agents/<name>.md` and act as that agent", using an absolute path. |
| `~/.claude/plugins/` (where `poteto-agent` searches for `poteto-mode`) | Your parent gives you the absolute path. If it didn't, stop and say so. |
| The `pstack-models.mdc` rule, and "`setup-pstack` has nothing to write" | In T3 Code, the Models section of `<pstack>/adapters/t3.md` replaces this row. `setup-pstack` writes the project file it names. |
