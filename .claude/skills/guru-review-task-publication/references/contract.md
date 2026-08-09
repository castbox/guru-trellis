# Task Publication Review Contract

## Entry

`publication_review` consumes the target-owned merge of Branch Review seed
`task_ref`, `branch_review_commit` and caller-authored `profile`, `mode`,
`review_intent`. The Branch Review checkpoint and digest remain private to the
Branch Review owner and are not read by this v2 path. `publication_review_stale`
consumes Finalizer seed `task_ref`, `branch_review_commit`, `stale_reason` and
caller-authored `profile`, `mode`, `review_intent`. Workflow and standalone use
the same eight preconditions. The recorder uses the stale reason only to bind
the current re-entry round; the checked owner result remains bound to the
supplied reviewed commit and never expands a public output. Inputs outside the
current profile schema fail closed. Publication never reads or projects another
Skill's checkpoint.

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

The owner may revise only its in-memory PR title/body and contract-listed
Issue-Scope-Ledger publication metadata. It never creates a task-local PR body
or finish-summary index handoff. After revision, reread all eight objective
preconditions and re-review only dimensions whose declared evidence
dependencies changed. The freshness reread is not a demand to repeat unrelated
semantic analysis. Carry forward an unchanged dimension only after its evidence
bindings remain current; the gate still contains all ten dimensions.
Any source, test, durable docs, spec, workflow, schema, config, preset, CI/CD,
deployment, or Branch Review drift returns to task work.

Use the immutable reviewed content identity, live base-to-HEAD Git facts,
current task and durable docs, Issue Scope Ledger, and the exact PR payload as
semantic evidence. Publication does not read Planning, Phase 2, or
Branch Review private checkpoints and never requires an
`implementation-handoff.md` transcription.

The repository status binding classifies task/runtime metadata through the
shared reviewed-content boundary; Branch Review continuity comes only from the
public `branch_review_commit`, the shared content identity, and live Git.
`pr-readiness.json` is the recorder-owned artifact and is excluded from its own
repository snapshot. Any dirty reviewed-content path makes
`review_range_and_working_tree` fail and prevents `ready`.

## Gate and exits

After the AI Gate and required confirmation, record and check the one
owner-private `pr-readiness.json` checkpoint. `ready` requires every dimension
passed and every current-scope finding closed with non-empty scope, evidence,
affected artifacts, and closure evidence. All three scope/Docs/safety
conclusions must pass.
`return_to_task_work` requires at least one `finding` dimension and an open
`task_work` finding whose dimension references that non-passed dimension.
For stale-profile content continuity drift this is the only non-blocked legal
exit: the checker permits the recorded reviewed identity solely so the semantic
owner can return the task to Phase 2. `ready` still requires current content
continuity and the complete Finalizer preflight. The exception requires a valid
reviewed commit that is proven to be an ancestor of current HEAD plus a successful
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

The `ready` DTO contains exactly `exit_id`, `task_ref`,
`branch_review_commit`, `pr_title`, and `pr_body`. Finalizer consumes those five
fields directly and runs the same side-effect-free closeout preflight already
required before `ready`; it never reads, augments, or understands the
Publication checkpoint. That preflight may classify one owner-private pre-#191
Finalizer plan as supersedable, but only after objectively proving its exact
legacy verification gate/request, unchanged task/repository/branch identities,
active pre-PR/pre-archive single-consumer state, untracked artifacts,
old-to-current reviewed ancestry, and fast-forwardable remote ancestor. It does
not retire the old state or create the provenance tail; only the checked
Finalizer transition may do so.

After any checked typed output passes its output schema, the Publication public
wrapper deletes its own checkpoint. A failed checker or invalid projection keeps
that checkpoint for same-owner repair. Finalizer therefore starts from the DTO
and live facts after Publication private state has already been retired.

The public wrapper derives actual exit only from the checker-passed owner
result. Eval `expected_exit` is compared afterward and never enters the native
request, owner result, or route selector.
