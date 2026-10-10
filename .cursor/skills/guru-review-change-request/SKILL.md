---
name: guru-review-change-request
description: Review whether a current change request is one independently deliverable unit through linked prerequisite evidence, an AI readiness gate, and five typed exits.
---

# Guru Review Change Request

The current executing AI is this Skill's semantic owner. Read the complete
contract and perform its review yourself before authoring the current owner
result and calling record, check, and invoke. `owner_not_yet_executed` is an
internal state to continue this review, not a typed stop or a missing external
owner. Do not wait for another agent, agent ID, subagent evidence, or a
pre-existing owner result. Real missing authority or prerequisites still
follow this Skill's declared routes; runtime cannot supply your judgment.

Use this Skill after `guru-review-contract-wording:change_request:pass` and
before task workspace creation. Load
[references/contract.md](references/contract.md) before acting.

Reread the current target authority, then validate clarity and wording evidence. Review all
ten readiness dimensions, record findings and one scope conclusion, complete
the AI Review Gate, and call the recorder and checker only after the semantic
judgment exists. Return exactly one declared typed exit.

Before a discovered behavior scenario can affect the delivery unit, readiness
finding, requested test, clarification route, or blocker, form only current
candidate refs and live locators and invoke `guru-qualify-normal-scenario` with
`change_request_candidate_set`. Only the classified router may return eligible
candidates to this review. Rejected candidates remain non-actionable and never
become clarification. Mechanism revision returns here for remove/replace and
fresh qualification; blocked stops. This package never persists or rereads a
qualification result.

At the same candidate boundary, invoke `guru-qualify-solution-mechanism` with
`change_request_candidate_set` before accepting a proposed mechanism as a
delivery-unit, finding, test, or blocker basis. A mechanism revision removes
or replaces only that proposal and returns here for fresh qualification; it
does not enter scope clarification.

The recorder and checker validate only closed JSON shape, hashes, linkage,
freshness, fixed consumers, and objective exit invariants. They never generate
findings, select a delivery unit, decide readiness, or choose a route. Pre-task
and standalone execution is stdout-only. `ready` routes by the current
`transition.target.kind` through `guru-task-intake-router`; Issue creation and
task creation have separate owners. Fail closed when evidence is missing, stale, mismatched, or the
compatible Guru Team preset runtime is unavailable. This package is not
self-contained or portable.

All three commands use `--invocation -` and one JSON envelope containing
`schema_version=1.0`, `public_input`, the independent public `transition`,
`owner_context.change_request` (current source snapshot), and `owner_result`.
For record, `owner_result` is this Skill's completed AI review. Replace it with
record receipt `result` for check; add the checker's `validation_receipt` only for invoke.
Record/check use `schemas/review-invocation.schema.json`; invoke uses the shared
semantic-owner invocation schema. No separate input locators or authored
`prerequisite_payloads` remain supported.

Run from the target repository root. The installed scripts are under
`.trellis/guru-team/skills/packages/guru-review-change-request/scripts/`,
not beside the platform discovery copy. Call `record-change-request-review.sh`,
`check-change-request-review.sh`, then `invoke.sh`, each with
`--root . --invocation - --json`. Follow the contract's
[Producer-Bound Draft Recipe](references/contract.md#producer-bound-draft-recipe)
for draft identity, authority digest and receipt consumption, and
[Same-Scope Authoring Recovery](references/contract.md#same-scope-authoring-recovery)
for ordinary construction errors. Rebuild this consumer's minimal authoring
from the unchanged actual producer output; do not patch private linkage or
request another confirmation for a same-scope, side-effect-free correction.
The minimum authored `ai_review_gate` is `status`, `reviewer`, and `summary`.
Explicit dimensions, findings (including `[]`), scope conclusion and selected
exit remain AI-owned and required. Record derives both gate digests and the
findings count; never import private linkage or eval runtime to author them.

Use the actual `wording_current` producer transition for ready, original
`clarity_current` for a missing-wording reroute, or original `context_current`
for a missing-clarity reroute. Do not reconstruct upstream private results or
downgrade a later transition. Preserve the original public context needed for
re-entry in the call-local conversation; never fabricate missing hashes.
The runtime derives minimal prerequisites, validates the AI-selected route,
and emits the public handoff. Checker alone rereads the issue; invoke checks
the exact receipt and current envelope without live calls. It does not decide
readiness or expose the private review artifact.


At this candidate boundary, consume actual normal-scenario and solution-mechanism
outcomes before loading `guru-qualify-root-cause` with `change_request_candidate_set`. Supply only eligible
refs. New or materially changed incident/protection mechanisms enter that owner;
ordinary features receive its stable applicability disposition. Consume a
still-applicable same-mechanism conclusion on later stages and independently
review this stage's current work/evidence; caller change alone does not repeat
qualification. Root `classified` continues this stage, retaining diagnosis or
mitigation disposition without claiming repair. `mechanism_revision_required`
removes/replaces that mechanism and reenters; `diagnosis_required` pauses only
the unsupported repair and continues bounded investigation of the returned
gaps through this owner, then resubmits. A concrete `blocked` stops. Do not turn
symptom suppression into unrelated scope confirmation, cache qualifications,
or use qualification as completion. Actual scope changes use existing routes.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
