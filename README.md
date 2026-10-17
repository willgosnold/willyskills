<img src="assets/icon.svg" width="64" height="64" alt="">

# wstack

Created in [T3 Code](https://t3.codes).

[pstack](https://github.com/cursor/plugins/tree/main/pstack), Lauren Tan's skills for Cursor, packaged for Claude Code and Codex running in T3 Code. Upstream text stays unchanged. Adapters map Cursor's names to each agent and to T3.

## Layout

| Path | What it is |
| --- | --- |
| `vendor/pstack/` | Upstream, byte for byte. Never edit it. |
| `upstream.json` | The pinned upstream commit and its tree hash. |
| `adapters/agents/` | Agent adapters: `claude-code.md` (on top of upstream's own) and `codex.md`. |
| `adapters/hosts/t3.md` | The T3 Code adapter: subagents, models, schedules, pull requests. |
| `patches/` | Policy changes to upstream, applied in `series` order. Empty so far. |
| `dist/<agent>/` | Build output. Never edit it. |
| `tools/wstack.py` | Sync, build and install. |

## Use

Needs Python 3.9+ and git. pstack's own scripts need [Bun](https://bun.sh).

```sh
tools/wstack.py sync [ref]        # replace vendor/ with upstream <ref> (default main)
tools/wstack.py build             # vendor/ + patches/ + adapters/ -> dist/
tools/wstack.py install codex --skills-dir <repo>/.agents/skills
tools/wstack.py install claude-code --skills-dir <repo>/.claude/skills
```

`install` copies `dist/<agent>/` to `~/.local/share/wstack/<agent>/` and links each skill into the skills folder. Without `--skills-dir` it uses the agent's user folder (`~/.claude/skills` or `~/.agents/skills`). It never replaces a skill it didn't install.

Invoke skills with `/poteto-mode` in Claude Code and `$poteto-mode` in Codex.

`build` fails if `vendor/` differs from `upstream.json`, if a patch lacks its header or doesn't apply, or if a conflict marker reaches `dist/`. A build at an unchanged pin leaves `git status` clean.
