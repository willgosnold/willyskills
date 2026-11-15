# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## skills/interrogate/SKILL.md [2df50e629aaa]

kind: translation
intent: Each reviewer is a read-only child sharing the checkout, with `target` from its entry per the model-entry snippet (inherit-parent omits target). Preserve configured-entry-else-default.
retired: At bf0c7cd upstream replaced the read-only reviewers with adversaries that run arena Phase A steps 3-4 and Phase B, each in its own worktree where it runs repros, so they are no longer read-only. Their targets now come from the patched arena runner step, so this paragraph has no successor. The default for the role moved into entry 396b0b06eb52.

## skills/interrogate/SKILL.md [6f513b774653]

kind: translation
intent: Deleted: the whole block is the rejected-slug and family-prefix fallback, which model-role drops (orchestrator_capabilities lists what exists). If upstream adds non-fallback guidance here, keep that part.
retired: At bf0c7cd upstream removed interrogate's own rejected-slug and family-prefix fallback paragraph. Interrogate now defers to the arena runner step, so there is nothing left to delete.

## skills/interrogate/SKILL.md [9cd5262f18c2]

kind: translation
intent: Replaces picking a reasoning level and fast or standard speed with the effort ceiling from the role's models-file line: lower it for routine work, never raise it. Keep the pointer to the Subagents section and the shared reviewer template.
retired: At bf0c7cd upstream deleted interrogate's references/ (reviewer-prompt.md, rubric.md, code-quality-review.md) and the paragraph that filled the shared reviewer template and set reasoning and speed. The adversary brief is now inline, and effort follows the arena runner step.

## skills/why/SKILL.md [1dee5fd9349d]

kind: translation
intent: Every spawn takes its model from its role line in the project models file, else the role's willyskills default, applied as the model-entry snippet says. Drops the rejected-slug fallbacks; the poteto-mode pointer now only lowers effort within the line's ceiling.
retired: At bf0c7cd upstream cut why down to one paragraph (answer from commits and PR discussions, cite the authors, mark inferences) with no spawns and no model roles, so there is no model paragraph left to translate.

## skills/why/SKILL.md [68051d8304d7]

kind: translation
intent: Every spawn is a plain `delegate_task` that keeps full tool and MCP access; never narrowing `runtimeMode` replaces "do not use readonly/Ask mode". Keeps the reason (MCP-backed investigators and citation spot-checks) and that investigators write nothing, now enforced by the brief and a `git status` check.
retired: At bf0c7cd upstream removed every why spawn, the MCP-backed investigators, and the synthesizer's citation spot-checks. The single remaining paragraph names no subagent or mode.

## skills/why/SKILL.md [e13a8a92d392]

kind: translation
intent: The available MCP servers are the MCP tools in this agent's tool list. Drops the available-tools map and the `mcps/` folder.
retired: At bf0c7cd upstream dropped the step that lists available MCPs before spawning investigators. The new why spawns no investigators and names no MCPs.

## skills/why/SKILL.md [9aad2f123d9c]

kind: translation
intent: Investigators spawn as one `delegate_task` per category in a single message, each owning one MCP, with the model from the `why investigators` line, else its willyskills default.
retired: At bf0c7cd upstream removed the investigator fan-out, and the `why investigators` role was retired from models.json.

## skills/why/SKILL.md [9ea9cff1882e]

kind: translation
intent: The synthesizer takes its model from the `why synthesizer` line, else its willyskills default. The list of what it gets is unchanged.
retired: At bf0c7cd upstream removed the synthesizer and deleted why's references (epistemics.md, synthesizer-prompt.md). The `why synthesizer` role was retired from models.json.
