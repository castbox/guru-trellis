# `guru-create-task-commit` Contract

## Entry And Forward Behavior

Workflow and standalone mode perform the same nine interface preconditions.
Read the current task planning files, durable Docs SSOT, fresh Phase 2 report,
Issue Scope Ledger and complete Git state. Reading dirty files discovers facts;
it does not grant commit authorization.

Require an ordinary Git operation state. Candidate validation, executor entry
before staging, and the check immediately before `git commit` each reject active
merge, cherry-pick, revert, rebase, sequencer, or `git am` state. The runtime
only observes these objective markers; it never consumes or clears them.

Create the next unused three-digit task-local
`task-commit-plans/<sequence>.json`. Classify every dirty path exactly once:

- `task-reviewed`: in task scope and covered by fresh Phase 2 evidence;
- `unrelated-preserved`: outside task scope and required to remain unchanged;
- `unreviewed-blocking`: in or possibly in scope but not covered by Phase 2;
- `ambiguous-blocking`: the AI cannot classify reliably.

The candidate self path uses `skill-artifact` coverage. The fresh
`phase2-check.json` recorder output is covered by its candidate evidence digest;
it cannot recursively include its own final bytes in `checked_artifacts`. Only
`task-reviewed` paths and the candidate self path may appear in
`exact_stage_paths`.

For an index entry with mode `160000`, bind the unique HEAD of the initialized,
clean submodule rooted at that exact path. Record `gitlink_head`,
`gitlink_initialized=true`, and `gitlink_dirty=false`; a deliberate gitlink
delete records the conditional deletion state instead. Uninitialized, dirty,
unborn, or root-mismatched submodules fail closed. Ordinary legacy snapshot
entries remain valid without gitlink-only fields. Changing reviewed revision B
to C changes the snapshot. Immediately before exact staging, re-read each
planned gitlink and block before any index mutation if it no longer equals the
artifact. For a non-deleted mode `160000` path, do not use `git add` to derive
the index OID from the mutable worktree. Write the artifact's reviewed
`gitlink_head` directly through `git update-index --cacheinfo`, then require the
exact index entry to equal `(gitlink_head, 160000)` and recheck the worktree
identity. Revision C must never enter the index or commit through a plan that
reviewed B. A deliberate gitlink delete retains ordinary literal delete
staging.

Apply the same content-authority rule to every ordinary path. For a non-delete
regular file, executable, or symlink, the snapshot's `worktree_sha256` and
`mode` authorize one exact Git blob/mode. The executor may re-read those bytes
once to materialize that blob only when SHA-256 and mode still match; it must
not let `git add` choose content later. A reviewed delete or rename source
authorizes exact absence. Existing schema 1.0 ordinary entries already contain
these fields and remain compatible. Candidate self is different only because
of recursion: its exact planned blob is deterministic JSON serialization of
the validated in-memory plan, never a later raw file read.

Author one exact Chinese Conventional Commit message from the diff, task docs,
durable docs and ledger. Use `Refs #<primary_issue>` only; close keywords belong
to the PR body. Store the exact UTF-8 message bytes and SHA-256 in the plan.

## AI Review Gate

Before any Git side effect, the AI reviews stage scope, message semantics,
issue refs, deployment/upgrade/security boundaries, unrelated preservation and
evidence freshness. Record a concrete reviewer, summary and evidence. A script
cannot produce or infer this semantic pass.

Set `revision-required` and re-enter this skill when the candidate can be
corrected without new scope/evidence. Return `blocked` when task/issue/evidence
ownership conflicts, a path cannot be classified, or a safe route is unknown.

## Conditional Human Confirmation

A message candidate alone does not pause. Obtain explicit confirmation or stop
when authorization is absent, paths conflict with parallel work, the operation
would amend/rebase/reset/force or touch published history, a planned/resulting
hook mutation adds paths outside the artifact, or task/issue/scope/evidence
ownership conflicts. Record authorization only for the exact plan.

## Recorder, Validator, Executor

Run `scripts/check-task-commit-plan.sh --json --candidate-artifact <path>` only
after AI review and any required confirmation. It must call the shared commit
message parser `validate_commit_message()` and fail if the branch range is empty but candidate facts are
missing.

Then run `scripts/create-task-commit.sh --json --candidate-artifact <path>`.
The executor revalidates the candidate, repeats the ordinary-operation check,
rejects artifact-external staged paths, materializes every ordinary/gitlink/
candidate binding from artifact authority, and builds a literal exact index in
an isolated transaction. The transaction uses a detached HEAD sharing the
repository object/config/hook store, so the real `git commit
--cleanup=verbatim -F` hook chain executes without moving the live branch or
touching the live index. It requires exact path and per-path blob/mode/delete
equality before and after hooks, then validates parent, raw message bytes,
committed path set, shared parser and the complete isolated commit tree.

