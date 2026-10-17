#!/usr/bin/env python3
"""Sync upstream pstack into vendor/, patch it from patchbook/, and build dist/skills/ for the `skills` CLI."""

import argparse
import difflib
import hashlib
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
PATCHBOOK = REPO / "patchbook"
ENTRIES = PATCHBOOK / "entries"
MODELS_JSON = REPO / "models.json"
DIST = REPO / "dist"
CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "wstack" / "upstream"

# docs/ and automations/ are for Cursor users. No T3 skill reads them.
SHIPPED = ("skills/", "agents/", "LICENSE")
SUPPORT_SKILL = "pstack"
SUPPORT_SKILL_MD = """---
name: pstack
description: Subagent briefs the other pstack skills hand to their subagents. Not a task skill.
disable-model-invocation: true
---

# pstack support files

The other pstack skills point here. Nothing to run.
"""
CONFLICT_MARKER = re.compile(r"^(<{7}|>{7}) ", re.MULTILINE)

# A block of shipped Markdown that matches one of these needs a patchbook entry.
CURSOR_TERMS = re.compile("|".join([
    r"\bCursor\b", r"\.cursor\b", r"cursor-(?:team-kit|grok)", r"\bTask\b", r"subagent_type",
    r"\breadonly\b", r"run_in_background", r"is_background", r"cloud_base_branch",
    r'environment: ?"', r"AskQuestion", r"\.mdc\b", r"\b[Gg]rok\b", r"\bcomposer-", r"\bComposer\b",
    r"claude-opus-\d+-\d+-", r"agent-transcripts", r"/loop\b", r"[Cc]loud agent",
    r"control-(?:ui|cli)", r"mcps/", r"[Tt]odo ?list", r"generalPurpose",
    r"\bcreate-skill\b", r"fast or standard", r"\bVMs?\b", r"allow_multiple", r"workspace-scoped",
    r"docs/guide/", r"\.\./README\.md",
]))
PLACEHOLDER = re.compile(r"\{\{(model|snippet):([^}]+)\}\}")
ENTRY_KINDS = ("translation", "policy", "keep")


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


# patchbook

FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
ENTRY_HEAD = re.compile(r"^=== entry ([0-9a-f]{12})$")
ENTRY_FIELDS = ("kind", "rules", "intent")


def block_hash(block):
    return hashlib.sha256(block.encode()).hexdigest()[:12]


def block_spans(lines):
    """Line ranges of a Markdown file's blocks: the frontmatter, then each run of non-blank lines.

    Blank lines inside a code fence don't end a block.
    """
    spans, first = [], 0
    if lines and lines[0] == "---" and "---" in lines[1:]:
        first = lines.index("---", 1) + 1
        spans.append((0, first))
    start, fence = None, None
    for i in range(first, len(lines)):
        stripped = lines[i].strip()
        m = FENCE.match(lines[i])
        if fence is None and m:
            fence = m.group(1)
        elif fence and set(stripped) == {fence[0]} and len(stripped) >= len(fence):
            fence = None
        if stripped or fence:
            start = i if start is None else start
        elif start is not None:
            spans.append((start, i))
            start = None
    if start is not None:
        spans.append((start, len(lines)))
    return spans


def entries_path(rel):
    return ENTRIES / f"{rel}.entries"


def read_entries(path):
    """Parse an entries file into {hash: entry}. Field problems are left for check_entry."""
    entries, entry, section, last_field = {}, None, None, None
    for n, line in enumerate(path.read_text().split("\n"), 1):
        m = ENTRY_HEAD.match(line)
        if m:
            if m.group(1) in entries:
                raise Fail(f"{path.relative_to(REPO)}:{n}: duplicate entry {m.group(1)}")
            entry = entries[m.group(1)] = {"hash": m.group(1), "line": n, "upstream": [], "patched": []}
            entry.update((f, "") for f in ENTRY_FIELDS)
            section, last_field = "fields", None
        elif entry is None:
            if line.strip():
                raise Fail(f"{path.relative_to(REPO)}:{n}: text before the first entry")
        elif line in ("--- upstream", "--- patched"):
            section = line[4:]
        elif section == "fields":
            field, sep, value = line.partition(": ")
            if field in ENTRY_FIELDS and sep:
                entry[field] = value.strip()
                last_field = field
            elif line.strip() and last_field == "intent":
                entry["intent"] += " " + line.strip()
            elif line.strip():
                raise Fail(f"{path.relative_to(REPO)}:{n}: expected one of {', '.join(ENTRY_FIELDS)}")
        else:
            entry[section].append(line)
    for entry in entries.values():
        for section in ("upstream", "patched"):
            entry[section] = "\n".join(entry[section]).strip("\n")
    return entries


def format_entry(entry):
    return (
        f"=== entry {entry['hash']}\n"
        + "".join(f"{f}: {entry[f]}\n" for f in ENTRY_FIELDS)
        + f"--- upstream\n{entry['upstream']}\n--- patched\n{entry['patched']}\n"
    )


