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

## skills/interrogate/SKILL.md fc18e66f1474

Retired at upstream pstack c742dd6. Kind: translation (model-role).

intent: The default table comes from willyskills's `interrogate reviewers` role. The placeholder expands to a list, so one row covers all reviewers in order. Preserve the table form.

Why: upstream deleted the default table. The `interrogate reviewers` default now sits in entry 396b0b06eb52.

## skills/interrogate/SKILL.md 2df50e629aaa

Retired at upstream pstack c742dd6. Kind: translation (general-purpose, read-only, model-role).

intent: Each reviewer is a read-only child sharing the checkout, with `target` from its entry per the model-entry snippet (inherit-parent omits target). Preserve configured-entry-else-default.

Why: upstream's reviewers became adversaries that run repros in their own worktrees, so they are no longer read-only. Agent type, model and target now come through the arena skill's step 3 and Phase B, which arena's entries translate.

## skills/interrogate/SKILL.md 6f513b774653

Retired at upstream pstack c742dd6. Kind: translation (model-role).

intent: Deleted: the whole block is the rejected-slug and family-prefix fallback, which model-role drops (orchestrator_capabilities lists what exists). If upstream adds non-fallback guidance here, keep that part.

Why: upstream deleted the block. The fallback now lives only in arena's step 3, which arena's entry d4a7c6b535e0 handles.

## skills/interrogate/SKILL.md 9cd5262f18c2

Retired at upstream pstack c742dd6. Kind: translation (model-effort).

intent: Replaces picking a reasoning level and fast or standard speed with the effort ceiling from the role's models-file line: lower it for routine work, never raise it. Keep the pointer to the Subagents section and the shared reviewer template.

Why: upstream deleted the block and the shared reviewer template (`references/reviewer-prompt.md`, `rubric.md`, `code-quality-review.md`). The effort choice moved into arena's step 3.
