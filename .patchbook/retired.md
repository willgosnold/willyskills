# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## check-plan-hourly-tick (change)

Retired at upstream pstack 93b916d.

intent: The Program checklist must arm an hourly audit tick. The patched plan skeleton arms it with schedule_task and everyMs: 3600000, so check-plan.mjs looks for that instead of /loop 1h. The test's valid-plan fixture keeps in step, in a code span as in a real plan, because the checker rejects a mid-sentence colon in prose.

why: upstream deleted skills/poteto-mode/scripts/check-plan.mjs and check-plan.test.ts, and nothing upstream refers to the checker or its hourly tick any more, so there is no script left to adapt.
