# `guru-create-task-commit` Contract

## Entry And Forward Behavior

Workflow and standalone mode perform the same eight interface preconditions.
Read the current task planning files, durable Docs SSOT, fresh Phase 2 report,
Issue Scope Ledger and complete Git state. Reading dirty files discovers facts;
it does not grant commit authorization.

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
The executor revalidates the candidate, rejects artifact-external staged paths,
stages literal exact paths, requires exact index equality, and records the
complete expected index tree plus each exact path's blob and mode. It commits
with `--cleanup=verbatim -F`, then compares the real commit tree and per-path
blob/mode identities with that pre-hook evidence in addition to validating
parent, raw message bytes, committed path set, shared parser, unrelated
preservation and remaining index. Every Git query that accepts a path uses
literal pathspecs and accepts only zero or one exact NUL-delimited record.
Same-path content, mode or index mutation by a hook returns `blocked`, records
`hook_mutation=true` with expected/actual tree evidence, and preserves the Git
state. A hook that only rejects the commit without changing the bound index,
planned-path worktree state, unrelated paths, or other staged/dirty paths
records `hook_mutation=false`; planned paths that remain staged after rejection
are not themselves mutation evidence. Blocked results record unexpected dirty
paths and planned-path unstaged drift separately. The executor never pushes,
rewrites history, resets, stashes or guesses a correction.

The executor atomically updates the working-tree plan result. The committed
tree intentionally contains the pre-commit `planned` bytes; the current
task-local file contains the real post-commit result for later metadata capture.
The public result schema is a closed four-state machine. `planned` has no exit;
`revision-required`, `blocked` and `committed` pair with their same-named exit.
Recorded terminal results require a timestamp and auditable evidence;
`committed` requires commit/parent/message/path/preservation/hook and tree/blob
evidence, while every `blocked` branch requires its failure stage, current or
created commit identity, errors and explicit preservation/hook facts. The
runtime validates the constructed post-result against this public schema before
writing it.

## Typed Exits And Re-entry

Return exactly one exit declared by the interface. `committed` proceeds to
Branch Review or finding closure. `revision-required` re-enters this skill.
`blocked` stops the workflow. Unknown, multiple or unmapped exits fail closed.

Any non-metadata finding fix returns through implementation and the full Phase
2 check before this skill. Create a new sequence bound to the new Phase 2 digest,
pre-commit HEAD and dirty snapshot; never reuse an earlier plan.
