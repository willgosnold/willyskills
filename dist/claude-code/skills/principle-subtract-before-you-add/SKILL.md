---
name: principle-subtract-before-you-add
description: "Apply when sequencing an addition, refactor, or rewrite. Remove dead code, redundant validators, and stub references first, then build on the simpler base."
disable-model-invocation: true
---

> **pstack install note.** `<pstack>` is `{{PSTACK_ROOT}}`. Once per session, before following this skill, read `{{PSTACK_ROOT}}/docs/harness/claude-code.md`, then `{{PSTACK_ROOT}}/adapters/claude-code.md`. They map the Cursor names below to this agent. If the T3 Code tools are present (`delegate_task`), also read `{{PSTACK_ROOT}}/adapters/t3.md`. Its rows win for subagents, models, schedules, pull requests, and transcripts.

# Subtract Before You Add

When evolving a system, remove complexity first, then build. Default to subtraction.

Make simplification a continual investment. Leave the design slightly simpler and more capable behind the same or smaller surface than you found it.

- Sequence removal before construction
- Cut before you polish (get to the minimum before investing in quality)
- Design for observed usage, not speculative edge cases
- No speculative validators, parsers, or guards beyond what the spec demands
- Simplify prompts (remove redundant instructions, excessive templates)
- When a reference has no novel content, delete it rather than leaving a stub
