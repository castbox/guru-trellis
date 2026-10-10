# Guru Review Task Delivery Contract

## Ownership And Boundary

`guru-review-task-delivery` exclusively decides whether one approved Delivery
slice is ready for remote publication. It uses `judgment_mode=semantic` and
performs no GitHub mutation, push, merge, task completion, Issue closure,
archive, Finish bookkeeping, Reactivate, or cleanup action.

Workflow and standalone modes have identical entry preconditions. The current
AI is the semantic owner; deterministic runtime only binds live task/Git facts,
checks the completed judgment, projects one DTO, and retires private state.

## Public Entry

The only input profile is `delivery_review`:

- `profile=delivery_review`;
- `mode=workflow|standalone`;
- `task_ref` identifies one active task below `.trellis/tasks/`;
- `branch_review_commit` is the exact current committed HEAD passed by the
  complete Branch Review.

Publish's `review_stale` exit projects only `task_ref`. The caller authors
`profile=delivery_review`, `mode`, and `branch_review_commit` from a currently
applicable checked Branch Review output as follows:

- If that output is still available in the current context, reread live
  candidate, base, exact review range and applicable review obligations. When
  all remain unchanged, use its existing anchor directly and execute fresh
  Delivery Review. Loss of Delivery output or Publish-private state, and normal
  checkpoint retirement, do not by themselves require another Branch Review.
- If committed content or applicable review obligations changed, return to
  the earliest affected existing owner. Required content revisions use the
  existing implementation/Phase 2/Task Commit path, followed by complete
  independent Branch Review for the new exact base-to-HEAD. Base evolution
  uses the existing pair guard, Reconcile and bounded-continuity contracts;
  it is not an automatic full-history replay or a base/range bypass.
- If the Branch Review output itself is unavailable, rerun that semantic
  owner against current authority. Do not manufacture it from Git shape,
  task status, an old summary, mutation receipt, or Phase 2 checkpoint. A
  new raw commit value alone does not establish that Branch Review occurred.

`stale_reason` remains Publish-owned context and is not part of this Skill's
public input. An authority identity update requires its original owner's fresh
applicability judgment; an equivalent applicable contract does not alone
invalidate unrelated review. Current facts and the checked output, rather than
a changed-path whitelist, establish anchor applicability. This entry creates
no additional recovery DTO, retained checkpoint, or continuation authority.

The owner freshly reads current requirement authority, approved planning,
Delivery policy, current slice, remaining work, independent delivery
conditions, validation boundaries, RDT/Docs, Architecture, base, complete
Branch Review, and live Git/GitHub facts. All ten Delivery dimensions receive
current judgment. A previous Delivery pass is not reusable, even when the
Branch Review anchor remains applicable; fresh review does not mechanically
replay unaffected Planning, Check, Task Commit or Branch Review.

Before readiness, consume the actual matching
`task_impact_sync(stage=publication)` current result. Its Architecture owner
uses the contract's Downstream eligibility entry with the still-applicable
independent conclusion and live committed-review/promotion facts. A caller
change alone does not dispatch a duplicate assessment; a relabelled Branch
Review DTO or Phase 2 pass does not satisfy this entry. Changed Architecture
facts, missing/stale evidence or unpromoted contribution follow that owner's
existing routes. Delivery does not judge impact/path/ADR or perform promotion.

## Semantic Result

Author exactly the shape in `schemas/semantic-result.schema.json`:

- `delivery_policy` keeps `task_scope_refs`, `delivery_slice_refs`,
  `remaining_work_refs`, `independent_delivery_conditions`,
  `validation_boundaries`, and `followup_owner` distinct;
- `pr_payload` contains the exact reviewed Chinese title and body;
- `remaining_work_state` is `none` only when `remaining_work_refs` is empty,
  otherwise `remaining`;
- `candidate_classifications` records the final current classification and
  direct-consumer witness for every candidate used by a finding or proposal;
- `dimensions` contains the exact ordered ten dimensions below;
- `findings` and `scope_proposals` contain only current qualified items;
- `conclusions` covers Delivery readiness, Docs/RDT/Architecture, and safety /
  deployment truthfulness;
- `route` selects exactly one declared exit.

Dimension order:

1. `requirement_authority`
2. `delivery_policy`
3. `slice_completeness`
4. `independent_delivery`
5. `implementation_quality`
6. `validation_truthfulness`
7. `docs_rdt_architecture`
8. `branch_review_freshness`
9. `pr_payload_truthfulness`
10. `base_and_live_facts`

