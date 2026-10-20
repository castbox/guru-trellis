---
name: guru-merge-task-delivery
description: Merge one reviewed active-task Delivery PR through a semantic live gate, exact merge-commit trailers, and terminal recovery.
---

# Guru Merge Task Delivery

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

For an already manually MERGED, published Delivery, select
`delivery_merged_recovery` and read its closed profile in
`references/contract.md#manual-merged-recovery`. Perform that terminal-fact
review before the same public invocation. It records only the actual public
Delivery fact, calls no merge, needs no old gate or trailers, and returns to
original Completion. Never apply the pre-merge checks/confirmation to this
already occurred fact. Both modes use the same entry and review.

Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget` before
any confirmation, choice or clarification. This Skill retains its own action
plan, confirmation boundary and execution/recovery contract.

Read and apply `.trellis/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage`
for shared candidate coverage, engineering facts and recovery. This package
retains its own current judgment, formal result and action boundary.

Read the current Delivery integration contract in [references/contract.md](references/contract.md) first.

Use this Skill only after `guru-publish-task-delivery:ready_for_merge`. Read
[references/contract.md](references/contract.md), preview the exact active task
and live PR facts, then complete the six-dimension semantic review.

`delivered` requires one dialogue-local confirmation for the displayed
repository, PR, expected head, merge method, subject, body, and action identity.
After confirmation invoke the sole public transaction entry:

```bash
scripts/invoke.sh --input <ready-for-merge.json> \
  --review-input <semantic-review.json> --json
```

The reviewed merge body ends with exactly these trailers:

```text
Guru-Task-Identity: <stable-task-id>
Guru-Delivery-Schema: 2
Guru-Delivery-Head: <40-hex-reviewed-head>
Guru-Delivery-Identity: <public-delivery-uuid>
Guru-Task-Generation: <lifecycle-generation>
```

The public invocation performs one pre-read, at most one expected-head
`--merge` mutation, and one post-read. Repeating the same invocation after
output loss reconstructs the same `delivered` result from live PR, commit,
parent, base-ref, and trailer facts without repeating the mutation.
Its terminal DTO carries Task locator and TaskKey only. The Completion owner
reads current overall scope and every actual public Delivery fact, including
history, before judging overall completion. Merge never decides Completion.

The package also exposes the deterministic history command (business facts
remain read-only; temporary Git data is written):

```bash
scripts/discover-task-deliveries.sh --input <delivery-history-query.json>
```

Query 1.0 reconstructs all matching historical Delivery facts from the target-base
first-parent merge history and exact GitHub PR/merge identity. It ignores
merges without Delivery trailers and is independent of PR body text, deleted
head branches, and the task's current branch or worktree binding.
Query 2.0 adds the exact `task_ref` and reads that public Task's already recorded
manual facts, cross-checking real PR/commit/head/base and legal trailer history.
It never imports a PR or writes Task history. Both inputs return result 3.0,
with explicit `task_identity`, `repo_ref`, `base_ref`, `cutoff_commit` and
`deliveries`. The original query owner reads the remote cutoff B1 once,
reuses complete local history or prepares missing immutable objects in a
call-local bare Git context, and verifies that same cutoff without chasing B2.
It does not write caller/peer HEAD, index, workfiles, shared objects/shallow,
refs, FETCH_HEAD, tags, or remote resources. Actual writes are temporary Git
initialization/config/objects/pack and existing candidate file snapshots;
both are removed on exit. Preparation/permission/network, incomplete history
and attribution failures are errors, never an empty success or a request to
fetch manually. A complete scan with no matching facts may return empty.

Consumers use only the public result and their query identity. Unrelated B2
advancement permits direct consumption of B1; a known same-Task new Delivery or
changed required evidence calls this original owner again for missing facts,
without replaying delivered business gates. A lost result reenters this owner
with the known query identity and returns a newly explicit cutoff; it cannot
recover an unobserved old B1 from private state. Query success is not Completion.
See MIGRATION-569 for the synchronized result/consumer migration and
MIGRATION-557 for existing public recorded-fact semantics.

`merge_blocked`, `implementation_required`, and `review_refresh_required` do
not request merge confirmation and perform no remote mutation. Fail closed on
stale task, head, base, PR body, checks, policy, message, gate, or terminal
identity. Never use squash or rebase fallback, parse PR body as Delivery
history, mutate an Issue, complete or archive a task, run Finish, or clean a
branch/worktree/runtime owned by another step.

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
