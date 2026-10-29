# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## skills/poteto-mode/playbooks/orchestrate.md, entries a3856a70a3d4, da6d7e9ea334, 850c1a1d2385

Retired at upstream pstack 1ba91fc, which rewrote the Orchestrate playbook around `notes.md`, worker kickoffs and PR owners, and deleted `scripts/orch/`.

- **a3856a70a3d4** (policy, same-model-review). Intent: a dedicated verifier runs on its worker's model, not a different family, unless the user names another. The block that scaled verification to the unit is gone. The policy still applies and moved to the Topology entry (ca155dd357b3), whose verifier bullet now says "on the same model and effort as the PR's owner".
- **da6d7e9ea334** (translation: isolation, cursor-only). Intent: the lost-work example is a worktree removed or the machine dying, not a cloud VM. Upstream dropped the externalize-the-moment-it-lands block.
- **850c1a1d2385** (translation: stop, cursor-only). Intent: the liveness probe uses `task_status`, and the Cursor-restart bullet becomes a T3 restart. Upstream replaced the list with Supervision bullets that have no Cursor terms: judge a worker by its pushes and PR activity, and retry by cause.

## skills/interrogate/SKILL.md, entries 341a35d859a2, fc18e66f1474, 6f513b774653, 9cd5262f18c2

Retired at upstream pstack 1ba91fc, which rewrote interrogate to run adversaries through the **arena** skill's Phase A steps 3 and 4 and Phase B, and deleted `references/`. Arena's own entries now cover the launch, the models and the effort. The remaining reviewer-spawn entry (2df50e629aaa) moved to the new Fan out paragraph (396b0b06eb52).

- **341a35d859a2** (delegate, model-role). Intent: reviewers are `delegate_task` calls in one message, one per `interrogate reviewers` entry. Arena Phase B launches them now.
- **fc18e66f1474** (model-role). Intent: the default reviewer table comes from willyskills's `interrogate reviewers` role. Upstream dropped the table. The Fan out entry names `{{model:interrogate reviewers}}` as the default.
- **6f513b774653** (model-role). Intent: delete the rejected-slug and family-prefix fallback. Upstream dropped the block.
- **9cd5262f18c2** (model-effort). Intent: effort is the role line's ceiling. The block and the `references/` it pointed at are gone, and arena step 3 carries the effort rule.
