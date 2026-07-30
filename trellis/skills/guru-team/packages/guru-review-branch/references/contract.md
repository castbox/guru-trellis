# `guru-review-branch` Contract

## Entry

The public `branch_review` input contains only profile, mode, task/base refs,
committed HEAD and review intent. Public input schema 1.1 allows only
`initial_review` and `fresh_final_review`. `guru-create-task-commit:committed`
supplies the task and commit identity; Branch Review verifies parent, message,
paths and tree from live Git.

Workflow and standalone mode use the same eleven preconditions: runtime,
workspace, task, commit, planning, Phase 2, ledger, Docs SSOT, complete review
range, working tree and invocation freshness. New reviews allow only their
compact gate plus explicitly named ignored runtime inputs. Existing completed
tracked commit plans and schema 2.0 assignment/report files remain read-only
compatibility inputs for active tasks; they are not generated or required by a
new review.

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
original `introduced_head`, bind the current `resolved_at_head`, and carry only
concrete closure evidence into the next judgment. These heads intentionally
differ across a normal fix commit.

Closure has no public exit, recorder call, or artifact. The AI workflow
immediately dispatches a distinct fresh reviewer over the complete current
range. That reviewer consumes the transient closure result, authors one
`fresh_final_review`, and is the only reviewer whose compact passing gate is
persisted. A closure reviewer never also performs the fresh final review.

Mapped finding-fix, stale, re-entry and final-review routes continue within the
AI workflow. They are not user choices. A user prompt remains only for real
scope/authority decisions or a separately displayed Git/GitHub side effect.

## Gate And Exits

After the AI gate exists, `review-branch` writes one compact
`review-gate.json`; `check-review-gate` validates objective structure,
task/base/HEAD identity, complete range, finding lifecycle, fresh-final intent,
facts digest and exact consumer. It never decides review sufficiency, severity
or route.

New gates use schema 2.1. Schema 2.0 gates and their tracked assignment/raw
reports remain read-only compatibility evidence. Their legacy
`finding_fix_review` intent is readable but is never accepted by public input
schema 1.1 or a new 2.1 gate. Re-entry completes closure in memory, invokes
`fresh_final_review`, writes one 2.1 gate, and does not copy legacy review prose
forward.

Return exactly one of:

- `passed`: minimal `task_ref`, `reviewed_head`, `review_ref` seed for
  `guru-review-task-publication`;
- `implementation_required`: current finding refs;
- `scope_confirmation_required`: exact proposal refs;
- `blocked`: stable reason/remediation only.

Unknown, multiple, stale, unmapped or consumer-mismatched results fail closed.
