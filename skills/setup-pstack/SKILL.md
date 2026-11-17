---
name: setup-pstack
description: Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes a project models file that overrides the defaults. Use for /setup-pstack or $setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack

Write `.agents/pstack-models.md` in the project's main checkout (`"$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")/.agents/pstack-models.md"`, which may not exist). It sets pstack's model per role and overrides the defaults.

## Steps

### 1. Detect available models

Call `orchestrator_capabilities`. Each entry in `providers` lists a provider instance's models and each model's effort options (`effort`, or `reasoningEffort` for `codex`). That is the dependable source. A provider whose `canRunChildTask` is false can't run a role, so leave it out. If you cannot detect any, ask the user to paste the models they have access to. Never write a real model you have not confirmed is available. The alias `inherit-parent` is always valid even though it is not a detected model.

### 2. Load current state

The defaults are the role entries listed in step 5 below. If that file already exists, read it and treat its `# budget:` line and its role entries as the current choices. Otherwise start from those defaults. A line whose role is not in step 5, such as `how critics`, is from a retired role. Drop it.

A file without the `# defaults: 3` line comes from an older setup. Before step 3, replace this value:

- A `# budget: unlimited` line becomes `large`, because no role runs above `xhigh`.

Every other value is the user's choice and stays, including every `inherit-parent` value. Tell the user which values you replaced.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Ask in plain text, then end the turn. Offer these three options with these exact labels, and name the current budget when the file records one. With no models file, say that `large` matches the defaults.

- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) Apply it.** Build the working table from the defaults, and on a re-run keep any role you changed by model, list, or alias (`inherit-parent`). Each real entry has a target effort: the effort of the role's default entry for the same model, else the role's highest default effort, moved by the budget. `large` keeps it, `medium` lowers it one step, and `small` lowers it two steps, on the ladder `xhigh` > `high` > `medium` > `low`. Ignore effort options off that ladder. No entry runs above `xhigh`, and a target at the bottom of the ladder stays there. Each budget label names where an `xhigh` default lands. Set the effort of every real entry, panel entries included, to its target. If the model doesn't offer that effort, use the highest effort it offers below it, else mark the role as needing a choice. `inherit-parent` does not change. So `medium` turns an `xhigh` entry into `high` and a `high` entry into `medium`, and `small` turns them into `medium` and `low`.

**(c) Show the roles and confirm.** Show every role with its entries, marking any real entry not in the detected set as needing a choice. Also list each line step 2 dropped. Ask whether to accept as-is or change specific roles, offering the detected models at `xhigh` or below plus `inherit-parent` (this role runs on the parent chat model) as the options. Ask in plain text, then end the turn. For panel roles (arena runners, architect runners, interrogate reviewers) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena runs one judge. It takes the first value in list order whose provider differs from the parent's, else the first value, so order it by preference. An `inherit-parent` value is the parent's model, so it never counts as another provider. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

### 4. Validate

Every real entry written must be a detected model with an effort that model offers, at `xhigh` or below. `inherit-parent` always passes. If a chosen real entry is not available, stop and ask again.

### 5. Write the models file

Write that file with the `# defaults: 3` line, a `# budget:` line holding the chosen label and the effort that label names, and one line per role, using the role names below. Create `.agents/` if it is missing. Overwrite the whole file so re-runs stay idempotent. Shape:

```
# pstack model configuration. One line per role. Delete a line to fall back to the default.
# Entry: <provider>/<model> <effort>. `inherit-parent` runs the role on the parent's model (omit `target`). Alias entries in a panel list still count toward its fan-out.
# defaults: 3
# budget: <label> (<effort>)
<role>: <entry>, <entry>, ...
```

The roles, in this order, with their defaults:

- `feature, refactoring`: `claudeAgent/claude-sonnet-5-5 high`
- `bug-fix`: `claudeAgent/claude-sonnet-5-5 high`
- `perf-issue`: `claudeAgent/claude-haiku-5-5 xhigh`
- `hillclimb`: `claudeAgent/claude-sonnet-5-5 high`
- `judgment and prose`: `claudeAgent/claude-opus-5-5 high`
- `hardest tasks`: `claudeAgent/claude-opus-5-5 xhigh`
- `how explorer`: `claudeAgent/claude-haiku-5-5 xhigh`
- `how explainer`: `claudeAgent/claude-opus-5-5 high`
- `why investigators`: `claudeAgent/claude-haiku-5-5 xhigh`
- `why synthesizer`: `claudeAgent/claude-opus-5-5 high`
- `reflect tooling`: `claudeAgent/claude-haiku-5-5 xhigh`
- `reflect judgment, divergent, synthesizer`: `claudeAgent/claude-opus-5-5 high`
- `arena runners`: `claudeAgent/claude-opus-5-5 high`, `codex/gpt-6.1-sol xhigh`
- `arena cross-judge pool`: `claudeAgent/claude-opus-5-5 high`
- `swarm workers`: `claudeAgent/claude-haiku-5-5 xhigh`
- `architect runners`: `claudeAgent/claude-opus-5-5 high`, `codex/gpt-6.1-sol xhigh`
- `interrogate reviewers`: `claudeAgent/claude-opus-5-5 high`, `codex/gpt-6.1-sol xhigh`

### 6. Confirm

Tell the user the file was written and that skills read it at each spawn. Re-running this skill updates it. Tell the user to commit the file if worktrees and other people should see it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with the **create-verification-skill** skill." On yes, run the **create-verification-skill** skill (resolves wherever pstack is installed: workspace, user, or plugin). On no, move on without pushing.

### 8. Offer a formal verification skill (optional)

Check whether the project already has a formal verification skill (a project skill that runs a model checker, a proof, or another verifier against the code). If not, offer once: "want a formal verification skill, so agents can prove a key property of your code holds in every case in scope, not only the cases tests reach? I can generate one with the **create-formal-verification-skill** skill." On yes, run the **create-formal-verification-skill** skill (resolves wherever pstack is installed: workspace, user, or plugin). On no, move on without pushing.
