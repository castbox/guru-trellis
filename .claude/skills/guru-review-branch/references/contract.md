# `guru-review-branch` Contract

## Entry

The public `branch_review` input contains only profile, mode, task/base refs,
committed HEAD and review intent. Public input schema 1.1 allows only
`initial_review` and `fresh_final_review`. `guru-create-task-commit:committed`
supplies the task and commit identity; Branch Review verifies parent, message,
paths and tree from live Git.

Workflow and standalone mode use the same eight preconditions: runtime,
workspace, task identity, the committed DTO plus live Git, the current Issue
Scope Ledger, complete review range, working tree, and invocation freshness.
The new path reads no Planning or Phase 2 checkpoint, Task Commit candidate,
digest, or schema. Existing completed tracked commit plans and schema 2.0
assignment/report files remain read-only compatibility inputs only when an old
active task enters without the new committed DTO; they are not generated or
required by a new review.

## Semantic Review

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
judgment. The distinct fresh-final result then binds immutable
`reviewed_content_head`. These heads intentionally differ across a normal fix
and closure sequence; ancestry, not equality, proves continuity.

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
objective structure, task/base/content identity, complete range, finding
lifecycle, fresh-final intent, facts digest and exact consumer. It never
decides review sufficiency, severity or route. A later commit may preserve the
gate only when every changed path is an explicitly allowed active-task workflow
metadata descendant; code, planning, durable SSOT, ledger and unknown paths
make it stale.

The Branch Review public wrapper validates the selected output schema and then
deletes its own checkpoint. Publication receives only the minimal typed DTO and
live Git facts; it never reads or deletes Branch Review private state. A failed
checker or invalid projection retains the checkpoint for same-owner repair.

New gates use schema 2.2. Schema 2.0 gates and their tracked assignment/raw
reports, plus schema 2.1 compact gates, remain read-only compatibility
evidence. Their legacy `finding_fix_review` intent is readable but is never
accepted by public input schema 1.1 or a new 2.2 gate. Re-entry completes
closure in memory, invokes `fresh_final_review`, writes one 2.2 private gate,
and does not copy legacy review prose forward.

Return exactly one of:

- `passed`: minimal `task_ref`, `reviewed_content_head` seed for
  `guru-review-task-publication`;
- `implementation_required`: immutable reviewed content identity and current
  finding refs;
- `scope_confirmation_required`: exact proposal refs;
- `blocked`: stable reason/remediation only.

Unknown, multiple, stale, unmapped or consumer-mismatched results fail closed.
