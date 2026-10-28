# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## skills/poteto-mode/playbooks/orchestrate.md 850c1a1d2385

Retired at upstream pstack c742dd6. Kind: translation (stop, cursor-only).

intent: The read-only liveness probe uses `task_status`, which reads state without waking the agent. The Cursor-restart bullet becomes a T3 restart: no rule covers it, so it keeps upstream's recovery steps and drops the local-versus-cloud split, since every child runs on this machine and its worktree and pushed branches outlive the session. Preserve never resuming to check on an agent, the retry-by-mode table, and reattaching by PR and branch rather than agent id.

Why: upstream folded the liveness, retry, late-return and stop bullets into a new Supervision block and dropped the after-a-restart recovery bullet. The probe and stop translations carry on in entries ca155dd357b3 and b0d7f0bf067a. The restart part has nothing left to apply to.

## skills/poteto-mode/playbooks/orchestrate.md da6d7e9ea334

Retired at upstream pstack c742dd6. Kind: translation (isolation, cursor-only).

intent: Every child runs in a worktree on this machine, so the lost-work example is a worktree removed or the machine dying, not a cloud VM. Keep the rule that output is externalized the moment it lands, and the three examples of externalizing.

Why: upstream deleted the externalize-on-landing rule along with the orchestrator's store layout and its `orch` CLI. No new block carries it.
