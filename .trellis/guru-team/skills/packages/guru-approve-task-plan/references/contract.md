# Guru Approve Task Plan Contract

## Ownership And Profile

`guru-approve-task-plan` is the only semantic owner of Phase 1 planning
approval and of the single task-local `planning-approval.json` artifact. It
uses `judgment_mode=semantic` and the exact stage order
`forward_behavior -> ai_review_gate -> conditional_human_confirmation -> recorder_validator -> typed_exit`.

The global workflow owns phase order, one mandatory invocation, four typed
exit consumers, and the approved-only task activation transition. It must not
copy this Skill's adequacy, provenance, proposal, confirmation, revision, or
recorder/checker loop. `guru-review-contract-wording` remains the only owner of
the fixed `planning_artifacts` wording profile. `guru-clarify-requirements`
remains the only owner of requirement-authority and scope mutation.

Workflow and standalone modes use the same ordered entry preconditions:

1. `runtime_dependency`
2. `task_workspace`
3. `requirement_authority`
4. `planning_artifacts`
5. `docs_ssot_plan`
6. `contract_wording_evidence`
7. `scope_ledger`
8. `repository_snapshot`
9. `invocation_freshness`

Standalone mode discovers the current task directly but does not weaken any
gate. Both modes require a complete compatible Guru Team preset and shared
runtime; this package is not self-contained or portable.

## Semantic Closed Loop

After all entry facts are current:

1. Read `prd.md`, `design.md`, `implement.md`, the current requirement
   authority, issue scope ledger, and the locatable `Docs SSOT Plan`.
   Bind scope identity through the canonical positive issue-number projection
   of primary, close, related, and follow-up categories. Exclude decision
   trails, acceptance metadata, and embedded approval hashes; those records may
   evolve without circularly invalidating the approval, but category changes
   require full re-entry.
2. Review planning adequacy, ambiguity, acceptance coverage, implementation
   sequence, validation, compatibility, rollback, and durable-docs ownership.
3. Review one authoritative provenance matrix and cover every load-bearing
   requirement, design contract, acceptance item, and test obligation.
4. Review every necessary implementation choice and every unusual-scenario
   proposal. Do not introduce a mechanism merely because it is theoretically
   stronger.
5. Revise task-local planning gaps and rerun
   `guru-review-contract-wording:planning_artifacts`. Route any source
   authority or scope mutation to `guru-clarify-requirements`.
6. Complete the final AI Review Gate. Recorder/checker success is not evidence
   that this Gate occurred.
7. When an unusual scope expansion remains necessary, obtain exact dedicated
   proposal confirmation and update the current source authority before it may
   enter approved execution.
8. Separately display links to all three current planning documents and obtain
   explicit `post-planning-approval` confirmation.
9. Send the AI-reviewed input to `record-planning-approval`, run
   `check-planning-approval`, and return exactly one declared typed exit.

## Provenance Review

Every load-bearing item has one stable id, planning artifact path, statement
locator, statement SHA-256, one classification, authority references, and an
AI-authored reason. The four classifications are:

- `explicit_requirement`: directly supported by a current source authority;
- `necessary_implementation_choice`: required to implement an explicit
  contract, with ordered alternatives, selected id, selection reason, and both
  product/risk scope expansion flags false;
- `approved_scope_expansion`: one runtime-recomputable exact proposal with
  dedicated confirmation and updated current authority all bound to the same
  proposal digest;
- `out_of_scope_proposal`: excluded from approved execution and assigned an
  explicit route/disposition.

The AI decides which statements are load-bearing, whether coverage is complete,
which class applies, and whether a choice changes product or risk scope. The
runtime may only resolve a caller-authored locator, hash its canonical UTF-8
statement bytes, validate field combinations and unique ids, and verify the
caller-authored coverage digest. It must never infer or generate provenance.

Every `approved_scope_expansion.scope_expansion` has three closed bindings:

- `proposal_binding`: either `source_kind=planning_artifact` with one controlled
  locator under the current task's `prd.md`, `design.md`, or `implement.md`, or
  `source_kind=unusual_scenario_candidate` with one current candidate id;
- `confirmation`: the source-appropriate dedicated confirmation kind and the
  exact proposal digest;
- `authority_binding`: one entry authority ref, that current authority's
  runtime-materialized SHA-256, and the same proposal digest.

The recorder and checker recompute proposal bytes from the controlled planning
locator or the canonical unusual-candidate projection. A caller-declared digest
without that content source, a stale locator/candidate, a generic or wrong-kind
confirmation, a stale authority digest, or any disagreement among the three
proposal digests fails closed. `planning_artifact` uses
`dedicated-scope-expansion`. `unusual_scenario_candidate` reuses exactly the
candidate's `dedicated-unusual-scenario` confirmation and authority ref; it does
not duplicate proposal content or ask for a second confirmation. Both source
kinds may coexist in one review without sharing or conflating their digests.

