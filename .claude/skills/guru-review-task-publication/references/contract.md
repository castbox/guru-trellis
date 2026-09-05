# Task Publication Review Contract

## Recommended Happy Path

The only normal public invocation is the stable package command
`invoke-guru-review-task-publication` through `scripts/invoke.sh`:

```bash
scripts/invoke.sh \
  --root <repository> \
  --input <public-input.json> \
  --semantic-result <ai-completed-publication-result.json>
```

The AI completes the ten-dimension semantic review before this call. The
invocation validates that the semantic result belongs to the exact public profile,
task, reviewed commit, intent, and stale reason; then it performs the existing
record, objective check, public projection, and checkpoint retirement in one
process. Its `TaskPublicationInvocationContext` is invocation-local only: it
reuses one objective Publication snapshot and one checked owner result between
record and check, is never persisted or exposed in the public DTO, and is not
semantic authority.

The invocation preserves the existing `ready`, `return_to_task_work`, and `blocked`
outputs. Metadata-only revision remains inside the AI owner loop. Reviewed
content, durable docs, task, ledger, or publication metadata drift still fails
the existing bindings or returns through the AI-authored current route; the
invocation never selects or changes that route. Package-private record and check
commands remain supported for tests and bounded diagnosis. The same public
command accepts `--owner-result` only for compatibility with callers that
already recorded and checked the owner result; `--semantic-result` and
`--owner-result` are mutually exclusive, and the compatibility branch is not
executed during the normal path.

## Semantic result authoring contract

The semantic-result file is the AI-owned judgment submitted to the invocation. For
`publication_review`, it contains exactly these nine top-level members:
`profile`, `mode`, `review_intent`, `pr_payload`,
`candidate_classifications`, `dimensions`, `findings`, `conclusions`, and
`route`. For `publication_review_stale`, add the tenth member `stale_reason` and
use `review_intent=stale_reentry_review`.

Do not add `task_ref`, `branch_review_commit`, `reviewed_content_sha256`,
schema identity, timestamps, digests, or live repository facts. The invocation
derives those private and objective bindings from the public input and current
repository state.

Author the members as follows:

- `pr_payload` has exactly non-empty `title` and `body` strings.
- `candidate_classifications` contains every candidate that participated in
  the final route. Each item has exactly `candidate_ref`, `decision`, `witness`,
  and `consumer_use=publication_route_checker`. `decision` is one of
  `qualified_current`, `qualified_explicit_nonstandard`,
  `qualified_approved_expansion`, `rejected_no_authority`,
  `rejected_unsupported_entry`, `rejected_not_reproduced`, or
  `rejected_out_of_scope`. `witness` has exactly `requirement_refs`,
  `supported_entry_refs`, `existing_caller_refs`, `honest_action_sequence`,
  `defect_observation`, and `excluded_assumptions`; every list except
  `excluded_assumptions` is non-empty.
- `dimensions` contains the exact ordered ten ids listed below. Every item has
  exactly `id`, `status`, `summary`, and non-empty `evidence_refs`; `status` is
  `passed`, `finding`, or `blocked`.
- `findings` contains zero or more items with exactly `finding_ref`,
  `candidate_ref`, `dimension`, `summary`, `scope_basis`, `evidence_refs`,
  `affected_artifacts`, `route_class`, `status`, and `closure_evidence`.
  `route_class` is `metadata_revision`, `task_work`, or `external_blocker`;
  `status` is `open` or `closed`. An open finding has an empty
  `closure_evidence`; a closed finding has non-empty closure evidence. Every
  non-passed dimension has a matching open finding, and an open finding cannot
  reference a passed dimension.
- `conclusions` has exactly `issue_scope`, `docs_ssot`, and
  `safety_deployment`. Each conclusion has exactly `status`, `summary`, and
  non-empty `evidence_refs`, using the same three statuses as dimensions.
- `route` is exactly `{"typed_exit":"ready"}`,
  `{"typed_exit":"return_to_task_work"}`, or
  `{"typed_exit":"blocked","reason_code":"...","remediation":"..."}`.
  `ready` requires all dimensions and conclusions passed and all findings
  closed. `return_to_task_work` requires at least one `finding` dimension and
  an open `task_work` finding, permits no blocked dimension or conclusion, and
  carries only task-work open findings. `blocked` requires a blocked dimension,
  a blocked conclusion, and an open `external_blocker` finding.

The following is a complete valid initial `ready` authoring template. Replace
the placeholder prose and evidence refs with the current review; duplicate or
remove candidate items as needed, but keep the declared object shapes exact.

