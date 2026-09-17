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
content, durable docs, task, requirement-authority, or publication metadata drift still fails
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
- Publication authors the `Issue 关闭范围` section from current requirement
  authority and live target/default-branch facts. Use exactly one applicable
  semantic route:
  - `issue-backed completed + default branch`: complete delivery defaults to
    closure; write a GitHub closing keyword for the completed Issue.
  - `issue-backed remain-open`: use an ordinary Issue reference and state the
    concrete current-authority condition that remains after merge. Preference or
    uncertainty alone is not a remain-open reason.
  - `no external work item`: state that there is no external work item and emit
    no Issue number, reference, or closing keyword.
  - `issue-backed completed + non-default branch`: use an ordinary reference,
    state that this PR has no closing effect, and leave the later default-branch
    Publication owner to make a fresh decision.
  The reviewed PR body is the only projection of this decision. Do not create a
  closure DTO, replacement closure aggregate, hidden aggregate, or Issue-close API plan.
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
    "body": "## 变更摘要\n\n- 具体结果。\n\n## 验证结果\n\n- 当前验证证据。\n\n## Issue 关闭范围\n\n- 按上述四条路径写入当前审查结论；不要保留此占位文字。\n\n## 安全与部署影响\n\n- 如实说明。"
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
      "id": "external_work_item_effect",
      "status": "passed",
      "summary": "External work item effect matches current requirement authority.",
      "evidence_refs": ["current-requirement-authority"]
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
      "summary": "The reviewed PR payload has the intended external work item effect.",
      "evidence_refs": ["current-requirement-authority"]
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
selects the narrow stable field owned by that namespace: the PR payload
`title`/`body`, `input.branch_review_commit`,
or `runtime`. The public error
contains only `code`, `field_path`, `remediation`, and the optional bounded
`recovery_scope`; stderr, exception text, URLs, credentials, tokens, absolute
paths, and external payloads are discarded.
Freshness failures alone map to `publication_stale`. Missing or invalid
classification maps to `internal_error` with the generic owner locator and
remediation.

## Archived Entry And Independent Semantic Variant

The additive `archived_publication_review` profile has exactly `profile`,
`mode`, `task_ref`, `branch_review_commit` (A),
`pr_payload_snapshot_sha256`, and `reviewed_base_head` (B). Consume the fresh
Branch Review `archived_review_passed` seed and author only profile/mode.
The original two input schemas and schema 5.0 active semantic union are
unchanged. Aggregate 5.0 adds this independent profile, not optional active
fields or a conversion of an old checkpoint.

This entry accepts only a completed, committed and completely clean archive
whose current local HEAD, remote branch and exact same-repository Ready Open
PR are A. The summary must identify this archive, branch/base and PR. Both
runtime mappings must match their producer-owned identities: the task mapping
owns this archive locator, while the workspace mapping owns workspace and
branch identity. Missing/stale mapping stops without rebuild. Selected local
base ref and live GitHub base ref must
both still equal B, and B must be an ancestor of A. No fetch or ref update is
performed. Title and body are read from the existing PR without trimming or
newline normalization. SHA-256 of their UTF-8 sorted-key compact JSON object,
without a trailing newline, must match the input snapshot. That snapshot is
only a local freshness binding, never a prior pass or authorization.

Consume fresh Architecture `task_impact_sync(stage=publication,
source_exit=archived_review_passed)` and re-review all ten dimensions against
current authority and existing PR bytes. Only `baseline_current` permits this
review to continue. Evidence insufficiency or a result requiring writes stops;
never omit Architecture, promote, repair, or route to a writing consumer.

The semantic authoring object contains the exact six public input fields plus
`pr_payload`, `candidate_classifications`, `dimensions`, `findings`,
`conclusions`, and `route`. It has no `review_intent` or `stale_reason`.
The independent `archived-pr-readiness.schema.json` adds only schema identity
to that object when recorded in the same owner-private short-lived checkpoint.
The recorder/checker validate the fresh authoring, not a transformed active
result. Both record and check perform the read-only preflight; check does not
skip live rereads because the invocation has an earlier cached result.

- `archived_ready` requires all ten dimensions and all three conclusions
  passed, and zero open findings. Existing exact PR bytes must already be
  sufficient; do not author a replacement payload.
