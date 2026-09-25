# #454 C6/C7 Task Creation And Phase C Validation Architecture Contribution

## Identity And State

- contribution identity: `architecture-contribution-454-task-lifecycle-state-model-c6-c7-v1`.
- state: `candidate_unreviewed`; no shared-current promotion or gate pass is claimed.
- source: live `castbox/guru-trellis#454`, task `.trellis/tasks/09-20-454-task-lifecycle-state-model` generation 4, `implement.md` C6/C7.
- expected Architecture and RDT baseline: `current-main-0.6.17-guru.63` / `active`.
- related RDT candidate: `docs/requirements-design-test-contributions/454-task-lifecycle-state-model-c6-c7/`.
- constitution/change contract: `guru-trellis-design-constitution-v1` / `guru-trellis-architecture-change-contract-v1`.
- change path: `target_native`; `ADR-015` remains the identity/framework boundary owner, so no new ADR is proposed.

This is an isolated proposal for C6 shared task-creation substrate and activation inputs, followed by C7 subtraction
evidence and Phase C validation. It does not assert that code, schema, registry, installer, workflow, or tests have been
changed in this Docs-only contribution. `.63` continues to own CURRENT; this candidate must not be cited as `.64`
CURRENT or as evidence that the production graph has switched.

## Proposed Boundary

`guru-create-task` is the future task-creation owner for reviewed `existing_issue | standalone_request` targets.
Issue creation and fresh Intake stay separate. Both acquisition routes project one stable TaskId, generation 0,
mutable TaskRef, current branch association and resource responsibility: adoption validates the registered invocation
checkout and preserves caller ownership; provision binds the call-local reviewed live pre-state to C3
`CheckoutAcquisitionPlan.provision_disposition` (`new_branch | existing_branch | existing_checkout`). The first
creates a branch and linked worktree, the second creates only a linked worktree for an existing branch, and the third
reuses the exact registered linked checkout. Only resources actually created by Guru become Guru-owned; adoption
has no provision disposition. Machine-local checkout root stays call-local. The task source and
accepted scope remain separate; no-Issue creates no synthetic Issue or Closure authority. Official Fixed Fork
task create/rename/archive and schema-2 session persistence remain framework-owned, while C2/C3/C4/C5 provide the
shared lifecycle, checkout, branch and ledger primitives; C6 may compose them without copying their stores.

Task creation must align initial binding and ledger identity, use the C5 adapter to bind a usable context key, and
otherwise return `explicit_task_mode` without undoing a completed lifecycle mutation. Loss of output recovers the
same established task/result by read-only identity checks; it must not repeat Issue, task, branch, worktree, binding
or ledger creation. The planned `guru-activate-task` is the sole future `planning -> in_progress` mutation owner;
Planning approval alone is not activation, and its output-loss recovery must not repeat the status mutation.

The six C6 owner IDs (`guru-create-task`, `guru-establish-task-identity`, `guru-establish-task-branch-binding`,
`guru-ensure-task-checkout`, `guru-rebind-task-branch`, `guru-activate-task`) are planned activation inputs, not
complete packages. A planned registry row contains only future stable identity, not package/interface/route/I/O;
`planned_skill_ids` does not activate `active_skill_ids`. No canonical package tree for a planned owner, mandatory
workflow invocation, installed/platform projection or production selector change belongs to Phase C. E434 owns
the complete packages, consumer closure and atomic activation; D443/D436 own their later package migrations.

## Validation And Retirement Boundary

C7 establishes evidence that newly added Phase C code has zero reads/writes of task/workspace mappings,
`worktree_path`, `source_checkout` and legacy session path fields. Existing production predecessor readers/writers
remain until E434 switches and retires them together. A search over old production code is not a valid zero-use
claim; the scope of the proof must be the new substrate. There is no dual-read/write alias or second durable
workspace identity in the target model.

Candidate validation must distinguish focused Fork and lifecycle runtime/schema tests, no-Issue and both acquisition
routes, session explicit-task result, activation-input requirements, planned-versus-active inventory and absence of
planned package trees. It also requires source preparation, upstream ownership, overlay drift, recursive sidecars,
managed Python routing, task validation, formatting/lint/type checks, secret scan, and a touched non-generated file
line-count report. A representative clean throwaway is conditional on accepted scope and proves only fixed Fork
primitives, not installed planned packages. Full multi-platform Release matrix remains with #410. These are
acceptance obligations, not test results; no Phase 2, Task Commit, independent full Branch Review, serialized Docs
promotion, Publication, push, PR, merge or release result is asserted here.

This candidate narrows `ARCH-GAP-011` only after implementation and review. The current `.63` gap remains open;
C6/C7, D443, D436, E434 and #434 activation cannot be inferred from this contribution alone.
