---
name: guru-publish-task-delivery
description: Publish one reviewed active-task Delivery through a semantic gate and an idempotent push, PR binding, metadata, and Ready transaction.
---

# Guru Publish Task Delivery

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
