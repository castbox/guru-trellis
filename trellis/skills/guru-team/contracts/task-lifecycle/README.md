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
the current task-to-branch association. Its exact five fields are
`schema_version`, `task_id`, `lifecycle_generation`, `binding_revision`, and
portable `branch_name`. Repository identity comes from the Git common-dir. The
record never stores a binding epoch, checkout path, Git HEAD, session identity,
or resource ownership.

`BranchBindingRefDTO` remains an unchanged public DTO in the shared catalog.
It is not the durable branch record and consumers must not serialize it as one.

`task-branch-rebind-transaction.schema.json` is an owner-private, short-lived
checkpoint for exact rollback and lost-output recovery. It may bind call-local
paths, Git identities, byte digests, and the resource-ledger revision because
those facts are retired with the transaction. The two closed routes are
`same_checkout_new_ref` and `existing_target`; neither route changes the five-
field durable binding contract.

`guru-establish-task-branch-binding` and `guru-rebind-task-branch` are reserved
only as planned stable IDs in C4. Their canonical packages, workflow routes,
installed copies, and platform projections remain owned by the E434 atomic
activation.
