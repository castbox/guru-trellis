# `guru-review-branch` Contract

GitHub review/check/mergeability facts use the shared authenticated,
repo-bound `gh` adapter in `.trellis/spec/workflow/workflow-contract.md`; they
remain evidence for, not substitutes for, this Skill's semantic judgment.

## Entry

The public `branch_review` input contains only profile, mode, task/base refs,
`branch_review_commit` and review intent. Public input schema 2.0 allows only
`initial_review` and `fresh_final_review`. `guru-create-task-commit:committed`
supplies the task and commit identity; Branch Review verifies parent, paths and
tree from live Git. Commit message format is not downstream freshness authority.

Workflow and standalone mode use the same eight preconditions: runtime,
workspace, task identity, the committed DTO plus live Git, the current Issue
Scope Ledger, complete review range, working tree, and invocation freshness.
The Skill reads no Planning or Phase 2 checkpoint or Task Commit candidate.
Input that does not satisfy the current public schema fails closed.

The independent `base_continuity` profile is entered only from
`guru-reconcile-task-base:review_continuity_required`. It binds the unchanged
task HEAD and prior passing `branch_review_commit` to one exact
`old_base_head...new_base_head` delta, temporary candidate tree, relevant paths,
and original resume target. It reviews only that bounded integration surface;
it does not rewrite or replay the task-content review.

## Semantic Review

Before full-range Docs, code, test, fixture, consumer, or history retrieval,
read `.trellis/spec/workflow/semantic-retrieval.md`. Use its minimal concept
family and evidence-coverage bar during candidate qualification, including
before any negative existence or impact conclusion. Search transcripts and
query metadata remain transient and never enter the gate or public handoff.

Perform one independent semantic review of the complete current
`origin/<base>...HEAD` range. Qualify every candidate before assigning
severity. Bind affected behavior, evidence, requirement/scope basis and one
scenario class. Only supported current-scope scenarios may become a P0-P3
finding. Unconfirmed scope expansion returns `scope_confirmation_required`;
out-of-scope or disproved candidates remain non-blocking observations,
follow-ups or rejections.

Return `implementation_required` for an open current-scope finding. After its
fix passes Phase 2 and a fresh commit, run one internal closure judgment by the
finding owner or, only after a real unfinished event, a replacement. Retain the
original `introduced_head`, bind the fixing `fix_head`, bind a later
`closure_head`, and carry only concrete closure evidence into the next
judgment. The distinct fresh-final result records `review_commit`. These commit
anchors intentionally differ across a normal fix and closure sequence;
ancestry, not equality, proves finding continuity.

Closure has no public exit, recorder call, or artifact. The AI workflow
immediately dispatches a distinct fresh reviewer over the complete current
range. That reviewer consumes the transient closure result, authors one
`fresh_final_review`, and is the only reviewer whose compact passing gate is
persisted. A closure reviewer never also performs the fresh final review.

Mapped finding-fix, stale, re-entry and final-review routes continue within the
AI workflow. They are not user choices. A user prompt remains only for real
scope/authority decisions or a separately displayed Git/GitHub side effect.

## Gate And Exits

After the AI gate exists, `review-branch` writes one compact owner-private
`review-gate.json` under ignored runtime; `check-review-gate` validates
objective structure, task/base/reviewed-content identity, complete range, finding
lifecycle, fresh-final intent, facts digest and exact consumer. It never
decides review sufficiency, severity or route. The checker recalculates
`guru-reviewed-content-1.0`: excluded task/runtime metadata may change without
staling the gate, while any reviewed-content change makes it stale. Git commit
anchors remain responsible only for review range and finding ancestry.

The Branch Review public wrapper validates the selected output schema and then
deletes its own checkpoint. Publication receives only the minimal typed DTO and
live Git facts; it never reads or deletes Branch Review private state. A failed
checker or invalid projection retains the checkpoint for same-owner repair.

The gate uses only schema 3.0 with `review_commit` and
`reviewed_content_sha256`. Any schema mismatch is invalid input and fails
closed before owner evaluation.

Return exactly one of:

- `passed`: minimal `task_ref`, `branch_review_commit` seed for
  `guru-review-task-publication`;
- `continuity_passed`: exact pair and candidate identity to the workflow-owned
  `guru-base-continuity-passed-router`, which resumes the original target;
- `implementation_required`: `branch_review_commit` and current finding refs;
- `scope_confirmation_required`: exact proposal refs;
- `blocked`: stable reason/remediation only.

Unknown, multiple, stale, unmapped or consumer-mismatched results fail closed.