def check_entry(entry):
    """What is wrong with an entry's fields, if anything."""
    if block_hash(entry["upstream"]) != entry["hash"]:
        return "its upstream text does not match its hash"
    if entry["kind"] not in ENTRY_KINDS:
        return f"kind must be one of {', '.join(ENTRY_KINDS)}"
    if not entry["intent"]:
        return "it has no intent"
    if entry["kind"] == "translation" and not entry["rules"]:
        return "a translation must name its rules"
    if entry["kind"] == "keep" and entry["patched"] != entry["upstream"]:
        return "a keep entry must leave the block unchanged"
    return None


def read_snippets():
    snippets, name = {}, None
    for line in (PATCHBOOK / "snippets.md").read_text().split("\n"):
        if line.startswith("## "):
            name = line[3:].strip()
            snippets[name] = []
        elif name:
            snippets[name].append(line)
    return {k: "\n".join(v).strip() for k, v in snippets.items()}


def read_models():
    models = json.loads(MODELS_JSON.read_text())
    return {k: v for k, v in models.items() if not k.startswith("_")}


def expand(text, models, snippets, problems, where):
    def fill(m):
        kind, name = m.group(1), m.group(2)
        if kind == "model" and name in models:
            return ", ".join(f"`{e}`" for e in models[name])
        if kind == "snippet" and name in snippets:
            return snippets[name]
        problems.append({"problem": "placeholder", **where, "detail": f"unknown {kind} {name!r}"})
        return m.group(0)
    return PLACEHOLDER.sub(fill, text)


def nearest(block, candidates, limit=2):
    scored = sorted(
        ((difflib.SequenceMatcher(None, block, c["upstream"]).ratio(), c) for c in candidates),
        key=lambda pair: -pair[0],
    )
    return [{"line": c["line"], "hash": c["hash"], "similarity": round(r, 2)} for r, c in scored[:limit] if r >= 0.4]


def patch_tree(staged):
    """Apply the patchbook to staged/, in place: every shipped Markdown file, plus any other
    shipped file that has an entries file (scripts). Only Markdown is checked for Cursor terms.

    Returns the problems found, each a dict with a "problem" key: missing, orphan, invalid,
    placeholder, or leak (a Cursor term left in the output).
    """
    models, snippets = read_models(), read_snippets()
    problems, applied = [], 0
    unread = {p.relative_to(ENTRIES).as_posix()[: -len(".entries")]: p for p in ENTRIES.rglob("*.entries")}
    patched_files = set(staged.rglob("*.md")) | {staged / rel for rel in unread if (staged / rel).is_file()}
    for path in sorted(patched_files):
        rel = path.relative_to(staged).as_posix()
        markdown = path.suffix == ".md"
        entries = read_entries(unread.pop(rel)) if rel in unread else {}
        lines = path.read_text().split("\n")
        spans = block_spans(lines)
        out, prev, used, unmatched = [], 0, set(), []
        for i, (start, end) in enumerate(spans):
            block = "\n".join(lines[start:end])
            h = block_hash(block)
            where = {"file": rel, "line": start + 1, "hash": h}
            out.extend(lines[prev:start])
            prev = end
            entry = entries.get(h)
            if entry is None:
                unmatched.append({"line": start + 1, "hash": h, "upstream": block})
                terms = sorted({m.group(0) for m in CURSOR_TERMS.finditer(block)}) if markdown else []
                if terms:
                    problems.append({"problem": "missing", **where, "terms": terms, "upstream": block})
                out.extend(lines[start:end])
                continue
            used.add(h)
            error = check_entry(entry)
            if error:
                problems.append({"problem": "invalid", **where, "detail": error})
            applied += 1
            patched = expand(entry["patched"], models, snippets, problems, where)
            if markdown and entry["kind"] != "keep":
                terms = sorted({m.group(0) for m in CURSOR_TERMS.finditer(patched)})
                if terms:
                    problems.append({"problem": "leak", **where, "terms": terms})
            if patched:
                out.extend(patched.split("\n"))
            elif i + 1 < len(spans):
                prev = spans[i + 1][0]  # drop the blank lines after a deleted block
        out.extend(lines[prev:])
        path.write_text("\n".join(out))
        for h, entry in entries.items():
            if h not in used:
                problems.append(orphan(rel, entry, unmatched))
    for rel, entries_file in unread.items():
        for entry in read_entries(entries_file).values():
            problems.append(orphan(rel, entry, []))
    return problems, applied


def orphan(rel, entry, candidates):
    return {
        "problem": "orphan", "file": rel, "hash": entry["hash"], "kind": entry["kind"],
        "rules": entry["rules"], "intent": entry["intent"], "upstream": entry["upstream"],
        "patched": entry["patched"], "nearest": nearest(entry["upstream"], candidates),
    }


