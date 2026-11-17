# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## Block entries retired at pstack e1cc031

Upstream deleted or rewrote these paragraphs so that nothing in them needs a change any more.

### skills/poteto-mode/playbooks/multi-phase-plan.md, entry ef26c450e81f
Upstream rewrote the steps without explorer subagents, the agent store, the technical-writing and unslop pass, or check-plan.mjs, so the new steps have no Cursor term.
Intent: Explorers are delegate_task children whose brief opens with the poteto-agent read line (absolute paths resolved from this skill's folder), and the effort pick becomes a ceiling taken from the role line, never raised; the plan file's default home is the shared pstack state folder. Keep the explicit model per the Subagents section, the file-pointer return contract, and every other step as written. Step 5 names the technical-writing and unslop skills with no slash.

### skills/poteto-mode/playbooks/multi-phase-plan.md, entry c8af48ae5edc
Upstream deleted the plan skeleton's Verification paragraph and its `swarm workers` slug; the new step 4 states the verification rule with no model.
Intent: The live lanes' model comes from the swarm workers role line in the project models file, else the willyskills default, with no hard-coded slug. Everything else in the verification rule stays verbatim.

### skills/poteto-mode/playbooks/multi-phase-plan.md, entry badec09370bc
Upstream deleted the plan skeleton's Control skill paragraph with its control-ui and control-cli picks.
Intent: The control skill is the project's own verification skill when it has one, else T3's preview tools for browser, Electron, and web UIs and the shell for CLIs and TUIs. Keep the per-surface pick, native mobile, two-surface lanes, and the Appendix C risk for an uncontrolled surface.

### skills/poteto-mode/playbooks/multi-phase-plan.md, entry a1c6fc6a1a6a
Upstream deleted the plan skeleton, including the hourly `/loop 1h` tick and the PR mechanics box, and scripts/check-plan.mjs with it.
Intent: In the plan skeleton: the hourly audit tick is an interval schedule_task (reported nextRunAt, deleted at close); PRs open through origin or gh and are linked with link_pull_request; /deslop is conditional on being installed; live lanes run in their own worktree on this machine and drive the project verification skill, preview tools, or the shell, not a cloud VM. The PR heading placeholder says 'The task' because the bare capitalized word trips the Cursor-term check (no rule covers that). Keep every heading, sub-block, box order, and the tick prompt verbatim. Rule gap: scripts/check-plan.mjs still requires the literal "/loop 1h" marker in Program checklist, so it reports a false problem until the script's marker is patched. The PR mechanics box names the deslop and no-comments skills with no slash.


## reload-the-orchestrator-after

Retired at pstack e1cc031, with its frontmatter `PreToolUse` hook in poteto-mode's `SKILL.md` (entry 9ab9dbbc3978) and its state-file bullet in the Orchestrate playbook (entry 46658be16fff). Upstream deleted the Orchestrate playbook and its coordinator, so no playbook keeps the state file this hook reloads, and `references/compact-reload.md` would point at `playbooks/orchestrate.md`, which no longer exists.

Intent: Reload the orchestrator after auto-compaction. The frontmatter PreToolUse hook records the coordinator's session id once; the project's settings.json SessionStart compact hook (a compact hook in skill frontmatter does not fire) prints a reload directive and the state file for that session only. The Orchestrate playbook names the state file the coordinator keeps current, and references/compact-reload.md holds the settings snippet and script.

## check-plan-hourly-tick

Retired at pstack e1cc031. Upstream deleted `skills/poteto-mode/scripts/check-plan.mjs` and its test, and the Multi-phase plan playbook no longer has a plan skeleton with a Program checklist or an audit tick. Nothing is left to check.

Intent: The Program checklist must arm an hourly audit tick. The patched plan skeleton arms it with schedule_task and everyMs: 3600000, so check-plan.mjs looks for that instead of /loop 1h. The test's valid-plan fixture keeps in step, in a code span as in a real plan, because the checker rejects a mid-sentence colon in prose.