Immediately before publication it also requires the full worktree snapshot,
candidate raw bytes, operation state, branch ref and complete live index bytes
to equal their executor-entry preimages. Same-path content/mode/index mutation,
candidate raw mutation, an extra path, a partial cache write, or a rejecting or
mutating hook returns `blocked` while the real ref/index/candidate remain exact.
Only a fully validated isolated commit may be published to the real branch,
live index and committed candidate result. Index/result publication is
recoverable: the executor retains the real `index.lock` as a sentinel while it
conditionally advances the ref, immediately acquires/verifies that loose-ref
lock, and publishes/restores the guard-owned candidate. Final index bytes use
an independent temporary file that is published to the live index without
removing the sentinel. Rollback releases the owned ref guard before
compare-and-swap so a third-party ref is preserved.
Candidate rollback additionally requires the exact executor-published result identity;
ownership loss preserves third-party state and cannot claim exact
restoration. After ref, index and candidate result all hold transaction state,
and while ref/index guards remain held, one final candidate inode/content
identity read is the success linearization point. A bypassing candidate writer
that publishes C before the read is detected: owned ref/index are rolled back,
C is preserved and the executor returns blocked. A writer after the read is a
later operation: C is preserved, the executor remains committed, and immutable
commit blob plus returned result digest evidence stays authoritative. Candidate
guards still bind every compliant companion writer. After the successful read
there is only best-effort guard/temp cleanup and return, with no fallible branch
that can change the outcome.

Every Git query that accepts a path uses literal pathspecs and accepts only zero
or one exact NUL-delimited record. The executor never pushes, rewrites published
history, resets, stashes or guesses a correction.

The executor publishes the working-tree plan result in the same recoverable
transaction as the real ref and index. The committed
tree intentionally contains the pre-commit `planned` bytes; the current
task-local file contains the real post-commit result at linearization for later
metadata capture. A later independent writer may replace that mutable file;
the executor response therefore returns the exact committed-result SHA-256 in
addition to the immutable planned blob already present in the commit tree.
The public result schema is a closed four-state machine. `planned` has no exit;
`revision-required`, `blocked` and `committed` pair with their same-named exit.
Recorded terminal results require a timestamp and auditable evidence;
`committed` requires commit/parent/message/path/preservation/hook and tree/blob
evidence. The schema retains legacy `blocked` result rows for historical plan
validation; a transaction failure returns structured blocked command evidence
and does not replace the candidate entry bytes. Those rows require their failure
stage, current or created commit identity, errors and explicit preservation/
hook facts. The runtime validates every constructed terminal result against
this public schema before publishing or returning it.

`blocked.failure_stage` owns this closed evidence matrix:

| Failure stage | HEAD / commit identity | Tree evidence | Hook mutation |
| --- | --- | --- | --- |
| `pre-commit` | `HEAD` and `commit_sha` remain at `pre_commit_head`; parent, message and committed paths are absent | `null` before tree binding, otherwise a matching `actual_source=index` observation | always `false`; a mismatched tree is not a legal pre-hook result |
| `commit`, unchanged HEAD | no created parent/message/path identity | required `actual_source=index` observation of the bound tree after `git commit` failed | derived from tree, index, worktree and unrelated-path drift; an unchanged rejecting hook is `false` |
| `commit`, changed HEAD | created message/path identity is present; parent may be `null` only to preserve invalid parent-cardinality evidence | required `actual_source=commit` observation | derived from tree/path/index/worktree/unrelated evidence |
| `postcondition` | HEAD changed and created message/path identity is present; parent may be `null` only to preserve invalid parent-cardinality evidence | required `actual_source=commit` observation | derived from the same mutation evidence; a non-tree postcondition error may remain `false` |

For `commit` and `postcondition`, any tree/blob/mode mismatch, unexpected
staged or dirty path, planned-path unstaged drift, unrelated-path drift, or
changed-HEAD committed path-set drift requires `hook_mutation=true`. Schema and
runtime validation both reject missing tree evidence, the wrong
`actual_source`, impossible HEAD/identity combinations, and mutation flags that
contradict their facts.

## Typed Exits And Re-entry

Return exactly one exit declared by the interface. `committed` proceeds to
Branch Review or finding closure. `revision-required` re-enters this skill.
`blocked` stops the workflow. Unknown, multiple or unmapped exits fail closed.

Any non-metadata finding fix returns through implementation and the full Phase
2 check before this skill. Create a new sequence bound to the new Phase 2 digest,
pre-commit HEAD and dirty snapshot; never reuse an earlier plan.
