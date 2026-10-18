# Requirements Design Test SSOT Contract

This semantic package owns one atomic repository authority across Requirements,
Design, and Test. The default versioned roots are `docs/requirements/`,
`docs/design/`, and `docs/test/`; the default isolated task contribution is
`docs/requirements-design-test-contributions/<task-ref>/` with `manifest.yaml`,
`requirements.md`, `design.md`, `test.md`, and `traceability.md`.

Every active requirement or behavior links to an owning design responsibility
or contract and at least one test strategy, scenario, or case. References carry
identity and location, not duplicated prose. Subtraction and structural changes
preserve predecessor/successor and version history. Two parallel tasks use
different contribution locators and do not mutate the same shared current file.

The package inherits the public Architecture Baseline identity as
locator/version/status. It does not read Architecture private state or copy
Architecture content. Repository authority remains separate from Trellis
task-local `prd.md`, `design.md`, and `implement.md`.

The AI owns provenance, authority, completeness, traceability, conflict,
revision, sync, and route decisions. The deterministic runtime validates the
AI-authored exact public-input digest, Architecture Baseline
locator/version/status, explicit AI gate, declared mode/profile, continuation
identity, safe locator, direct version/freshness binding, unique consumer,
minimal output, and schema. It never overwrites those semantic-owner bindings. Public
output never contains document bodies, scan history, review narrative, Git
facts, authorization, recorder state, or private digests.

## Stage applicability

Read [current-knowledge.md](current-knowledge.md) completely before every
profile. That shared contract owns unit completeness, status, stable identity,
necessary relationships, reading, structural revision and migration. This
package remains the only RDT semantic owner; it adds no public fields.

This owner selects the RDT/Architecture versions applicable to the current
Task plan and candidate. Use actual immutable version/Git-history authority
when shared CURRENT advances without affecting this Task. Such advancement
does not require contribution rewrite, promotion or fresh business gates.
Explicitly applicable rules and real requirement/scope/dependency/solution
changes still enter the original revision owners. Shared-current promotion
retains its own live expected-current and subtraction/traceability checks.

## Complete-definition maintenance by profile

- `bootstrap_foundation`: establish the applicable entries and complete
  R/D/T units. When migrating an existing authority, compare all effective
  predecessor constraints, list migrated and unmigrated scope, and retain old
  complete-source navigation until the reviewed cutover.
- `task_impact_sync`: read the applicable complete units and necessary
  relationships before judging the delta. Select the original no-op,
  isolated-contribution, narrowly safe direct-sync or revision route. An
  isolated delta identifies complete resulting definitions at its own
  proposed-target locators without duplicating unchanged authority.
- `promotion`: reread the actual target, reconcile intervening changes, and
  integrate the reviewed contribution into complete current R/D/T units.
  Check surviving conditions, subtraction, stable identities and relationships
  before updating navigation/version entry. Historical contributions remain
  sources, not required assembly steps for ordinary migrated queries.
- `repair`: name missing or conflicting objects and affected conclusions.
  Restore complete definitions and links within the existing scope, or return
  the original incomplete/revision/blocked exit. Never infer that an
  unmigrated object is complete because its navigation resolves.

All profiles retain their existing gate, freshness, confirmation, invocation
and typed-exit contracts. Planning and implementation consume selected bodies;
final Check and independent Review judge their current candidate and
reconciliation. Those stages do not inherit semantic pass from navigation,
promotion or an earlier stage.
