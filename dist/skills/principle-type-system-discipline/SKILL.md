---
name: principle-type-system-discipline
description: "Apply when designing types, reviewing a function signature, or writing code in any statically-typed language. Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, exhaust variants, derive from authoritative schemas."
disable-model-invocation: true
---

> **pstack install note.** Once per session, before following this skill, read your agent's adapter. It maps the Cursor names below to your agent. Paths are relative to this file's folder. In Claude Code, read `../pstack/docs/harness/claude-code.md`, then `../pstack/adapters/claude-code.md`. In Codex, read `../pstack/adapters/codex.md`. If the T3 Code tools are present (`delegate_task`), also read `../pstack/adapters/t3.md`. Its rows win for subagents, models, schedules, pull requests, and transcripts.

# Type System Discipline

Make the compiler reject impossible states, mismatched primitives, and unhandled variants. Prefer defining errors and special cases out of existence over proliferating handlers. For TypeScript syntax, see the `typescript-best-practices` skill.

- **Brand semantic primitives.** `UserId` and `OrderId` are strings underneath but should not be interchangeable. Give each its own type, such as a branded intersection in TypeScript or a newtype elsewhere. Validate once at creation, trust the type downstream. If two arguments share a primitive type but mean different things, brand them.
- **External data is untyped until parsed.** RPC payloads, JSON, IPC messages, CLI args, config files, environment variables, database rows. Have a parse function at every boundary that turns unstructured input into the typed model. The **boundary-discipline** principle skill says where to put validation.
- **Derive types from authoritative schemas.** When a protocol buffer, OpenAPI spec, GraphQL schema, database migration, design-token file, or another file owns a shape, derive from it instead of hand-rolling a parallel type. See the **encode-lessons-in-structure** principle skill.
