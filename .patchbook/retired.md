# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## skills/poteto-mode/playbooks/orchestrate.md, entries a3856a70a3d4, da6d7e9ea334, 850c1a1d2385

Retired at upstream pstack 1ba91fc, which rewrote the Orchestrate playbook around `notes.md`, worker kickoffs and PR owners, and deleted `scripts/orch/`.

- **a3856a70a3d4** (policy, same-model-review). Intent: a dedicated verifier runs on its worker's model, not a different family, unless the user names another. The block that scaled verification to the unit is gone. The policy still applies and moved to the Topology entry (ca155dd357b3), whose verifier bullet now says "on the same model and effort as the PR's owner".
- **da6d7e9ea334** (translation: isolation, cursor-only). Intent: the lost-work example is a worktree removed or the machine dying, not a cloud VM. Upstream dropped the externalize-the-moment-it-lands block.
- **850c1a1d2385** (translation: stop, cursor-only). Intent: the liveness probe uses `task_status`, and the Cursor-restart bullet becomes a T3 restart. Upstream replaced the list with Supervision bullets that have no Cursor terms: judge a worker by its pushes and PR activity, and retry by cause.
