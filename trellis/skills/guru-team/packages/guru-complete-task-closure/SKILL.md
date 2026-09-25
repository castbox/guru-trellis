---
name: guru-complete-task-closure
description: Apply the exact source Issue disposition after Completion approval and return a recoverable closure result.
---

# Guru Complete Task Closure

Consume only the current Completion `completed` ResultRef. Freshly review source
relation, accepted scope, target, branch binding, content and evidence slots,
then author the complete per-Issue action set. No-Issue and relations without
close authority produce no Issue mutation. Show each exact close action and
obtain dialogue-local confirmation before invoking with `--confirmed-close`.
Reread the current `task.json.source` disposition before any action; only a
missing source with exact canonical Issue scope may normalize to `exact_source`.
An input source mismatch or non-exact close action fails before mutation.
The runtime freezes this entire set in owner-private state, rereads exact Issue
state, and closes only actions with reviewed close authority.

`resume_closure` carries `TransactionRefDTO` for same-owner output-loss
recovery. A changed frozen authority or reopened required-closed Issue returns
`external_change_conflict` for fresh Closure semantic re-entry; Finish must
not repair or replay that disposition. `closed|no_mutation` carry only the
Closure `ResultRefDTO`. This canonical package is not a production graph
activation; downstream Finish and workflow projection migration belong to
the later activation owner.
