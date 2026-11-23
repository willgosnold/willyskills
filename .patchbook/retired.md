# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## skills/poteto-mode/playbooks/runtime-forensics.md 135b89dd7690 (translation)

intent: Replaces picking a reasoning level and fast or standard speed with the effort ceiling from the role's models-file line: lower it for routine work, never raise it. Keep the pointer to the Subagents section and every step unchanged.

Retired at pstack 7a58391: upstream's sentence dropped 'fast or standard speed' and now only defers to the Subagents section, which carries the effort ceiling, so the block has no Cursor term left to translate.

## skills/poteto-mode/playbooks/orchestrate.md 25ab709f3f5f (translation)

intent: Coordinator spawns, resumes, and drains agents only through T3's task tools, and sets effort under the role line's ceiling. Workers and verifiers that write default to their own worktree the way upstream defaulted them to cloud, and the list of reasons to stay on this machine becomes a note that every child runs here; the 'cloud agents cannot read the local store' clause becomes 'briefs give the store's absolute path'. The verifier's different model family comes from the cross-judge pool. Preserve the three-layer roles, the never-edits-code rule, the rolling window cap, and one writer per worktree. Policy: verifiers run on their worker's model and effort (rule same-model-review).

Retired at pstack 7a58391: upstream deleted playbooks/orchestrate.md, and no surviving file carries this text.

## skills/poteto-mode/playbooks/orchestrate.md 850c1a1d2385 (translation)

intent: The read-only liveness probe uses `task_status`, which reads state without waking the agent. The Cursor-restart bullet becomes a T3 restart: no rule covers it, so it keeps upstream's recovery steps and drops the local-versus-cloud split, since every child runs on this machine and its worktree and pushed branches outlive the session. Preserve never resuming to check on an agent, the retry-by-mode table, and reattaching by PR and branch rather than agent id.

Retired at pstack 7a58391: upstream deleted playbooks/orchestrate.md, and no surviving file carries this text.

## skills/poteto-mode/playbooks/orchestrate.md da6d7e9ea334 (translation)

intent: Every child runs in a worktree on this machine, so the lost-work example is a worktree removed or the machine dying, not a cloud VM. Keep the rule that output is externalized the moment it lands, and the three examples of externalizing.

Retired at pstack 7a58391: upstream deleted playbooks/orchestrate.md, and no surviving file carries this text.

## skills/poteto-mode/playbooks/orchestrate.md a3856a70a3d4 (policy)

intent: Policy: a dedicated verifier runs on its worker's model, not a different family, unless the user names another (rule same-model-review).

Retired at pstack 7a58391: upstream deleted playbooks/orchestrate.md, and no surviving file carries this text.

## skills/poteto-mode/playbooks/orchestrate.md 46658be16fff (policy)

intent: Reload the orchestrator after auto-compaction. The frontmatter PreToolUse hook records the coordinator's session id once; the project's settings.json SessionStart compact hook (a compact hook in skill frontmatter does not fire) prints a reload directive and the state file for that session only. The Orchestrate playbook names the state file the coordinator keeps current, and references/compact-reload.md holds the settings snippet and script.

Retired at pstack 7a58391: upstream deleted playbooks/orchestrate.md along with its state-file list, so there is no block left to name the orchestrator state file in; the reload-the-orchestrator-after change (frontmatter hook and references/compact-reload.md) is with the user as a separate decision, and if it is kept, the state file needs a new home in a surviving block.

## skills/poteto-mode/playbooks/opening-a-pr.md 49969656b7a9 (translation)

intent: Parallel writers on one branch are `delegate_task` calls with `isolation: "worktree"`, which copies only committed work. Preserves the worktree-off-main rule, the reset alternative, and the dirty and snarled worktree recoveries.

Retired at pstack 7a58391: upstream replaced the Worktree paragraph with one sentence that no longer mentions parallel Task calls on one branch, so there is no spawn left to translate.

## skills/poteto-mode/playbooks/opening-a-pr.md a60ae6c65955 (translation)

intent: The subagent runs the interrogate, deslop, and no-comments skills, named with no slash. Preserve the no-babysitting default and the Autopilot owner exemption.

