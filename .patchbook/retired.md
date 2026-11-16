# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## orchestrate.md failure, externalizing, and verification entries

Retired at upstream bf0c7cd. Upstream rewrote the Orchestrate playbook and deleted the failure-handling list, the externalize-on-landing rule, and the scale-verification paragraph these entries patched. The new Supervision list judges a stalled worker by its pushes and PR activity and has no Cursor terms. The verifier policy (same-model-review) moved to the new topology entry.

- `850c1a1d2385`: The read-only liveness probe uses `task_status`, which reads state without waking the agent. The Cursor-restart bullet becomes a T3 restart: no rule covers it, so it keeps upstream's recovery steps and drops the local-versus-cloud split, since every child runs on this machine and its worktree and pushed branches outlive the session. Preserve never resuming to check on an agent, the retry-by-mode table, and reattaching by PR and branch rather than agent id.
- `da6d7e9ea334`: Every child runs in a worktree on this machine, so the lost-work example is a worktree removed or the machine dying, not a cloud VM. Keep the rule that output is externalized the moment it lands, and the three examples of externalizing.
- `a3856a70a3d4`: Policy: a dedicated verifier runs on its worker's model, not a different family, unless the user names another (rule same-model-review).

## interrogate/SKILL.md reviewer entries

Retired at upstream bf0c7cd. Upstream rebuilt interrogate on the arena skill's runner and fan-out steps, and deleted the reviewer table, the slug fallbacks, the read-only reviewer setup, and the reviewer-prompt, rubric, and code-quality references these entries patched. Adversaries now write repros in their own worktrees, so the read-only rule no longer fits. The launch entry was rewritten on the new fan-out block instead.

- `fc18e66f1474`: The default table comes from willyskills's `interrogate reviewers` role. The placeholder expands to a list, so one row covers all reviewers in order. Preserve the table form.
- `2df50e629aaa`: Each reviewer is a read-only child sharing the checkout, with `target` from its entry per the model-entry snippet (inherit-parent omits target). Preserve configured-entry-else-default.
- `6f513b774653`: Deleted: the whole block is the rejected-slug and family-prefix fallback, which model-role drops (orchestrator_capabilities lists what exists). If upstream adds non-fallback guidance here, keep that part.
- `9cd5262f18c2`: Replaces picking a reasoning level and fast or standard speed with the effort ceiling from the role's models-file line: lower it for routine work, never raise it. Keep the pointer to the Subagents section and the shared reviewer template.

## why/SKILL.md block entries

Retired at upstream bf0c7cd. Upstream rewrote the why skill as one paragraph that reads the record itself: no subagents, no MCP inventory, no investigators or synthesizer, and its references/ folder is gone. No block in it uses a Cursor term, so none of these entries has a block to patch. The `why investigators` and `why synthesizer` roles retired with it.

- `1dee5fd9349d`: Every spawn takes its model from its role line in the project models file, else the role's willyskills default, applied as the model-entry snippet says. Drops the rejected-slug fallbacks; the poteto-mode pointer now only lowers effort within the line's ceiling.
- `68051d8304d7`: Every spawn is a plain `delegate_task` that keeps full tool and MCP access; never narrowing `runtimeMode` replaces "do not use readonly/Ask mode". Keeps the reason (MCP-backed investigators and citation spot-checks) and that investigators write nothing, now enforced by the brief and a `git status` check.
- `e13a8a92d392`: The available MCP servers are the MCP tools in this agent's tool list. Drops the available-tools map and the `mcps/` folder.
- `9aad2f123d9c`: Investigators spawn as one `delegate_task` per category in a single message, each owning one MCP, with the model from the `why investigators` line, else its willyskills default.
- `9ea9cff1882e`: The synthesizer takes its model from the `why synthesizer` line, else its willyskills default. The list of what it gets is unchanged.
