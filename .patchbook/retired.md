# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## skills/interrogate/SKILL.md 341a35d859a2

kind: translation
rules: delegate, model-role
intent: Reviewers are delegate_task calls in one message, one per entry on the `interrogate reviewers` line of the project models file, else the defaults below. Preserve the single-message launch and the A, B labeling.
retired: Upstream 4dd1d05 rewrote interrogate: adversaries now spawn through arena's Phase A steps 3 and 4 and Phase B, and the reviewer table, launch paragraph, slug fallback, and reviewer-prompt references are gone. Arena's own entries and the new Fan out entry carry the model and spawn translation.

## skills/interrogate/SKILL.md fc18e66f1474

kind: translation
rules: model-role
intent: The default table comes from willyskills's `interrogate reviewers` role. The placeholder expands to a list, so one row covers all reviewers in order. Preserve the table form.
retired: Upstream 4dd1d05 rewrote interrogate: adversaries now spawn through arena's Phase A steps 3 and 4 and Phase B, and the reviewer table, launch paragraph, slug fallback, and reviewer-prompt references are gone. Arena's own entries and the new Fan out entry carry the model and spawn translation.

## skills/interrogate/SKILL.md 2df50e629aaa

kind: translation
rules: general-purpose, read-only, model-role
intent: Each reviewer is a read-only child sharing the checkout, with `target` from its entry per the model-entry snippet (inherit-parent omits target). Preserve configured-entry-else-default.
retired: Upstream 4dd1d05 rewrote interrogate: adversaries now spawn through arena's Phase A steps 3 and 4 and Phase B, and the reviewer table, launch paragraph, slug fallback, and reviewer-prompt references are gone. Arena's own entries and the new Fan out entry carry the model and spawn translation.

## skills/interrogate/SKILL.md 6f513b774653

kind: translation
rules: model-role
intent: Deleted: the whole block is the rejected-slug and family-prefix fallback, which model-role drops (orchestrator_capabilities lists what exists). If upstream adds non-fallback guidance here, keep that part.
retired: Upstream 4dd1d05 rewrote interrogate: adversaries now spawn through arena's Phase A steps 3 and 4 and Phase B, and the reviewer table, launch paragraph, slug fallback, and reviewer-prompt references are gone. Arena's own entries and the new Fan out entry carry the model and spawn translation.

## skills/interrogate/SKILL.md 9cd5262f18c2

kind: translation
rules: model-effort
intent: Replaces picking a reasoning level and fast or standard speed with the effort ceiling from the role's models-file line: lower it for routine work, never raise it. Keep the pointer to the Subagents section and the shared reviewer template.
retired: Upstream 4dd1d05 rewrote interrogate: adversaries now spawn through arena's Phase A steps 3 and 4 and Phase B, and the reviewer table, launch paragraph, slug fallback, and reviewer-prompt references are gone. Arena's own entries and the new Fan out entry carry the model and spawn translation.

## skills/poteto-mode/playbooks/orchestrate.md 25ab709f3f5f

kind: translation
rules: delegate, resume, background, model-effort, isolation, verify-surface, team-kit, transcripts, store, model-unnamed, cursor-only, same-model-review
intent: Coordinator spawns, resumes, and drains agents only through T3's task tools, and sets effort under the role line's ceiling. Workers and verifiers that write default to their own worktree the way upstream defaulted them to cloud, and the list of reasons to stay on this machine becomes a note that every child runs here; the 'cloud agents cannot read the local store' clause becomes 'briefs give the store's absolute path'. The verifier's different model family comes from the cross-judge pool. Preserve the three-layer roles, the never-edits-code rule, the rolling window cap, and one writer per worktree. Policy: verifiers run on their worker's model and effort (rule same-model-review).
retired: Upstream 4dd1d05 cut the Orchestrate playbook to Topology and Supervision lists and deleted scripts/orch, so this block no longer exists. The new Topology entry carries the worktree, effort, messaging, and same-model-review parts that still apply.

## skills/poteto-mode/playbooks/orchestrate.md 850c1a1d2385

kind: translation
rules: stop, cursor-only
intent: The read-only liveness probe uses `task_status`, which reads state without waking the agent. The Cursor-restart bullet becomes a T3 restart: no rule covers it, so it keeps upstream's recovery steps and drops the local-versus-cloud split, since every child runs on this machine and its worktree and pushed branches outlive the session. Preserve never resuming to check on an agent, the retry-by-mode table, and reattaching by PR and branch rather than agent id.
retired: Upstream 4dd1d05 cut the Orchestrate playbook to Topology and Supervision lists and deleted scripts/orch, so this block no longer exists. The new Topology entry carries the worktree, effort, messaging, and same-model-review parts that still apply.

## skills/poteto-mode/playbooks/orchestrate.md da6d7e9ea334

kind: translation
rules: isolation, cursor-only
intent: Every child runs in a worktree on this machine, so the lost-work example is a worktree removed or the machine dying, not a cloud VM. Keep the rule that output is externalized the moment it lands, and the three examples of externalizing.
retired: Upstream 4dd1d05 cut the Orchestrate playbook to Topology and Supervision lists and deleted scripts/orch, so this block no longer exists. The new Topology entry carries the worktree, effort, messaging, and same-model-review parts that still apply.

## skills/poteto-mode/playbooks/orchestrate.md a3856a70a3d4

kind: policy
rules: same-model-review
intent: Policy: a dedicated verifier runs on its worker's model, not a different family, unless the user names another (rule same-model-review).
retired: Upstream 4dd1d05 cut the Orchestrate playbook to Topology and Supervision lists and deleted scripts/orch, so this block no longer exists. The new Topology entry carries the worktree, effort, messaging, and same-model-review parts that still apply.
