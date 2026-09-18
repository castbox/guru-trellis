# #436 Post-Delivery Completion And Finish Architecture contribution

## Identity And Authority Boundary

- candidate identity: `architecture-contribution-436-post-delivery-completion-finish-v1`.
- lifecycle state: `reviewed_candidate`; not promoted to shared current.
- source authority: Issue #436 contract `2026-09-18-r3`.
- task locator: `.trellis/tasks/09-19-436-post-delivery-completion-finish`.
- related RDT contribution: `docs/requirements-design-test-contributions/436-post-delivery-completion-finish/`.
- source/expected baseline: `docs/architecture/README.md` / `current-main-0.6.17-guru.55` / `active`.
- design constitution: `docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `docs/architecture/06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1`.
- change path: `target_native`.
- decision candidate: Completion, Closure, Finish, Cleanup and Reactivate remain five independent semantic owners, while #434 alone activates their production edges.

This contribution is task-owned. It does not update CURRENT, close `ARCH-GAP-009`, create a second production graph or claim Release evidence. Promotion requires an independent committed full-diff review and expected-current-bound Architecture owner action.

## Before And Target

Before: `.55` provides repeated active-task Delivery and identifies #436 as the successor owner, but production still terminates through Publication/Finalizer/Merge. There is no package-level Completion aggregation, exact Issue-close transaction, lifecycle-only bookkeeping PR, current-Finish-bound Cleanup or normal archived-task Reactivate.

Target: five additive packages provide those responsibilities with closed public inputs/outputs and owner-private recovery state. Delivery success remains non-terminal. Completion alone decides whether the accepted task scope is complete; Closure alone decides and executes exact Issue disposition; Finish alone persists the archive through a lifecycle-only bookkeeping PR and verifies the remote target; Cleanup consumes only the current Finish receipt; Reactivate preserves the original task identity and invalidates prior Finish receipts. The production graph remains unchanged until #434 atomically activates it.

## Ownership And Single Writers

- `guru-review-task-completion` owns fresh aggregation of accepted scope, all Delivery facts, remaining work and evidence.
- `guru-complete-task-closure` owns no-mutation disposition or one exact confirmed Issue-close transaction.
- `guru-finish-task` owns local archive projection, bookkeeping publication and expected-head merge as three separately confirmed stages.
- `guru-cleanup-task-resources` owns exact current-cycle branch, worktree and ignored-runtime deletion after Finish success.
- `guru-reactivate-task` owns normal completed-task archive-to-active recovery and explicit return routing.
- #435 continues to own Delivery Review/Publish/Merge; #434 alone owns graph activation and old-edge retirement.
- Architecture and RDT shared current retain their serialized promotion single writers.

## Required Concerns

| Concern | Applicability | Candidate contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | Bind Architecture 2.0, current `.55`, Issue #436 r3, task planning and project change contract v1. |
| `constitution-binding` | `applicable` | Bind semantic completeness, cohesion/change isolation, minimum necessary complexity and one-way convergence by identity. |
| `boundary-and-decision` | `applicable` | Select `target_native`; separate Completion, Closure, Finish, Cleanup and Reactivate without shifting Delivery or #434 ownership. |
| `owner-and-single-writer` | `applicable` | Each semantic judgment and mutation has one owner; only Finish writes terminal bookkeeping and only Reactivate restores a normally completed task. |
| `compatibility-and-exit` | `applicable` | Add deferred packages with no adapter or active dual graph; #434 performs the only cutover and retirement. |
| `gap-and-deviation` | `applicable` | Provide the #436 capability needed to close the lifecycle portion of `ARCH-GAP-009`; do not claim the gap closed before #434 activation. |
| `parallel-scope` | `applicable` | #436 writes isolated packages, projections, lifecycle SSOT and task contributions; it does not edit #434 task state or shared current before promotion. |
| `evidence-and-freshness` | `applicable` | Bind package tests, transaction recovery, exact allowlists, projection parity, preset reapply, production graph counts and the current worktree candidate. |
| `review-and-promotion` | `applicable` | Independent committed review precedes expected-`.55` promotion; any promotion-created diff re-enters Phase 2, Task Commit and Branch Review. |

## Identity, Persistence And Recovery Decision

Task, Issue, workspace, Delivery and terminal identities remain separate. Public outputs carry only the minimal reference needed by the unique consumer. Recovery state is ignored, owner-private and closed to the same transaction identity. Completion cannot be inferred from merge, deployment, tests, Issue state or archive presence. Closure authorization remains dialogue-local. Finish success is based on the remote target containing one final archive and no active copy, not on a local move or PR creation. Reactivate preserves the stable task identity while allowing a new branch/worktree from the current base, and deletes prior Finish receipts before the restored task can continue.

The design deliberately excludes a Delivery ledger, old-output adapter, dual runtime graph, shared recovery framework, automatic exceptional Finish repair and hostile-input/concurrency hardening. These have no accepted direct consumer in #436.

## Project Check And Promotion

- descriptor identity: `guru-trellis-architecture-convergence:repository:1`.
- check identity/version: `guru-trellis-architecture-convergence@1`.
- refs: `ARCH-GOV-006..011`, `ADR-005`, `ADR-009`, `ADR-012`, `ARCH-GAP-009`.
- before: `.55` contains 26 packages / 114 exits / 96 commands and a 22-invoke / 98-exit production graph, with #436 capability absent.
- after candidate: canonical and managed projections contain 31 packages / 101 commands; the production graph remains 22 invokes / 98 exits. Five deferred lifecycle owners, closed schemas, package tests, transaction recovery and lifecycle SSOT are present.
- current result: targeted package, registry, installed/projection, preset recovery, task and drift checks pass. The existing Finish-family suite retains three base failures unrelated to #436: an old expected-exit set and two existing Finalizer eval-schema mismatches.
- promotion state: `reviewed_candidate`; shared current remains `current-main-0.6.17-guru.55`.
- expected current identity: `current-main-0.6.17-guru.55`.
- ADR: required at promotion because this task establishes terminal lifecycle owner topology, transaction persistence, Issue-close ownership and normal Reactivate semantics.

## Review Boundary

Phase 2 reviews the complete dirty worktree and the current project check. Independent Branch Review must recompute this contribution from the committed `origin/main...HEAD` range. Promotion and #434 activation are separate later mutations. Full multi-platform Release validation remains unverified and outside this ordinary feature task.
