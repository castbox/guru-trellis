---
name: guru-finish-task
description: Persist Completion and Closure into one reviewed task archive and terminal bookkeeping result.
---

# Guru Finish Task

`judgment_mode=semantic`: review current Closure and terminal bookkeeping,
complete the AI Review Gate, confirm each actual mutation boundary in the
current dialogue, then invoke the executor/validator and return one typed exit.

Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget` before
any confirmation, choice or clarification. This Skill retains its own action
plan, confirmation boundary and execution/recovery contract.

Before archive projection, verify current public Closure. Preserve the schema-2
Task aggregate byte semantics: never write `status`, `completedAt`, `commit`, or
`pr_url`. Finish alone owns archive summary and bookkeeping publication, with
separate confirmations for its exact Git/GitHub mutations. Public Delivery
facts and planning roots move with the Task; archive and terminal persistence
do not erase them or pretend Cleanup succeeded.


Finish accepts only the current Closure ResultRefDTO, resolves TaskRef from the
stable TaskId, and reads the exact terminal action set through the shared
read-only Closure result API. Before terminal mutation it compares the
Closure-frozen source with the current task source and rereads each frozen
action: `retain_open` requires OPEN; `close` and `already_closed_at_review`
require CLOSED; `no_close_authority` retains its no-close-state requirement.
The aggregate terminal is `closed` only when the set contains a closing action;
it never means every Issue or the exact source must be CLOSED. Drift returns
`closure_refresh_required` for Closure's semantic re-entry. A bookkeeping
merge is not a business Delivery and never closes an Issue.
Finish never chooses a new disposition or closes/reopens a retained source.
Archive current planning and Delivery history with their accepted scope and
unverified integration boundaries; source OPEN does not invalidate a current
retain result or prove whole-task Completion. Normal output-loss recovery uses
the same archive/bookkeeping transaction, without repeating successful mutations.
Use the matching Closure/Finish package set for the additive action; old complete
installations retain their separate migration boundary in task-delivery-migration.
For a noncanonical legacy task still lacking `task.json.source`, the exact
Closure-frozen non-exact source is used until the already-required archive
metadata write materializes it; a short Issue scope never grants close authority.

The normal transaction has three independently confirmed mutations: local
archive projection, bookkeeping commit/push/PR publication, and expected-head
merge. The executor recovers only that exact transaction and returns `success`
only after the remote target baseline contains the final archive and no active
copy. Before moving the task out of the active tree, the archive projection
uses the Fixed Fork session API to retire only pointers for this exact TaskId
and generation. A projected but unsealed archive resumes the original Finish
transaction by explicit identity; it is not a Reactivate candidate. The archive
locator belongs in finish-summary, not in the retired
`task.json.archive_dir` metadata field. The reviewed payload forbids
Issue-closing keywords and both legacy `Guru-Delivery-Task` /
`Guru-Delivery-Cycle` and current `Guru-Task-Identity` /
`Guru-Delivery-Schema` / `Guru-Delivery-Head` trailers. Validate the current
semantic payload before local archive projection and on every successful
re-entry, including an already open bookkeeping PR before its merge.
Only after remote target verification does Finish seal the current generation
and exact result in the common-dir resource ledger against the bookkeeping PR
head (the cleanup refs' actual HEAD), then retire its branch binding. The
target merge commit separately proves that the archive is persisted. `success` hands its
ResourceSealRefDTO to Cleanup; missing terminal ownership returns
`manual_cleanup_required`. Finish never deletes a resource. This canonical
manual route records the minimal terminal identity in Git common-dir so it
survives removal of the original checkout;
Reactivate requires its matching completed manual Cleanup receipt before using
the archived generation. The Finish bookkeeping commit and target merge commit
remain distinct identities. The active graph invokes this package only after
Completion and Closure.
Before terminal mutation, consume the matching current Architecture
`task_impact_sync(stage=acceptance_finish)` output through that owner's
Downstream eligibility entry. Completion or Branch Review output cannot be
relabelled as Architecture; caller changes alone do not repeat assessment.
Changed applicable Architecture facts and missing review/promotion follow the
existing routes, while Finish retains its archive/bookkeeping responsibility.
If the shared Closure result reader is unavailable, Finish stops before
terminal mutation instead of accepting an unbound caller action list.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.

For explicit selected legacy maintenance, load the legacy section in `references/legacy-maintenance.md` and use `scripts/legacy-maintenance.sh`; ordinary current invocation remains unchanged.

## Fixed bookkeeping candidate

Finish consumes actual Completion/Closure and preserves their Delivery facts.
It does not require the Task branch to include the latest target, recheck
delivered development gates or compare target SHA with an earlier snapshot.
The current semantic bookkeeping input is 2.0 and private transaction 3.0;
expected_base_head is retired. Exact files, parent/commit, PR payload, expected
bookkeeping head and same-operation recovery remain required. Verify the real
bookkeeping merge is reachable from current target and archive state exists;
subsequent unrelated target commits do not invalidate success.
