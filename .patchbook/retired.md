# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## orchestrate entries (blocks/skills/poteto-mode/playbooks/orchestrate.md), retired at pstack 6e359ce

Upstream rewrote the Orchestrate playbook around the agent's own tools and deleted `scripts/orch/`, the store layout, the drains, the roles section, the externalize paragraph and the verification-scaling paragraph. The new "Run it with your own tools" entry (651cc2734134) carries the reload-the-orchestrator-after policy, and the Topology entry (ca155dd357b3) carries same-model-review for the PR verifier.

- 850c1a1d2385 (stop, cursor-only): The read-only liveness probe uses `task_status`, which reads state without waking the agent. The Cursor-restart bullet becomes a T3 restart, keeping upstream's recovery steps, never resuming to check on an agent, the retry-by-mode table, and reattaching by PR and branch rather than agent id. Retired: upstream replaced the whole list with a new Supervision list that has no Cursor terms; the dashboard probe, the restart bullet and the `orch` lock bullet are gone.
- da6d7e9ea334 (isolation, cursor-only): Every child runs in a worktree on this machine, so the lost-work example is a worktree removed or the machine dying, not a cloud VM. Keep the rule that output is externalized the moment it lands. Retired: upstream deleted the externalize paragraph.
- a3856a70a3d4 (policy, same-model-review): A dedicated verifier runs on its worker's model, not a different family, unless the user names another. Retired: upstream deleted the verification-scaling paragraph; the policy still applies through the Topology entry.

