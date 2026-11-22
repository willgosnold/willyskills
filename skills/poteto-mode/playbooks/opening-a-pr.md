### Opening a PR

Invoked at the end of every other playbook.

Work from a git worktree off trunk, and keep unrelated work out of it. Rebase into small, landable commits. Run the **deslop** skill, if it is installed, over the diff before commit.

Title: `type(scope): subject`, naming a real symbol when one carries the change. Body: a one-minute briefing under 40 lines with these `##` headings in order, dropping empty ones: `## Why`, `## What changed`, `## Scope`, `## Tradeoffs` (only rejected alternatives a reviewer would otherwise ask about), `## Blast Radius`, `## Verification`.

Stack follow-ups by base branch. Open PRs ready, with `gh pr create` without `--draft`, or `origin pr create --status open` when Origin's CLI resolves the repository. Right after creating each PR, one per stack layer, call `link_pull_request` with its URL. Before finishing, check `list_thread_pull_requests`. Opening a PR does not start a babysit.
