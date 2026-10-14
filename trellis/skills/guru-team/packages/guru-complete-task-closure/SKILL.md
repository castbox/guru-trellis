---
name: guru-complete-task-closure
description: Apply the exact source Issue disposition after Completion approval and return a recoverable closure result.
---

# Guru Complete Task Closure

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
close authority produce no Issue mutation. Show each exact close action and
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
recovery. A changed frozen authority or reopened required-closed Issue returns
`external_change_conflict` for fresh Closure semantic re-entry; Finish must
not repair or replay that disposition. `closed|no_mutation` carry only the
Closure `ResultRefDTO`. The current graph sends these results to Finish; this
package does not decide Completion or own the workflow projection.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
