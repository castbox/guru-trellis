# Phase C Surface Inventory

## 1. Ownership Decision

Phase C uses one fixed Fork prerequisite plus Guru-owned target-native
substrate.

| Surface | Owner | Current Phase C state | Write repository |
| --- | --- | --- | --- |
| Official task/session primitives | `castbox/Trellis` Fork | fixed source already consumed by promoted C2 | `castbox/Trellis` |
| `trellis/skills/guru-team/contracts/task-lifecycle/**` | Guru canonical | C2 promoted; four C3 call-local checkout DTOs are current candidate | `castbox/guru-trellis` |
| `trellis/skills/guru-team/runtime/task_lifecycle/**` | Guru canonical | C2 promoted; C3 checkout modules are current candidate | `castbox/guru-trellis` |
| `guru-ensure-task-checkout` | Guru canonical | C3 reserves the planned stable ID; package directory is deferred to E434 | `castbox/guru-trellis` |
| Other Phase C planned Skill IDs | Guru canonical | C4-C7 activation inputs not started; package directories remain absent | `castbox/guru-trellis` |
| Planned registry metadata and canonical `planned_skill_ids` | Guru canonical | C3 records `guru-ensure-task-checkout` as planned, not active | `castbox/guru-trellis` |
| Active registry selector/workflow/graph/installed/platform bytes | E434 | forbidden in C3 | none in C3 |

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

## 5. C3 Planned Skill Inventory

`guru-ensure-task-checkout` is reserved by one `state=planned` registry row and
canonical `planned_skill_ids` membership. Under the shared registry contract,
that row owns only the future stable consumer id: it has no package,
interface, invoke marker, exit marker, platform destination or canonical
package directory and is never installed.

C3 runtime/schema tests close checkout discovery, validation, selection and
acquisition behavior without presenting a callable public Skill. E434 later
creates the complete semantic package, declares its input profiles/exits/
consumers and activates it atomically with the workflow and projections.

## 6. Remaining Planned Skill Inventory

| Package | Judgment mode | State after C3 | Activation owner |
| --- | --- | --- | --- |
| `guru-create-task` | semantic | C6 not started | E434 |
| `guru-establish-task-identity` | semantic | C5/C6 not started | E434 |
| `guru-establish-task-branch-binding` | semantic | C4/C6 not started | E434 |
| `guru-ensure-task-checkout` | semantic | C3 planned ID only; package absent | E434 |
| `guru-rebind-task-branch` | semantic | C4/C6 not started | E434 |
| `guru-activate-task` | deterministic | C6 not started | E434 |

Planned ID reservation is not package existence or production capability.

## 7. Consumer Boundary

- C4 consumes live Git/checkout facts without persisting checkout paths.
- C5 consumes lifecycle keys and acquisition ownership projections.
- C6 completes shared activation inputs without creating planned package trees.
- D443 consumes lifecycle/session primitives without copying their authority.
- D436 consumes lifecycle, branch, resource and result primitives.
- E434 consumes complete substrate/activation inputs, creates package-ready
  interfaces and exclusively activates workflow, active registry selector,
  active graph and distribution projections.
- #410 retains the complete Release matrix; C3 runs focused validation only.

## 8. C3 Zero-Second-Authority Checks

C3 Phase 2 must prove:

- Guru diff contains no `.trellis/scripts/**` production patch;
- runtime does not copy Fork task/session modules;
- no task/workspace mapping reader or writer appears in new C3 modules;
- no durable checkout locator, topology, HEAD or candidate store is added;
- no branch/session/resource store is implemented early;
- planned ownership metadata names exactly the C3 stable ID, no canonical
  package directory exists for that ID, and the
  active registry selector, `active_skill_ids`, workflow, active graph and
  installed/platform bytes are unchanged;
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
