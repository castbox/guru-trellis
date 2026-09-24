# #454 C5 Session And Resource Control Stores Architecture Contribution

## Identity And Review State

- contribution identity: `architecture-contribution-454-task-lifecycle-state-model-c5-v1`.
- lifecycle state: `contribution_candidate`.
- source authority: live Issue #454 and active generation 3 task planning.
- task locator: `.trellis/tasks/09-20-454-task-lifecycle-state-model`.
- related RDT contribution: `docs/requirements-design-test-contributions/454-task-lifecycle-state-model-c5/`.
- predecessor baseline: `current-main-0.6.17-guru.62` / `active`.
- candidate successor: assigned by reviewed promotion.
- design constitution: `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `guru-trellis-architecture-change-contract-v1`.
- change path: `target_native`.

This candidate covers only C5 path-free session adaptation, resource ownership ledger, Finish seal input and Cleanup
resolution primitives. It does not activate a Skill package or production workflow and does not claim C6-C7, D443,
D436, E434, #434 activation, Publication, Finalizer, Delivery or Release proof.

## Boundary And Decision

The Fixed Fork official schema-2 session store remains the only session persistence authority. Guru adds a thin adapter
that validates and projects `TaskLifecycleDTO`, delegates repository/common-dir discovery and record writes to the
official primitive, and returns `explicit_task_mode` when no usable context key exists. Session write failure never
rolls back an already established lifecycle mutation. Task locator, branch, checkout path, HEAD, ownership, semantic
pass and user authorization do not enter the session record.

The C5 resource ledger is repository-local under Git common-dir and keyed by `TaskId + lifecycle_generation`. It records
each resource incarnation with acquisition origin, conservative ownership, portable resource ref, binding epoch and
revision, lifecycle state and responsibility role. C4 consumes only the existing `OwnershipPort`; it does not read the
ledger representation. Current binding, ownership and resource incarnation must agree on epoch, revision and branch,
but that consistency check is not an automatic task selector.

Missing ownership and conflicting ownership are distinct. Active control loss may reconstruct pre-existing resources as
caller-owned after fresh branch/live-resource validation. Terminal control loss never recreates historical Guru
ownership and instead requires user-directed manual cleanup selection. Ordinary Cleanup sees only Guru-owned resources
in `cleanup_pending`; caller-owned, unknown ownership and retained handoff-control refs remain outside its deletion set.

Automatic discovery selects only one valid candidate. Zero or multiple candidates return selection-required facts, and
the user may select a discovered candidate or specify another target. Both routes re-read and apply the same repository,
task, generation, branch exclusivity, resource-incarnation and live freshness contract before mutation.

## Ownership And Compatibility

- Fixed Fork `castbox/Trellis@eb370008c7689d4e272ae626bd002190ecbb3296` owns official TaskId/TaskRef/generation and
  common-dir schema-2 session persistence.
- C2 owns package-neutral lifecycle identity and DTO validation.
- C4 owns branch association, establishment and rebind algorithms and depends on C5 only through `OwnershipPort`.
- C5 owns the concrete resource ledger, session adapter, Finish seal input and Cleanup resolution substrate.
- E434 owns complete Skill packages, registry activation, workflow edges and installed/platform projections.

`guru-establish-task-identity` remains a planned stable ID with no package tree. No alias, compatibility reader, second
session store, workspace locator authority, broad fallback or strict branch/path naming policy is introduced.

## Recovery And Evidence Boundary

Ledger mutation owners capture exact prior bytes and expected ledger revision through the concrete C4 port. Failed
composed mutations restore the same snapshot. Conservative active recovery recognizes only its exact whole-ledger
successor. Remote-delivery recording instead recognizes the exact current resource incarnation bound to the same branch,
epoch and revision; unrelated valid ledger rows or later ledger revision increments do not invalidate that local
idempotent result. Both routes rematerialize without rewriting ownership. This recovery is ledger-backed runtime behavior,
not a second transaction store or an unused checkpoint schema. Rebind retires the old resource
incarnation without dropping its responsibility and establishes one current successor. The same portable ref cannot
represent two unresolved incarnations.

Focused evidence must cover context key present/absent, multi-session and A-to-B-to-A switching, generation invalidation,
session write failure, pre-write stale-generation rejection, acquisition ownership projections, rebind retirement, active
missing recovery and output-loss rematerialization, terminal missing manual selection, remote responsibility recovery,
Finish seal inventory, ordinary Cleanup filtering and retained-control-ref exclusion. It must also cover schema/runtime
parity, C4 port compatibility, task validation, Python compilation, line limits and `git diff --check`.

No new ADR is required because `ADR-015` already owns stable lifecycle identity and the framework/extension boundary.
This candidate narrows `ARCH-GAP-011` without closing the full lifecycle gap. Serialized promotion has not run; any
successor diff must re-enter fresh Phase 2, Task Commit and independent complete Branch Review before Publication.
