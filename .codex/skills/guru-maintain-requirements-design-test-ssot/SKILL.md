---
name: guru-maintain-requirements-design-test-ssot
description: Maintain one traceable Requirements, Design, and Test repository authority through semantic profiles.
---

# Guru Maintain Requirements Design Test SSOT

`judgment_mode=semantic`. This Skill is the single semantic owner for the
Requirements, Design, and Test authority of a repository. It supports exactly
`bootstrap_foundation`, `task_impact_sync`, `promotion`, and `repair`.

The default authority is `docs/requirements/`, `docs/design/`, and
`docs/test/`. Each layer has a current entry, version history, and navigation.
Task work defaults to the isolated contribution root
`docs/requirements-design-test-contributions/<task-ref>/`; ordinary parallel
tasks do not edit shared current authority. A compatible reviewed locator may
replace either default without changing this package contract.

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
Public exits are `ssot_current`, `sync_required`,
`revision_required`, `baseline_incomplete`, and `blocked`.

## Profiles

- `bootstrap_foundation`: establish, reuse, or migrate one versioned three-layer
  authority; verify provenance, navigation, traceability, and Architecture
  Baseline inheritance.
- `task_impact_sync`: decide no-op, isolated contribution, narrowly safe direct
  sync, or current-task revision from the approved task delta.
- `promotion`: reread one contribution and current authority, then review
  traceability, subtraction, version/history, and Architecture inheritance
  before promotion.
- `repair`: repair incomplete, stale, conflicting, version, navigation, or
  migration state without expanding business requirements or unrelated history.

## Closed Loop

Perform positive behavior, then the AI Review Gate. Ask for confirmation only
when the call introduces a real choice or side effect. Author the semantic
owner result, including the explicit AI Review Gate and unique consumer, only
after that review; invoke `scripts/invoke.sh`; and consume exactly one declared
exit. Workflow and standalone modes use the same entry,
review, freshness, and projection rules.

`sync_required` re-enters this Skill through a target-authored `promotion`
input. `revision_required` returns to the current planning/implementation
owner. `baseline_incomplete` returns to bootstrap or controlled repair.
`blocked` stops fail closed. Unknown, multiple, stale, or unmapped results do
not imply a route.

Read [references/contract.md](references/contract.md) for the reusable authority
and public I/O contract.
