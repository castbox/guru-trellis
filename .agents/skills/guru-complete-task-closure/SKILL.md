---
name: guru-complete-task-closure
description: Apply the exact source Issue disposition after Completion approval and return a recoverable closure result.
---

# Guru Complete Task Closure

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

`judgment_mode=semantic`: review current authority and the complete action set,
complete the AI Review Gate, obtain current-dialogue confirmation for actual
close mutations, then invoke the executor/validator and return one typed exit.

Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget` before
any confirmation, choice or clarification. This Skill retains its own action
plan, confirmation boundary and execution/recovery contract.

Before any Closure transaction, reread the exact public Completion result for
the current Task generation and accepted scope. Keep source-disposition and
frozen action-set review/confirmation/remote recovery unchanged. After actual
source closure or no-mutation completion, project only the public Closure fact.
Projection failure returns the same resume transaction; a closed Issue must not
be closed again. No authorization is persisted. Closure is not Finish archive.


Consume only the current Completion `completed` ResultRef. Freshly review source
relation, accepted scope, target, branch binding, content and evidence slots,
then author the complete per-Issue action set. No-Issue and relations without
close authority produce no Issue mutation. `exact_source` establishes source
relation and eligibility for a reviewed disposition; it does not require a close.
Judge the whole current Task scope separately from the source Issue's remaining
responsibilities. A completed Task whose source retains explicit responsibility
uses `retain_open`, preserving TaskId, generation and source. Do not rewrite it
as `reference_only` or `no_issue` to obtain Finish.

| Action | Required provider state and execution |
| --- | --- |
| `close` | Existing confirmed close and same-owner recovery require terminal CLOSED. |
| `already_closed_at_review` | Observe CLOSED without invoking close. |
| `retain_open` | Exact-source authority reviewed to retain OPEN; observe OPEN without invoking close. |
| `no_close_authority` | A non-exact relation has no close qualification; retain its existing no-mutation behavior. |

No-Issue uses an empty action set. Exact source rejects `no_close_authority` on
its own action; non-exact sources reject executable/retain actions. Review the
eligibility of every additional Issue in the existing multi-Issue action set.
If the semantic review is blocked, return its original reason after identity
and action uniqueness validation, before executable action eligibility; do not
create a transaction or mutate the provider for a blocked review.

Show each exact close action and
obtain dialogue-local confirmation before invoking with `--confirmed-close`.
Reread the current `task.json.source` disposition before any action; only a
missing source with exact canonical Issue scope may normalize to `exact_source`.
For a noncanonical legacy scope with no structured source, freshly review the
non-exact relation and freeze it in the Closure transaction without writing
task metadata. An input source mismatch or non-exact close action fails before
mutation.
The runtime freezes this entire set in owner-private state, rereads exact Issue
state, and closes only actions with reviewed close authority.

`resume_closure` carries `TransactionRefDTO` for same-owner output-loss
recovery. A changed frozen authority, reopened required-closed Issue or closed
required-open Issue returns
`external_change_conflict` for fresh Closure semantic re-entry; Finish must
not repair or replay that disposition. `closed|no_mutation` carry only the
Closure `ResultRefDTO`. Aggregate `closed` means the set contains a close or
already-closed action; a pure retain set returns `no_mutation`. Public Task2
`source_closed` derives only from the exact source action, never another Issue's
closure. A retained source records public `no_mutation` with `source_result=null`,
even when another action makes the aggregate terminal `closed`.
Both results hand the existing reference to Finish, which reads the exact
frozen action set and required OPEN/CLOSED states. Apply the matching Closure
and Finish packages together before using the additive action; older consumers
must not receive `retain_open`. Existing action values, refs and exits retain
their meanings; see the installed task-delivery-migration spec.
The current graph sends these results to Finish; this
package does not decide Completion or own the workflow projection.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
