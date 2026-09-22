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
