# Workflow Mode Selector Contract

This is a semantic Skill with a minimal public handoff. The public input only
identifies the invocation mode and caller continuation. The AI must not infer
the selection from a script, keyword list, or recorder result.

Entry includes proposed-change requirements discussion, feature design, and
planning even when this turn defers file writes or resource creation. A direct
information-only answer about existing facts remains outside this entry.
For no-task change intent, loading an upstream method does not replace the
actual public selection or the selected Guru owner. Respect deferred side
effects while following the workflow's mandatory graph.

The owner-private result is transient and contains the semantic selection,
confirmation disposition, and current continuation identity. The public DTO
contains only `exit_id`; the consumer is selected by the typed exit. Missing,
stale, duplicate, unknown, or unmapped results fail closed.

The selection has three AI-owned outcomes when there is no explicit task-free
intent: high-confidence bounded low-risk work selects `task_free`; likely but
insufficient evidence opens one mode question; clearly complex or high-risk
work, requirements clarification, or full change planning selects
`standard_intake`. The AI judges that need from the current request and facts;
deferred writes alone neither select task-free nor introduce a mode question.
An already bounded local edit retains the ordinary task-free selection rules,
including explicit intent and the one real mode choice when needed.
Issue presence, file count, paths, and keywords
cannot independently decide the outcome.

Checkout suitability is owned by `guru-execute-task-free-change`, not this DTO.
That Skill checks only local repository, branch/worktree,
active-task scope, and dirty overlap facts before writes and never queries
branch protection. The dialogue-local origin of the selection distinguishes
automatic re-selection from explicit-task-free scope narrowing without adding
public fields or persisted authorization state.
