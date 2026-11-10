# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## orchestrate liveness and externalization entries (blocks/skills/poteto-mode/playbooks/orchestrate.md), retired at pstack de8ee15

Upstream rewrote Orchestrate as a short Topology and Supervision list: the store layout, the `orch` CLI, the brief template, the drain queue, the ledger, and the Liveness and Verification sections are gone. The roles entry (25ab709f3f5f) and the verifier policy (a3856a70a3d4) are carried into the Topology entry (ca155dd357b3), and the reload state file (46658be16fff) into a Supervision bullet (b0d7f0bf067a).

- 850c1a1d2385 (stop, cursor-only): The read-only liveness probe uses `task_status`, and the Cursor-restart bullet became a T3 restart. Retired: upstream deleted the Liveness section and its restart bullet; the Topology entry keeps the `task_status` probe on its "never message one to check on it" line.
- da6d7e9ea334 (isolation, cursor-only): The lost-work example was a removed worktree or a dead machine, not a cloud VM. Retired: upstream deleted that paragraph; the new text has no VM to translate.

## interrogate reviewer entries (blocks/skills/interrogate/SKILL.md), retired at pstack de8ee15

Upstream rewrote interrogate: adversaries now run through arena's runner pick and fan-out (Phase A steps 3 and 4, Phase B), write repros in their own worktrees, and the reviewer template, rubric, code-quality lens, and lead-judgment buckets (`references/*.md`) were deleted. The blocks these entries patched are gone, and the new fan-out block's entry (396b0b06eb52) carries the spawn through arena's patched text.

- 341a35d859a2 (delegate, model-role): Reviewers are delegate_task calls in one message, one per entry on the `interrogate reviewers` line of the project models file, else the defaults below. Preserve the single-message launch and the A, B labeling. Retired: arena's Phase B now does the single-message launch, and upstream dropped the A, B labels.
- fc18e66f1474 (model-role): The default table comes from willyskills's `interrogate reviewers` role. Retired: upstream removed the default table; the role's default is named in the new fan-out entry.
- 2df50e629aaa (general-purpose, read-only, model-role): Each reviewer is a read-only child sharing the checkout, with `target` from its entry per the model-entry snippet. Retired: adversaries now write repros in their own worktrees, and arena's step 3 applies the model-entry snippet.
- 6f513b774653 (model-role): Deleted the rejected-slug and family-prefix fallback. Retired: upstream removed that block; arena's step 3 entry drops the same fallback.
- 9cd5262f18c2 (model-effort): The effort ceiling replaces picking a reasoning level and speed, with the shared reviewer template. Retired: upstream removed the template block; arena's step 3 entry applies the effort ceiling.