- `blocked` requires a concrete reason/remediation, at least one open finding
  and a non-passed dimension. Every open finding binds its corresponding
  dimension. `metadata_revision` and `task_work` retain `finding` dimensions;
  `external_blocker` retains `blocked` dimensions. Every non-passed dimension
  has an open finding. The stop does not relabel content as external failure.

There is no archived metadata-revision loop or `return_to_task_work`. Do not
write tasks, archives, history, branches, PRs or Issues; do not call active
`prepare_closeout`. Recorder/checker may create and retire only their own
short-lived private result. A current identity/snapshot mismatch returns the
existing explicit diagnostic and stops the round.

`archived_ready` contains exactly `exit_id`, `task_ref`,
`branch_review_commit`, `reviewed_base_head`, `pr_title`, and `pr_body`.
Select the five payload fields into Finalizer's target-owned
`archived_review_refresh` authoring seed; its caller adds profile/mode.
Publication consumes the snapshot hash and never emits it downstream.
The checker-passed output retires the checkpoint using the existing lifecycle.
Finalizer receives current bytes and A/B, not Publication's internal schema.

## Active Entry

`publication_review` consumes the target-owned merge of Branch Review seed
`task_ref`, `branch_review_commit` and caller-authored `profile`, `mode`,
`review_intent`. The Branch Review checkpoint and digest remain private to the
Branch Review owner and are not read by this v2 path. `publication_review_stale`
consumes Finalizer seed `task_ref`, `branch_review_commit`, `stale_reason` and
caller-authored `profile`, `mode`, `review_intent`. Workflow and standalone use
the same seven preconditions. The recorder uses the stale reason only to bind
the current re-entry round; the checked owner result remains bound to the
supplied reviewed commit and never expands a public output. Inputs outside the
current profile schema fail closed. Publication never reads or projects another
Skill's checkpoint.

`publication_review_stale` is not a base-reconciliation entry. A base-only
mismatch is projected by Finalizer only as `base_reconciliation_required` and
must be resolved by the reconcile owner. If that path creates a persistent local
reconciliation commit, `guru-review-branch:base_continuity` reviews the bounded
delta and projects the current continuity-reviewed commit into the ordinary
`publication_review` seed. Publication consumes that current commit exactly as
it consumes a complete Branch Review `passed` anchor; it does not receive the
prior complete review identity and does not bypass the shared reviewed-content
check.

## Semantic loop

Review these dimensions against current private evidence:

1. `diff_outcome_consistency`
2. `external_work_item_effect`
3. `pr_body_quality`
4. `validation_claims`
5. `branch_review_summary`
6. `docs_ssot_reconciliation`
7. `safety_deployment_impact`
8. `finish_summary_semantics`
9. `metadata_tail_integrity`
10. `artifact_binding_freshness`

For `external_work_item_effect`, independently establish whether a current
external work item exists, whether the reviewed delivery completes it, and
whether the PR target is the repository default branch. Completed Issue-backed
work defaults to closure only on a default-branch PR. Any remain-open result
must cite the specific uncompleted condition in current authority. No-work-item
and non-default-branch routes must contain no closing keyword. This is a
semantic Publication judgment; recorder/checker success cannot select the route.

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
current requirement authority and live GitHub facts. It never creates a task-local PR body
or finish-summary index handoff. After revision, reread all eight objective
preconditions and re-review only dimensions whose declared evidence
dependencies changed. The freshness reread is not a demand to repeat unrelated
semantic analysis. Carry forward an unchanged dimension only after its evidence
bindings remain current; the gate still contains all ten dimensions.
Any source, test, durable docs, spec, workflow, schema, config, preset, CI/CD,
deployment, or Branch Review drift returns to task work.

Use the immutable reviewed content identity, live base-to-HEAD Git facts,
current task and durable docs, current requirement authority, and the exact PR payload as
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
This exception applies only to genuine Publication/task-content drift. A
base-only mismatch never reaches this profile and cannot use
`return_to_task_work` or the stale checker exception as a continuity substitute.
`blocked` requires at least one `blocked` dimension, one blocked
scope/Docs/safety conclusion, and an open `external_blocker` finding whose
dimension references blocked evidence. Open metadata-revision findings remain
inside the Skill loop and cannot satisfy an external exit. Recorder and checker
rebuild all seven objective preconditions transiently; those live facts and
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
