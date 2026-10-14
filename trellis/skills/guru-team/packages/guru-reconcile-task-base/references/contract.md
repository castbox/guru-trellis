# `guru-reconcile-task-base` Contract

## Entry And Pair Guard

The semantic Skill has six caller-owned input profiles: `delivery_post_plan`,
`delivery_post_check`, `delivery_post_commit`, `delivery_post_branch_review`, `delivery_post_publication`, and
`delivery_finalizer_base_mismatch`. Each carries one exact active-task identity,
selected base ref, task HEAD, and a closed `resume_target`. The three
pre-review profiles do not accept caller-supplied old/new base SHAs: the guard
resolves the selected base and derives the old base from the unique live merge
base of task HEAD and selected base. The three post-review profiles carry the
adjacent old/new pair plus their minimum caller-owned full-review identity.
There is no optional continuity bag.

Before semantic invocation, `guard-task-base-pair` performs one live resolution
of the selected base ref. For a pre-review profile it treats the selected base
being an ancestor of task HEAD as `unchanged`; otherwise it emits the
operation-scoped `(live merge base, selected base HEAD)` pair. For a
post-review profile it validates the caller-bound adjacent pair. It returns
only `unchanged`, `current_pair`, `new_pair`, or `blocked`. It checks identity
and ancestry, but never judges
authority, task-content impact, integration impact, relevant paths, validation
sufficiency, findings, or route. `unchanged` creates no checkpoint. A matching
owner-private result makes `current_pair` return its already validated exact
typed output and delete the checkpoint as the deterministic one-use consumer.
It never replaces that output with an unconditional `resume_target`; only
`unchanged` resumes the caller target directly.

## Common causal authority impact

Read `.trellis/spec/workflow/causal-completion-semantics.md` when judging the
exact base delta's dependency impact. If that authority or mechanism/evidence
assumptions changed semantically, identify the earliest affected original owner
and use this profile's existing planning, implementation or review-continuity
route. An unchanged applicable mechanism reuses its qualification while the
current stage still reviews its own evidence. Unrelated bytes or a version
identity alone do not require all-stage requalification; runtime/digests do not
make that semantic choice. The common spec owns no integration route.

## Bounded Reconciliation Owner

This Skill owns only the semantic impact judgment for one exact caller-supplied
task and old/new base pair. It consumes the current task authority and planning,
the exact base delta, candidate validation facts, and qualified base-impact
candidates. It does not own or consume the broad Guru semantic retrieval SSOT,
construct a repository-wide concept family, or infer absence from an unbounded
search. A repository-searchable negative conclusion not established by these
closed inputs is insufficient evidence and fails closed.

The AI reviews three independent dimensions:

1. authority impact from live Issue, accepted requirements, Docs SSOT and scope;
2. task-content impact on approved planning, task code, tests and documentation;
3. integration impact for the exact candidate pair, conflicts and affected
   validations.

These dimensions carry two independent clocks. The exact old/new base pair is
the integration clock. Live Issue authority, accepted scope, approved planning
assumptions, and task content form the authority/task-content clock. Advancing
the integration clock alone never makes planning stale and never changes the
caller's closed `resume_target`. If authority and task content remain unchanged
and the exact candidate is compatible, `delivery_post_plan`, `delivery_post_check`, and
`delivery_post_commit` create one checked local reconciliation merge commit before
returning `reconciled`. `delivery_post_plan` preserves `delivery_activation`; `delivery_post_check`
and `delivery_post_commit` both route to fresh Phase 2. The three post-review profiles
also return `reconciled` when the candidate preserves the reviewed-content
identity. When that identity must advance, only those three profiles may return
`review_continuity_required`. Bounded continuity does not itself require a new
full Branch Review or provide a public gate pass. Its workflow consumer rereads
public Check and full-review applicability for the reconciled candidate:
missing/stale Check reenters the existing rework, begin-check, Check and clean
TaskCommit path; missing/stale full review reenters independent complete Branch
Review. `planning_stale` is valid only when current live
authority or an approved planning assumption has actually changed; it carries
exact reason refs for that change.

Base identity or path overlap alone is not a finding, stale result, pass, or
block. Insufficient applicable evidence fails closed. A semantic conclusion is
recorded only after the AI has bound the pair, reviewed scope, key delta,
validation adequacy, findings, remaining boundaries, and exactly one exit.

The AI first forms a candidate-only set from the exact base delta and invokes
`guru-qualify-normal-scenario:base_impact_candidate_set`. Candidate inputs carry
observation and live locators only, never impact classification, severity,
route, or a caller-authored normal-path conclusion. `classified` returns to this
owner before impact/severity/route work; `scope_confirmation_required` enters
requirements clarification; `mechanism_revision_required` returns here for
remove/replace and a fresh candidate round; `blocked` stops. Rejected candidates
cannot become validation obligations, findings, implementation, planning stale,
or clarification. The base checkpoint records only this owner's final
direct-consumer result and never embeds or references qualification state.

