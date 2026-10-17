# check-plan-hourly-tick

intent: The Program checklist must arm an hourly audit tick. The patched plan skeleton arms it with schedule_task and everyMs: 3600000, so check-plan.mjs looks for that instead of /loop 1h. The test's valid-plan fixture keeps in step, in a code span as in a real plan, because the checker rejects a mid-sentence colon in prose.

edits:
- file skills/poteto-mode/scripts/check-plan.mjs
- file skills/poteto-mode/scripts/check-plan.test.ts
