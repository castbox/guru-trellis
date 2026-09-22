# Phase C Surface Inventory

## 1. Ownership Decision

Phase C uses one fixed Fork prerequisite plus Guru-owned target-native
substrate.

| Surface | Owner | Current Phase C state | Write repository |
| --- | --- | --- | --- |
| Official task/session primitives | `castbox/Trellis` Fork | fixed source already consumed by promoted C2 | `castbox/Trellis` |
| `trellis/skills/guru-team/contracts/task-lifecycle/**` | Guru canonical | C2 promoted; four C3 call-local checkout DTOs are current candidate | `castbox/guru-trellis` |
| `trellis/skills/guru-team/runtime/task_lifecycle/**` | Guru canonical | C2 promoted; C3 checkout modules are current candidate | `castbox/guru-trellis` |
| `guru-ensure-task-checkout` | Guru canonical | C3 package-ready candidate, production inactive | `castbox/guru-trellis` |
| Other Phase C packages | Guru canonical | C4-C7 not started | `castbox/guru-trellis` |
| Registry/workflow/manifest/installed/platform bytes | E434 | forbidden in C3 | none in C3 |

Guru ownership does not include `.trellis/scripts/**`. No overlay, installer
post-patch, copied Fork module or alternate task/session store may bypass that
boundary.

## 2. Fixed Fork Prerequisite

Current fixed source:
`castbox/Trellis@eb370008c7689d4e272ae626bd002190ecbb3296`.

The Fork owns immutable TaskId, lifecycle generation, TaskId-to-TaskRef
resolution and path-free session primitives. It does not own Guru branch
association, checkout acquisition, resource ownership, semantic package gates
or production workflow activation.

## 3. Guru Runtime Inventory

| Module | Responsibility | C3 state | Forbidden responsibility |
| --- | --- | --- | --- |
| `identity.py` | TaskId/TaskRef/TaskLifecycleKey validation and resolution adapter | promoted C2 | session, branch, checkout or ledger mutation |
| `source.py` | issue/no-Issue source and delivery target normalization | promoted C2 | Closure disposition |
| `results.py` | result/transaction reference primitives | promoted C2 | package semantic decisions |
| `git_facts.py` | common-dir, ref and registered-worktree live facts | C3 candidate | durable checkout authority |
| `checkout_resolution.py` | candidate validation, classification and fresh selection | C3 candidate | candidate persistence or branch binding |
| `checkout_acquisition.py` | adopt/provision transaction, rollback and recovery | C3 candidate | session, branch or ledger authority |
| `branch_store.py` | current branch association | C4 not started | checkout path, HEAD or ownership |
| `branch_resolution.py` | establishment and four-state recovery | C4 not started | checkout persistence |
| `rebind.py` | two-route branch mutation | C4 not started | stash, merge, rebase, cherry-pick, reset or force push |
| `session_adapter.py` | Fork session DTO adapter | C5 not started | alternate session store |
| `resource_ledger.py` | resource ownership and responsibility state | C5 not started | Cleanup semantic judgment |

Each touched non-generated module must remain below 3000 lines. C3 must not
introduce a general `common.py` store or another durable identity index.

## 4. C3 Shared DTO Inventory

The catalog adds exactly four call-local DTOs:

- `CheckoutAcquisitionPlanDTO`
- `CheckoutCandidateDTO`
- `CheckoutResolutionDTO`
- `CheckoutSelectionDTO`

Machine paths, current HEADs and timestamps are valid only in these call-local
DTOs. Durable `TaskArtifactDTO`, `TaskLifecycleDTO`, `BranchBindingRefDTO` and
result/reference DTOs remain path-free and do not inherit those fields.

## 5. C3 Package Inventory

`guru-ensure-task-checkout` is a semantic canonical package with:

- input profiles: `ensure_checkout`, `resume_checkout_acquisition`;
- exits: `checkout_ready`, `resume_checkout_acquisition`, `blocked`;
- consumers: `guru-task-checkout-ready-router`, same-Skill recovery, and
  `task-checkout-acquisition-blocked`;
- package-owned schemas, examples, error catalog, wrapper and focused tests;
- no registration, active manifest entry, workflow edge or installed/platform
  projection.

Zero or multiple candidates stay inside the semantic owner for reviewed
selection/acquisition. They do not create a durable candidate artifact or an
additional public authority. The wrapper projects only the final minimal exit.

## 6. Remaining Package Inventory

| Package | Judgment mode | State after C3 | Activation owner |
| --- | --- | --- | --- |
| `guru-create-task` | semantic | C6 not started | E434 |
| `guru-establish-task-identity` | semantic | C5/C6 not started | E434 |
| `guru-establish-task-branch-binding` | semantic | C4/C6 not started | E434 |
| `guru-ensure-task-checkout` | semantic | C3 candidate inactive | E434 |
| `guru-rebind-task-branch` | semantic | C4/C6 not started | E434 |
| `guru-activate-task` | deterministic | C6 not started | E434 |

Package existence is not production capability.

## 7. Consumer Boundary

- C4 consumes live Git/checkout facts without persisting checkout paths.
- C5 consumes lifecycle keys and acquisition ownership projections.
- C6 composes package contracts without changing active selectors.
- D443 consumes lifecycle/session primitives without copying their authority.
- D436 consumes lifecycle, branch, resource and result primitives.
- E434 consumes complete package-ready interfaces and exclusively activates
  workflow, registry, manifest and distribution projections.
- #410 retains the complete Release matrix; C3 runs focused validation only.

## 8. C3 Zero-Second-Authority Checks

C3 Phase 2 must prove:

- Guru diff contains no `.trellis/scripts/**` production patch;
- runtime does not copy Fork task/session modules;
- no task/workspace mapping reader or writer appears in new C3 modules;
- no durable checkout locator, topology, HEAD or candidate store is added;
- no branch/session/resource store is implemented early;
- active registry, workflow, manifest and installed/platform bytes are
  unchanged;
- adoption and provisioning use the same live validation boundary;
- caller-owned resources are preserved and rollback only removes exact
  transaction-created resources;
- output-loss recovery performs no second mutation.

## 9. Current Task Resume

This inventory describes the C3 candidate, not bootstrap authority. The active
task continues to use current production owners. A fresh Phase 2 Architecture
result must bind this inventory, the C3 change contract, live Issue #454,
current `.59` authority and the complete worktree candidate before
`guru-check-task` may run.
