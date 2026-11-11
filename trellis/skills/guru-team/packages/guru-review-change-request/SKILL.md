---
name: guru-review-change-request
description: Use when the user asks to review GitHub Issue readiness, including 审核 Issue 是否可以开工、评审 Issue 是否可独立交付, or to assess a change request as one independently deliverable unit. Preserve linked prerequisite evidence, the AI readiness gate and declared typed exits.
---

# Guru Review Change Request

## Common review sufficiency

Before reviewing this owner's object, read `review-sufficiency.md` in full from
the complete Guru provider that supplies this Skill. Its workflow-spec root is
`trellis/presets/guru-team/spec/workflow` in source, or `.trellis/spec/workflow`
after installation. Resolve target-project authority separately; the target
need not install Trellis to receive review from another provider. Apply the
common rules within this owner's original scope, order and stage conditions.

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

## Qualification Applicability

At this Skill's candidate boundary, first read the original owners' short
[normal](../guru-qualify-normal-scenario/references/applicability.md),
[solution](../guru-qualify-solution-mechanism/references/applicability.md), and
[root](../guru-qualify-root-cause/references/applicability.md) conditions before
loading any qualifier in full. This owner judges each condition independently
from current authority, actual candidates and material changes; it does not
copy a qualifier's complete verdict. Adopt a still-applicable conclusion. Only
when an owner's conditions require a current invocation, explicitly load that
stable Skill and invoke it with its real applicable nonempty set and the
profile below. If it does not trigger, load no qualifier body, assemble no
input and emit no empty, classified or skipped result for it. The complete
current-stage judgment and all applicable non-passing routes remain required.

## Issue Content

For Issue and proposed-draft review, read the shared
[Issue content specification](../guru-clarify-requirements/references/issue-content.md)
in full before the existing readiness gate, together with the writing
specification above and necessary current sources. Apply it within the ten
existing dimensions to the complete final title/body, scope, delivery unit,
and observable acceptance. Return ordinary omissions to the affected original
owner through existing exits; do not turn unsettled technical elaboration into
a product requirement gap or silently expand a local revision. The full
installed content body is
`.trellis/guru-team/skills/packages/guru-clarify-requirements/references/issue-content.md`.

## Intent Entry

Load this Skill for an explicit Issue readiness or independent-deliverability
review, including “审核 Issue 是否可以开工” and “评审 Issue 是否可独立交付”.
General “审核 Issue” without that purpose enters `guru-clarify-requirements`
for requirements review. A status lookup or discussion of these trigger
phrases does not itself request readiness review.

Loading is distinct from a valid public invocation. Obtain missing current
Discovery, Clarify and Wording evidence through the existing workflow and
original owners before invoking this review; never synthesize their results
or treat a prior informal review as current prerequisite evidence.

Review-only scope does not authorize Issue mutation, Task/resource creation
or implementation. Preserve the existing typed exits and their consumers;
`ready` is a readiness conclusion, not authorization for downstream creation.
Any later mutation retains its owning Skill's current-dialogue boundary.

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
finding, requested test, clarification route, or blocker, apply Qualification
Applicability. When normal requires a current invocation, form only its real
candidate refs and live locators and invoke `guru-qualify-normal-scenario` with
`change_request_candidate_set`; consume eligibility through its classified
router. Rejected candidates remain non-actionable and never
become clarification. Mechanism revision returns here for remove/replace and
fresh qualification; blocked stops. This package never persists or rereads a
qualification result.

At the same candidate boundary, apply solution's own conditions. When they
require a current invocation, invoke `guru-qualify-solution-mechanism` with
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
The same recipe covers `standalone_request`: source `draft_id`, target
`request_id`, and public target locator use the actual producer locator.
The caller locator can differ. Keep the actual transition's mode; the source
profile does not select workflow or standalone execution.
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


At this candidate boundary, apply the original
[root conditions](../guru-qualify-root-cause/references/applicability.md).
When they require a current invocation, explicitly load `guru-qualify-root-cause`
with `change_request_candidate_set` and supply only actual eligible refs. This caller uses its
current scenario and authority-placement judgments and consumes actual normal
or solution outcomes when those owners triggered. It never requires an outcome
from an owner that correctly did not trigger. Adopt a still-applicable
same-mechanism conclusion and independently review this stage's current
work/evidence; stage or caller change alone does not repeat qualification.
Material changes refresh only affected judgments; a lost necessary conclusion
returns to its original owner for recovery or fresh judgment. Root `classified`
continues this stage, retaining diagnosis or mitigation disposition without
claiming repair. `mechanism_revision_required` removes/replaces that mechanism
and reenters; `diagnosis_required` pauses only the unsupported repair and
continues bounded investigation of the returned gaps through this owner, then
resubmits. A concrete `blocked` stops. Do not turn symptom suppression into
unrelated scope confirmation, cache qualifications, or use qualification as
completion. Actual scope changes use existing routes.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
