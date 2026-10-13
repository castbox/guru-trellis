## Public Delivery integration 1.0

### Bounded private historical merge migration

The original Merge owner reviews the exact schema-1 gate/cycle and actual
Task/generation/PR/head/body/message/parents plus the public Publication fact.
Only then call owner-private `scripts/migrate-delivery-transaction.sh` with
private `historical_merge_migration` input and actual migration review. For an
already MERGED PR it validates original three-field message bytes and parents,
records only `historical_success`, and retains the minimal key/Publication
result/original gate locator for same-result formal output recovery. The old
gate is a historical source, never a currently passing six-dimension review.
An OPEN PR returns `fresh_merge_review_required` without copying a gate or
performing a merge; the original owner performs current review/confirmation.
No historical message is rewritten into schema-2. Upgrade consumes only the
intermediate receipt and exact owner-private writes for recovery/rollback.
New merges continue to require the five-field schema-2 trailer contract.

`--preview` checks the same actual historical message, parents and target-base
ancestry without writing. It reports only the exact association and any
necessary public-record write. A normal archive move changes `task_ref`, not
the original gate's stable Task identity/generation. MERGED recovery reads that
identity and actual PR facts without requiring an active binding or current
HEAD; an OPEN source still requires fresh current Merge review before mutation.

The installed public store permits archived history reads, not a new
`record_delivery` write. If the reviewed Plan2 target record already contains
the exact historical Delivery fact, this owner validates it and recovers output
without another public apply. If it is missing, stop with the explicit
`delivery_result` migration prerequisite: the original Merge owner must supply
its reviewed historical result in the prospective Plan2 target record. Required
fields are result/owner IDs, minimal PR/merge evidence, pull_request profile,
the exact public Publication candidate, repo/PR/reviewed HEAD/merge SHA/target
ref. No reopen, direct aggregate write or current gate pass substitutes for it.

This current Skill consumes the target installation's reviewed Delivery API
1.0 and Task schema 2.0 through a thin projection. `task_ref` is a locator;
`delivery_key` is the opaque public identity. Read the current `interface.json`
profile schema and its exact exit consumer before invoking. Do not derive an
identity from branch, worktree, legacy cycle, PR, or Task status. D1 and later
Deliveries use the same entry and lifecycle. The public phase never proves a
semantic pass. Historical facts never prove a currently applicable gate.

Read the Delivery's public `planning_root` for its three planning documents and
context JSONL; Task-root PRD remains overall scope. Rework keeps the Delivery
identity and returns through the real current stage owner's public operation to
the earliest affected role. Invalidate only the affected results. Unchanged,
still-applicable execution facts need not be rerun. A successful recorder is
objective evidence only; the AI must actually perform this Skill's full review.
Missing public API or an unmigrated old record stops with precise migration
remediation. Do not install a private alternative, select a source fallback,
convert a legacy checkpoint into pass, or switch an old installation before
upstream migration/default-cutover qualification.

### Expected-head merge and historical recovery

`delivery_ready_for_merge` consumes the exact public Publication result and
current readiness applicability before a new remote merge. Preserve all six
semantic dimensions, real CI/reviews/policy, expected HEAD, exact merge method,
message and first-parent evidence. New merge messages use schema-2 trailers:

```text
Guru-Task-Identity: <stable-task-id>
Guru-Delivery-Schema: 2
Guru-Delivery-Head: <reviewed-head>
Guru-Delivery-Identity: <public-delivery-id>
Guru-Task-Generation: <lifecycle-generation>
```

Schema-1 three-field history remains readable; its attribution must be judged
and migrated by the history owner, never guessed from a cycle. Schema-2 history
returns explicit public identity in its separately versioned result.

Read actual MERGED PR, exact message/parents and current-base ancestry before
projecting `record_delivery(historical_success=true)`. Public projection failure
retains the same recovery input/gate; retries never repeat an already successful
merge and do not demand a current gate to record historical fact. `delivered`
contains only `task_ref` and `task_key` beside the exit; whole-task Completion
rereads all public facts, and Merge never declares overall completion.
`review_refresh_required.reason_code` goes directly to Readiness refresh;
implementation re-entry uses this fixed delivery owner and public rework.

### Scope withdrawal in the current stage

`delivery_scope_withdrawal` is an independent semantic entry with mode,
`task_ref` and `delivery_key`. Before authoring its separate review input,
read the current whole-scope decision and selected undelivered slice; judge
that its full scope was withdrawn/replaced, with no remaining obligations in
that slice. Partial changes use ordinary same-Delivery rework. This package
uses only its fixed public role and expected phase; it never accepts a role
parameter or selects an owner from phase. Record the actual reason,
`scope_decision` and minimum evidence through public `stop`, then release the
selection. `delivery_stopped` hands Task identity to whole-task Completion.
Stop preserves commits/PR/resources; PR close and cleanup require their actual
owners and any necessary current side-effect confirmation. Lost output retries
the identical stored stop result and releases selection without another stop.

