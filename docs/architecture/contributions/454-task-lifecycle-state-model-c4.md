# #454 C4 Branch Association Architecture Contribution

## Identity And Review State

- contribution identity: `architecture-contribution-454-task-lifecycle-state-model-c4-v1`.
- lifecycle state: `reviewed_promoted`.
- source authority: live Issue #454 and active generation 2 task planning.
- task locator: `.trellis/tasks/09-20-454-task-lifecycle-state-model`.
- related RDT contribution: `docs/requirements-design-test-contributions/454-task-lifecycle-state-model-c4/`.
- predecessor baseline: `current-main-0.6.17-guru.61` / `active`.
- promoted successor: `current-main-0.6.17-guru.62` / `active`.
- reviewed range: `origin/main@77fa1a2250998ad8c71f0fffedf9a99a15a76dec...c7fab600e6e29385c23c276ac2b1828d0465fd77`.
- design constitution: `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `guru-trellis-architecture-change-contract-v1`.
- change path: `target_native`.

Independent complete Branch Review reported P0/P1/P2/P3 `0/0/0/0`. At admission,
`BR454-C4-P3-001` was a reproducible `qualified_finding` at
`6ab9dde1385c03f406ef3663e61dd010533462b7`; it was closed by
`c7fab600e6e29385c23c276ac2b1828d0465fd77`. Post-fix qualification against the current supported path returned
normal-scenario `classified / rejected_not_reproduced` and solution-mechanism `classified / qualified_current`. This
promotion covers only C4 branch association, establishment and rebind substrate. It does not claim production
activation, complete package delivery, promotion-created Branch Review, Publication or Release proof.

## Boundary And Decision

C4 adds one repository-local TaskBranchBinding record under Git common-dir. Its durable shape is exactly six fields:
schema version, stable task id, lifecycle generation, binding epoch, epoch-local monotonically increasing revision and
bare portable branch name. `binding_epoch` is an opaque repository-local application control identity. It is not TaskId,
lifecycle generation, session identity or cross-repository authority, but it is part of the association and must match
the current ownership set and same-owner transaction/recovery state. Machine path, checkout topology, HEAD, session and
ownership payload remain outside the record.

Branch establishment resolves live registered worktrees and local refs against exact task artifact identity. It handles
the four binding/ownership presence combinations while preserving any valid existing side. If either association or
current ownership survives, the missing side reuses that side's epoch, revision and branch. Only complete loss of both
control states creates a new epoch at revision 0; pre-existing resources are then rebuilt conservatively as caller-owned.
C4 consumes that behavior through a narrow port; C5 remains the sole owner of the actual multi-revision resource ledger.

Rebind has only two routes and preserves the current binding epoch while advancing revision once. `same_checkout_new_ref`
creates and switches one absent ref in the same checkout while preserving HEAD, real index bytes and Git-visible
working-tree bytes. `existing_target` accepts one already registered, clean, artifact-matching, ancestor-compatible target
checkout and performs no content migration. Divergent histories stop for explicit reconcile.

Candidate labels are call-local selection/display identities, not freshness tokens. Discovery excludes retained
`refs/heads/guru-task-lifecycle/*` machine-handoff control refs. Every mutation and lost-output recovery binds a reviewed
expected HEAD and fresh rereads that HEAD together with task artifact, epoch, revision, branch and ownership; branch name,
candidate label or candidate ordering cannot substitute for that freshness check.

## Ownership And Compatibility

- C2 identity/schema primitives remain unchanged; durable TaskBranchBinding and `BranchBindingRefDTO` project the same
  epoch/revision identity while the DTO still omits branch/path/HEAD details.
- C3 live Git checkout facts are reused and extended only with exact mutation snapshots.
- C4 owns TaskBranchBinding, establishment/rebind algorithms and their epoch/expected-HEAD transaction schemas.
- C5 owns the concrete resource ledger and session adapter; C4 introduces no second store.
- E434 owns canonical package creation, workflow activation, installed copies and platform projections.

The two new Skill IDs remain planned registry identities with no package tree. No alias, dual-read, mapping repair,
durable checkout path or machine handoff expansion is introduced.

## Recovery And Evidence Boundary

Mutation captures exact epoch-bearing binding, ownership and checkout pre-state plus reviewed expected source/target HEAD.
Failure restores the control snapshots and removes only the still-matching branch created by the same transaction.
Rollback eligibility begins before `git switch -c` because a failing `post-checkout` hook can return non-zero after Git
has already created and checked out the target ref; rollback accepts that same hook failure only when fresh Git state
proves the source branch was restored. The short-lived transaction stores the source binding as the sole epoch authority
and stores only the target revision separately, so it cannot encode contradictory source and target epochs.
Output-loss recovery verifies the same epoch, exact successor revision and expected live HEAD, then rematerializes the
result without another mutation. Reusing a ref with an unresolved resource incarnation is rejected.

Focused evidence must cover schema/runtime parity, epoch/revision progression, four recovery quadrants, complete-control-
loss new epoch, rebind epoch preservation, candidate cardinality, candidate-label/expected-HEAD separation, mutation and
recovery HEAD drift, retained control-ref exclusion, dirty byte preservation, exact existing target, reconcile stop,
rollback, output-loss recovery, planned-ID package absence, full lifecycle runtime, task validation, JSON/compile checks,
line limits and `git diff --check`. Epoch continuity/new-epoch, HEAD freshness and control-ref filtering require distinct
regression cases rather than being inferred from aggregate suite counts.

Fresh finding-fix targeted evidence passes task-lifecycle runtime `93/93`, Python compile, task validation,
`git diff --check` and per-file line checks; task validation reported the optional `implement.jsonl` and `check.jsonl` as
absent/skipped. The real generation 2 common-dir binding remains absent, so the tests did not mutate live task control
state. The pre-finding-fix preset suite was `85/86`: raw apply reported the expected pre-E434 installed task-lifecycle
README/schema/registry sidecars. That broader suite was not passing, was not rerun as part of this narrow finding-fix, and
C4 does not synchronize installed or platform projections.

No new ADR is required because `ADR-015` already owns lifecycle identity and the framework/extension boundary. C5-C7,
D443, D436, E434, #434 production graph activation and the complete multi-platform Release matrix remain pending or
unverified. Architecture/RDT owners promoted expected `.61` to successor `.62`; this promotion-created diff must re-enter
fresh Phase 2, Task Commit and independent complete Branch Review before Publication.