def describe(problem):
    p = problem
    at = f"{p['file']}:{p.get('line', '?')} [{p['hash']}]"
    if p["problem"] == "missing":
        return f"missing  {at} needs an entry ({', '.join(p['terms'])})"
    if p["problem"] == "leak":
        return f"leak     {at} still says {', '.join(p['terms'])}"
    if p["problem"] == "orphan":
        near = ", ".join(f"line {n['line']} [{n['hash']}] {n['similarity']}" for n in p["nearest"]) or "none"
        return f"orphan   {p['file']} [{p['hash']}] intent: {p['intent']}\n         nearest new blocks: {near}"
    return f"{p['problem']:<8} {at}: {p['detail']}"


# build


def stage_shipped(files, dest):
    for f in files:
        if str(f).startswith(SHIPPED):
            (dest / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(VENDOR / f, dest / f)


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
    shutil.copytree(staged / "agents", support / "agents")
    shutil.copy2(staged / "LICENSE", support / "LICENSE")

    for skill_md in sorted(out.glob("*/SKILL.md")):
        if skill_md.parent == support:
            continue
        front, body = frontmatter_split(skill_md.read_text())
        # The skills CLI names each install folder after `name`, and Codex matches `$name` against it.
        front = re.sub(r"^name: .*$", f"name: {skill_md.parent.name}", front, count=1, flags=re.MULTILINE)
        skill_md.write_text(front + body)

    # Bun installs packages next to these, inside the user's project.
    for package_json in out.glob("*/scripts/package.json"):
        (package_json.parent / ".gitignore").write_text("node_modules/\n")

    for path in out.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".ts", ".mjs", ".sh", ".json"}:
            if CONFLICT_MARKER.search(path.read_text(errors="replace")):
                raise Fail(f"conflict marker in {path.relative_to(REPO)}")


def checked_vendor():
    files, tree = vendor_files_and_tree()
    pin = read_upstream()
    if tree != pin["tree"]:
        raise Fail(
            f"vendor/ (tree {tree[:7]}) differs from upstream.json (tree {pin['tree'][:7]}). "
            "Never edit vendor/ by hand. Record the change in patchbook/, or run sync."
        )
    return files, pin


def cmd_build(args):
    files, pin = checked_vendor()
    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp)
        stage_shipped(files, staged)
        problems, applied = patch_tree(staged)
        if problems:
            for p in problems:
                print(describe(p), file=sys.stderr)
            raise Fail(f"{len(problems)} problems; nothing built. See patchbook/patch.md.")
        build_tree(staged)
    print(f"built dist/skills/ from {pin['commit'][:7]} with {applied} patchbook entries")


def cmd_status(args):
    files, pin = checked_vendor()
    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp)
        stage_shipped(files, staged)
        problems, applied = patch_tree(staged)
    if args.json:
        print(json.dumps({"upstream": pin["commit"], "applied": applied, "problems": problems}, indent=2))
    else:
        for p in problems:
            print(describe(p))
        counts = {}
        for p in problems:
            counts[p["problem"]] = counts.get(p["problem"], 0) + 1
        summary = ", ".join(f"{n} {k}" for k, n in sorted(counts.items())) or "no problems"
        print(f"{applied} entries apply at {pin['commit'][:7]}; {summary}")
    return 1 if problems else 0


def cmd_scaffold(args):
    """Append a skeleton entry for each missing block, to be filled in by hand or by an agent."""
    files, _ = checked_vendor()
    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp)
        stage_shipped(files, staged)
        problems, _ = patch_tree(staged)
    missing = [p for p in problems if p["problem"] == "missing" and (not args.file or p["file"] in args.file)]
    by_file = {}
    for p in missing:
        by_file.setdefault(p["file"], []).append(p)
    for rel, blocks in by_file.items():
        path = entries_path(rel)
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text().rstrip("\n") + "\n\n" if path.exists() else ""
        skeletons = [
            format_entry({"hash": p["hash"], "kind": "translation", "rules": "", "intent": "",
                          "upstream": p["upstream"], "patched": p["upstream"]})
            for p in blocks
        ]
        path.write_text(existing + "\n".join(skeletons))
    print(f"scaffolded {len(missing)} entries in {len(by_file)} files")
    return 0


def main():
    parser = argparse.ArgumentParser(prog="wstack")
    sub = parser.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sync", help="replace vendor/ with an upstream commit")
    s.add_argument("ref", nargs="?", default="main")
    s.set_defaults(func=cmd_sync)
    b = sub.add_parser("build", help="build dist/skills/ from vendor/ and patchbook/")
    b.set_defaults(func=cmd_build)
    st = sub.add_parser("status", help="list missing, orphaned, and invalid patchbook entries")
    st.add_argument("--json", action="store_true", help="machine-readable output, with block text")
    st.set_defaults(func=cmd_status)
    sc = sub.add_parser("scaffold", help="append skeleton entries for missing blocks")
    sc.add_argument("file", nargs="*", help="only these upstream files, such as skills/arena/SKILL.md")
    sc.set_defaults(func=cmd_scaffold)
    args = parser.parse_args()
    try:
        sys.exit(args.func(args) or 0)
    except Fail as e:
        print(f"wstack: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
