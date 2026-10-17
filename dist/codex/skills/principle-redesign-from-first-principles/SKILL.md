---
name: principle-redesign-from-first-principles
description: "Apply when integrating a new requirement into an existing design."
disable-model-invocation: true
---

> **pstack install note.** `<pstack>` is `{{PSTACK_ROOT}}`. Once per session, before following this skill, read `{{PSTACK_ROOT}}/adapters/codex.md`. It maps the Cursor names below to this agent. If the T3 Code tools are present (`delegate_task`), also read `{{PSTACK_ROOT}}/adapters/t3.md`. Its rows win for subagents, models, schedules, pull requests, and transcripts.

# Redesign From First Principles

When integrating a change, don't bolt it onto the existing design. Redesign as if the requirement had been a foundational assumption from the start.

- Read all affected files and understand the current design
- Ask: "if we were writing this from scratch with this new requirement, what would we build?"
- Propagate the change through every reference: types, docs, examples, rationale sections
- Think about the whole redesign, then deliver it incrementally

This is the method for preserving option value when integrating changes into an existing design.
