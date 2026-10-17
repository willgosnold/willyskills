#!/usr/bin/env python3
"""Sync upstream pstack into vendor/ and build dist/skills/ for the `skills` CLI."""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VENDOR = REPO / "vendor" / "pstack"
UPSTREAM_JSON = REPO / "upstream.json"
PATCHES = REPO / "patches"
DIST = REPO / "dist"
CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "wstack" / "upstream"

# docs/guide is the human guide (2.4 MB of images). No skill reads it.
SHIPPED = ("skills/", "agents/", "docs/harness/", "LICENSE", "README.md")
SUPPORT_SKILL = "pstack"
SUPPORT_SKILL_MD = """---
name: pstack
description: Support files the other pstack skills read (agent and T3 adapters, subagent briefs). Not a task skill.
disable-model-invocation: true
---

# pstack support files

The other pstack skills point here. Nothing to run.
"""
PATCH_HEADER_FIELDS = ["Kind", "Why", "Source", "Upstream"]
CONFLICT_MARKER = re.compile(r"^(<{7}|>{7}) ", re.MULTILINE)
PREAMBLE = (
    "> **pstack install note.** Once per session, before following this skill, read your agent's "
    "adapter. It maps the Cursor names below to your agent. Paths are relative to this file's folder. "
    "In Claude Code, read `../pstack/docs/harness/claude-code.md`, then `../pstack/adapters/claude-code.md`. "
    "In Codex, read `../pstack/adapters/codex.md`. If the T3 Code tools are present (`delegate_task`), "
    "also read `../pstack/adapters/t3.md`. Its rows win for subagents, models, schedules, pull "
    "requests, and transcripts.\n\n"
)


class Fail(Exception):
    pass


def git(*args, cwd=REPO, env=None, check=True):
    result = subprocess.run(
        ["git", *args], cwd=cwd, env=env, capture_output=True, text=True
    )
    if check and result.returncode != 0:
        raise Fail(f"git {' '.join(args)} failed:\n{result.stderr.strip()}")
    return result.stdout.strip()


def vendor_files_and_tree():
    """Hash vendor/ as git would commit it, ignoring gitignored files."""
    with tempfile.TemporaryDirectory() as tmp:
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(tmp) / "index")}
        git("read-tree", "--empty", env=env)
        git("add", "--", str(VENDOR.relative_to(REPO)), env=env)
        prefix = f"{VENDOR.relative_to(REPO)}/"
        tree = git("write-tree", f"--prefix={prefix}", env=env)
        files = git("ls-files", "--", prefix, env=env).splitlines()
    return [Path(f).relative_to(prefix) for f in files], tree


def read_upstream():
    return json.loads(UPSTREAM_JSON.read_text())


def frontmatter_split(text):
    if not text.startswith("---\n"):
        return "", text
    end = text.index("\n---\n", 4) + len("\n---\n")
    return text[:end], text[end:]


# sync


def cmd_sync(args):
    pin = read_upstream()
    if not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        git("clone", "--quiet", "--filter=blob:none", pin["remote"], str(CACHE))
    git("fetch", "--quiet", "origin", cwd=CACHE)
    commit = None
    for candidate in (f"origin/{args.ref}", args.ref):
        out = git("rev-parse", "--verify", "--quiet", f"{candidate}^{{commit}}", cwd=CACHE, check=False)
        if out:
            commit = out
            break
    if not commit:
        raise Fail(f"unknown upstream ref: {args.ref}")
    tree = git("rev-parse", f"{commit}:{pin['path']}", cwd=CACHE)
    if tree == pin["tree"]:
        print(f"vendor/ already matches {commit[:7]} (tree {tree[:7]}). Nothing to do.")
        return

    with tempfile.TemporaryDirectory() as tmp:
        archive = subprocess.run(
            ["git", "archive", commit, pin["path"]], cwd=CACHE, capture_output=True, check=True
        ).stdout
        subprocess.run(["tar", "-x", "-C", tmp], input=archive, check=True)
        shutil.rmtree(VENDOR)
        shutil.move(str(Path(tmp) / pin["path"]), VENDOR)

    plugin = json.loads((VENDOR / "plugin.json").read_text())
    pin.update(commit=commit, tree=tree, version=plugin.get("version", "unknown"))
    UPSTREAM_JSON.write_text(json.dumps(pin, indent=2) + "\n")
    _, actual = vendor_files_and_tree()
    if actual != tree:
        raise Fail(f"vendored tree {actual} does not match upstream tree {tree}")
    print(f"vendor/ now at {commit[:7]} (v{pin['version']}). Review with: git diff --stat -- vendor")


