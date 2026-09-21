# `guru-reconcile-task-base` Contract

## Entry And Pair Guard

The semantic Skill has six caller-owned input profiles: `post_plan`,
`post_check`, `post_commit`, `post_branch_review`, `post_publication`, and
`finalizer_base_mismatch`. Each carries one exact active-task identity,
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
and the exact candidate is compatible, `post_plan`, `post_check`, and
`post_commit` create one checked local reconciliation merge commit before
returning `reconciled`. `post_plan` preserves `task_activation`; `post_check`
and `post_commit` both route to fresh Phase 2. The three post-review profiles
also return `reconciled` when the candidate preserves the reviewed-content
identity. When that identity must advance, only those three profiles may return
`review_continuity_required`; they do not route through implementation or a
new full Branch Review. `planning_stale` is valid only when current live
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

`execute-base-reconciliation` is package-private. It requires a clean,
uniquely branch-bound task worktree at the exact prior task HEAD and binds the
selected ref to the exact new base. For pre-review profiles it re-derives the
old base from the live merge base. For post-review profiles it validates the
adjacent old-base ancestry and prior full-review ancestry. It creates one local
`--no-ff` merge commit and verifies exact parent order, result ancestry,
candidate tree identity, and final cleanliness. Stale or mismatched
preconditions fail before commit. A failed merge or candidate mismatch is
aborted back to the prior task HEAD. The executor never pushes or records user authorization.

The recorder and checker validate the AI-authored result and live Git facts.
They do not generate semantic retrieval terms or infer impact/route. The
ignored `base-reconciliation.json` checkpoint contains only the exact pair,
selected exit, minimal consumer fields, and local digest. It is deleted after a
successful same-owner public invocation; stale state is removed before a fresh
review rather than chained.

## Conflict-Resolved Candidate

The `resolved_candidate` profile is entered only from
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
second commit. `project-resolved-full-review` combines that checked result with
explicit Branch Review authoring and emits the complete existing
`branch_review` input. This marker-free deterministic projection is not a
Reconcile external exit; bounded base continuity is not used for this path.

## Exits

- `reconciled`: the workflow router receives task/current-base identity and the
  checked resume target. `post_plan` preserves task activation; `post_check`
  and `post_commit` route to fresh Phase 2; post-review profiles preserve their
  closed target when no bounded continuity review is needed.
- `review_continuity_required`: Branch Review receives the exact old/new pair,
  prior full-review commit, current reconciled task HEAD, candidate tree token,
  semantically relevant paths, and original route for bounded continuity. This
  exit is invalid for `post_plan`, `post_check`, and `post_commit`, and cannot
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
