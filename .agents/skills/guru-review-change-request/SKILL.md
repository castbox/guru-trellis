---
name: guru-review-change-request
description: Review whether a current change request is one independently deliverable unit through linked prerequisite evidence, an AI readiness gate, and five typed exits.
---

# Guru Review Change Request

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
and standalone execution is stdout-only. `ready` declares
`guru-create-task-workspace` as its consumer but does not create or persist a
task workspace. Fail closed when evidence is missing, stale, mismatched, or the
compatible Guru Team preset runtime is unavailable. This package is not
self-contained or portable.

All three commands use `--invocation -` and one JSON envelope containing
`schema_version=1.0`, `public_input`, the independent public `transition`,
`owner_context.change_request` (current source snapshot), and `owner_result`.
For record, `owner_result` is this Skill's completed AI review. Replace it with
record stdout for check; add the checker's `validation_receipt` only for invoke.
Record/check use `schemas/review-invocation.schema.json`; invoke uses the shared
semantic-owner invocation schema. No separate input locators or authored
`prerequisite_payloads` remain supported.

Use the actual `wording_current` producer transition for ready, original
`clarity_current` for a missing-wording reroute, or original `context_current`
for a missing-clarity reroute. Do not reconstruct upstream private results or
downgrade a later transition. Preserve the original public context needed for
re-entry in the call-local conversation; never fabricate missing hashes.
The runtime derives minimal prerequisites, validates the AI-selected route,
and emits the public handoff. Checker alone rereads the issue; invoke checks
the exact receipt and current envelope without live calls. It does not decide
readiness or expose the private review artifact.
