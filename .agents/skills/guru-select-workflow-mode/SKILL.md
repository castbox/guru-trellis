---
name: guru-select-workflow-mode
description: Select standard Guru Team intake or a bounded task-free current-checkout route through one AI-owned semantic decision.
---

# Guru Select Workflow Mode

Run this Skill for every file-changing request that has not already entered an
active-task route. Issue presence, current branch, and task-free wording do not
control entry. The AI owns the semantic decision; scripts only validate a
completed selection and serialize the one typed exit.

Use `task_free` immediately when the user explicitly requests that semantic;
the shortest public expression is `这次走 task-free`. Recognize equivalent
multilingual wording semantically rather than through a keyword table. Neither
`帮我改一下` nor `不要开 Issue` is explicit task-free intent.

Without explicit intent, read only the limited live repository and Issue facts
needed for the decision:

- automatically select `task_free` when the boundary is clear, local,
  reversible, and confidently has no obvious high-risk effect;
- ask one concise mode question when task-free is likely but scope or risk
  evidence is insufficient; an affirmative answer selects `task_free` and a
  refusal selects `standard_intake`, with no repeated question for the same
  scope;
- automatically select `standard_intake` when isolation, planning, complete
  review, or high-risk validation is clearly needed, including material runtime,
  cross-layer contract, public API, schema, CI, install/update, deploy,
  permission, security, or data impact.

An Issue supplies evidence but never decides the mode. File count, paths, and
keywords are weak evidence only and never independent classifiers. Once
selected, mapped exits, ordinary recovery, and same-scope retries reuse the
selection. Material scope, authority, or risk changes require a fresh semantic
decision.

`task_free` is limited to the current checkout and the explicitly bounded
files for this turn. It never authorizes task/worktree/branch creation,
commit, push, PR, merge, tag, release, installation, or cleanup. Preserve all
unrelated dirty and untracked files. Its workflow consumer separately checks
checkout suitability using local branch/worktree, active-task scope, and dirty
overlap facts; it never reads remote branch protection and does not add fields
to this Skill's public DTO.

During execution, stop further writes when scope or risk expands. For an
automatically selected task-free route, run this semantic selection again. For
an explicitly selected route, report the new facts and let the user narrow the
scope or choose `standard_intake`; do not silently upgrade. Commit, push, PR,
merge, release, installation, cleanup, and Issue closure remain independent
later authorizations.

Return exactly one of `standard_intake`, `task_free`, or `blocked`.
