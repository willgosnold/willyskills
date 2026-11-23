# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

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
