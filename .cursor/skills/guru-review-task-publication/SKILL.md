---
name: guru-review-task-publication
description: Review task publication readiness through ten semantic dimensions, ordinary metadata revision or read-only archived review, and four typed exits.
---

# Guru Review Task Publication

## Completed Archive Profile

`archived_publication_review` is a separate read-only entry. Its exact input is
`profile`, `mode`, `task_ref`, `branch_review_commit` (A),
`pr_payload_snapshot_sha256`, and `reviewed_base_head` (B), from fresh
`guru-review-branch:archived_review_passed`. Consume current Architecture
`task_impact_sync(stage=publication, source_exit=archived_review_passed)` before
the ten-dimension review. Only `baseline_current` resumes; insufficient evidence
or a result requiring writes stops read-only. Do not promote, repair, restore,
or enter active `prepare_closeout`.

Reread the completed committed/clean archive, current local/remote/Ready Open PR
A, selected local and live base B, current requirement authority, and existing
PR title/body bytes. Re-review all ten dimensions; the snapshot is identity,
not semantic approval. Do not reuse a retired checkpoint or earlier pass.
Author the independent archived semantic variant described in the contract.
When existing bytes are sufficient, return `archived_ready`; otherwise return
`blocked` with truthful findings. Metadata/content findings retain
`metadata_revision`/`task_work` and `finding` dimensions; external evidence
blockers retain `external_blocker` and `blocked` dimensions. Never relabel
content findings, revise metadata, return active task work, or edit PR/task/
archive/history/Issue. Only owner-private recorder/checker output and retirement
are permitted. The two active profiles below retain their original rules.

Use after `guru-review-branch:passed`, or for a checker-declared stale
finalization handback. Read `references/contract.md`, author the selected public
input profile, and complete the semantic review. The sole public Happy Path is
`scripts/invoke.sh`, bound to stable command
`invoke-guru-review-task-publication`: pass the public input and the
AI-completed semantic result, and let that invocation record, objectively
check, project, and retire the private checkpoint in one process.

Use the exact authoring fields, enums, route rules, and valid JSON template in
`references/contract.md`. The invocation derives task, reviewed-commit, and content
identity fields; do not guess or repeat them in the semantic result.

Do not read package runtime, schemas, examples, evals, or tests for the normal
path. `record-task-publication-review` and `check-task-publication-review`
remain package-private diagnostic, testing, and bounded recovery commands.
The old `--owner-result` argument shape remains compatibility-only on the same
public invoke command; it is selected only when that argument is supplied and
never precedes or runs alongside the semantic-result Happy Path.

The stale profile requires the Finalizer-projected `branch_review_commit`.
Bind the checked owner result to that same commit. Normal content continuity drift
may produce a semantic `task_work` finding and `return_to_task_work`; it can
never produce `ready`. This exception applies only after the runtime proves the
reviewed commit is an ancestor of current HEAD and successfully inspects the
descendant diff; an invalid or non-ancestor commit, or an uninspectable diff,
fails closed.

Do not use `publication_review_stale` for a base-only mismatch. Finalizer owns a
separate `base_reconciliation_required` exit for that condition. When post-review
base reconciliation creates a new committed HEAD, bounded continuity must first
review the exact base delta and project that current continuity-reviewed commit
as `branch_review_commit`; only then may ordinary `publication_review` run.
Publication does not inspect the prior complete review commit or relax its
current reviewed-content identity check.

Never treat scanner success, empty findings, changed-file classification, a
deterministic readiness flag, or script success as semantic pass. Metadata-only
revision remains inside this Skill. Reread every objective precondition, then
re-review only dimensions whose direct evidence changed. A prior passed
dimension may be carried forward only when its evidence references remain
current and byte-identical; source, test, durable-doc, spec, workflow, schema,
config, or deployment drift returns to task work.

Publication alone decides the external work item effect from current requirement
authority, the reviewed diff, and live Git/GitHub branch facts. Apply these
normal-path rules without creating a cross-stage closure DTO:

- An Issue-backed delivery that completely resolves the current Issue defaults
  to closure. When the PR targets the repository default branch, put a GitHub
  closing keyword for that Issue in the reviewed PR body.
- Keep an Issue open only when current authority names a concrete condition that
  remains after this merge, such as later verification, observation, release, or
  uncovered scope. State that reason and use a reference without a closing
  keyword.
- A task with no external work item produces no Issue reference and no closing
  effect.
- A PR targeting a non-default branch references the Issue without a closing
  keyword. A later PR into the default branch receives a fresh Publication
  judgment; this PR must not claim that it closes the Issue.

GitHub owns the actual automatic close when a closing-keyword PR reaches the
default branch. Publication does not call an Issue-close API, and Finalizer or
Merge must not reinterpret the reviewed effect.

Re-entry is scope-precise: tracked task artifacts, code, tests, durable docs,
or current requirement authority return through Phase 2, Task Commit, Branch Review,
and Publication; PR title/body or other publication payload changes retry only
Publication; identity-only expiry refreshes the affected identity; and scope,
reviewed-content, or close-scope changes invalidate the prior ready result.
Publication-only retry must not recreate commits, PRs, archives, Ready
mutations, or unrelated Branch Review evidence.

Before a publication observation can become a finding, task-work return, or
publication blocker, form only candidate refs and live publication/diff/test
locators and invoke `guru-qualify-normal-scenario` with
`publication_candidate_set`. Do not assign severity or route before
`classified`. Rejected candidates cannot become clarification, task work, or a
blocker. Mechanism revision returns to task work for remove/replace and a fresh
publication review; blocked stops. The Publication gate records only this
owner's final direct-consumer classification/witness and never references
qualification stdout, a result/report, locator, or checkpoint.

Before a proposed publication mechanism participates in a finding, task-work
return, blocker, or readiness judgment, invoke `guru-qualify-solution-mechanism`
with `publication_candidate_set`. A `mechanism_revision_required` result
removes or replaces only that mechanism and returns to task work for fresh
qualification; it never enters scope confirmation.

Emit exactly one declared typed exit. Missing, stale, ambiguous, multiple,
unmapped, or checker-failed evidence fails closed.

For an explicit independent manual operation after an automatic stop, read
`.trellis/workflow.md#manual-gitgithub-operations` (Manual Git/GitHub Operations).
That global boundary does not relax this Skill's entry or completion contract.

`ready` has exactly one consumer: `guru-finalize-task`. The caller must not
push the reviewed/publication HEAD or create a PR between this Skill and that
consumer; Finalizer owns the complete remote transaction.
