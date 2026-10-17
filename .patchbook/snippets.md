# Snippets

Shared sentences for patched blocks. `{{snippet:<name>}}` in a patched block expands to the text under `## <name>`, trimmed.

## models-file

`.agents/pstack-models.md` in the project's main checkout (`"$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")/.agents/pstack-models.md"`, which may not exist)

## model-entry

A role line is `<role>: <entry>, <entry>, ...`, and a panel role runs one subagent per entry. An entry `<provider>/<model> <effort>` becomes `target: {providerInstanceId: <provider>, model: <model>, options: {effort: <effort>}}`, with `reasoningEffort` instead of `effort` for `codex`. `inherit-parent` means omit `target`. The effort is a ceiling: lower it for routine work, never raise it, and never set `fastMode`.
