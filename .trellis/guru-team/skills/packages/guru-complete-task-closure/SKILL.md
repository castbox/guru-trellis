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
The runtime freezes this entire set for same-owner recovery. Before any provider
action, it also writes the minimal Task-owned shared carrier described below.
It rereads exact Issue state and closes only reviewed close actions.

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
Both results hand the existing reference to Finish. Finish reads the public
Closure and its shared action-set carrier, then checks required OPEN/CLOSED states. Apply the matching Closure
and Finish packages together before using the additive action; older consumers
must not receive `retain_open`. Existing action values, refs and exits retain
their meanings; see the installed task-delivery-migration spec.
The current graph sends these results to Finish; this
package does not decide Completion or own the workflow projection.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.

## Shared result and cross-environment recovery

Current input aggregate 3.0 adds `closure_shared_result_recovery`. The normal
`completion_approved` input 2.0 and all existing outputs retain their meanings.
Use the same public invocation for both profiles. Load the closed input from
`schemas/public-shared-result-recovery-input.schema.json` and the corresponding
semantic result from `schemas/shared-result-recovery-semantic.schema.json`.

Normal Closure writes `closeout/closure/<base64url-result-id>.json` under the
selected Task before provider actions. The filename encodes the UTF-8 result id
with URL-safe base64 and removes padding. The independent shared schema 1.0
contains only schema version, original ResultRef, Completion result id, source
and action set. Public `close_task` evidence includes its AuthorityRef and keeps
the original source evidence. The carrier is necessary input, not authorization
or proof that provider actions occurred. Closure never overwrites an existing
carrier with different inputs. The Task and carrier must be committed and
obtainable from the selected source ref/commit for cross-environment use.

For `closure_shared_result_recovery`, read the exact TaskRef, ResultRef and
carrier AuthorityRef. Freshly review public Completion, current accepted scope,
source relation, every original action and current provider state. This is the
AI Review Gate; the executor only verifies those inputs and provider facts.
Required CLOSED still OPEN, required OPEN now CLOSED, or changed source returns
to original Closure through `external_change_conflict`. Missing provider state
returns `blocked` with the exact missing Issue fact. A blocked review preserves
its original reason and performs no projection or provider mutation.

After a current semantic review and matching live states, the executor reads
back an existing identical public result or restores only its missing public
projection with the original result id. This profile never invokes provider
close, creates no local transaction, and does not recover a previous dialogue's
confirmation. If a real close remains necessary, use the normal profile and
review its current action boundary. `closed|no_mutation` still hand only the
ResultRef to Finish. Finish keeps snapshot 2.0 and independently rereads source
and every required provider state.

The existing authority resolver preserves Task-owned locators through archive
relocation and `artifact_origin`. The carrier follows the Task into its archive;
new results use new files. No carrier or history is fabricated for old finished
archives. For old in-flight results, original Closure can produce this minimum
input only when its actual original action set remains verifiable. Missing
original inputs stop the affected Closure/Finish step with a concrete gap.
Apply matching Closure, shared reader and Finish consumers together through
MIGRATION-635. Pinned old installations retain their original contract.
