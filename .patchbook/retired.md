# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

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
