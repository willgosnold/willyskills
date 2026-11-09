# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## skills/interrogate/SKILL.md 341a35d859a2
intent: Reviewers are delegate_task calls in one message, one per entry on the `interrogate reviewers` line of the project models file, else the defaults below. Preserve the single-message launch and the A, B labeling.
retired: upstream 6b03002 rewrote interrogate to launch adversaries through the arena skill's Phase A step 3 and Phase B, whose entries already translate the single-message delegate_task launch. The A, B labels are gone upstream.

## skills/interrogate/SKILL.md fc18e66f1474
intent: The default table comes from willyskills's `interrogate reviewers` role. The placeholder expands to a list, so one row covers all reviewers in order. Preserve the table form.
retired: upstream 6b03002 removed the default table. Taking the default from the `interrogate reviewers` role now lives in entry 396b0b06eb52.

## skills/interrogate/SKILL.md 2df50e629aaa
intent: Each reviewer is a read-only child sharing the checkout, with `target` from its entry per the model-entry snippet (inherit-parent omits target). Preserve configured-entry-else-default.
retired: upstream 6b03002 turned reviewers into adversaries that write repros in their own worktrees, so they are no longer read-only. Model selection comes from arena step 3.

## skills/interrogate/SKILL.md 6f513b774653
intent: Deleted: the whole block is the rejected-slug and family-prefix fallback, which model-role drops (orchestrator_capabilities lists what exists). If upstream adds non-fallback guidance here, keep that part.
retired: upstream 6b03002 removed the block.

## skills/interrogate/SKILL.md 9cd5262f18c2
intent: Replaces picking a reasoning level and fast or standard speed with the effort ceiling from the role's models-file line: lower it for routine work, never raise it. Keep the pointer to the Subagents section and the shared reviewer template.
retired: upstream 6b03002 deleted the reviewer template, rubric and code-quality references, and moved effort to arena step 3, whose entry carries the effort ceiling through the model-entry snippet.

## skills/poteto-mode/playbooks/orchestrate.md 850c1a1d2385
intent: The read-only liveness probe uses `task_status`, which reads state without waking the agent. The Cursor-restart bullet becomes a T3 restart: no rule covers it, so it keeps upstream's recovery steps and drops the local-versus-cloud split, since every child runs on this machine and its worktree and pushed branches outlive the session. Preserve never resuming to check on an agent, the retry-by-mode table, and reattaching by PR and branch rather than agent id.
retired: upstream 6b03002 removed the Liveness and failure section. Its retry-by-cause and late-worker rules moved into Supervision with no Cursor terms, a stalled worker is judged by its pushes rather than its status, and a restart has no step of its own.

## skills/poteto-mode/playbooks/orchestrate.md da6d7e9ea334
intent: Every child runs in a worktree on this machine, so the lost-work example is a worktree removed or the machine dying, not a cloud VM. Keep the rule that output is externalized the moment it lands, and the three examples of externalizing.
retired: upstream 6b03002 removed the Verification section and this paragraph with it.
