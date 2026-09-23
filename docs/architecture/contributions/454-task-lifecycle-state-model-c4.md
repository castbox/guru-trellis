# #454 C4 Branch Association Architecture Contribution

## Identity And Review State

- contribution identity: `architecture-contribution-454-task-lifecycle-state-model-c4-v1`.
- lifecycle state: `contribution_candidate`.
- source authority: live Issue #454 and active generation 2 task planning.
- task locator: `.trellis/tasks/09-20-454-task-lifecycle-state-model`.
- related RDT contribution: `docs/requirements-design-test-contributions/454-task-lifecycle-state-model-c4/`.
- predecessor baseline: `current-main-0.6.17-guru.61` / `active`.
- candidate successor: assigned by reviewed promotion.
- design constitution: `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `guru-trellis-architecture-change-contract-v1`.
- change path: `target_native`.

This contribution candidate covers only C4 branch association, establishment and rebind substrate. Serialized promotion
has not run; it does not claim production activation, complete package delivery, shared-current write, Branch Review,
Publication or Release proof.

## Boundary And Decision

C4 adds one repository-local TaskBranchBinding record under Git common-dir. Its durable shape is exactly five fields:
schema version, stable task id, lifecycle generation, monotonically increasing revision and bare portable branch name.
Repository identity comes from common-dir scope. Machine path, checkout topology, HEAD, session, ownership and binding
epoch remain outside the record.

Branch establishment resolves live registered worktrees and local refs against exact task artifact identity. It handles
the four binding/ownership presence combinations while preserving any valid existing side. Missing ownership is rebuilt
conservatively as caller-owned. C4 consumes that behavior through a narrow port; C5 remains the sole owner of the actual
multi-revision resource ledger.

Rebind has only two routes. `same_checkout_new_ref` creates and switches one absent ref in the same checkout while
preserving HEAD, real index bytes and Git-visible working-tree bytes. `existing_target` accepts one already registered,
clean, artifact-matching, ancestor-compatible target checkout and performs no content migration. Divergent histories stop
for explicit reconcile.

## Ownership And Compatibility

- C2 identity/schema primitives remain unchanged; `BranchBindingRefDTO.binding_epoch` is not the durable record.
- C3 live Git checkout facts are reused and extended only with exact mutation snapshots.
- C4 owns TaskBranchBinding, establishment/rebind algorithms and their transaction schemas.
- C5 owns the concrete resource ledger and session adapter; C4 introduces no second store.
- E434 owns canonical package creation, workflow activation, installed copies and platform projections.

The two new Skill IDs remain planned registry identities with no package tree. No alias, dual-read, mapping repair,
durable checkout path or machine handoff expansion is introduced.

## Recovery And Evidence Boundary

Mutation captures exact binding, ownership and checkout pre-state. Failure restores the control snapshots and removes only
the still-matching branch created by the same transaction. Output-loss recovery verifies the exact successor revision and
fresh live target, then rematerializes the result without another mutation. Reusing a ref with an unresolved resource
incarnation is rejected.

Focused evidence must cover schema/runtime parity, revision progression, four recovery quadrants, candidate cardinality,
dirty byte preservation, exact existing target, reconcile stop, rollback, output-loss recovery, reserved refs, planned-ID
package absence, full lifecycle runtime, task validation, JSON/compile checks, line limits and `git diff --check`.

The current candidate evidence passes task-lifecycle runtime `72/72`, planned-ID ownership `3/3`, installed extension
manifest `1/1`, JSON/compile/task/diff/line checks, and confirms that no real generation 2 binding was written. The preset
suite remains `85/86`: raw apply reports the expected pre-E434 installed task-lifecycle README/schema/registry sidecars.
That broader suite is not claimed as passing, and C4 does not synchronize installed or platform projections.

No new ADR is required because `ADR-015` already owns lifecycle identity and the framework/extension boundary. C5-C7,
D443, D436, E434, #434 production graph activation and the complete multi-platform Release matrix remain pending or
unverified. Serialized promotion has not run. Any successor diff it creates must re-enter fresh Phase 2, Task Commit
and independent complete Branch Review.
