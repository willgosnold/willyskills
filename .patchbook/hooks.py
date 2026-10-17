"""wstack's rules that a config pattern can't express."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# `/name` for an installed skill, but not a path such as `docs/how` or `/tmp/how`.
SLASH_SKILL = r"(?<![\w/.~-])/({names})\b(?![\w/.-])"
CODEX_SLASH_NOTE = "start with `$`"


def placeholder(kind, name):
    if kind != "model":
        return None
    models = json.loads((ROOT / "models.json").read_text())
    if name.startswith("_") or name not in models:
        return None
    return ", ".join(f"`{e}`" for e in models[name])


_slash = {}


def block_terms(path, block, outputs):
    """Users type `/name` in Claude Code and `$name` in Codex, so a block naming a skill as `/name` gives both."""
    if not path.endswith(".md"):
        return []
    key = frozenset(outputs)
    if key not in _slash:
        names = sorted({p.split("/")[0] for p in outputs if p.endswith("/SKILL.md")}, key=len, reverse=True)
        _slash[key] = re.compile(SLASH_SKILL.format(names="|".join(map(re.escape, names))))
    if CODEX_SLASH_NOTE in block:
        return []
    return sorted({m.group(0) for m in _slash[key].finditer(block) if f"${m.group(1)}" not in block})


def check(outputs):
    problems = []
    for path, data in outputs.items():
        parts = path.split("/")
        if len(parts) == 2 and parts[1] == "SKILL.md":
            m = re.search(rb"^name: (.*)$", data, re.M)
            if not m or m.group(1).decode().strip() != parts[0]:
                problems.append({"problem": "check", "file": path,
                                 "detail": "a skill's name must be its folder name (the skills CLI and Codex's $name use it)"})
        if path.endswith("/scripts/package.json"):
            ignore = outputs.get(path.rsplit("/", 1)[0] + "/.gitignore", b"")
            if b"node_modules/" not in ignore:
                problems.append({"problem": "check", "file": path,
                                 "detail": "gitignore node_modules/ beside it; Bun installs packages in the user's project"})
    return problems
