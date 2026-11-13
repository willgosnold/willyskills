# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## orchestrate entries (blocks/skills/poteto-mode/playbooks/orchestrate.md), retired at pstack 6e359ce

Upstream rewrote the Orchestrate playbook around the agent's own tools and deleted `scripts/orch/`, the store layout, the drains, the roles section, the externalize paragraph and the verification-scaling paragraph. The new "Run it with your own tools" entry (651cc2734134) carries the reload-the-orchestrator-after policy, and the Topology entry (ca155dd357b3) carries same-model-review for the PR verifier.

- 850c1a1d2385 (stop, cursor-only): The read-only liveness probe uses `task_status`, which reads state without waking the agent. The Cursor-restart bullet becomes a T3 restart, keeping upstream's recovery steps, never resuming to check on an agent, the retry-by-mode table, and reattaching by PR and branch rather than agent id. Retired: upstream replaced the whole list with a new Supervision list that has no Cursor terms; the dashboard probe, the restart bullet and the `orch` lock bullet are gone.
- da6d7e9ea334 (isolation, cursor-only): Every child runs in a worktree on this machine, so the lost-work example is a worktree removed or the machine dying, not a cloud VM. Keep the rule that output is externalized the moment it lands. Retired: upstream deleted the externalize paragraph.
- a3856a70a3d4 (policy, same-model-review): A dedicated verifier runs on its worker's model, not a different family, unless the user names another. Retired: upstream deleted the verification-scaling paragraph; the policy still applies through the Topology entry.

## interrogate reviewer entries (blocks/skills/interrogate/SKILL.md), retired at pstack 6e359ce

Upstream rewrote interrogate: adversaries now run through arena's runner pick and fan-out (Phase A steps 3 and 4, Phase B) and write repros in their own worktrees, and the reviewer template, rubric, code-quality lens and lead-judgment references (`references/*.md`) were deleted. The blocks these entries patched are gone. The fan-out block's entry (396b0b06eb52, carried from 341a35d859a2) takes the spawn through arena's patched text.

- fc18e66f1474 (model-role): The default table comes from willyskills's `interrogate reviewers` role. Retired: upstream removed the default table; defaults now come through arena's step 3.
- 2df50e629aaa (general-purpose, read-only, model-role): Each reviewer is a read-only child sharing the checkout, with `target` from its entry per the model-entry snippet. Retired: adversaries now write repros in their own worktrees, so read-only no longer applies, and arena's step 3 applies the model-entry snippet.
- 6f513b774653 (model-role): Deleted the block that held only the rejected-slug and family-prefix fallback. Retired: upstream deleted the block.
- 9cd5262f18c2 (model-effort): Replaces picking a reasoning level and fast or standard speed with the models-file effort ceiling. Retired: the block and the reviewer template it pointed at are gone; arena's step 3 carries the effort rule.