# build


def read_series():
    series = PATCHES / "series"
    if not series.exists():
        return []
    names = [l.strip() for l in series.read_text().splitlines()]
    return [PATCHES / n for n in names if n and not n.startswith("#")]


def check_patch_header(patch):
    text = patch.read_text()
    if "\ndiff --git " not in text:
        raise Fail(f"{patch.name} changes nothing")
    head = text.split("\ndiff --git ", 1)[0]
    missing = [f for f in PATCH_HEADER_FIELDS if not re.search(rf"^{f}: \S", head, re.MULTILINE)]
    if missing:
        raise Fail(f"{patch.name} is missing header fields: {', '.join(missing)}")


def stage_patched_tree(files, dest):
    """Copy the shipped part of vendor/ to dest and apply the patch series there."""
    shipped = [f for f in files if str(f).startswith(SHIPPED)]
    for f in shipped:
        (dest / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(VENDOR / f, dest / f)
    patches = read_series()
    if not patches:
        return
    for p in patches:
        check_patch_header(p)
    git("init", "--quiet", cwd=dest)
    git("add", "-A", cwd=dest)
    git("-c", "user.name=wstack", "-c", "user.email=wstack@localhost",
        "commit", "--quiet", "-m", "vendor", cwd=dest)
    for p in patches:
        result = subprocess.run(
            ["git", "apply", "--3way", "--index", str(p)], cwd=dest, capture_output=True, text=True
        )
        if result.returncode != 0:
            raise Fail(f"{p.name} does not apply cleanly:\n{result.stderr.strip()}")
    shutil.rmtree(dest / ".git")


ADAPTER_FILES = {
    "claude-code": ["docs/harness/claude-code.md", "adapters/claude-code.md"],
    "codex": ["adapters/codex.md"],
}


def build_tree(staged):
    out = DIST / "skills"
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(staged / "skills", out)

    support = out / SUPPORT_SKILL
    if support.exists():
        raise Fail(f"upstream now has a skill called {SUPPORT_SKILL}; rename the support skill")
    support.mkdir()
    (support / "SKILL.md").write_text(SUPPORT_SKILL_MD)
    for name in ("agents", "docs", "LICENSE", "README.md"):
        src = staged / name
        (shutil.copytree if src.is_dir() else shutil.copy2)(src, support / name)
    (support / "adapters").mkdir()
    for adapter in [*(REPO / "adapters" / "agents").glob("*.md"), REPO / "adapters" / "hosts" / "t3.md"]:
        shutil.copy2(adapter, support / "adapters" / adapter.name)

    for skill_md in sorted(out.glob("*/SKILL.md")):
        if skill_md.parent == support:
            continue
        front, body = frontmatter_split(skill_md.read_text())
        # The skills CLI names each install folder after `name`, and Codex matches `$name` against it.
        front = re.sub(r"^name: .*$", f"name: {skill_md.parent.name}", front, count=1, flags=re.MULTILINE)
        skill_md.write_text(front + "\n" + PREAMBLE + body.lstrip("\n"))

    # Bun installs packages next to these, inside the user's project.
    for package_json in out.glob("*/scripts/package.json"):
        (package_json.parent / ".gitignore").write_text("node_modules/\n")

    for path in out.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".ts", ".mjs", ".sh", ".json"}:
            if CONFLICT_MARKER.search(path.read_text(errors="replace")):
                raise Fail(f"conflict marker in {path.relative_to(REPO)}")


def cmd_build(args):
    files, tree = vendor_files_and_tree()
    pin = read_upstream()
    if tree != pin["tree"]:
        raise Fail(
            f"vendor/ (tree {tree[:7]}) differs from upstream.json (tree {pin['tree'][:7]}). "
            "Never edit vendor/ by hand. Put the change in patches/, or run sync."
        )
    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp)
        stage_patched_tree(files, staged)
        build_tree(staged)
    print(f"built dist/skills/ from {pin['commit'][:7]} with {len(read_series())} patches")


def main():
    parser = argparse.ArgumentParser(prog="wstack")
    sub = parser.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sync", help="replace vendor/ with an upstream commit")
    s.add_argument("ref", nargs="?", default="main")
    s.set_defaults(func=cmd_sync)
    b = sub.add_parser("build", help="build dist/skills/ from vendor/, patches/ and adapters/")
    b.set_defaults(func=cmd_build)
    args = parser.parse_args()
    try:
        args.func(args)
    except Fail as e:
        print(f"wstack: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
