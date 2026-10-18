#!/usr/bin/env bash
# Reinstall willystack's skills from GitHub in every project that installed them, then commit and push.
# Touches only willystack's skills. Skips a project that isn't on its default branch, has staged
# changes, or can't fast-forward, and says why.
#
# Usage: tools/update-projects.sh [root ...]   (default: ~/Projects)

set -uo pipefail

SOURCE="willgosnold/willystack"
OLD_SOURCE="willgosnold/wstack"   # the repo's name before the rename; old installs still record it
SKILLS=(npx -y skills@1.7.2)
WILLYSTACK=$(cd "$(dirname "$0")/.." && pwd)
VERSION=$(git -C "$WILLYSTACK" rev-parse --short HEAD)
ROOTS=("${@:-$HOME/Projects}")

installed_from_willystack() {
  python3 - "$1" "$SOURCE" "$OLD_SOURCE" <<'PY'
import json, sys
lock = json.load(open(sys.argv[1]))
print("\n".join(n for n, s in lock.get("skills", {}).items() if s.get("source") in sys.argv[2:]))
PY
}

failed=0
while IFS= read -r lock; do
  repo=$(dirname "$lock")
  names=$(installed_from_willystack "$lock")
  [ -n "$names" ] || continue
  skip() { echo "skipped  $repo: $1"; failed=1; }

  branch=$(git -C "$repo" branch --show-current)
  default=$(git -C "$repo" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##')
  if [ -n "$default" ] && [ "$branch" != "$default" ]; then skip "on $branch, not $default"; continue; fi
  if ! git -C "$repo" diff --cached --quiet; then skip "has staged changes"; continue; fi
  if [ -n "$default" ] && ! git -C "$repo" pull --ff-only --quiet; then skip "can't fast-forward $branch"; continue; fi

  agents=()
  [ -e "$repo/.claude/skills" ] && agents+=(-a claude-code)
  [ -e "$repo/.agents/skills" ] && agents+=(-a codex)
  [ ${#agents[@]} -gt 0 ] || agents=(-a claude-code -a codex)
  if ! (cd "$repo" && "${SKILLS[@]}" add "$SOURCE" --skill '*' "${agents[@]}" -y >/dev/null 2>&1); then
    skip "npx skills add failed"; continue
  fi
  # Skills upstream dropped: installed from willystack before, no longer in its skills/.
  for name in $names; do
    if [ ! -d "$WILLYSTACK/skills/$name" ]; then
      (cd "$repo" && "${SKILLS[@]}" remove "$name" -y >/dev/null 2>&1) || skip "couldn't remove $name"
    fi
  done

  paths=()
  for p in .agents/skills .claude/skills skills-lock.json; do [ -e "$repo/$p" ] && paths+=("$p"); done
  git -C "$repo" add -A -- "${paths[@]}"
  if git -C "$repo" diff --cached --quiet; then echo "current  $repo"; continue; fi
  git -C "$repo" commit --quiet -m "Update willystack skills to $VERSION

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" -- "${paths[@]}"
  if [ -n "$default" ] && git -C "$repo" push --quiet; then
    echo "updated  $repo (pushed)"
  elif [ -n "$default" ]; then
    skip "committed, but the push failed"
  else
    echo "updated  $repo (committed; no origin to push to)"
  fi
done < <(for root in "${ROOTS[@]}"; do find "$root" -maxdepth 3 -name skills-lock.json -not -path '*/node_modules/*'; done)

exit $failed
