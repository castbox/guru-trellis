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
evidence freshness. Scripts cannot infer this pass.

An ordinary plan with authority already present in the live conversation
proceeds without a routine pause. When one current, unique commit action
requires user authorization,
display its repo, branch, HEAD, paths and message and prompt `确认继续`. Any clear
affirmative response authorizes the displayed action in the conversation only;
the user never repeats its SHA, digest or prescribed sentence. Reconfirm only
when plan, target, HEAD, scope or authority changes.

Return `revision-required` when the candidate can be corrected without new
scope/evidence. Return `blocked` when task ownership, evidence or a path remains
ambiguous.

## Validation And Execution

`scripts/prepare-task-commit.sh` canonicalizes and validates the candidate
before any required confirmation. `scripts/check-task-commit-plan.sh` repeats
objective validation immediately before execution. `scripts/create-task-commit.sh` repeats
that validation, rejects active merge/cherry-pick/revert/rebase/sequencer/`git
am` state, and rejects staged paths outside the exact plan.

The executor materializes exact blobs/modes in an isolated index, runs the real
repository commit hooks through a detached commit transaction, and verifies
parent, raw message, committed path set and complete tree before conditionally
advancing the live branch with `git update-ref <ref> <new> <old>`. It then uses
`git reset --mixed --quiet HEAD` only to refresh the live index. It never pushes,
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
