# Testing a willystack build

Run these after `patchbook build`, before the review. They check that agents in T3 can load the built skills and follow them. Both run in the sandbox project, `~/Projects/pstack-phase0-sandbox` (T3 project "pstack-phase0-sandbox"). Its `main` has a known bug: `ledger summary --month` ignores the year.

## Set up

For each check, make a worktree of the sandbox from `main` and install this build into it:

```sh
S=~/Projects/pstack-phase0-sandbox
B=pbtest-$(date +%Y%m%d)-claude    # and -codex for the second check
git -C $S worktree add -q ~/.t3/worktrees/pstack-phase0-sandbox/$B -b $B main
cd ~/.t3/worktrees/pstack-phase0-sandbox/$B
npx -y skills@1.7.2 add <this willystack checkout> --skill '*' -a claude-code -a codex -y
git add -A && git commit -qm "Install the willystack build under test"
```

Install before the thread starts: agents load skills when a session begins.

## Run

Start each check with `t3_thread_launch` in the sandbox project, with `workspaceStrategy: {type: "existing_worktree", worktreePath, branch}`:

| Check | Model | Message |
| --- | --- | --- |
| Claude | `claudeAgent`, `claude-opus-5-5`, effort `medium` | `/poteto-mode The monthly summary in ledger/summary.py puts some transactions in the wrong year. Fix it and commit locally. Don't push or open a PR.` |
| Codex | `codex`, `gpt-6.1-sol`, reasoningEffort `low` | The same message, starting `$poteto-mode`. |

If upstream changed a skill that can run against this repo (not `poteto-mode`), add one Claude check of that skill with a small task that exercises the changed part.

Wait with `t3_thread_wait`. If a turn ends on an API error, such as `apply Claude credential metadata`, send "continue" once.

## Pass

A check passes when the thread:

- opened the skill and followed its playbook, without looking for a tool, path, or command that doesn't exist here;
- wrote a failing test first, then the fix, and `python -m unittest` passes;
- in Codex, delegated through `delegate_task`.

Read the thread with `t3_thread_read` (view `activity`) to judge this, not just the last message.

## Clean up

Archive the threads, then remove each worktree and its branch:

```sh
git -C ~/Projects/pstack-phase0-sandbox worktree remove --force ~/.t3/worktrees/pstack-phase0-sandbox/$B
git -C ~/Projects/pstack-phase0-sandbox branch -D $B
```
