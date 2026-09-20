# Workflow Mode Selector Contract

This is a semantic Skill with a minimal public handoff. The public input only
identifies the invocation mode and caller continuation. The AI must not infer
the selection from a script, keyword list, or recorder result.

The owner-private result is transient and contains the semantic selection,
confirmation disposition, and current continuation identity. The public DTO
contains only `exit_id`; the consumer is selected by the typed exit. Missing,
stale, duplicate, unknown, or unmapped results fail closed.

The selection has three AI-owned outcomes when there is no explicit task-free
intent: high-confidence bounded low-risk work selects `task_free`; likely but
insufficient evidence opens one mode question; clearly complex or high-risk
work selects `standard_intake`. Issue presence, file count, paths, and keywords
cannot independently decide the outcome.

Checkout suitability is owned by `guru-execute-task-free-change`, not this DTO.
That Skill checks only local repository, branch/worktree,
active-task scope, and dirty overlap facts before writes and never queries
branch protection. The dialogue-local origin of the selection distinguishes
automatic re-selection from explicit-task-free scope narrowing without adding
public fields or persisted authorization state.
