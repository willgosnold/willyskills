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
| `dist/skills/` | Build output, one folder per skill, plus a `pstack` folder holding the adapters and agent briefs. Never edit it. |
| `tools/wstack.py` | Sync and build. |

## Use

Install into a project with the [`skills` CLI](https://github.com/vercel-labs/skills). Take every skill: they read each other, and the `pstack` folder.

```sh
cd <project>
npx skills add <path-to-wstack>/dist --skill '*' -a claude-code -a codex
```

This puts one copy of each skill in `.agents/skills/`, which Codex reads, and symlinks `.claude/skills/` to it. Invoke `/poteto-mode` in Claude Code and `$poteto-mode` in Codex. pstack's own scripts need [Bun](https://bun.sh).

Maintaining the build needs Python 3.9+ and git:

```sh
tools/wstack.py sync [ref]   # replace vendor/ with upstream <ref> (default main)
tools/wstack.py build        # vendor/ + patches/ + adapters/ -> dist/skills/
```

`build` fails if `vendor/` differs from `upstream.json`, if a patch lacks its header or doesn't apply, or if a conflict marker reaches `dist/`. A build at an unchanged pin leaves `git status` clean.
