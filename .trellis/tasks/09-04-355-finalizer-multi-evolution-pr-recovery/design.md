# #355 技术设计

## Boundary

变更限定在 canonical `guru-finalize-task` runtime 的旧
`ordinary_publication/push_content` transaction 恢复分类、current-plan
reprepare/rebind 以及对应测试。保留现有两种 transaction mode、五个 transition、
六个 Finalizer exits 和 Publication -> Finalizer -> Merge 的 owner 边界。

## Failure Model

当前 `classify_provenance_tail_transaction_rebind()` 把 transaction 的旧
Publication HEAD、当前 Publication HEAD 和合法演进链一起判断。当旧 HEAD 之后
存在 base merge/task commit，再追加一个合法 provenance tail 时，直接以当前
Publication HEAD 作为 tail 端点会把合法 direct-parent 关系与 base/task 演进混在
一起，产生 `provenance_tail_parent_mismatch`，随后错误地进入
`provenance_tail_transaction_rebind_invalid`。

## Proposed Flow

```text
live task/publication/PR/remote facts
  -> validate exact old ordinary/push_content transaction
  -> identify current HEAD and its Git-derived direct parent
  -> validate one provenance tail against that direct parent
  -> compare predecessor -> tail-parent as the existing base-evolution delta
  -> classify strict-ancestor existing-PR recovery or current-plan reprepare
  -> persist bound current transaction before first remaining mutation
  -> reuse existing push/bind/archive/Ready engine
```

The composed topology is the only new route: one validated tail may follow a legal
base-evolution/task-content chain. Direct-tail and pure base-evolution routes retain
their current predicates. The implementation must not introduce a general multi-tail
walker or treat arbitrary business commits as provenance.

## Invariants

- `provenance_tail_commit_errors()` remains the sole provenance-tail validity predicate.
- The tail has exactly one Git-derived parent and only the existing manifest/path/action
  allowlist; any extra business delta or second tail remains blocked.
- Old transaction fields other than the explicitly supported HEAD evolution remain exact:
  task, repository, base, branch, close scope, publication lineage, PR/remote identity,
  and archive state.
- Current Publication title/body and reviewed head remain current owner authority; old
  transaction payload is predecessor evidence only.
- Rebind/reprepare persists before push, PR edit/create, archive, archive push or Ready;
  recovery retries never repeat an already successful mutation.
- No public schema, DTO, typed exit, transaction mode or external Issue/PR state changes.

## Compatibility And Projections

Implement in canonical `trellis/skills/guru-team/packages/guru-finalize-task` first.
Update only directly affected contract/spec text and tests, then run
`trellis/presets/guru-team/scripts/bash/apply.sh --repo .` from the task worktree to
regenerate `.trellis/guru-team`, `.agents`, `.claude`, `.codex` and `.cursor` projections.
Do not hand-edit installed copies as the only source.

## Architecture Impact

Planning hypothesis: `no_architecture_impact`. The change keeps the existing Finalizer
owner, package-local runtime, transaction state machine and Merge consumer. Phase 1 must
still obtain the current Architecture planning impact result; a contract or owner-boundary
change routes back to planning.

## Test Topology

Use real temporary Git histories for:

- predecessor Publication plus one direct tail;
- predecessor plus base evolution/task commits plus one direct tail;
- merge/multiple-base commits accepted only when the exact binary delta is legal;
- invalid parent, extra path, invalid manifest action, multi-tail and business delta;
- PR/remote/scope/title/body/archive drift;
- interruption after transaction persistence and same-plan retry.

Positive assertions must cover preview classification, transaction-before-mutation order,
exact mutation cardinality and terminal retry idempotence. Negative assertions must verify
zero external mutation before fail-closed output.

## Rollback

Rollback is limited to the task-owned canonical runtime/test/spec delta and regenerated
projections. Never revert or rewrite #342, #344, #347, #350, #353, #333 or PR #337.
