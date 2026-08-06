---
name: guru-select-workflow-mode
description: Select standard Guru Team intake or a bounded task-free current-checkout route through one AI-owned semantic decision.
---

# Guru Select Workflow Mode

Run this Skill before normal Intake for a no-task request. The AI owns the
semantic decision; scripts only validate a completed selection and serialize
the one typed exit.

Use `task_free` immediately when the user explicitly says to avoid the flow,
not use Trellis, skip the process, or edit directly in the current checkout.
If the intent is only implicit, ask one concise confirmation. A refusal maps to
`standard_intake` without another question. Once selected, mapped exits,
ordinary recovery, and same-scope retries reuse the selection. Scope,
authority, or a new side effect must be re-evaluated. Ambiguity always maps to
`standard_intake`.

`task_free` is limited to the current checkout and the explicitly bounded
files for this turn. It never authorizes task/worktree/branch creation,
commit, push, PR, merge, tag, release, installation, or cleanup. Preserve all
unrelated dirty and untracked files.

Return exactly one of `standard_intake`, `task_free`, or `blocked`.