## Preserved semantic and transaction duties

The duties below apply to the current Delivery input and output contracts.
Historical data is read only by its named history or migration owner.

# Contract

## Ownership

`guru-merge-task-delivery` is the sole owner of Delivery merge readiness,
confirmation, expected-head mutation, merge-message trailers, and terminal
recovery. It consumes only the reviewed publication handoff plus live facts.
It does not own Delivery Review, publication, task completion, Issue closure,
archive, Finish, Reactivate, or cleanup.

The current production graph invokes this owner after Delivery Publish and
routes `delivered` to Completion. Its other exits have the unique workflow or
stop consumers declared by the active interface.

## Public Input

Current `delivery_ready_for_merge` consumes the exact Publication result,
Delivery key, repository/PR/head and actual PR-body revision. New remote
mutation requires current public readiness and candidate, active unique Task
checkout, full semantic Merge review and the exact dialogue-local action.
Historical MERGED recovery reads the actual PR, parents, base ancestry and
trailers before projection; it does not require current HEAD or gate pass.

## Semantic Gate

The AI reviews exactly six dimensions: `active_task`, `pr_identity`,
`checks_and_reviews`, `mergeability`, `repository_policy`, and
`message_and_delivery_boundary`. The reviewed route is one of:

- `delivered`: all dimensions pass, no objective blocker exists, merge commit
  policy is supported, and the exact subject/body/trailers are reviewed;
- `merge_blocked`: a current external, provider, policy, permission, checks,
  or mergeability blocker prevents mutation;
- `implementation_required`: a current-slice task-work finding requires Phase
  2 and carries concrete `finding_refs`;
- `review_refresh_required`: current Delivery review authority is stale and
  carries a concrete `reason_code`.

Only `delivered` reaches the independent confirmation boundary. The private
gate stores current facts, semantic results, exact message bytes,
`pre_merge_base_head`, and an action digest. It never stores authorization.

## Mutation And Recovery

The executor calls exactly:

```text
gh pr merge <number> --repo <owner/repo> --merge \
  --match-head-commit <expected-head> --subject <subject> \
  --body-file <owner-private-temporary-file>
```

There is no squash/rebase fallback. The body file is removed after every
attempt. A successful post-read requires:

- PR state `MERGED` and one merge commit SHA;
- commit subject/body equal the reviewed bytes;
- parents exactly `[pre_merge_base_head, expected_head_sha]`;
- remote target base ref equals the merge commit immediately after mutation,
  or, on read-only output-loss recovery after a normal base advance, the exact
  merge commit is proven an ancestor of current base HEAD by GitHub compare;
- trailer Task/Delivery identity, schema `2`, generation and reviewed head are exact;
- the PR body still has no closing keyword;
- the active task identity remains current.

If mutation succeeded but stdout, post-read, or result projection was lost,
the same input and semantic review perform one read-only reconstruction. A
retained gate is checked when present. If the gate was already retired, parent
1 supplies the historical pre-merge base only after every other terminal fact
matches. Unknown or ambiguous terminal state fails closed and never triggers a
second merge.

## Delivery History Discovery

`discover-task-deliveries` is a deterministic, read-only package command. Its
closed query contains only the stable task identity, repository, and target
base. It scans the fresh target-base first-parent merge history, ignores merge
commits without Delivery trailers, and reads exact schema-1 or schema-2 trailer
block for every matching task Delivery.

Each matching merge is cross-checked against exactly one GitHub merged PR:
same repository, target base, merge commit, reviewed head, and two-parent merge
identity. The command returns only immutable Delivery facts in target-base
order. It never reads a PR body, current task branch, worktree binding, task
creation branch, or ledger. Duplicate or drifted task/head/PR/merge identity
fails closed. Deleting an old head branch or changing the current active
binding therefore does not change historical Delivery identity, while a
bookkeeping merge without the trailers is excluded.

## Typed Outputs

`delivered` contains only `exit_id`, `task_ref` and `task_key`. Completion
reads the public aggregate and current authority to review all actual Delivery
facts and whole Task responsibilities. Historical facts remain facts; current
Check/readiness and Completion still require their own actual conclusions.

`implementation_required` contains `task_ref`, `finding_refs`, and
`resume_target=phase-2`. `review_refresh_required` contains `task_ref` and a
reason code. `merge_blocked` contains repository/PR identity plus a reason and
remediation. No output mutates task or Issue lifecycle state.

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
