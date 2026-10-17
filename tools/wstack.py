#!/usr/bin/env python3
"""Sync upstream pstack into vendor/, build dist/<agent>/, and install a build."""

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

AGENTS = {
    "claude-code": {"skills_dir": Path.home() / ".claude" / "skills"},
    "codex": {"skills_dir": Path.home() / ".agents" / "skills"},
}
# docs/guide is the human guide (2.4 MB of images). No skill reads it.
SHIPPED = ("skills/", "agents/", "docs/harness/", "LICENSE", "README.md", ".gitignore")
ROOT_PLACEHOLDER = "{{PSTACK_ROOT}}"
PATCH_HEADER_FIELDS = ["Kind", "Why", "Source", "Upstream"]
CONFLICT_MARKER = re.compile(r"^(<{7}|>{7}) ", re.MULTILINE)
INSTALL_MANIFEST = ".wstack-install.json"


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


def preamble(agent):
    return (
        f"> **pstack install note.** `<pstack>` is `{ROOT_PLACEHOLDER}`. Once per session, "
        f"before following this skill, read `{ROOT_PLACEHOLDER}/adapters/{agent}.md`. "
        f"It maps the Cursor names below to this agent.\n\n"
    )


def build_agent(agent, staged):
    out = DIST / agent
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(staged, out)
    (out / "adapters").mkdir()
    shutil.copy2(REPO / "adapters" / "agents" / f"{agent}.md", out / "adapters" / f"{agent}.md")
    shutil.copy2(REPO / "adapters" / "hosts" / "t3.md", out / "adapters" / "t3.md")

    for skill_md in sorted((out / "skills").glob("*/SKILL.md")):
        front, body = frontmatter_split(skill_md.read_text())
        skill_md.write_text(front + "\n" + preamble(agent) + body.lstrip("\n"))
        if agent == "codex" and re.search(r"^disable-model-invocation: true$", front, re.MULTILINE):
            yaml = skill_md.parent / "agents" / "openai.yaml"
            if yaml.exists():
                raise Fail(f"{yaml.relative_to(out)} already exists upstream; merge it instead")
            yaml.parent.mkdir()
            yaml.write_text("policy:\n  allow_implicit_invocation: false\n")

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
        for agent in AGENTS:
            build_agent(agent, staged)
    print(f"built dist/ from {pin['commit'][:7]} with {len(read_series())} patches")


# install


def cmd_install(args):
    agent = args.agent
    src = DIST / agent
    if not src.exists():
        raise Fail(f"dist/{agent} does not exist. Run build first.")
    root = Path(args.root or Path.home() / ".local" / "share" / "wstack" / agent).expanduser().resolve()
    skills_dir = Path(args.skills_dir or AGENTS[agent]["skills_dir"]).expanduser()

    previous = root / INSTALL_MANIFEST
    old_skills = set()
    if previous.exists():
        old = json.loads(previous.read_text())
        if old["skills_dir"] == str(skills_dir):
            old_skills = set(old["skills"])
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(src, root, symlinks=True)
    for md in root.rglob("*.md"):
        text = md.read_text()
        if ROOT_PLACEHOLDER in text:
            md.write_text(text.replace(ROOT_PLACEHOLDER, str(root)))

    skills_dir.mkdir(parents=True, exist_ok=True)
    installed, skipped = [], []
    for skill in sorted(p for p in (root / "skills").iterdir() if p.is_dir()):
        link = skills_dir / skill.name
        if link.is_symlink() and Path(os.readlink(link)).is_relative_to(root):
            link.unlink()
        elif link.exists() or link.is_symlink():
            skipped.append(skill.name)
            continue
        link.symlink_to(skill, target_is_directory=True)
        installed.append(skill.name)
    for name in old_skills - set(installed):
        link = skills_dir / name
        if link.is_symlink() and Path(os.readlink(link)).is_relative_to(root):
            link.unlink()

    upstream = read_upstream()
    previous.write_text(json.dumps(
        {"agent": agent, "commit": upstream["commit"], "skills_dir": str(skills_dir), "skills": installed},
        indent=2,
    ) + "\n")
    print(f"installed {len(installed)} {agent} skills into {skills_dir} (files in {root})")
    if skipped:
        print(f"skipped {len(skipped)} that already exist and are not ours: {', '.join(skipped)}")


def main():
    parser = argparse.ArgumentParser(prog="wstack")
    sub = parser.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sync", help="replace vendor/ with an upstream commit")
    s.add_argument("ref", nargs="?", default="main")
    s.set_defaults(func=cmd_sync)
    b = sub.add_parser("build", help="build dist/<agent>/ from vendor/, patches/ and adapters/")
    b.set_defaults(func=cmd_build)
    i = sub.add_parser("install", help="install dist/<agent>/ and link its skills")
    i.add_argument("agent", choices=AGENTS)
    i.add_argument("--skills-dir", help="default: the agent's user skills folder")
    i.add_argument("--root", help="where the files live, default ~/.local/share/wstack/<agent>")
    i.set_defaults(func=cmd_install)
    args = parser.parse_args()
    try:
        args.func(args)
    except Fail as e:
        print(f"wstack: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