## Candidate And Script Boundary

`execute-base-candidate` creates a detached temporary worktree, merges the task
HEAD into the new base without committing or updating a persistent ref, runs
only closed argv-array validation commands, records objective return codes and
candidate tree identity, and removes the worktree. It never selects commands,
interprets failures, resolves conflicts, or chooses a route. Arbitrary shell
strings are rejected.

Candidate and persistent reconciliation use the same stage-0 index identity
owner, `index_tree_digest`. In Git index order, each `160000` gitlink contributes
`path_bytes + NUL + b"160000" + NUL + index_oid_ascii + NUL`.
The recorded pointer participates directly: no `cat-file` call, initialized
submodule, local child commit object, credentials, or remote download is needed.
All blob-backed entries retain
`path_bytes + NUL + sha256(blob_bytes).hexdigest().encode() + NUL`, including
ordinary files, executable files, and symlink target blobs. The final identity
is SHA-256 of the concatenated rows. This does not expand blob-backed mode-only
identity semantics or change their existing read-failure behavior.

Trees without gitlinks retain byte-identical digests and existing successful
short-lived evidence. The previous implementation could not produce successful
candidate evidence for a gitlink tree. Rerun those failed attempts with the
updated complete preset/runtime; do not migrate errors into candidate tokens.
There is no digest/schema version bump, fallback, or dual-read path. Existing
managed-copy consistency and live candidate-tree comparisons remain in force
when updating between candidate validation and persistent reconciliation.

For every compatible pre-review result and every post-review continuity result,
the AI completes the semantic gate before any persistent Git write. It then
displays the exact branch, prior task HEAD, operation-scoped old/new pair,
candidate tree, commit message, and the fact that no push or remote mutation
will occur. A post-review continuity action also displays the prior full-review
commit. Current-dialogue confirmation authorizes only that displayed invocation
and is not included in any request, result, checkpoint, or DTO.

`execute-base-reconciliation` is package-private. It requires a uniquely
branch-bound task worktree at the exact prior task HEAD and binds the
selected ref to the exact new base. For pre-review profiles it re-derives the
old base from the live merge base. For post-review profiles it validates the
adjacent old-base ancestry and prior full-review ancestry. It creates one local
`--no-ff` merge commit and verifies exact parent order, result ancestry,
candidate tree identity, and final cleanliness for post-review profiles.
Pre-review planning or implementation changes may be staged, unstaged, or
untracked. The executor temporarily shelves them, commits only the reviewed
base merge tree, then restores their index and worktree state before returning.
Its checker reads the committed tree rather than the restored dirty index.
An unsuccessful merge or candidate mismatch aborts back to the prior HEAD and
restores pending changes; if restoration fails, the exact stash remains for
manual recovery and the route stops. The executor never pushes or records user authorization.

The recorder and checker validate the AI-authored result and live Git facts.
They do not generate semantic retrieval terms or infer impact/route. The
ignored `base-reconciliation.json` checkpoint contains only the exact pair,
selected exit, minimal consumer fields, and local digest. It is deleted after a
successful same-owner public invocation; stale state is removed before a fresh
review rather than chained.

## Pre-Implementation Resolved Baseline

The two private candidate/reconciliation requests add the closed optional
`resolved_candidate` object with exactly `stage0_tree` and `integration_paths`.
Omitting it retains the ordinary clean-merge algorithm. Persistent consumption
is restricted to `delivery_post_plan` with `resume_target=delivery_activation`;
it creates no new public input, exit, checkpoint, or downstream gate.

This owner reads the current live source, approved planning and exact base
delta for the same Task generation and Delivery, resolves the genuine document
conflict, and selects the integration paths. In a temporary index, build the
stage-0 candidate from the resolved live index and restore every unselected
entry to the prior task HEAD. Path selection, preservation of both authorities,
planning applicability, resolution sufficiency and validation choice remain AI
judgments. The real index/worktree are never rewritten by candidate building.

`execute-base-candidate` verifies current HEAD, one active selected-base
`MERGE_HEAD`, zero unmerged entries, no other sequencer, and the reviewed
candidate path set. Every prior-HEAD-to-candidate change must be selected;
selected live index mode/oid/stage entries must equal the candidate, and
selected paths must have no unstaged changes. It loads that exact tree into a
temporary detached checkout, runs the AI-supplied argv-array baseline checks,
returns the original candidate facts using `index_tree_digest`, and removes
the checkout. Baseline validation proves integration and planning applicability;
unimplemented business scope is not a prerequisite and receives no Check pass.

