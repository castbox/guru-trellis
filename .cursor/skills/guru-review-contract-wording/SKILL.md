---
name: guru-review-contract-wording
description: Use when the user asks to review Issue wording, including 审核 Issue 措辞、评审 Issue 表述是否明确, or controlled wording in change requests, planning artifacts and explicit Markdown paths. Preserve fixed scope, semantic classification and declared typed exits.
---

# Guru Review Contract Wording

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

## Intent Entry

Load this Skill for an explicit Issue wording review, including “审核 Issue
措辞” and “评审 Issue 表述是否明确”. A live Issue uses the existing
`change_request` profile; `explicit_paths` applies only to explicitly selected
repository Markdown files and cannot substitute for a live Issue review.
Obtain the profile's actual prerequisites through their existing owners before
public invocation; loading alone does not satisfy them.

General requirements review belongs to `guru-clarify-requirements`; readiness
belongs to `guru-review-change-request`. A status lookup or discussion of the
trigger phrases does not itself request wording review.

For review-only requests, report findings and proposed revisions without
editing Issue title/body, posting comments or rewriting files. If a repair
is needed for pass, retain the actual finding and existing blocked/revision
contract until that concrete mutation is authorized; do not silently rewrite
or claim pass. Preserve fixed-scope rereads, semantic gates and typed exits.

The current executing AI is this Skill's semantic owner. Read the complete
contract and perform its review yourself before authoring the current owner
result and calling record, check, and invoke. `owner_not_yet_executed` is an
internal state to continue this review, not a typed stop or a missing external
owner. Do not wait for another agent, agent ID, subagent evidence, or a
pre-existing owner result. Real missing authority or prerequisites still
follow this Skill's declared routes; runtime cannot supply your judgment.

Use this Skill after requirements clarification, before planning approval, or
for an explicit standalone Markdown review. Load
[references/contract.md](references/contract.md) before acting.

Run from the reviewed repository root. The full package is
`.trellis/guru-team/skills/packages/guru-review-contract-wording`; resolve its
`scripts/`, `schemas/`, and `examples/` there rather than under a thin Agent
discovery projection. Use the existing managed wrappers and the contract's
profile-specific argv; recorder and checker do not share every argument.

Choose exactly one fixed profile. Build its complete scope, call the
deterministic scanner, prefer a permitted rewrite over retaining weak
wording, classify every retained hit with a non-empty reason, rebuild and
rescan after any mutation, then complete the AI Review Gate and any required
real-choice or side-effect interaction before calling the recorder and checker
wrappers. Any authorization stays only in the current dialogue; the owner
result contains no authorization state or process.

Return exactly one declared typed exit. `content_changed` requires complete
re-entry by the profile consumer; it is not a partial pass. Fail closed when
scope can be narrowed, evidence is stale or incomplete, a hit is unclassified
or a contract violation, mutation preconditions are missing, product semantics
would change without confirmation, or the compatible Guru Team runtime is not
installed. Results are stdout-only owner-private evidence. A mapped
`content_changed` re-entry rebuilds the complete current scope and discards the
prior result; it never creates a task-local replacement chain. This package is
not self-contained or portable.

After the semantic gate and owner recorder/checker complete, invoke
`scripts/invoke.sh --invocation -` with the closed call-local public input,
`clarity_current` transition, and checked owner result on stdin.
The minimal DTO preserves the fixed profile for the workflow router; the
runtime validates the actual checker receipt, derives the route from its checked result,
and never reclassifies wording or reads private evidence on behalf of a
consumer.

For change-request scan, record, and check, use the existing wrappers with
`--invocation -` and the closed four-field envelope in
`schemas/review-invocation.schema.json`: `profile`, `mode`, `change_request`,
`owner_result`. Scan adds `--scan-only` and uses `owner_result={}`; record uses
the flat AI authoring object; validate the intermediate recorder receipt and
pass its unchanged `result` as the check's `owner_result`. Each reads stdin
once. Keep the complete record and check receipts in current-owner memory.
Validate the checker receipt and set
`invoke.validation_receipt = checker_response.result.validation_receipt` unchanged
as an object, not the outer checker response, a string, a recomputed receipt,
or an example. For an invoke-envelope-only error after a successful check with
unchanged facts and owner result, correct the envelope and invoke again as
defined in the contract; do not re-record, re-check, or wait for another owner.
The migration and remaining unmixed legacy callers are defined in the contract.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.


For delivery_planning_artifacts, pass routes through the existing pass router to
Architecture delivery_task_impact_sync purpose-bound final_plan on Wording-current design,
then adjacent Approval. content_changed goes through the original change
router with the selected content_changed 2.0 planning DTO: `task_ref` and
`change_refs` projected by this owner from the checked task scope and completed
revision locators. The router adds only fixed `profile=wording_reentry` and
`mode=workflow` for Author; it never reads this owner's private result. Author distinguishes
equivalent wording from changed design facts and re-enters the earliest
affected dependency. Wording remains the controlled rewrite owner, never the
business planner or approval owner. Do not route a planning pass directly to
Approval or replay a prewrite Architecture result.

## Delivery Planning input

For `delivery_planning_artifacts`, actually read
`.trellis/guru-team/skills/packages/guru-author-task-plan/references/planning-body.md`
and that same package's `templates/delivery-prd.md`,
`templates/delivery-design.md`, and `templates/delivery-implement.md` alongside
the three current documents and necessary source references. Load referenced
clauses and associated conditions before judging their wording; link presence
does not establish semantic preservation.

Use these bodies only within this owner's controlled wording review and its
existing seven planning dimensions. Keep the fixed three-file scan scope and
original rewrite/scan/re-entry contract. Do not become the general planning
sufficiency reviewer or business writer. An equivalent wording repair refreshes
only affected gates through the original `content_changed` route. A missing
commitment or changed mechanism returns through the existing route to Author
and the earliest affected owner; technical elaboration alone is not a product
scope change. Approval retains the complete planning adequacy judgment.

For Delivery documents explicitly use delivery_planning_artifacts and the
opaque public DeliveryKey. Resolve its task_ref/planning_root through the installed
API and scan/review all three current files. Never review Task-root documents as
a surrogate. With no official context key, its explicit DeliveryKey resolves
through the original projection's current-generation/C4/public-record checks;
with context, require the matching official current selection and preserve
missing/stale/conflict stops. Current change_request and explicit_paths retain their existing
contracts. The old planning_artifacts activity profile is retired; no Task
status fallback is supported. Pass carries its continuation; content_changed carries actual change_refs, key and task_ref to
their selected router. Recorder/checker envelope carries key/task_ref and the
same scope; the public DTO never carries the scan or private digest bundle.
