# Task Publication Review Contract

## Entry

`publication_review` consumes the target-owned merge of Branch Review seed
`task_ref`, `reviewed_content_head` and caller-authored `profile`, `mode`,
`review_intent`. The Branch Review checkpoint and digest remain private to the
Branch Review owner and are not read by this v2 path. `publication_review_stale`
consumes Finalizer seed `task_ref`, `reviewed_content_head`, `stale_reason` and
caller-authored `profile`, `mode`, `review_intent`. Workflow and standalone use
the same eight preconditions. The recorder uses the stale reason only to bind
the current re-entry round; the checked owner result remains bound to the
supplied reviewed HEAD and never expands a public output. A legacy two-field
stale seed is invalid and must be regenerated from current Finalizer facts.

For one-time active-task compatibility, the Branch Review owner reads its own
legacy gate, completes any required fresh-final re-entry, and emits the current
minimal `passed` DTO. Publication accepts only that DTO. A legacy Publication
input containing `reviewed_head` or `review_ref` fails closed and routes back to
Branch Review; Publication never reads or projects another Skill's checkpoint.

## Semantic loop

Review these dimensions against current private evidence:

1. `diff_outcome_consistency`
2. `issue_scope_closure`
3. `pr_body_quality`
4. `validation_claims`
5. `branch_review_summary`
6. `docs_ssot_reconciliation`
7. `safety_deployment_impact`
8. `finish_summary_semantics`
9. `metadata_tail_integrity`
10. `artifact_binding_freshness`

Every finding records a stable ref, dimension, scope basis, evidence and
affected artifacts, route, status, and closure evidence. The AI chooses
`metadata_revision`, `task_work`, or `external_blocker`; scripts do not.

Only `pr-body.md`, `finish-summary-index.json`, and contract-listed
Issue-Scope-Ledger publication metadata are eligible for internal revision.
After revision, reread all eight objective preconditions, recompute the changed
artifacts, and re-review only dimensions whose declared evidence dependencies
changed. The freshness reread is not a demand to repeat unrelated semantic
analysis. Carry forward an unchanged dimension only after its evidence bindings
remain byte-identical and current; the gate still contains all ten dimensions.
Any source, test, durable docs, spec, workflow, schema, config, preset, CI/CD,
deployment, or Branch Review drift returns to task work.

Use the immutable reviewed content identity, live base-to-HEAD Git facts,
current task and durable docs, Issue Scope Ledger, PR body, and finish summary
index as semantic evidence. Publication does not read Planning, Phase 2, or
Branch Review private checkpoints and never requires an
`implementation-handoff.md` transcription.

The repository status binding uses one closed publication allowlist. New
reviews allow the current Issue Scope Ledger, `pr-body.md`,
`finish-summary-index.json`, and the current command's explicitly named ignored
runtime input; Branch Review continuity comes only from the public
`reviewed_content_head` and live Git.
Completed legacy `task-commit-plans/NNN.json` and legacy review artifacts remain
read-only compatibility inputs when the current task was created before the
AI-first migration; they are never generated or required by a new review.
`pr-readiness.json` is the recorder-owned artifact and is excluded from its own
repository snapshot. A runtime path is allowed only when it is the current
command's explicit regular-file input under `.trellis/.runtime/guru-team/`;
the runtime prefix itself is never an allowlist. Any other task-local, runtime,
or repository status path makes `review_range_and_working_tree` fail and
prevents `ready`.

## Gate and exits

After the AI Gate and required confirmation, record and check the one
owner-private `pr-readiness.json` checkpoint. `ready` requires every dimension
passed and every current-scope finding closed with non-empty scope, evidence,
affected artifacts, and closure evidence. All three scope/Docs/safety
conclusions must pass.
`return_to_task_work` requires at least one `finding` dimension and an open
`task_work` finding whose dimension references that non-passed dimension.
For stale-profile content continuity drift this is the only non-blocked legal
exit: the checker permits the old reviewed identity solely so the semantic
owner can return the task to Phase 2. `ready` still requires current content
continuity and the complete Finalizer preflight. The exception requires a valid
reviewed HEAD that is proven to be an ancestor of current HEAD plus a successful
descendant diff inspection. Invalid or non-ancestor identities and failed diff
inspection remain fail-closed continuity errors on every exit.
`blocked` requires at least one `blocked` dimension, one blocked
scope/Docs/safety conclusion, and an open `external_blocker` finding whose
dimension references blocked evidence. Open metadata-revision findings remain
inside the Skill loop and cannot satisfy an external exit. Recorder and checker
rebuild all eight objective preconditions transiently; those live facts and
digests do not enter the private semantic checkpoint or public DTO. Every
`ready` precondition must be passed. A non-ready semantic route may carry its
explicit finding or blocker without a script choosing that route.
`return_to_task_work` carries exact finding refs. `blocked` carries a stable
reason and remediation.

The `ready` DTO contains only `exit_id`, `task_ref`, and
`reviewed_content_head`. Finalizer consumes that DTO directly and runs the same
side-effect-free closeout preflight already required before `ready`; it never
reads, augments, or understands the Publication checkpoint.

After any checked typed output passes its output schema, the Publication public
wrapper deletes its own checkpoint. A failed checker or invalid projection keeps
that checkpoint for same-owner repair. Finalizer therefore starts from the DTO
and live facts after Publication private state has already been retired.

The public wrapper derives actual exit only from the checker-passed owner
result. Eval `expected_exit` is compared afterward and never enters the native
request, owner result, or route selector.
