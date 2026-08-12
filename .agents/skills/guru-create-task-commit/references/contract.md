# `guru-create-task-commit` Contract

## Entry And Candidate

Workflow and standalone mode perform the same seven preconditions. Read the
current task, the minimal passed Phase 2 DTO, Issue Scope Ledger and complete
Git state. The DTO supplies `task_ref`, its profile-owned `source_exit`, and
`phase2_commit_anchor`; Task Commit rereads the Phase 2 owner's retained
checkpoint to verify its current reviewed-content identity and capture-commit
ancestry. It never reads the Planning owner's private checkpoint. Dirty files
are facts, not commit authorization.

The public input is only `profile`, `mode`, `task_ref`, `source_exit`, and the
`phase2_commit_anchor`. It never carries message authoring, path selection,
semantic outcome, user authorization, an expected exit, or a Phase 2 digest.

Build the next three-digit candidate under the ignored owner-private path
`.trellis/.runtime/guru-team/task-commit-plans/<task-key>/<sequence>.json`.
The candidate is a temporary semantic plan and executor input. It contains
only task/Git preimage, the complete dirty snapshot, AI path classifications,
derived exact paths, canonical message, and final AI semantic result. It has no
authorization, cross-Skill digest, freshness journal, or terminal result. It is never a
task artifact, never enters `path_classifications` or `exact_stage_paths`, and
is never staged or committed.

Candidate 5.0 supersedes 4.0. An unfinished 4.0 candidate is not converted and
no removed facts are synthesized. The owner deletes or rejects it and performs
a complete reprepare from current Phase 2 evidence, live task/HEAD/snapshot,
scope classifications, and message review.

Classify every dirty path exactly once:

- `task-reviewed`: current task scope covered by fresh Phase 2 evidence;
- `unrelated-preserved`: outside scope and preserved byte-for-byte;
- `unreviewed-blocking`: possibly in scope but not covered by Phase 2;
- `ambiguous-blocking`: the AI cannot classify reliably.

Only `task-reviewed` paths and a rename source inherited from its reviewed
destination may enter `exact_stage_paths`. Copy provenance does not grant stage
authority. Every ordinary file binds exact bytes and mode; every gitlink binds
the reviewed submodule HEAD and clean state. The executor rechecks these facts
before any index/ref mutation.

Author `type`, `scope`, `summary`, `background`, `changes`, `boundaries`, and
`validations` from the current diff, task docs, durable docs and ledger. The
builder produces the exact Chinese Conventional Commit subject, four-section
body, and `Refs #<primary_issue>`, then runs the shared parser. Missing primary
issue, sections, footer, line-ending normalization, and similar mechanical
errors are corrected before the action is shown. Issue close keywords belong
to the PR body.

## Semantic Gate And Confirmation

Before any Git side effect, the AI reviews scope, stage paths, message meaning,
issue refs, deployment/upgrade/security impact, unrelated preservation and
evidence freshness. Scripts cannot infer this semantic pass. Branch name,
branch role, protection, sharing, other task ownership, remote branch presence,
open PR presence, and publication state are not commit eligibility facts and
must not be queried to grant or deny this action.

When the current conversation already contains one exact commit request, that
request is the authority for the matching displayed action. Otherwise, when one
current, unique commit action requires user authorization,
display its repo, branch, HEAD, paths and message and prompt `确认继续`. Any clear
affirmative response authorizes the displayed action in the conversation only;
the user never repeats its SHA, digest or prescribed sentence. Reconfirm only
when plan, target, HEAD, scope or authority changes.

Return `revision-required` when the candidate can be corrected without new
scope/evidence. Return `blocked` when task ownership, evidence or a path remains
ambiguous.

## Validation And Execution

`scripts/prepare-task-commit.sh` canonicalizes and validates candidate 5.0
before any required confirmation. `scripts/check-task-commit-plan.sh` repeats
objective validation immediately before execution. `scripts/create-task-commit.sh` repeats
that validation, rejects active merge/cherry-pick/revert/rebase/sequencer/`git
am` state, and rejects staged paths outside the exact plan.

The executor creates a temporary detached worktree at the reviewed parent,
materializes exact blobs/modes in an isolated index, checks that index out into
the transaction worktree, and invokes real repository hooks through
`git commit --cleanup=verbatim -F <0600-message-file>`. The hook lookup honors
the repository's current `core.hooksPath`; a transaction-local proxy only
forwards arguments and records each hook exit code so `post-commit` failure can
be reported even though Git itself does not fail the command for that exit.
Hooks therefore observe the reviewed parent HEAD, exact index and worktree, and
the reviewed message file rather than the unrelated live workspace.

Before live-ref publication, the executor verifies hook exits, the unchanged
message file, transaction index and worktree, parent, raw commit-object message,
committed path set, every blob/mode and complete tree. Any hook rejection,
message rewrite, extra tracked or untracked path, rename, deletion, stage,
unstage, exact-path mutation or mode drift fails closed. A transaction commit
created before such a failure is reported as `created_commit_sha`; the live
branch remains at the reviewed parent and the private candidate plus Phase 2
checkpoint remain available for bounded recovery.

The same pre-publication gate compares the live worktree's semantic dirty
snapshot as well as its branch and semantic index preimage, so a normally
misconfigured hook cannot publish after touching the user's live tracked,
untracked, staged, unstaged, or gitlink state. The isolated index lives inside
the transaction temporary directory. Every success and failure path removes
the detached worktree registration; cleanup failure is a bounded recovery and
retains any already-created commit identity.

Only after those checks pass does the executor conditionally advance the live
branch with `git update-ref <ref> <new> <old>`. It then refreshes only the exact
live index paths and compares semantic `mode/blob/stage/path` entries, never raw
index-file bytes. A failure after live ref advance reports the same created
commit with `transaction_stage=live_ref_published`. It never pushes,
rewrites published history, stashes, amends, or guesses a correction, and owns
no custom lock, rollback, atomic-replace, or concurrency protocol. A failure
before ref publication preserves the live ref/index and keeps the private
candidate; a failure after ref advance reports the created commit for bounded
same-plan recovery.

On success, immutable Git history is the source for parent, message, paths and
tree facts. The executor returns only `pre_commit_head` and `commit_sha`, then
deletes the private candidate and consumed Phase 2 checkpoint. A failed attempt
retains both for bounded retry; successful same-plan recovery verifies the
published commit before deleting both. The executor does not append `committed`,
`result`, `tree_evidence` or other Git-derived facts to tracked task metadata.

## Exit

Return exactly one declared exit: `committed`, `revision-required`, or
`blocked`. The committed DTO is projected to Branch Review, which verifies the
current commit directly from live Git. A finding fix returns through
implementation and a full Phase 2 rerun before a fresh private candidate.