After the baseline semantic gate, display the exact Task/Delivery, branch,
prior HEAD, live operation pair, `MERGE_HEAD`, selected paths, tree/digest,
message, parent order `[prior_task_head,new_base_head]` and zero remote effects.
Only current-dialogue confirmation permits the persistent Git invocation.
No authorization is present in a request, schema, result or checkpoint.

`execute-base-reconciliation` rechecks the branch-bound Task/Delivery, selected
ref and unique old merge base, active merge facts and candidate equality. It
loads the reviewed tree into a temporary `GIT_INDEX_FILE` and uses ordinary
`git commit`. The real index, unrelated staged/unstaged/untracked content and
parallel pending planning remain intact; no stash or reset occurs. Commit
readback verifies exact parents, tree, message, digest and terminal merge state.
The original receipt then enters record/check/invoke and returns `reconciled`
to the original Activation owner for the same Task generation and Delivery.

If stdout is lost, the same request may recover only the current HEAD with
those exact parents/tree/message/digest, the same selected base/old pair and a
terminal Git operation state. Unrelated pending changes remain allowed. The
receipt identifies the existing commit; recovery never commits or amends.
Ordinary HEAD/base/tree/index changes, unresolved conflicts or changed reviewed
paths stop without altering the existing state and require this owner's fresh
read/re-entry. Actual authority/planning changes follow its existing semantic
exits. This route does not call business Check, Task Commit, Branch Review or
readiness; those owners run after implementation.

## Post-Implementation Conflict-Resolved Candidate

The `delivery_resolved_candidate` profile is entered only from
`guru-check-task:resolved_reconciliation_passed`. Its public input binds the
fresh Phase 2 commit anchor, active `MERGE_HEAD`, selected new base, stage-0
tree object, index-tree digest, exact parent order, branch, and commit message.
It never consumes the ordinary Task Commit path.

`execute-resolved-base-reconciliation` accepts only the exact branch-bound task
worktree with `HEAD == phase2_commit_anchor`, one `MERGE_HEAD == new_base_head`,
zero unresolved entries, zero unstaged or untracked paths, and no other Git
sequencer. The stage-0 tree and index digest must equal the reviewed input
before one local merge commit is created. It performs no push or remote
mutation.

If stdout is lost after that commit, the same request may recover only when
current `HEAD` has the exact reviewed parents, tree, and message in a clean
terminal Git state. Recovery returns the existing commit and never creates a
second commit. Before Full Review, the reviewing owner invokes public rework
to implementation; the implementation owner binds the reconciled candidate with
`begin_check`, and the Check owner reviews current applicability and records a
fresh candidate-bound public Check. This preserves the Delivery identity, plan
and existing reconciled commit; still-valid test evidence need not be rerun.
`project-resolved-full-review` combines that checked result with explicit Branch
Review authoring only after validating the actual current public Check owner,
passed result, predecessor applicability, exact reconciled HEAD/base, live
candidate bytes and scope/plan/evidence references. A token by itself is not
sufficient. It emits the complete current `delivery_branch_review` input. This marker-free deterministic projection is not a
Reconcile external exit; bounded base continuity is not used for this path.

## Exits

- `reconciled`: the workflow router receives task/current-base identity and the
  checked resume target. `delivery_post_plan` preserves Delivery activation; `delivery_post_check`
  and `delivery_post_commit` route to fresh Phase 2; post-review profiles preserve their
  closed target when no bounded continuity review is needed.
- `review_continuity_required`: Branch Review receives the exact old/new pair,
  prior full-review commit, current reconciled task HEAD, candidate tree token,
  semantically relevant paths, and original route for bounded continuity. This
  exit is invalid for `delivery_post_plan`, `delivery_post_check`, and `delivery_post_commit`, and cannot
  substitute for the first complete Branch Review.
- `implementation_required`: implementation receives exact finding refs and
  resumes the affected downstream graph.
- `planning_stale`: Planning receives exact reason refs for changed live
  authority or an invalidated approved planning assumption; a base advance by
  itself is not sufficient.
- `scope_confirmation_required`: Requirements Clarification receives exact
  proposal refs; any user confirmation remains dialogue-local.
- `blocked`: stop with zero public payload.

Unknown, multiple, stale, consumer-mismatched, or structurally invalid results
fail closed.

## Compatibility

The continuity output and private result are direct current-only 2.0 contracts.
Older continuity output/private checkpoints are stale and are not dual-read,
migrated, or wrapped. Legacy active-task
base anchors may form one initial pair; absent anchors require a complete
bounded reconciliation. The package never reads another Skill's private
checkpoint, restores the retired shared compatibility dispatcher, rewrites
tracked task artifacts, or creates a remote ref or commit.
