# Design: Publication Review Error Projection and Re-entry

## Authority and Scope

Issue #361 is the sole delivery target. The canonical source is
`trellis/skills/guru-team/packages/guru-review-task-publication/`; generated
dogfood and platform copies are projections. #247 remains the owner of Issue
Scope Ledger authority, #223 owns checks/Draft-Ready/Merge policy, and #332 is
only a later Release consumer.

## Current Failure

Owner failures may be namespaced strings such as
`issue_scope_ledger:issue_scope_ledger_primary_disposition_invalid` or
`publication_content:PR body 缺少 ...`. The shared Publication projection
currently accepts only a bare safe code, so namespaced values are discarded and
become `internal_error` with `field_path=owner`.

## Proposed Model

1. Add one shared, deterministic owner-error normalizer that accepts the
   existing namespaced owner code format, preserves the stable owner code,
derives a closed recovery class from the namespace, and preserves only a
bounded field path and remediation. Bare legacy codes remain supported
where the existing contract requires them; unknown namespaces fail closed.
2. Extend the Publication public invocation-error contract with the minimal
   recovery classification consumed by the caller. Keep the schema closed and
   update canonical examples, generated extension data, and all installed
   projections together.
3. Make Publication preflight use the existing objective PR-body validator as
   the single deterministic source for required headings and Docs SSOT keys.
   Its failures must be emitted under the Publication-content class, not as a
   task-work finding.
4. Keep semantic route selection in the Publication owner. The facade only
   validates and projects the owner result. A task-work finding returns through
   `return_to_task_work`; a metadata/publication-only correction stays in the
   owner loop; stale identity refreshes the affected identity; runtime or
   unmapped failures block.
5. Add an explicit re-entry matrix to the contract and tests. The matrix binds
   changed artifact class to the first owner to rerun and prohibits unrelated
   mutation/evidence recreation.

## Data Flow

`owner error -> namespace normalizer -> public error DTO` preserves
`error_code`, `field_path`, `recovery_scope`, and remediation. The DTO carries
no checkpoint, digest bundle, secret, absolute path, or review history.

`PR payload -> objective preflight -> Publication-content diagnostic` runs
before semantic route consumption and covers all currently required sections.
Semantic review still owns adequacy, scope, findings, and route; scripts only
record/check objective facts.

## Compatibility and Projection

The active public contract is updated in canonical package files first. The
preset extension and dogfood copies are regenerated/synchronized, then
`.agents/skills`, `.codex/skills`, `.claude/skills`, and `.cursor/skills` are
checked for byte/content parity. No legacy fallback route or second authority
is introduced.

## Risks and Controls

- Risk: a new field is ignored by an old projection. Control: closed-schema
  tests, extension regeneration, installed discovery, and overlay drift.
- Risk: classification is inferred from free-form text. Control: only stable
  owner namespaces/codes are mapped; unknown values block or remain generic.
- Risk: publication-only retry accidentally re-enters task work. Control:
  table-driven re-entry tests assert the first consumer and mutation counts.
- Risk: facade output is mistaken for semantic approval. Control: tests assert
  semantic result/AI gate inputs separately from deterministic DTO projection.

## Acceptance Evidence

Targeted package tests, schema validation, canonical/dogfood/installed
discovery, platform projection parity, `apply.sh` plus overlay drift check,
`git diff --check`, and a fresh Phase 2/Branch Review after implementation.
