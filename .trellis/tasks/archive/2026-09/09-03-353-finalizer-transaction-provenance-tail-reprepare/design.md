# #353 技术设计

## Boundary

变更限定在 `guru-finalize-task` 的 current-transaction provenance-tail recovery。保留既有 `ordinary_publication` 与 `existing_pr_recovery` 两种 transaction mode、五个 deterministic transition、六个 public exits，以及 Publication -> Finalizer 的现有 authority 分工。

## Current Failure

现有分类路径把旧 ordinary transaction、当前 publication tail 与 live PR/remote topology 的合法组合过早当作 predecessor rebind。tail 校验使用了不适合旧 transaction 的 parent/changed-path基准，导致正常 tail 在 `provenance_tail_commit_errors()` 或其组合分类后落入 `provenance_tail_transaction_rebind_invalid`。修复应区分“tail 本身非法”和“旧 transaction 只能重新准备 current plan”两种状态，而不是放宽校验。

## Proposed Flow

```text
current live task/publication/branch/PR facts
  -> validate old exact ordinary/push_content transaction
  -> validate one direct-child provenance tail from Git-derived parent
  -> classify pure direct-tail or composed base-evolution topology
  -> if predecessor payload/identity remains exact:
       existing strict-ancestor transaction rebind
     else if only allowed current Publication metadata changed:
       reprepare_required with current Publication authority
     else:
       fail closed
  -> semantic reprepare review/confirmation
  -> write current-plan recovery transaction before mutation
  -> reuse existing push/bind/archive/Ready engine
```

The classifier must keep the existing order that gives bound current-plan transactions and explicit reprepare states precedence over generic fresh adoption. A reprepare result carries only the minimal current-plan handoff already defined by the existing `reprepare_preview`/`reprepare_required` contracts; predecessor transaction details remain owner-private.

## Invariants

- `provenance_tail_commit_errors()` remains the sole tail validity predicate; the current tail must have exactly one direct parent and only allowed manifest bytes/actions.
- Direct-tail and pure base-evolution compatibility behavior remains unchanged. The composed route may compare base-evolution against the validated tail parent, never against an unstripped endpoint.
- Reprepare can replace only an exact same-owner predecessor transaction and only before the first remaining external mutation. It cannot repair a scope, repository, branch, PR, close-set, archive, or business-content mismatch.
- The current Publication Review owns current title/body and reviewed head. Old transaction payload is predecessor evidence, not new authority.
- Existing PR/remote HEAD adoption and metadata convergence remain the existing owners; no second push, PR create, archive, Ready, or Issue mutation is introduced.

## Compatibility And Projections

Prefer package-private runtime helpers and existing schema fields. Update canonical Finalizer runtime/tests and only the contract/spec text directly affected. Run the repository preset apply command to regenerate `.trellis/guru-team`, `.agents`, `.claude`, `.codex`, and `.cursor` projections; never hand-edit installed copies as the only source.

## Test Topology

Use real temporary Git commits for: direct tail, base evolution plus tail, merge or multiple base commits, one invalid extra path, invalid manifest action, wrong parent, chained/multiple tails, business delta, stale PR/remote/head/scope, and interrupted execution. The positive test must assert preview classification, transaction-before-mutation ordering, exact mutation cardinalities, and terminal retry idempotence.

## Rollback

Rollback is the task-owned canonical runtime/spec/test/RDT delta followed by preset reapply and parity checks. Do not roll back or rewrite #333, PR #337, or any unrelated worktree.

## Architecture Impact

Planning hypothesis: `no_architecture_impact`. The change preserves the single Finalizer owner, package-local runtime, existing transaction state machine, public graph, and Merge dependency. Phase 1 must obtain a fresh Architecture `task_impact_sync(stage=planning)` result before approval; any conflict or contract change routes back to planning.
