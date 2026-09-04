# #358 技术设计：fresh reviewed descendant transaction rebind

## 1. Boundary

变更限定在 canonical `guru-finalize-task` package 的 predecessor transaction 恢复分类与
对应合同/测试。保留 `ordinary_publication|existing_pr_recovery`、五个 deterministic
transition、六个 public exits、Publication -> Finalizer -> Merge owner 边界和 transaction
schema 3.0。

## 2. Failure Model

当前分类顺序将 predecessor Publication 到 current Publication 的整段演进先当作单一
provenance tail 校验。若 current Publication HEAD 本身是 fresh reviewed task-content commit：

```text
predecessor publication
  -> remote / existing PR head
  -> fresh reviewed task-content head == current publication head
```

整段 changed paths 不可能满足 manifest-only tail；而 reviewed-base-descendant predicate 又只
能从“current HEAD 是 provenance tail，comparison head 是其 parent”的组合路径进入，因此
合法 reviewed descendant 被提前拒绝。

## 3. Proposed Flow

```text
current Finalizer plan + predecessor ordinary/push_content/unbound transaction
  -> run existing exact non-HEAD/task/scope/archive checks
  -> try existing direct-tail / pure-base / base-plus-tail classifications
  -> when errors are only provenance-shape inapplicability:
       classify current reviewed publication head directly
       require branch_review_commit == publication_head
       require predecessor publication and selected base ancestry
       require current fresh Publication/reviewed identity already passed
  -> resolve unique Open PR and exact remote head
  -> reuse classify_existing_pr_recovery(strict_ancestor)
  -> preview existing recovery shape
  -> execute rechecks same projection
  -> persist current-plan existing_pr_recovery/push_content transaction
  -> push once -> metadata convergence -> archive -> push_archive -> Ready
```

## 4. Narrow Predicate

新增或扩展 package-private helper，使
`provenance_tail_transaction_rebind_is_reviewed_base_descendant()` 可直接消费 current
reviewed/Publication HEAD，而不要求一个额外 tail parent。predicate 必须证明：

- predecessor/current commit OID 均合法；
- `branch_review_commit == publication_head == comparison_head`；
- predecessor Publication HEAD 是 comparison HEAD 的祖先；
- current selected base HEAD 是 comparison HEAD 的祖先，但不是 predecessor Publication
  HEAD 的祖先；
- predecessor Publication 与 current reviewed HEAD 必须不同；
- 其它 task/repo/base/head/scope/archive identity 仍由现有 rebind errors 和 existing-PR
  classifier 校验。

该 predicate 不自行判断 changed paths 是否“像业务内容”或是否命中 task 目录；fresh reviewed identity 来自 current
Phase 2、Task Commit、Branch Review 和 Publication authority。任意未审 HEAD 漂移会使这些 current
identity 或 transaction/plan 校验失效，而不是通过新 helper 获得认可。

## 5. Classification Order

1. 保留 exact current transaction、post-bind 和 terminal recovery 的现有优先级。
2. 保留 direct-tail、pure base evolution、base evolution plus tail 的现有判定。
3. 仅当 error set 限定在 provenance-shape inapplicability 与受控的 current reviewed/publication
   identity差异时，尝试 direct reviewed-descendant predicate。
4. predicate 通过后，remote/PR HEAD 还必须位于 predecessor Publication 到 current
   Publication 的祖先链上，再调用 `classify_existing_pr_recovery()`；scope/metadata 不由新 helper
   重复实现。
5. predicate 不通过时维持当前 `provenance_tail_transaction_rebind_invalid` fail-closed。

## 6. Transaction And Retry

preview 只返回既有 `existing_pr_recovery` shape。execute 重新计算同一 predicate 和 live PR/
remote comparison，与 preview 完全一致后，复用现有 transaction conversion/build path，在首个
外部 mutation 前写入 current-plan `existing_pr_recovery/push_content`。后续阶段与 retry 继续由
现有 transaction engine 拥有，不新增中间 transaction 或恢复 artifact。

## 7. Tests

### 7.1 Focused real-Git classifier

- predecessor publication -> base evolution -> reviewed task commit，current
  `branch_review_commit == publication_head`，无额外 tail：通过。
- predecessor publication -> current reviewed commit，selected base 未演进：阻断。
- current Publication 与 Branch Review HEAD 不同：阻断。
- predecessor/current 或 selected-base ancestry 不满足：阻断。
- task/repo/base/head/scope/archive/Publication payload drift：阻断。

### 7.2 Preview and execution

以 #333 / PR #337 去敏拓扑覆盖 Ready/Draft 与 metadata equal/convergence：

- preview 进入 strict-ancestor recovery；
- transaction write 先于 push/PR edit/archive/Ready；
- current push 一次、PR create 零次、metadata edit 0/1、Ready 0/1；
- terminal retry 对所有已完成 mutation 为零重复。

### 7.3 Compatibility

继续运行 direct-tail、pure base-evolution、base-evolution-plus-tail、invalid tail/path/manifest/
business/multi-tail、equal-HEAD、post-bind 和 terminal recovery 既有测试。

## 8. Projection And Docs

canonical runtime/tests/contract/spec 先修改；随后运行
`trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms` 同步 dogfood installed、
Shared/Codex/Claude/Cursor。不得把 installed 副本当作唯一源头，不修改官方 Trellis 上游源码、
全局 npm 包、`node_modules` 或 hook 来分叉流程。

## 9. Rollback

回滚本 task 的 canonical runtime/test/contract/RDT delta，并重新执行 preset apply 恢复投影一致。
不得回滚 #342/#353/#355，也不得修改 #333 或 PR #337 live state。
