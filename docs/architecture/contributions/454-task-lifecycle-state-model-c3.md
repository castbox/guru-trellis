# #454 C3 Checkout Substrate Architecture Contribution

## Identity And Review State

- contribution identity: `architecture-contribution-454-task-lifecycle-state-model-c3-v1`.
- lifecycle state: `reviewed_promoted`.
- source authority: live Issue #454 and approved C3 task planning.
- task locator: `.trellis/tasks/09-20-454-task-lifecycle-state-model`.
- related RDT contribution: `docs/requirements-design-test-contributions/454-task-lifecycle-state-model-c3/`.
- predecessor baseline: `current-main-0.6.17-guru.59` / `active`.
- promoted successor: `current-main-0.6.17-guru.60` / `active`.
- reviewed range: `origin/main@9c2238bad7e73ea4a1f23dddcb7e8e9204c244da...e965b7e8b6850614a2cd21f899a02b3ea9da73f3`.
- design constitution: `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `guru-trellis-architecture-change-contract-v1`.
- change path: `target_native`.

The range completed independent review with no open P0-P3 finding after the
C3 fixes. It promotes only checkout acquisition and live resolution substrate;
C4-C7, D443, D436, E434 and production activation remain pending.

## Boundary And Decision

C3 extends the package-neutral lifecycle substrate from 35 to 39 named DTOs.
The four new checkout DTOs, machine paths and transaction identities are
call-local. Live candidates come from current Git common-dir and registered
worktree facts, not persisted checkout paths or legacy mappings.

Resolution uses closed candidate, resolution and selection states. Authority
conflicts and invalid candidates cannot be downgraded by explicit selection.
Adopt and provision reuse one live validator; provision returns the adoption
route for a primary checkout. Rollback removes only transaction-created
resources whose identities still match, while output-loss recovery is
read-only.

`guru-ensure-task-checkout` is reserved as one `state=planned` stable ID and is
listed only in canonical `planned_skill_ids`. No canonical package directory,
active selector, active graph edge, workflow route or installed/platform
projection is created. E434 remains the only owner of complete package
composition and atomic activation.

## Ownership And Compatibility

- Fork official task/session primitives remain the framework authority.
- C2 lifecycle identity/runtime remains the shared predecessor substrate.
- C3 owns only shared checkout DTO/runtime and inactive planned metadata.
- C4-C7 own branch, session, resource, owner composition and subtraction work.
- D443 and D436 retain their package migration ownership.
- E434 retains package creation, production graph activation and predecessor retirement.

There is no alias, adapter, dual-read or dual-write compatibility layer. The
predecessor production path remains active only because C3 is deliberately
inactive.

## Evidence And Limits

Focused evidence covers 51 lifecycle runtime tests, Draft 2020-12 validation,
live checkout discovery/acquisition fixtures, identifier and error contracts,
planned ownership, source/installed-active checks, task validation, workspace
boundary, Python compilation, static zero legacy/path-authority checks, line
limits and `git diff --check`.

The global package suite remains `19/20` because the unchanged
`guru-complete-task-closure` relative-ref defect is outside the C3 range. The
preset suite remains `85/86` because raw apply intentionally reports the
unsynchronized installed projection. Neither suite is claimed as passed.
Complete installer/upgrade/workflow-switch/multi-platform Release proof,
production activation and remote publication remain unverified.

No new ADR is required. `ADR-015` already owns lifecycle identity and the
framework/extension boundary. Promotion narrows `ARCH-GAP-011` but does not
close the full lifecycle gap. The promotion-created diff must receive fresh
Phase 2, Task Commit and independent complete Branch Review before Publication.
