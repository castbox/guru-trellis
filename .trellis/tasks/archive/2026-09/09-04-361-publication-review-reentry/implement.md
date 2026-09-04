# Implementation Plan

## Phase A: Contract and Runtime Inventory

- Read the current Publication `common.py`, `owner.py`, `invoke.py`, schemas,
  examples, contract, and tests.
- Trace `_stable_code`, `_diagnostic_from_owner_error`, owner namespaces, PR
  body preflight, and every `return_to_task_work`/`blocked` projection.
- Identify the shared helper boundary without moving semantic route judgment
  into deterministic code.

## Phase B: Canonical Change

- Implement namespaced owner-error normalization and stable recovery-class
  projection in the canonical Publication package/shared runtime.
- Update public error schemas/examples and the Publication contract with the
  exact closed field set and re-entry matrix.
- Strengthen/centralize deterministic PR-body preflight for every current
  required heading/key while preserving owner semantic review responsibilities.
- Add focused regression tests for ledger mismatch, each missing heading,
  stale/cross-SHA/unknown/unmapped input, and mutation-free publication retry.

## Phase C: Projection Synchronization

- Regenerate or update the preset extension from canonical sources.
- Run the preset apply against dogfood and verify no `.new`/`.bak` remains.
- Run overlay drift checks and compare `.agents`, `.codex`, `.claude`, and
  `.cursor` Publication package projections.

## Phase D: Validation and Review

- Run package contract/runtime tests and JSON/schema validation.
- Run installed contract discovery and representative canonical/dogfood tests.
- Run `git diff --check` and the repository-required Python/Bash checks.
- Run Phase 2 check, independent complete-range Branch Review, and Publication
  readiness. Report any unavailable external evidence honestly.

## Explicit Non-Goals

Do not change Issue Scope Ledger ownership, required checks, Draft/Ready or
Merge policy, Finalizer semantics, Release behavior, hostile-input defenses,
or unrelated platform installer matrices.

## Completion Gate

Implementation is complete only when the code, schemas, workflow/Skill
contracts, tests, and all declared projections agree on the same error classes
and re-entry matrix, and semantic gates independently confirm the full current
diff. No commit, push, PR, merge, Issue closure, or cleanup is authorized by
this plan.
