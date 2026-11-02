# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## skills/interrogate/SKILL.md [341a35d859a2]

kind: translation (delegate, model-role)

intent: Reviewers are delegate_task calls in one message, one per entry on the `interrogate reviewers` line of the project models file, else the defaults below. Preserve the single-message launch and the A, B labeling.

Retired at pstack ae5650f: upstream deleted the reviewer launch step; adversaries now spawn through arena Phase B, which has its own entry.

## skills/interrogate/SKILL.md [fc18e66f1474]

kind: translation (model-role)

intent: The default table comes from willyskills's `interrogate reviewers` role. The placeholder expands to a list, so one row covers all reviewers in order. Preserve the table form.

Retired at pstack ae5650f: upstream deleted the default reviewer table; the `interrogate reviewers` default now sits in the Fan out entry [396b0b06eb52].

## skills/interrogate/SKILL.md [2df50e629aaa]

kind: translation (general-purpose, read-only, model-role)

intent: Each reviewer is a read-only child sharing the checkout, with `target` from its entry per the model-entry snippet (inherit-parent omits target). Preserve configured-entry-else-default.

Retired at pstack ae5650f: upstream deleted the per-reviewer settings; adversaries take arena's runner settings, and each writes repros in its own worktree, so the read-only rule no longer applies.

## skills/interrogate/SKILL.md [6f513b774653]

kind: translation (model-role)

intent: Deleted: the whole block is the rejected-slug and family-prefix fallback, which model-role drops (orchestrator_capabilities lists what exists). If upstream adds non-fallback guidance here, keep that part.

Retired at pstack ae5650f: upstream deleted the rejected-slug fallback paragraph.

## skills/interrogate/SKILL.md [9cd5262f18c2]

kind: translation (model-effort)

intent: Replaces picking a reasoning level and fast or standard speed with the effort ceiling from the role's models-file line: lower it for routine work, never raise it. Keep the pointer to the Subagents section and the shared reviewer template.

Retired at pstack ae5650f: upstream deleted the reviewer template and its references (reviewer-prompt.md, rubric.md, code-quality-review.md); effort follows arena step 3 and the model-entry snippet.

## skills/poteto-mode/playbooks/orchestrate.md [850c1a1d2385]

kind: translation (stop, cursor-only)

intent: The read-only liveness probe uses `task_status`, which reads state without waking the agent. The Cursor-restart bullet becomes a T3 restart: no rule covers it, so it keeps upstream's recovery steps and drops the local-versus-cloud split, since every child runs on this machine and its worktree and pushed branches outlive the session. Preserve never resuming to check on an agent, the retry-by-mode table, and reattaching by PR and branch rather than agent id.

Retired at pstack ae5650f: upstream rewrote the Orchestrate playbook and deleted the Liveness and failure section, with the dashboard probe and the Cursor-restart bullet. Its replacement (Supervision: stop or replace a worker that stalls) names no Cursor term. The `task_status` probe moved into the Topology entry [ca155dd357b3].

## skills/poteto-mode/playbooks/orchestrate.md [da6d7e9ea334]

kind: translation (isolation, cursor-only)

intent: Every child runs in a worktree on this machine, so the lost-work example is a worktree removed or the machine dying, not a cloud VM. Keep the rule that output is externalized the moment it lands, and the three examples of externalizing.

Retired at pstack ae5650f: upstream deleted the Verification section that held this paragraph, with the ledger and the VM example.
