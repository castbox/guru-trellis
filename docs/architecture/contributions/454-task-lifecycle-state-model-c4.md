# #454 C4 Branch Association Architecture Contribution

## Identity And Review State

- contribution identity: `architecture-contribution-454-task-lifecycle-state-model-c4-v1`.
- lifecycle state: `reviewed_promoted`.
- source authority: live Issue #454 and active generation 2 task planning.
- provenance extension: bounded Finalizer initial-publication recovery guard in the same C4 change scope, mapped to existing `REQ-048` / `DES-046` / `TST-032` authority.
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
promotion covers the C4 branch association, establishment and rebind substrate plus the bounded Finalizer provenance
recovery guard described below. It does not claim production
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

The same C4 provenance boundary includes the Finalizer's initial publication recovery guard. When no predecessor
transaction exists, a remote branch at absent, exact reviewed HEAD or a strict historical ancestor is a valid
pre-mutation baseline; ahead, diverged and unknown/unprovable commits remain fail-closed. The executor creates one
replacement transaction carrying the exact `pre_push_remote_head`, and the subsequent pre-mutation preflight must
re-read and accept that same remote identity before push, PR, archive or Ready mutation. This is a bounded recovery
composition on the existing Finalizer authority, not a second lifecycle ledger or a claim that Finalizer delivery is
complete.

`FIN454-C4-P1-002` extends that same boundary to normal Reactivate branch reuse after a legal provenance tail and
identity-matched `ordinary_publication/push_content` transaction already exist. That transaction is the current owner.
With no Open PR, a terminal PR on the same branch/base is historical fact rather than a current candidate. A live remote
equal to `pre_push_remote_head` admits one fast-forward to `publication_head`; a live remote already equal to
`publication_head` is a valid push-output-loss/converged state for the same transaction. Any remote outside those two
allowed heads, ahead/diverged/unknown topology, Open PR drift or transaction identity drift remains fail-closed. This
adds no broad fallback, manual PR-selection API, force push or second ledger, and never deletes or rewrites the
transaction.

`FIN454-C4-P1-004` keeps that recovery available after same-base finding-fix commits. When the predecessor review-to-
Publication span is equal or one valid provenance tail, the selected base is already in predecessor Publication
lineage, and current Branch Review/Publication/live HEAD are one strictly newer reviewed descendant, the same unbound
transaction can enter the existing reprepare route without requiring incidental base movement. No Open PR or archived
task may exist; terminal PR history is not a current candidate. Remote freshness is proven only by exact equality with
the transaction-owned `pre_push_remote_head` or `publication_head`; intermediate review commits and every other remote
endpoint reject. This is the minimal sufficient binding path: it adds no branch/session/path authority, manual selector,
fallback, force push, second ledger, schema field or public DTO.

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

The provenance recovery regression is an execution-level composition test in
`trellis/skills/guru-team/packages/guru-finalize-task/tests/test_provenance.py`: it builds a real predecessor/reviewed
Git graph, asserts replacement transaction creation with exact `pre_push_remote_head`, re-runs the pre-mutation
preflight against that transaction, and verifies the remote branch remains unchanged. It is supporting evidence for the
existing Finalizer `REQ-048` / `DES-046` / `TST-032` contract and does not replace fresh Phase 2 or Branch Review for the
promotion-created diff.

The `FIN454-C4-P1-002` implementation removes terminal-PR inventory from the exact transaction-owned no-Open-PR path
and keeps the existing transaction identity plus remote allowed-head preflight. Focused recovery `47/47`, complete
Finalizer package `111/111`, Python compile, canonical/dogfood parity, task validation and `git diff --check` pass. These
results support the implementation candidate only; they do not establish fresh Phase 2, Branch Review, Publication,
Finalizer, Delivery or Release results.

The `FIN454-C4-P1-004` regression uses the real old-review -> provenance-tail Publication -> two finding-fix topology.
It proves same-base reprepare accepts both transaction-owned remote endpoints, ignores terminal PR history, rejects an
Open PR and intermediate remote commit, and writes the replacement transaction from the current plan plus observed
remote. Finalizer provenance `23/23`, recovery `48/48`, and the complete package `113/113` pass with Python compile,
task validation, canonical/dogfood parity, dedicated dogfood drift, and `git diff --check`. Raw preset apply remains
blocked by the three disclosed pre-E434 task-lifecycle installed sidecars; this contribution does not convert that
broader boundary or the implementation evidence into a gate pass.

No new ADR is required because `ADR-015` already owns lifecycle identity and the framework/extension boundary. C5-C7,
D443, D436, E434, #434 production graph activation and the complete multi-platform Release matrix remain pending or
unverified. Architecture/RDT owners promoted expected `.61` to successor `.62`; this promotion-created diff must re-enter
fresh Phase 2, Task Commit and independent complete Branch Review before Publication.