<!-- publication-semantic-result-template:start -->
```json
{
  "profile": "publication_review",
  "mode": "workflow",
  "review_intent": "initial_review",
  "pr_payload": {
    "title": "具体的中文 PR 标题",
    "body": "## 变更摘要\n\n- 具体结果。\n\n## 验证结果\n\n- 当前验证证据。\n\n## Issue 关闭范围\n\n- Closes #123。\n\n## 安全与部署影响\n\n- 如实说明。"
  },
  "candidate_classifications": [
    {
      "candidate_ref": "candidate:publication:no-defect",
      "decision": "rejected_not_reproduced",
      "witness": {
        "requirement_refs": ["issue:#123"],
        "supported_entry_refs": ["entry:publication-review"],
        "existing_caller_refs": ["caller:guru-review-task-publication"],
        "honest_action_sequence": ["Review the current publication payload and complete diff."],
        "defect_observation": "Current evidence does not reproduce a publication defect.",
        "excluded_assumptions": []
      },
      "consumer_use": "publication_route_checker"
    }
  ],
  "dimensions": [
    {
      "id": "diff_outcome_consistency",
      "status": "passed",
      "summary": "The diff matches the reviewed outcome.",
      "evidence_refs": ["git:branch_review_commit"]
    },
    {
      "id": "issue_scope_closure",
      "status": "passed",
      "summary": "Issue closure matches the current ledger.",
      "evidence_refs": ["issue-scope-ledger.json"]
    },
    {
      "id": "pr_body_quality",
      "status": "passed",
      "summary": "The PR body is specific and reviewable.",
      "evidence_refs": ["pr_payload"]
    },
    {
      "id": "validation_claims",
      "status": "passed",
      "summary": "Validation claims match current evidence.",
      "evidence_refs": ["validation:current"]
    },
    {
      "id": "branch_review_summary",
      "status": "passed",
      "summary": "The Branch Review conclusion is current.",
      "evidence_refs": ["git:branch_review_commit"]
    },
    {
      "id": "docs_ssot_reconciliation",
      "status": "passed",
      "summary": "Docs SSOT reconciliation is complete.",
      "evidence_refs": ["durable-docs"]
    },
    {
      "id": "safety_deployment_impact",
      "status": "passed",
      "summary": "Safety and deployment impact are stated.",
      "evidence_refs": ["pr_payload#安全与部署影响"]
    },
    {
      "id": "finish_summary_semantics",
      "status": "passed",
      "summary": "The finish summary projection is current.",
      "evidence_refs": ["pr_payload#变更摘要"]
    },
    {
      "id": "metadata_tail_integrity",
      "status": "passed",
      "summary": "Only the allowed metadata tail follows content review.",
      "evidence_refs": ["git-status"]
    },
    {
      "id": "artifact_binding_freshness",
      "status": "passed",
      "summary": "Every directly consumed owner result is current.",
      "evidence_refs": ["owner-checkers"]
    }
  ],
  "findings": [],
  "conclusions": {
    "issue_scope": {
      "status": "passed",
      "summary": "The current close scope is complete.",
      "evidence_refs": ["issue-scope-ledger.json"]
    },
    "docs_ssot": {
      "status": "passed",
      "summary": "The approved Docs SSOT plan is reconciled.",
      "evidence_refs": ["durable-docs"]
    },
    "safety_deployment": {
      "status": "passed",
      "summary": "There is no undisclosed safety or deployment impact.",
      "evidence_refs": ["pr_payload#安全与部署影响"]
    }
  },
  "route": {
    "typed_exit": "ready"
  }
}
```
<!-- publication-semantic-result-template:end -->

## Structured invocation diagnostics

Recorder, checker, invocation, and dry-run use one sanitized owner-error
projection. A classified owner failure may supply a stable `error_code`, a
bounded locator, and a short recovery instruction. Namespaced owner errors are
projected by their stable namespace. A safe namespaced detail code remains the
public code; a non-code detail falls back to
`<namespace>_contract_failed`. When the owner omits a locator, the projection
selects the narrow stable field owned by that namespace: the ledger or its
`primary_issue`, the PR payload `title`/`body`, `input.branch_review_commit`,
or `runtime`. The public error
contains only `code`, `field_path`, `remediation`, and the optional bounded
`recovery_scope`; stderr, exception text, URLs, credentials, tokens, absolute
paths, and external payloads are discarded.
Freshness failures alone map to `publication_stale`. Missing or invalid
classification maps to `internal_error` with the generic owner locator and
remediation.

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

Before any new scenario participates in those findings or routes, this owner
forms a candidate-only set and invokes
`guru-qualify-normal-scenario:publication_candidate_set`. Candidate input has no
decision, severity, expected exit, route, or caller assertion of scope.
`classified` returns to Publication; `scope_confirmation_required` enters
requirements clarification; `mechanism_revision_required` returns to task work
for remove/replace and a complete fresh downstream round; `blocked` stops.
Rejected candidates cannot become clarification, task work, or publication
blockers. Publication neither reads nor persists a qualifier artifact.

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

The provenance metadata-tail manifest allowlist remains closed. Reapply may
change `skill_packages.files` and `overlays.files` only when both lists retain
their length and order, every entry retains all non-`action` fields, and every
entry changes exactly from `action=installed` to `action=unchanged`. Any other
action, entry, order, or content change remains outside the allowlist; source
binding, the manifest-only dirty path, reviewed-content parent, and publication
lineage checks remain unchanged.

## Gate and exits

After the AI Gate and required confirmation, record and check the one
owner-private schema 5.0 `pr-readiness.json` checkpoint. It directly records
this owner's final candidate classifications and the witness required by its
current checker: `requirement_refs`, `supported_entry_refs`,
`existing_caller_refs`, `honest_action_sequence`, `defect_observation`, and
`excluded_assumptions`. These fields never import or reference qualification
stdout, a result/report, temporary locator, or checkpoint. Older checkpoint
versions are stale and require a fresh Publication round. `ready` requires every dimension
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

Finalizer is the unique `ready` consumer and the unique owner of the subsequent
push, remote verification, Draft PR, archive push, and Ready transition. The
caller must not push either reviewed or publication HEAD and must not create a
PR after Publication returns `ready`.

After any checked typed output passes its output schema, the Publication public
wrapper deletes its own checkpoint. A failed checker or invalid projection keeps
that checkpoint for same-owner repair. Finalizer therefore starts from the DTO
and live facts after Publication private state has already been retired.

The public wrapper derives actual exit only from the checker-passed owner
result. Eval `expected_exit` is compared afterward and never enters the native
request, owner result, or route selector.
