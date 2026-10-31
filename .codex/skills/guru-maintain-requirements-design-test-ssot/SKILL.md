---
name: guru-maintain-requirements-design-test-ssot
description: Maintain and reconcile the repository 需求、设计、测试 SSOT and their traceability through existing semantic profiles. Dedicated requirements/design/test-plan document reviews use applicable specialist standards; this Skill retains authority maintenance and its profile prerequisites.
---

# Guru Maintain Requirements Design Test SSOT

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

Apply `.trellis/spec/workflow/quality-guidelines.md#specialist-review-standards`
within this owner's current-authority reading and maintenance scope. Load the
applicable requirements, design or test-plan specialist and its same-source
standards when the selected artifact requires that review. Consume current
evidence without copying standard bodies or treating specialist conclusions
as authority promotion, a formal Guru gate or Task Completion.

Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget` before
any confirmation, choice or clarification. This Skill retains its own action
plan, confirmation boundary and execution/recovery contract.

`judgment_mode=semantic`. This Skill is the single semantic owner for the
Requirements, Design, and Test authority of a repository. It supports exactly
`bootstrap_foundation`, `task_impact_sync`, `promotion`, and `repair`.

The default authority is `docs/requirements/`, `docs/design/`, and
`docs/test/`. Each layer has a current entry, version history, and navigation.
Task work defaults to the isolated contribution root
`docs/requirements-design-test-contributions/<task-ref>/`; ordinary parallel
tasks do not edit shared current authority. A compatible reviewed locator may
replace either default without changing this package contract.

Before executing any profile, read
[references/current-knowledge.md](references/current-knowledge.md) in full.
It owns complete-unit reading, revision, promotion and migration behavior.
Use applicable complete bodies and necessary relationships; navigation and
historical contributions do not replace a migrated current definition.

The stable traceability chain is:

`requirement_id / behavior_id -> design_responsibility_id / contract_id -> test_strategy_id / scenario_id / case_id`.

References carry identity, locator, version, status, and relationship only.
They do not copy source prose. Deletion, replacement, split, and merge retain
predecessor/successor identity and a historical boundary.

The AI rereads the live authority, current contribution, and the public
Architecture Baseline locator/version/status before every gate. It owns
authority selection, provenance, scope, completeness, traceability, findings,
revision, sync kind, and route. `code_recovered`, `inferred`, `unverified`, or
otherwise draft material never becomes confirmed/current requirement authority
without semantic review and evidence.

The deterministic invocation records the reviewed result only in call-local
memory, then validates the AI gate, mode, profile, continuation, safe locators,
direct version/freshness bindings, unique consumer, and exactly one minimal
typed projection. It never decides sufficiency or route and persists no result.
Public exits are `candidate_ready`, `ssot_current`, `sync_required`,
`revision_required`, `baseline_incomplete`, and `blocked`.

## Profiles

- `bootstrap_foundation`: establish, reuse, or migrate one versioned three-layer
  authority; verify provenance, navigation, traceability, and Architecture
  Baseline inheritance.
- `task_impact_sync` 2.0 (`schema_version=2.0`, `stage=phase2`): decide no-change,
  isolated complete proposed definitions, repair, or current-task revision.
  A complete changed proposal returns `candidate_ready`; do not write shared
  current here or call the proposal already current. No-change retains
  `ssot_current` and creates no empty contribution.
- `promotion` 2.0 (`schema_version=2.0`, `stage=final_integration`): after
  candidate Check, reread one contribution and the real current target, then review
  traceability, subtraction, version/history, and Architecture inheritance
  before integrating it into the complete current definitions. The original
  owner writes and reads back the real files before selecting `ssot_current`;
  the wrapper only validates a completed judgment and performs no document write.
- `repair`: repair incomplete, stale, conflicting, version, navigation, or
  migration state without expanding business requirements or unrelated history.

## Closed Loop

Perform positive behavior, then the AI Review Gate. Ask for confirmation only
when the call introduces a real choice or side effect. Author the semantic
owner result, including the exact current public-input SHA-256, Architecture
Baseline locator/version/status, explicit AI Review Gate, and unique consumer,
only after that review; invoke `scripts/invoke.sh`; and consume exactly one
declared exit. The runtime validates those AI-authored bindings and never
overwrites them. Workflow and standalone modes use the same entry,
review, freshness, and projection rules.

`candidate_ready` hands only contribution and applicable authority locators/version
to `guru-requirements-design-test-ssot-current-router`, which routes the complete
proposed definitions into candidate Check. It is not a current-authority update.
`sync_required` re-enters this Skill through a target-authored `promotion`
input. `revision_required` returns to the current planning/implementation
owner. `baseline_incomplete` returns to bootstrap or controlled repair.
`blocked` stops fail closed. Unknown, multiple, stale, or unmapped results do
not imply a route.

Read [references/contract.md](references/contract.md) for the reusable authority
and public I/O contract.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
