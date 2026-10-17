<img src="assets/icon.svg" width="64" height="64" alt="">

# wstack

Created in [T3 Code](https://t3.codes).

[pstack](https://github.com/cursor/plugins/tree/main/pstack), Lauren Tan's skills for Cursor, rewritten for Claude Code and Codex running in T3 Code. The build replaces each upstream paragraph that uses Cursor's names with one that uses T3's, so agents read only the finished skills. Every change, and the intent behind it, is recorded in `patchbook/`.

## Layout

| Path | What it is |
| --- | --- |
| `.patchbook/` | Every change to upstream, for the [patchbook](https://github.com/willgosnold/patchbook) CLI: `config.toml` (the upstreams and their mounts), `upstream.lock` (the pins), `blocks/` (paragraph edits, one file per upstream file), `changes/` (file edits and moves), `patch.md` (the rules for writing them), `hooks.py`, `testing.md`. |
| `models.json` | The default model for each pstack role. A project's `.agents/pstack-models.md` overrides it line by line (`/setup-pstack` writes that file). |
| `skills/` | Build output, one folder per skill, plus a `pstack` folder holding the subagent briefs. Never edit it. |
| `tools/update-projects.sh` | Runs `npx skills update` in every project under `~/Projects` that installed wstack, then commits and pushes the result. |

## Use

Install into a project with the [`skills` CLI](https://github.com/vercel-labs/skills). Take every skill: they read each other, and the `pstack` folder.

```sh
cd <project>
npx skills add willgosnold/wstack --skill '*' -a claude-code -a codex   # or a local checkout's path
```

This puts one copy of each skill in `.agents/skills/`, which Codex reads, and symlinks `.claude/skills/` to it. Invoke `/poteto-mode` in Claude Code and `$poteto-mode` in Codex. pstack's own scripts need [Bun](https://bun.sh).

Maintaining the build needs the [patchbook](https://github.com/willgosnold/patchbook) CLI:

```sh
patchbook check              # has upstream pstack moved? exits 10 if so
patchbook sync [pstack ref]  # move the pin to upstream (or <ref>) and carry the changes forward
patchbook status             # list what broke (--json for agents)
patchbook scaffold           # append a skeleton entry for each missing block
patchbook blocks <f>         # print an upstream file's blocks and hashes
patchbook upstream pstack    # read pstack at the pin: a file, --diff of the last sync, or --export <dir>
patchbook build              # pinned pstack + .patchbook/ + models.json -> skills/
```

`build` fails if `status` reports any problem, or if a conflict marker reaches `skills/`. A build at an unchanged pin leaves `git status` clean. After a sync, resolve what `status` lists as `.patchbook/patch.md` describes.

A daily T3 scheduled task does this on its own with the `patchbook-update` skill: it syncs, repairs, builds, tests (`.patchbook/testing.md`), reviews, merges, and runs `tools/update-projects.sh`. It asks you only when it can't decide.