## Unusual Scenarios And Confirmation

Review candidates only in the closed classes `security_or_threat`,
`attack_or_malicious_actor`, `toctou_or_concurrency_race`,
`fault_injection_or_crash_consistency`, `cross_os_atomicity`, and
`other_nonstandard`. Each candidate records trigger evidence, scope, cost,
at least one alternative, consequence, source references, and one disposition:
`explicit_requirement`, `mechanism_removed`, `mechanism_replaced`,
`confirmed_scope_expansion`, `clarification_required`, or `out_of_scope`.
An `explicit_requirement` disposition has at least one source requirement
reference, and every recorded source requirement reference resolves to a
current `requirement_authorities[].id`.

`confirmed_scope_expansion` requires
`confirmation_kind=dedicated-unusual-scenario`, the exact proposal SHA-256,
confirmation summary/time, and updated authority reference. This is not the
same evidence as `user_confirmation.kind=post-planning-approval`; generic
continuation or planning confirmation can never fill the dedicated field.
When the confirmed unusual proposal becomes a load-bearing provenance entry,
its `scope_expansion.proposal_binding` references this candidate id. Runtime
recomputes the candidate digest and requires the provenance confirmation and
authority binding to project the same candidate confirmation and authority;
the two structures are one confirmation projected across two review views, not
two independent approvals.
Refusal, missing authority, or a proposal that cannot safely be removed,
replaced, or clarified blocks approval.

When a non-required lock, atomic write, race hardening, fault injection, or
similar mechanism creates risk or scope, return `revision_required`; remove or
replace it and perform a fresh review. Do not manufacture an approved scope
expansion to preserve the mechanism.

## Artifact And Deterministic Boundary

The artifact path remains `{TASK_DIR}/planning-approval.json`. New evidence
uses `schema_version=2.0`, `skill_id=guru-approve-task-plan`, and closed schema
id `guru-planning-approval-2.0`. `reviewed_artifacts[]` and
`approved_artifacts[]` contain byte-identical entries for the three planning
documents. The payload binds current task/workspace, authorities, Docs SSOT
Plan, wording evidence, repository snapshot, ambiguity compatibility
projection, semantic reviews, confirmations, typed exit, consumer, and
`facts_sha256`.

`record-planning-approval` consumes AI-reviewed input and rebuilds objective
task/workspace, authority, planning, Docs SSOT, wording, base/HEAD, dirty-path,
statement locator, proposal locator/candidate, current authority, and digest
facts. `check-planning-approval` rebuilds current facts and validates schema,
projections, statement and proposal locator/digest binding, implementation
choice references, dedicated confirmation/current-authority same-proposal
binding, AI Gate shape,
post-planning confirmation, facts digest, artifact digest, and the closed
exit/consumer union.

Neither command selects load-bearing statements, assigns provenance, decides
choice necessity, decides scenario necessity, judges confirmation sufficiency,
passes the AI Gate, or chooses a route. The approved activation checker rejects
every non-approved artifact.

Recorder invocation records selected base, base ref/head, current HEAD and dirty
paths and rereads them around the write. Drift within that invocation fails.
After approved task activation, expected implementation HEAD and dirty-path changes
do not alone make planning stale. Planning document, Docs SSOT locator,
wording evidence, source authority, or task identity drift requires complete
Skill re-entry.

## Typed Exits And Re-entry

- `approved` requires passed AI Gate with empty findings, revision actions,
  scope proposals, and blocking reasons; complete provenance; no unresolved
  unusual proposal; current wording pass; explicit post-planning confirmation
  with non-null prompt and confirmation timestamps; and consumer
  `workflow:phase-1-task-activation`.
- `revision_required` requires task-local gaps and non-empty revision actions,
  no authority mutation, and consumer `skill:guru-approve-task-plan`. Planning
  changes require fresh wording evidence before re-entry.
- `clarify_scope` requires a non-empty authority/scope proposal excluded from
  approved execution and consumer `skill:guru-clarify-requirements`. After that
  Skill completes, rerun all nine entry checks.
- `blocked` requires missing authority, refusal, external blocker, or inability
  to revise safely and consumer `stop:task-plan-approval-blocked`.

Unknown, duplicate, multiple, unmapped, consumer-mismatched, or
Gate-inconsistent exits fail closed. Active schema 1.2 approval evidence cannot
be consumed by the new Skill or downstream gates; perform complete v2 semantic
re-entry and recording. Archived approval artifacts remain historical and are
not rewritten.
