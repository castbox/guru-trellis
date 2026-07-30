# `guru-create-task-commit` Contract

## Entry And Candidate

Workflow and standalone mode perform the same nine preconditions. Read the
current task, approved planning, fresh Phase 2 result, Issue Scope Ledger and
complete Git state. Dirty files are facts, not commit authorization.

Build the next three-digit candidate under the ignored owner-private path
`.trellis/.runtime/guru-team/task-commit-plans/<task-key>/<sequence>.json`.
The candidate is a temporary semantic plan and executor input. It is never a
task artifact, never enters `path_classifications` or `exact_stage_paths`, and
is never staged or committed.

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

Author one exact Chinese Conventional Commit message from the current diff,
task docs, durable docs and ledger. Use `Refs #<primary_issue>` only; issue close
keywords belong to the PR body.

## Semantic Gate And Confirmation

Before any Git side effect, the AI reviews scope, stage paths, message meaning,
issue refs, deployment/upgrade/security impact, unrelated preservation and
evidence freshness. Scripts cannot infer this pass.

An ordinary plan with already granted authority proceeds without a routine
pause. When one current, unique commit action requires user authorization,
display its repo, branch, HEAD, paths and message and prompt `确认继续`. Any clear
affirmative response authorizes the displayed plan; the user never repeats its
SHA, digest or prescribed sentence. Reconfirm only when plan, target, HEAD,
scope or authority changes.

Return `revision-required` when the candidate can be corrected without new
scope/evidence. Return `blocked` when task ownership, evidence or a path remains
ambiguous.

## Validation And Execution

`scripts/check-task-commit-plan.sh` validates the private candidate after the AI
gate and any required confirmation. `scripts/create-task-commit.sh` repeats
that validation, rejects active merge/cherry-pick/revert/rebase/sequencer/`git
am` state, and rejects staged paths outside the exact plan.

The executor materializes exact blobs/modes in an isolated index, runs the real
repository commit hooks through a detached commit transaction, and verifies
parent, raw message, committed path set and complete tree before conditionally
advancing the live branch/index. It never pushes, rewrites published history,
resets, stashes or guesses a correction. A failure preserves unrelated state
and keeps the private candidate for bounded recovery.

On success, immutable Git history is the source for parent, message, paths and
tree facts. The executor returns only `pre_commit_head` and `commit_sha`, then
deletes the private candidate. It does not append `committed`, `result`,
`tree_evidence` or other Git-derived facts to tracked task metadata.

## Compatibility And Exit

Existing task-local `task-commit-plans/*.json` remain read-only compatibility
evidence. A legacy completed plan may help an existing active task prove commit
ancestry, but no new invocation rewrites or stages it. A planned legacy
candidate can be rebuilt in private runtime through the normal current-input
path; the old file remains untouched.

Return exactly one declared exit: `committed`, `revision-required`, or
`blocked`. The committed DTO is projected to Branch Review, which verifies the
current commit directly from live Git. A finding fix returns through
implementation and a full Phase 2 rerun before a fresh private candidate.