The PR body must use `Refs #<issue>` for a source Issue in the PR repository,
or `Refs <owner>/<repo>#<issue>` for a cross-repository source Issue. It must
not contain GitHub closing keywords. It must state the delivered
slice, validation performed, remaining work, unverified boundaries, and safety
or deployment impact truthfully. It must not claim task completion or Issue
closure. A task without an external Issue emits no Issue reference.

## Causal public claims

Read `.trellis/spec/workflow/causal-completion-semantics.md` before authoring
or reviewing the exact PR payload. Apply its dimensions to the current
independent slice, separately reporting code/test, static, integration,
external and production evidence, mitigation and remaining risk. State the
actual diagnosis/mitigation/repair goal and supported disposition; the payload
must not upgrade the observation layer or imply task/root-cause completion.
Publish receives this already-reviewed payload and performs no causal judgment.

A payload-only overclaim is revised inside this owner and freshly reviewed.
A content defect uses `implementation_required`; an inadequate slice/policy
uses `planning_revision_required`; a real scope change uses
`scope_confirmation_required`. Only evidence required for this slice but
concretely unavailable blocks readiness. Production effects obtainable after
merge/deploy are reported as unverified with their remaining-task evidence
owner/condition; they do not make a valid independent slice circular.
Diagnosis or mitigation with an unknown cause can reach `ready` when its own
slice requirements are met. Keep Refs-only and the existing public I/O.

## Route Invariants

- `ready`: all dimensions and conclusions pass, no open finding or proposal,
  the PR payload is Refs-only, and Delivery policy is complete.
- `planning_revision_required`: at least one open `planning_revision` finding,
  with no open implementation, scope, or external blocker.
- `implementation_required`: at least one open `implementation` finding, with
  no open scope proposal or external blocker. A current-slice defect cannot be
  moved into remaining work.
- `scope_confirmation_required`: at least one open scope proposal and no open
  finding. This is reserved for a real authority or scope choice.
- `blocked`: at least one open `external_blocker` finding and a blocked
  dimension or conclusion, plus stable `reason_code` and `remediation`.

Planning gaps do not become external blockers. Ordinary remaining work does not
block an independently deliverable current slice. Prior Completion or Finish
does not prove the current cycle. A validation-only Reactivate with no business
diff belongs to the Completion owner and does not manufacture a Delivery.

## Private Gate And Freshness

The invocation derives task identity, current HEAD, base identity, and a
call-local `delivery_cycle_ref`. The cycle reference is deterministic over the
task, reviewed HEAD, and exact reviewed PR payload. It is a transport identity
for this cycle, not a Delivery ledger or historical authority.

The private gate is written under
`.trellis/.runtime/guru-team/owner-checkpoints/<task-key>/delivery-review-gate.json`.
The checker rereads task status, branch/worktree binding, current HEAD and base,
validates the semantic union and digest, and rejects drift. It does not judge
scope, sufficiency, findings, truthfulness, or route.

After the checker-passed DTO validates against its per-exit schema, the same
invocation deletes the checkpoint and its empty owner directory. Output loss
requires a fresh semantic Delivery Review; no public or downstream consumer may
read, interpret, or delete this private gate. Apply the Public Entry anchor
rules during that fresh review; absence of this normally retired gate does not
invalidate an otherwise current checked Branch Review output. Same-mutation
Publish recovery remains Publish-owned and never comes from this gate.

## Public Exits

- `ready`: `task_ref`, `delivery_cycle_ref`, `reviewed_head`, `pr_title`,
  `pr_body`, `remaining_work_state`; sole consumer is
  `guru-publish-task-delivery`.
- `planning_revision_required`: `task_ref`, `reason_refs`; sole consumer is the
  Delivery Planning re-entry route.
- `implementation_required`: `task_ref`, `finding_refs`,
  `resume_target=phase-2`; sole consumer is `guru-resume-implementation`.
- `scope_confirmation_required`: `task_ref`, `proposal_refs`; sole consumer is
  the existing clarification route.
- `blocked`: `reason_code`, `remediation`; sole consumer is the stop response.

No output contains review prose, timestamps, Git snapshots, digests, private
gate fields, authorization, completion state, closure intent, or historical
Delivery records.
