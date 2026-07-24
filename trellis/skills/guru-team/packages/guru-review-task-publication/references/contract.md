# Task Publication Review Contract

## Entry

`publication_review` consumes the target-owned merge of Branch Review seed
`task_ref`, `reviewed_head`, `review_ref` and caller-authored `profile`, `mode`,
`review_intent`. `publication_review_stale` consumes future seed `task_ref`,
`stale_reason` and caller-authored `profile`, `mode`, `review_intent`,
`reentry_context`. Workflow and standalone use the same twelve preconditions.
The recorder copies `stale_reason` and `reentry_context` into the private gate,
requires `supersedes_publication_ref` to equal the exact current prior gate,
and the public wrapper compares both public stale fields with the checked owner
result. These fields never expand the public output.

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
After revision, reread/rescan and repeat all ten dimensions. Any source, test,
durable docs, spec, workflow, schema, config, preset, CI/CD, deployment, or
Branch Review drift returns to task work.

## Gate and exits

After the AI Gate and required confirmation, record and check the one
task-local `pr-readiness.json`. `ready` requires every dimension passed and
every current-scope finding closed with non-empty scope, evidence, affected
artifacts, and closure evidence. Its closed semantic layer also records
scope/Docs/safety conclusions, revision history, reviewer-process evidence,
and confirmation status; all three conclusions must pass.
`return_to_task_work` requires at least one `finding` dimension and an open
`task_work` finding whose dimension references that non-passed dimension.
`blocked` requires at least one `blocked` dimension, one blocked
scope/Docs/safety conclusion, and an open `external_blocker` finding whose
dimension references blocked evidence. Open metadata-revision findings remain
inside the Skill loop and cannot satisfy an external exit. The closed
deterministic layer records all twelve
recomputed preconditions, artifact/repository facts, and the opaque identity.
Every `ready` precondition must be `passed`; a non-ready semantic route may
preserve objective `failed` precondition facts so the checker can reproduce
the AI-selected return/block outcome without choosing that route itself.
`return_to_task_work` carries exact finding refs. `blocked` carries a stable
reason and remediation.

`publication_ref` is an opaque current identity. The future finalization owner
may augment only a checker-passed `ready` gate with deterministic
`publish_inputs`; it must preserve every semantic section and never construct
ready state. When finalization first adds the exact validated
`closeout-plan.json`, it reruns all twelve entry preconditions and may accept
only the resulting repository binding plus the derived
`review_range_and_working_tree` digest change; every other entry binding must
remain exact and passed.

The public wrapper derives actual exit only from the checker-passed owner
result. Eval `expected_exit` is compared afterward and never enters the native
request, owner result, or route selector.
