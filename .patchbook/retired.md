# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## check-plan-hourly-tick

Retired at pstack e1cc031. Upstream deleted `skills/poteto-mode/scripts/check-plan.mjs` and its test, and the Multi-phase plan playbook no longer has a plan skeleton with a Program checklist or an audit tick. Nothing is left to check.

Intent: The Program checklist must arm an hourly audit tick. The patched plan skeleton arms it with schedule_task and everyMs: 3600000, so check-plan.mjs looks for that instead of /loop 1h. The test's valid-plan fixture keeps in step, in a code span as in a real plan, because the checker rejects a mid-sentence colon in prose.
