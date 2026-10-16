---
name: guru-review-contract-wording
description: Review controlled contract wording through fixed change-request, planning-artifact, or explicit-path scope, semantic revision and classification, deterministic evidence, and typed exits.
---

# Guru Review Contract Wording

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
