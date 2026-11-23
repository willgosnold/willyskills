# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

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
