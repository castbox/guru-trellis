---
name: guru-publish-task-delivery
description: Publish early Draft feedback or final Ready through the original recoverable transaction.
---

# Guru Publish Task Delivery

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget` before
any confirmation, choice or clarification. This Skill retains its own action
plan, confirmation boundary and execution/recovery contract.

Read and apply `.trellis/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage`
for shared candidate coverage, engineering facts and recovery. This package
retains its own current judgment, formal result and action boundary.

Read the current Delivery integration contract in [references/contract.md](references/contract.md) first.

Final Ready requires `guru-review-task-delivery:ready`. Early Draft uses its independent entry. Read
`references/contract.md` before invocation.

1. Run `preview-task-delivery-publication` and review the exact repository,
   branch, PR classification, metadata convergence, Ready action, and maximum
   side effects.
2. Complete the semantic review and obtain dialogue-local confirmation for the
   preview identity when the plan still contains a remote mutation.
3. Invoke `invoke-guru-publish-task-delivery` once with the reviewed input,
   semantic review, and confirmed preview identity.

The owner persists its private transaction before mutation and advances only
through the selected action to its Draft or final Ready terminal. A same-plan retry resumes that transaction. In particular, an unbound
`bind_pr` transaction may recover the unique same-repository Open PR whose
head already equals the reviewed head, persist the binding and convergence
decision, and continue without another push or PR create.

This Skill never archives or completes a task, closes an Issue, emits a closing
keyword, merges a PR, runs Finish, or cleans branches/worktrees. Unknown,
multiple, fork-owned, terminal, stale, or unmapped state fails closed.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.

## Early Draft and Ready revision

`delivery_draft_publish` consumes task/key/B/H and exact Chinese pr_title/pr_body.
It requires accepted Planning in implementing, a nonempty fixed complete range
and actual HEAD H. It does not consume readiness. Review scope, target,
sensitive content and evidence claims. The body separates HEAD checks from
target/integration checks and truthfully lists executed, failed, SKIP and pending
work. Every Delivery body remains Refs-only.

Preview the exact same repo/base/head/PR, title/body and maximum remote writes.
Obtain current-dialogue confirmation only for actual remote mutation. Invoke
the original public wrapper with the completed semantic review. This profile's
route.typed_exit is draft_published. The current 2.0 transaction records its
action/terminal and necessary mutation preimage/postimage. ensure_draft precedes
push. An existing Ready PR is first returned to Draft; binding and exact
metadata convergence reuse that PR. draft_published reads actual PR/HEAD/payload
and enters the feedback router. It never records final PublicationFact.

Before a publishing Delivery receives unreviewed changes, use independent
`delivery_return_to_draft` with concrete revision_reason. Read the original
same PR/HEAD/state and review the exact revision boundary. This owner confirms
Draft and lawfully reworks publication to implementation, invalidating
check/full_review/readiness while retaining Planning, identity and history.
The review route is draft_revision_ready. Its output returns task/key/repo/PR
to implementation. A new HEAD cannot use old readiness.

Same-plan resume keeps the original action/exit and reads actual state after
lost push/create/edit/Draft/Ready output. It accepts the original preimage or
completed postimage. No second PR, repeated push or empty commit restores
stdout. Recover an old action before previewing a new one. The next action
verifies and retires the prior completed transaction; no action journal or
second Delivery store remains.

Final delivery_review_ready still requires current candidate-bound readiness.
Only actual Ready records PublicationFact, and only current gates permit
ready_for_merge. Early feedback/analysis cannot supply a gate. One-time matching
1.0 transaction conversion is defined by MIGRATION-636.


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
