# Requirements Design Test SSOT

## Purpose

`guru-maintain-requirements-design-test-ssot` is the semantic owner for one
traceable Requirements, Design, and Test repository authority. It is a single
atomic capability because the three layers must change together; global
workflow and platform entries only invoke the stable Skill id and route its
typed exits.

## Repository Authority

The default authority is:

```text
docs/requirements/{README.md,versions/<version>/**}
docs/design/{README.md,versions/<version>/**}
docs/test/{README.md,versions/<version>/**}
```

Each README identifies the current version and preserves historical
navigation. A repository may supply reviewed compatible locators. Trellis task
planning remains task-local input and never becomes repository product
authority by itself.

The default task contribution is:

```text
docs/requirements-design-test-contributions/<task-ref>/
  manifest.yaml
  requirements.md
  design.md
  test.md
  traceability.md
```

Each contribution belongs to one task/ref. Parallel tasks use distinct
locators and do not modify the same shared current authority file. Promotion
rereads both the contribution and current authority; a failed promotion
re-enters only the current contribution.

## Traceability And Provenance

The stable chain is:

`requirement_id / behavior_id -> design_responsibility_id / contract_id -> test_strategy_id / scenario_id / case_id`.

References contain identity, locator, version/status, and relationship, not a
copy of source prose. Delete, replace, split, and merge changes preserve their
predecessor/successor and historical boundary. `code_recovered`, `inferred`,
`unverified`, draft, or proposed material is not confirmed/current requirement
authority until semantic review proves its source, applicability, and evidence.

The Skill inherits Architecture through the public Architecture Baseline
locator/version/status only. It neither reads Architecture private state nor
copies Architecture documents.

## Closed Profiles

- `bootstrap_foundation` establishes, reuses, or migrates a versioned authority.
- `task_impact_sync` selects no-op, isolated contribution, narrowly safe direct
  sync, or revision for one approved task delta.
- `promotion` reviews one isolated contribution for controlled promotion.
- `repair` repairs incomplete, stale, conflicting, version, navigation, or
  migration state without expanding business scope.

All four profiles use `judgment_mode=semantic`: forward behavior, AI Review
Gate, confirmation only for a real choice or side effect, deterministic
recorder/validator, then one typed exit. Workflow and standalone use identical
entry, review, freshness, and projection rules.

The five exits are `ssot_current`, `sync_required`, `revision_required`,
`baseline_incomplete`, and `blocked`. Each has one public consumer.
`sync_required` re-enters the Skill through `promotion`; `revision_required`
returns to the current planning/implementation owner; `baseline_incomplete`
enters controlled bootstrap/repair; `blocked` stops fail closed.

## Consumer Rules

Planning, Phase 2 Check, Branch Review, Publication, acceptance, and Finish
reread the live repository authority needed for their own judgment. They do not
read this package's private result or copy its semantic decision into an
aggregate handoff. Public DTOs carry only the next consumer's locator, version,
scope, status/freshness, or stable remediation fields.

Validation follows `quality-guidelines.md` Validation Scope Ownership. Ordinary
feature work runs targeted package/runtime, canonical/installed/platform,
reapply/drift, and any Issue-required single representative clean throwaway;
it does not claim the cumulative multi-platform installer or Release Gate.
