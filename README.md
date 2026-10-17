<img src="assets/icon.svg" width="64" height="64" alt="">

# wstack

Created in [T3 Code](https://t3.codes).

[pstack](https://github.com/cursor/plugins/tree/main/pstack), Lauren Tan's skills for Cursor, rewritten for Claude Code and Codex running in T3 Code. The build replaces each upstream paragraph that uses Cursor's names with one that uses T3's, so agents read only the finished skills. Every change, and the intent behind it, is recorded in `patchbook/`.

## Layout

| Path | What it is |
| --- | --- |
| `vendor/pstack/` | Upstream, byte for byte. Never edit it. |
| `upstream.json` | The pinned upstream commit and its tree hash. |
| `patchbook/` | Every change to upstream: `patch.md` (the rules and the entry format), `snippets.md`, `entries/` (one file per upstream file), `retired.md`. |
| `models.json` | The default model for each pstack role. A project's `.agents/pstack-models.md` overrides it line by line (`/setup-pstack` writes that file). |
| `dist/skills/` | Build output, one folder per skill, plus a `pstack` folder holding the subagent briefs. Never edit it. |
| `tools/wstack.py` | Sync, status, scaffold, and build. |

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
tools/wstack.py status       # list blocks missing an entry, orphaned entries, and leftover Cursor terms (--json for agents)
tools/wstack.py scaffold     # append a skeleton entry for each missing block
tools/wstack.py build        # vendor/ + patchbook/ + models.json -> dist/skills/
```

`build` fails if `vendor/` differs from `upstream.json`, if `status` reports any problem, or if a conflict marker reaches `dist/`. A build at an unchanged pin leaves `git status` clean. After a sync, run `status` and resolve what it lists as `patchbook/patch.md` describes.
