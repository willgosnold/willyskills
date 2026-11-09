# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## skills/poteto-mode/playbooks/orchestrate.md 850c1a1d2385
intent: The read-only liveness probe uses `task_status`, which reads state without waking the agent. The Cursor-restart bullet becomes a T3 restart: no rule covers it, so it keeps upstream's recovery steps and drops the local-versus-cloud split, since every child runs on this machine and its worktree and pushed branches outlive the session. Preserve never resuming to check on an agent, the retry-by-mode table, and reattaching by PR and branch rather than agent id.
retired: upstream 6b03002 removed the Liveness and failure section. Its retry-by-cause and late-worker rules moved into Supervision with no Cursor terms, a stalled worker is judged by its pushes rather than its status, and a restart has no step of its own.

## skills/poteto-mode/playbooks/orchestrate.md da6d7e9ea334
intent: Every child runs in a worktree on this machine, so the lost-work example is a worktree removed or the machine dying, not a cloud VM. Keep the rule that output is externalized the moment it lands, and the three examples of externalizing.
retired: upstream 6b03002 removed the Verification section and this paragraph with it.
