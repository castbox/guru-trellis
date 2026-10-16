---
name: guru-publish-task-delivery
description: Publish one reviewed active-task Delivery through a semantic gate and an idempotent push, PR binding, metadata, and Ready transaction.
---

# Guru Publish Task Delivery

Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget` before
any confirmation, choice or clarification. This Skill retains its own action
plan, confirmation boundary and execution/recovery contract.

Read the current Delivery integration contract in [references/contract.md](references/contract.md) first.

Use only after `guru-review-task-delivery:ready`. Read
`references/contract.md` before invocation.

1. Run `preview-task-delivery-publication` and review the exact repository,
   branch, PR classification, metadata convergence, Ready action, and maximum
   side effects.
2. Complete the semantic review and obtain dialogue-local confirmation for the
   preview identity when the plan still contains a remote mutation.
3. Invoke `invoke-guru-publish-task-delivery` once with the reviewed input,
   semantic review, and confirmed preview identity.

The owner persists its private transaction before mutation and advances only
through `push_content`, `bind_pr`, `converge_metadata`, `mark_ready`, and
`ready`. A same-plan retry resumes that transaction. In particular, an unbound
`bind_pr` transaction may recover the unique same-repository Open PR whose
head already equals the reviewed head, persist the binding and convergence
decision, and continue without another push or PR create.

This Skill never archives or completes a task, closes an Issue, emits a closing
keyword, merges a PR, runs Finish, or cleans branches/worktrees. Unknown,
multiple, fork-owned, terminal, stale, or unmapped state fails closed.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.

## Current-stage scope revision

`delivery_scope_revision` is this existing owner's semantic re-entry after original
Clarify has published the changed whole-Task scope. Read actual accepted scope,
selected Delivery and obligations; review the retained slice anchors and original
source_selection/revision_refs. Complete the AI gate before invoking this profile.
Do not require stale Planning/Check/Review/Readiness evidence to revise scope.
Project only the reviewed current scope_ref through upstream rework to planning;
invalidate planning/check/full_review/readiness and retain identity, candidate and
historical publication/delivery facts. No new acceptance or approval is inferred.
`delivery_scope_revised` goes only to guru-delivery-scope-revised-router and the
same Delivery Author active_task_scope_change. A retry after lost output reads
matching public scope, planning phase and cleared results; it returns the same
minimal handoff, without replaying rework or installing an approval token.
A new change receives fresh original Clarify and this owner judgment.

For explicit selected legacy maintenance, load the legacy section in `references/legacy-maintenance.md` and use `scripts/legacy-maintenance.sh`; ordinary current invocation remains unchanged.