Retired at pstack 7a58391: upstream dropped the paragraph on what a PR-opening subagent runs and the Autopilot owner exemption.

## skills/poteto-mode/playbooks/multi-phase-plan.md ef26c450e81f (translation)

intent: Explorers are delegate_task children whose brief opens with the poteto-agent read line (absolute paths resolved from this skill's folder), and the effort pick becomes a ceiling taken from the role line, never raised; the plan file's default home is the shared pstack state folder. Keep the explicit model per the Subagents section, the file-pointer return contract, and every other step as written. Step 5 names the technical-writing and unslop skills with no slash.

Retired at pstack 7a58391: upstream cut the playbook to five steps; explorer subagents, the poteto-agent brief, the effort pick, and the plan file's store location are gone.

## skills/poteto-mode/playbooks/multi-phase-plan.md c8af48ae5edc (translation)

intent: The live lanes' model comes from the swarm workers role line in the project models file, else the willyskills default, with no hard-coded slug. Everything else in the verification rule stays verbatim.

Retired at pstack 7a58391: upstream dropped the Verification section with its ten live lanes and their model, keeping only a one-line verification rule with no model choice.

## skills/poteto-mode/playbooks/multi-phase-plan.md badec09370bc (translation)

intent: The control skill is the project's own verification skill when it has one, else T3's preview tools for browser, Electron, and web UIs and the shell for CLIs and TUIs. Keep the per-surface pick, native mobile, two-surface lanes, and the Appendix C risk for an uncontrolled surface.

Retired at pstack 7a58391: upstream dropped the Control skill section; the plan now only says each live box drives the real surface, with no Cursor control skill named.

## skills/poteto-mode/playbooks/multi-phase-plan.md a1c6fc6a1a6a (translation)

intent: In the plan skeleton: the hourly audit tick is an interval schedule_task (reported nextRunAt, deleted at close); PRs open through origin or gh and are linked with link_pull_request; /deslop is conditional on being installed; live lanes run in their own worktree on this machine and drive the project verification skill, preview tools, or the shell, not a cloud VM. The PR heading placeholder says 'The task' because the bare capitalized word trips the Cursor-term check (no rule covers that). Keep every heading, sub-block, box order, and the tick prompt verbatim. Rule gap: scripts/check-plan.mjs still requires the literal "/loop 1h" marker in Program checklist, so it reports a false problem until the script's marker is patched. The PR mechanics box names the deslop and no-comments skills with no slash.

Retired at pstack 7a58391: upstream dropped the plan skeleton, including its hourly audit tick, PR opening, deslop step, and live-lane setup, so the check-plan-hourly-tick wording has nothing to apply to.

## skills/poteto-mode/playbooks/bug-fix.md 244bab33ef86 (translation)

intent: Replaces picking a reasoning level and fast or standard speed with the effort ceiling from the role's models-file line: lower it for routine work, never raise it. Keep the pointer to the Subagents section and the ownership line.

Retired at pstack 7a58391: upstream's sentence dropped 'fast or standard speed' and now only defers to the Subagents section, which carries the effort ceiling, so the block has no Cursor term left to translate.

## skills/poteto-mode/playbooks/babysit.md 303f48cdd024 (translation)

intent: Dropped the sentence about not routing to Cursor's built-in babysit skill; T3 has none. Keep the opening claim and the hand-off to playbooks/shipping.md.

Retired at pstack 7a58391: upstream dropped the sentence about Cursor's built-in babysit skill, so there is nothing left to remove.

## skills/poteto-mode/playbooks/babysit.md e971fea959f8 (translation)

intent: drive and background run on wakes from watch_pull_request on the frontier plus a 30-minute schedule_task heartbeat (a merge ends the watch without a wake); each wake re-runs the watcher, which stays the source of the verdict. Keep rearm-after-every-push-wave, the no-second-sleep-loop rule, and unwatching before handing work back.

Retired at pstack 7a58391: upstream cut the playbook to six bullets and dropped the 'run drive and background under /loop in dynamic mode' step, so no wake mechanism or Cursor term is left to translate.

## skills/poteto-mode/SKILL.md 1bec9809dcd4 (translation)

intent: Drops the cloud-agent URL from Session pickup's sources and the Cursor restart from Pause safely's triggers, and rewrites the quoted user phrase "/loop until X" as "keep going until X". Every playbook name and description otherwise stays verbatim, since routing matches on them.

Retired at pstack 7a58391: upstream replaced the described playbook list with a bare list of playbook names that holds no Cursor term, so there is nothing left to translate.

## skills/interrogate/SKILL.md fc18e66f1474 (translation)

intent: The default table comes from willyskills's `interrogate reviewers` role. The placeholder expands to a list, so one row covers all reviewers in order. Preserve the table form.

Retired at pstack 7a58391: upstream removed the default-model table; adversaries now take their models through the arena skill's Phase A step 3.

## skills/interrogate/SKILL.md 2df50e629aaa (translation)

intent: Each reviewer is a read-only child sharing the checkout, with `target` from its entry per the model-entry snippet (inherit-parent omits target). Preserve configured-entry-else-default.

Retired at pstack 7a58391: upstream's adversaries now write repros in their own worktrees through arena Phase B, so the read-only reviewer settings are gone; the `generalPurpose` omission carries into entry 396b0b06eb52.

## skills/interrogate/SKILL.md 6f513b774653 (translation)

intent: Deleted: the whole block is the rejected-slug and family-prefix fallback, which model-role drops (orchestrator_capabilities lists what exists). If upstream adds non-fallback guidance here, keep that part.

Retired at pstack 7a58391: upstream removed the rejected-slug and family-prefix fallback block.

## skills/interrogate/SKILL.md 9cd5262f18c2 (translation)

intent: Replaces picking a reasoning level and fast or standard speed with the effort ceiling from the role's models-file line: lower it for routine work, never raise it. Keep the pointer to the Subagents section and the shared reviewer template.

Retired at pstack 7a58391: upstream removed the reviewer-prompt, rubric and code-quality references and the reasoning-and-speed sentence with them.

## skills/figure-it-out/SKILL.md bb548e38e218 (translation)

intent: Replaces picking a reasoning level and fast or standard speed with the effort ceiling from the role's models-file line: lower it for routine work, never raise it. Keep the pointer to the Subagents section and the rest of the bullet list unchanged.

Retired at pstack 7a58391: upstream dropped "and fast or standard speed", and the remaining "pick each subagent's reasoning level" defers to poteto-mode's Subagents section, whose patched text already makes the line's effort a ceiling.

## skills/architect/SKILL.md bcaf34d31ad8 (translation)

intent: Opens the visible phase list in T3's terms (update_plan in Codex, the reply in Claude Code) and keeps it current. Preserve that it opens before starting, with one entry per phase.

Retired at pstack 7a58391: upstream cut architect to two paragraphs and removed the phase list and its todolist.

## skills/architect/SKILL.md 67769a2b1c21 (translation)

intent: Architect's runners come from the `architect runners` line in the project models file, else willyskills's default, replacing the arena runners line; entries apply as in arena's Phase A. The rejected-entry fallback is dropped.

Retired at pstack 7a58391: upstream removed the `architect runners` line, and architect now just runs the arena skill, which reads the `arena runners` line.

## skills/architect/SKILL.md 3ded7fe1302c (translation)

intent: The quoted opt-in phrase is what the user types, so it gives both forms. Preserve that the checkpoint is opt-in and pauses for sign-off.

Retired at pstack 7a58391: upstream removed the opt-in checkpoint and its quoted `/architect with checkpoint` phrase.

## check-plan-hourly-tick

intent: The Program checklist must arm an hourly audit tick. The patched plan skeleton arms it with schedule_task and everyMs: 3600000, so check-plan.mjs looks for that instead of /loop 1h. The test's valid-plan fixture keeps in step, in a code span as in a real plan, because the checker rejects a mid-sentence colon in prose.

Retired at pstack 7a58391: upstream deleted `skills/poteto-mode/scripts/check-plan.mjs` and its test, and no shipped file runs a plan checker any more.
