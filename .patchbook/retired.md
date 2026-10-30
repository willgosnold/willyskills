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
