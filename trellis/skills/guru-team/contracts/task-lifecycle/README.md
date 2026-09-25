# Task lifecycle contract primitives

`task-lifecycle-dtos.schema.json` is the canonical Draft 2020-12 catalog for
the shared lifecycle DTO family. Consumers reference one named definition,
for example `#/$defs/TaskArtifactDTO`; they do not accept the catalog's broad
top-level union as a public package output.

The catalog keeps stable task identity, mutable task locator, lifecycle
generation, source relation and operation-scoped result identity separate.
Durable and cross-Skill DTOs contain no checkout path, workspace path, session
identity, authorization state, generic evidence bundle or durable Git HEAD
authority. C3 checkout plan, candidate and selection DTOs are explicitly
call-local facts; their machine paths, Git heads and timestamps must not be
persisted or projected as task/session authority.

`CheckoutAcquisitionPlanDTO.task_artifact_expectation` separates existing
lifecycle resolution (`required`) from pre-task acquisition (`absent`). The
latter validates repository, branch, checkout and exclusivity before the task
creator materializes `task.json`; it does not weaken mismatched-artifact
handling or infer a task from the checkout.

This directory is substrate only. It does not register a Skill, select a
workflow edge or activate a production package.

`task-branch-binding.schema.json` is the closed durable common-dir record for
the current task-to-branch association. Its exact six fields are
`schema_version`, `task_id`, `lifecycle_generation`, integer opaque
`binding_epoch`, `binding_revision`, and portable `branch_name`. Repository
identity comes from the Git common-dir. The record never stores a checkout
path, Git HEAD, session identity, or resource ownership. Initial creation and
full control-state loss create a new epoch at revision zero; one-sided recovery
strictly reuses the surviving epoch and revision; rebind preserves the epoch
while incrementing the revision.

`BranchBindingRefDTO` remains an unchanged public DTO in the shared catalog.
It is not the durable branch record and consumers must not serialize it as one.

`task-branch-rebind-transaction.schema.json` is an owner-private, short-lived
checkpoint for exact rollback and lost-output recovery. It may bind call-local
paths, Git identities, byte digests, and the resource-ledger revision because
those facts are retired with the transaction. The two closed routes are
`same_checkout_new_ref` and `existing_target`; neither route changes the six-
field durable binding identity. The target revision is stored separately, but
the unchanged rebind epoch is derived only from `source_binding.binding_epoch`
so the checkpoint cannot encode contradictory source and target epochs.

Same-checkout rollback eligibility begins before `git switch -c`: a failing
`post-checkout` hook may return non-zero after Git has already created and
checked out the target ref. Recovery removes that ref only when it still points
to the reviewed pre-state HEAD and no registered checkout uses it.

Establishment candidate IDs are stable labels over branch, candidate kind, and
call-local checkout path; they deliberately exclude Git HEAD. The mutation
still consumes the reviewed candidate HEAD and performs fresh discovery before
writing control state. Read-only output-loss recovery consumes the expected
epoch, revision, branch, and HEAD, and rejects a branch that has advanced.

`guru-establish-task-branch-binding` and `guru-rebind-task-branch` are reserved
only as planned stable IDs in C4. Their canonical packages, workflow routes,
installed copies, and platform projections remain owned by the E434 atomic
activation.

`session_adapter.py` is the C5 boundary over the Fixed Fork official schema-2
session API. It validates `TaskLifecycleDTO`, writes exactly
`schema_version/task_id/lifecycle_generation`, and resolves the current TaskRef
through the official TaskId resolver. A missing context key returns
`explicit_task_mode`; a session write failure is session-local and never owns
rollback of an already completed lifecycle mutation. The adapter contains no
copy of `.trellis/scripts/common/**` and creates no second session store.

`task-resource-ledger.schema.json` is the closed Git-common-dir ownership
record at `trellis/task-resources/<task-id>/<generation>.json`. Each resource
incarnation records its acquisition origin, conservative ownership, portable
ref, binding epoch/revision, state, responsibility role, and exact cleanup
commit when sealed. A remote portable ref includes the remote name, repository
identity, and branch ref so Cleanup can identify the exact remote incarnation.
Unknown or unprovable ownership is represented as
`caller_owned`; checkout paths are never stored.

The same ledger records the exact `finish_result_id` and `finish_head` once
Finish seals the current bundle. An exact retry rematerializes the seal without
rewriting ownership; a different result or HEAD conflicts. Cleanup verifies
the same Finish result before projecting the sealed inventory. These fields
belong only to the Finish seal, not to a generic ledger transaction protocol.

Ledger mutation owners use exact-byte snapshot/restore through the concrete C4
port. Conservative active recovery and remote-delivery recording also
rematerialize an already established exact successor without rewriting it.
No second transaction store or speculative checkpoint schema is introduced.

`task-resource-seal-input.schema.json` carries the exact Finish HEAD used to
seal the current Guru-owned resources and returns one ledger revision and
complete responsibility inventory identity.
`task-resource-cleanup-resolution.schema.json` separates ordinary Guru-owned
cleanup, terminal manual selection, and already-clean results. Ordinary
Cleanup includes only `guru_owned + cleanup_pending` resources and excludes
caller-owned, unknown-ownership, and `refs/heads/guru-task-lifecycle/*`
retained control refs.

C5 remains substrate only. It does not activate D443/D436, create a planned
Skill package, change the production workflow, or publish installed/platform
projections; those transitions remain owned by E434.

The C6 `task-creation-input.schema.json` separates reviewed
`existing_issue | standalone_request` source from accepted scope identity and
portable delivery target. Its selected base ref/head and C3 checkout acquisition
plan are call-local preconditions, not durable task authority. The C3 provision
dispositions are `new_branch | existing_branch | existing_checkout`: the first
creates Guru-owned branch and worktree, the second creates only a Guru-owned
worktree, and the third reuses caller-owned resources. Primary and linked
adoption preserve caller ownership. After the official task creator writes a
generation-zero planning artifact containing the reviewed `source` and
`delivery_target`, `establish_created_control_state` composes the initial C4
binding and C5 ledger. `recover_created_control_state` reads the exact stable
task/source/target, binding epoch, ledger and deterministic
`task-created:<TaskId>` result identity without another mutation. Accepted
scope remains the separate reviewed input, not a substitute source or closure
decision; the future package must check its own scope authority and live Issue.
`bind_created_session` runs the C5 official-backed adapter only after the exact
initial creation state is verified. Missing context enters explicit-task mode;
session write failure does not roll back the established task or ownership.

`task-activation-input.schema.json` requires a planning result, current task
incarnation, selected base ref, base-current reviewed base HEAD or reconciled
new base HEAD plus task-head continuity, and the C5
`session_bound | explicit_task_mode` outcome. `prepare_activation_inputs`
checks the live planning status, current branch/ledger pair, task head,
selected base identity, live base HEAD, and ancestry. It does
not approve planning, select a route, mutate status or claim output-loss
recovery for the eventual activation owner. The E434 package must provide
those semantic and transaction contracts before either planned ID is active.
