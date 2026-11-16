# Retired entries

Patches that no longer apply, newest first. Each keeps its intent and says why it was retired.

## why/SKILL.md block entries

Retired at upstream bf0c7cd. Upstream rewrote the why skill as one paragraph that reads the record itself: no subagents, no MCP inventory, no investigators or synthesizer, and its references/ folder is gone. No block in it uses a Cursor term, so none of these entries has a block to patch. The `why investigators` and `why synthesizer` roles retired with it.

- `1dee5fd9349d`: Every spawn takes its model from its role line in the project models file, else the role's willyskills default, applied as the model-entry snippet says. Drops the rejected-slug fallbacks; the poteto-mode pointer now only lowers effort within the line's ceiling.
- `68051d8304d7`: Every spawn is a plain `delegate_task` that keeps full tool and MCP access; never narrowing `runtimeMode` replaces "do not use readonly/Ask mode". Keeps the reason (MCP-backed investigators and citation spot-checks) and that investigators write nothing, now enforced by the brief and a `git status` check.
- `e13a8a92d392`: The available MCP servers are the MCP tools in this agent's tool list. Drops the available-tools map and the `mcps/` folder.
- `9aad2f123d9c`: Investigators spawn as one `delegate_task` per category in a single message, each owning one MCP, with the model from the `why investigators` line, else its willyskills default.
- `9ea9cff1882e`: The synthesizer takes its model from the `why synthesizer` line, else its willyskills default. The list of what it gets is unchanged.
