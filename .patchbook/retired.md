# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## skills/poteto-mode/playbooks/orchestrate.md [850c1a1d2385]

kind: translation (stop, cursor-only)

intent: The read-only liveness probe uses `task_status`, which reads state without waking the agent. The Cursor-restart bullet becomes a T3 restart: no rule covers it, so it keeps upstream's recovery steps and drops the local-versus-cloud split, since every child runs on this machine and its worktree and pushed branches outlive the session. Preserve never resuming to check on an agent, the retry-by-mode table, and reattaching by PR and branch rather than agent id.

Retired at pstack ae5650f: upstream rewrote the Orchestrate playbook and deleted the Liveness and failure section, with the dashboard probe and the Cursor-restart bullet. Its replacement (Supervision: stop or replace a worker that stalls) names no Cursor term. The `task_status` probe moved into the Topology entry [ca155dd357b3].

## skills/poteto-mode/playbooks/orchestrate.md [da6d7e9ea334]

kind: translation (isolation, cursor-only)

intent: Every child runs in a worktree on this machine, so the lost-work example is a worktree removed or the machine dying, not a cloud VM. Keep the rule that output is externalized the moment it lands, and the three examples of externalizing.

Retired at pstack ae5650f: upstream deleted the Verification section that held this paragraph, with the ledger and the VM example.
