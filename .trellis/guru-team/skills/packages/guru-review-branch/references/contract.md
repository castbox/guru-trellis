# `guru-review-branch` Contract

GitHub review/check/mergeability facts use the shared authenticated,
repo-bound `gh` adapter in `.trellis/spec/workflow/workflow-contract.md`; they
remain evidence for, not substitutes for, this Skill's semantic judgment.

## Entry

Aggregate public input schema 3.0 dispatches two independent profiles. The
public `branch_review` schema 2.0 input contains only profile, mode, task/base
refs, `branch_review_commit` and one of `initial_review|fresh_final_review`.
`guru-create-task-commit:committed` supplies the task and commit identity;
Branch Review verifies parent, paths and tree from live Git. Commit message
format is not downstream freshness authority.

Workflow and standalone mode use the same eight preconditions: runtime,
workspace, task identity, the committed DTO plus live Git, the current Issue
Scope Ledger, complete review range, working tree, and invocation freshness.
The Skill reads no Planning or Phase 2 checkpoint or Task Commit candidate.
Input that does not satisfy the current public schema fails closed.

Every official independent-review worker is invoked with a prompt that
authorizes approved-plan work only. If it observes a planning-external
candidate, it stops before any edit, added test, self-fix, severity,
classification, or route and returns only the invocation-local
`candidate_ref`, `observed_behavior`, `locators`, and
`minimal_reproduction_hint`. The Guru owner rereads the live range and
authority and completes fresh `branch_review_candidate_set` qualification
before continuing or redispatching work for that candidate. Official
`trellis-*` agent files remain unchanged and upstream-owned.

The independent `base_continuity` schema 1.0 profile is entered only from
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
`origin/<base>...HEAD` range. Form a candidate-only set, then invoke
`guru-qualify-normal-scenario:branch_review_candidate_set` before assigning
severity. Candidate input carries no decision, scenario class, severity,
expected route, or caller assertion of a normal path. Only candidates returned
eligible through `classified` may become a P0-P3 finding.
`scope_confirmation_required` enters requirements clarification;
`mechanism_revision_required` returns to task work for remove/replace and a
fresh complete review; `blocked` stops. Rejected or disproved candidates remain
non-blocking observations and cannot become scope confirmation, negative tests,
implementation, follow-up, or publication blockers,
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
`review-gate.json` at
`.trellis/.runtime/guru-team/owner-checkpoints/<task-key>/review-gate.json` and
returns only a minimal task/exit/checkpoint receipt. The task owner and package
resolver determine the path; callers cannot choose a gate locator.
`check-review-gate` resolves that exact checkpoint and validates
objective structure, task/base/reviewed-content identity, complete range, finding
lifecycle, fresh-final intent, facts digest and exact consumer. It never
decides review sufficiency, severity or route. The checker recalculates
`guru-reviewed-content-1.0`: excluded task/runtime metadata may change without
staling the gate, while any reviewed-content change makes it stale. Git commit
anchors remain responsible only for review range and finding ancestry.

The current gate schema directly records this Branch Review owner's final
candidate classifications and, for every candidate, the direct-consumer witness
`requirement_refs`, `supported_entry_refs`, `existing_caller_refs`,
`honest_action_sequence`, `defect_observation`, and `excluded_assumptions`.
It never stores or points to qualification stdout, a result/report, a temporary
locator, or a qualification checkpoint. Legacy gates are stale and require a
fresh complete Branch Review.

The Branch Review public wrapper accepts current public input only, internally
reruns `check-review-gate`, validates the selected output schema and never
accepts caller-authored gate or checker output. Successful `passed`,
`continuity_passed`, and zero-payload stop `blocked` projection deletes the
checkpoint and empty owner directory. `implementation_required` and
`scope_confirmation_required` retain the same checkpoint for their mapped
same-owner re-entry; a
duplicate invocation deterministically returns the same DTO and creates no
second state. Publication receives only the minimal typed DTO and live Git
facts; it never reads or deletes Branch Review private state. A failed checker
or invalid projection retains the checkpoint for same-owner repair. Missing
after retirement, wrong-task/base/HEAD/content, unsafe components, and symlink
ancestors or gate files fail closed.

The current gate uses only schema 5.0 with profile-specific identity,
`review_commit`, `reviewed_content_sha256`, and the final terminal
candidate-classification witness required by its direct consumer. Aggregate
input schema 2.0 and gate schemas 3.0 and 4.0 remain legacy compatibility
inventory, not current runtime authority. Any current schema mismatch is
invalid input and fails closed before owner evaluation.

Return exactly one of:

- `passed`: minimal `task_ref`, `branch_review_commit` seed for
  `guru-review-task-publication`;
- `continuity_passed`: exact pair and candidate identity to the workflow-owned
  `guru-base-continuity-passed-router`, which resumes the original target;
- `implementation_required`: `branch_review_commit` and current finding refs;
- `scope_confirmation_required`: exact proposal refs;
- `blocked`: stable reason/remediation only.

Unknown, multiple, stale, unmapped or consumer-mismatched results fail closed.
