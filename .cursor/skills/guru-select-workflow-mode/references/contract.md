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

For a local fix, trace the actual changed behavior and its unchanged consumers
before judging risk. A purchase-eligibility prompt or its display condition does
not by itself change pricing, charging, entitlement, or a payment protocol.
Conversely, a UI-only diff may alter one of those behaviors through a shared
consumer. Read the relevant condition, data source and call path, then choose
the route from the actual effect and required validation. Reuse investigation
facts whose current inputs and dependencies still apply; redo the current mode
judgment when scope, authority or risk changes. An already relevant formal Task
continues through its original lifecycle rather than this no-task selection.

Checkout suitability is owned by `guru-execute-task-free-change`, not this DTO.
That Skill reads live local topology, binding, scope and dirty facts and owns
linked non-base execution location selection before writes; isolation alone
never selects standard Intake. It never queries branch protection. The selector
decides only mode and never acquires resources or creates a Task identity. The dialogue-local origin of the selection distinguishes
automatic re-selection from explicit-task-free scope narrowing without adding
public fields or persisted authorization state.
