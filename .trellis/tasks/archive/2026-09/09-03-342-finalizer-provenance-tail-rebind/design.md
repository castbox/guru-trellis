# #342 技术设计：provenance-tail transaction rebind

## 1. Design Boundary

在 Finalizer package 内增加一个位于“generic transaction base-evolution supersession”之前的窄 rebind 分类。
它只接受一个合法 direct-child provenance tail，并把旧 ordinary transaction 一次性转换为 current-plan-bound
strict-ancestor recovery transaction；后续复用现有 recovery engine，不引入新的 public profile、typed exit 或
transaction stage。

```text
rebuilt current plan
  -> read predecessor ordinary/push_content/unbound transaction
  -> exact plan validation fails because reviewed/publication identity advanced
  -> classify legal provenance-only tail continuity
       -> validate task/repo/base/head/scope/gate/archive invariants
       -> validate predecessor publication == live remote/PR HEAD
  -> classify strict-ancestor existing-PR recovery against current plan
  -> build current-plan existing_pr_recovery/push_content candidate
  -> preview exact recovery plan
  -> execute: reread -> persist bound transaction -> push current publication
  -> metadata convergence -> archive -> push_archive -> Ready -> ready_for_merge
```

## 2. Classification Order

Current preview 中 `finalization_validate_transaction_plan()` 的失败分支调整为：

1. 已绑定 `existing_pr_recovery` 且处于 archive 后阶段时，继续执行现有 retired-projection rebind。
2. 对 `ordinary_publication/push_content` 未绑定 transaction，尝试 provenance-tail current-plan rebind preview。
3. rebind 仅在完整 predicate 通过时返回候选；候选必须立即经过现有
   `classify_existing_pr_recovery()` 的 strict-ancestor live PR/HEAD/scope/metadata 校验。
4. 不满足该窄 predicate 的 transaction 才进入现有 base-evolution supersession 或原有 fail-closed 路径。
5. `reprepare_required`、已绑定 transaction 和 terminal/archive recovery 的现有优先级保持不变。

该顺序避免把 `push_content` 纳入原 `verify` supersession 合同，也避免把 provenance-tail rebind 变成任意
plan-drift migration。

## 3. Rebind Predicate And Projection

新增 package-private helper，输入 predecessor transaction、current plan 和 live root/task context，输出仅供当前
preview/executor 使用的 owner-private rebind projection：

- predecessor/current task、repo、base/head branch，以及 current plan remote 的 live repository/PR identity；
- predecessor `branch_review_commit`、`publication_head`；
- current `reviewed_content_head`、`branch_review_commit`、`publication_head`；
- single direct-child provenance-only ancestry validation result；
- unchanged Publication title/body 与 close scope identity；
- exact PR/remote predecessor publication binding；
- rebuilt current bound recovery transaction 与 expected digest。

不将该 projection 加入 public DTO。Preview 的外部可见字段仍使用现有 `existing_pr_recovery` shape。

## 4. Provenance Continuity

连续性只由现有 `provenance_tail_commit_errors()` 判定。设计需证明：

- predecessor reviewed 到 predecessor publication 是空差异或合法 provenance tail；
- predecessor publication 到 current reviewed/publication 必须且仅能包含一个合法 manifest-only direct-child
  provenance tail；
- current local HEAD 与 current reviewed/publication identity 满足现有 Finalizer 约束；
- 任意业务路径、task artifact、非 allowlist manifest 字段、merge commit 或不连续 ancestry 均阻断。

不得新增基于 commit message、文件名计数或“metadata 看起来符合预期”的平行分类器。

## 5. Transaction Mutation Order

执行器消费 checked preview 后：

1. 重新运行 rebind predicate 和 strict-ancestor live PR classifier。
2. 比较当前 rebind/recovery projection 与 preview；任意差异返回 drift。
3. 一次性持久化 current-plan `existing_pr_recovery/push_content` bound transaction，记录唯一 PR、旧 remote
   HEAD、原始 metadata comparison 与 Draft/Ready 状态。
4. 仅在 owner-private transaction 写入完成后推送新的 current publication HEAD，再进入 metadata、archive 或
   Ready mutation。

不得先写一个无外部 consumer 的 rebound ordinary 中间态；必须保持“外部 mutation 前 owner-private authority
已 current”与 idempotent retry 性质。

## 6. Compatibility And Recovery

- 旧 exact-plan #338 equal-HEAD recovery 行为保持不变，本任务不放宽其 equality predicate。
- 无 transaction 的 fresh equal-HEAD PR 仍被拒绝。
- 非 provenance plan drift 继续使用现有 base-evolution/reprepare 或 fail-closed 路径。
- Current transaction schema 3.0 若已有字段足够表达最终 bound recovery，则不升级 schema；若必须新增字段，
  应停止实施并重新评审公共/私有兼容性与 migration。
- Rebind 完成后所有 retry 使用现有 bound transaction；不得再次运行 provenance rebind、重复 current publication
  push 或重复 metadata mutation。

## 7. Test Design

### 7.1 Focused helpers

- 合法单个 provenance tail、predecessor publication 与 reviewed 一致、current publication 与 current reviewed 一致。
- 非 manifest 文件、非法 manifest 字段、业务 commit、断裂 ancestry、task/repo/base/head/scope/plan payload drift。
- predecessor stage/mode/binding/transaction 字段冲突。

### 7.2 Preview and execution fixture

以 #333 / PR #337 去敏拓扑覆盖 Ready/Draft、metadata equal/LF convergence：

- preview 报告 current-plan rebound 后的 strict-ancestor recovery；
- current publication push 调用一次，旧 publication push 和 PR create 调用次数为零；
- owner transaction rebind 在首个外部 mutation 前发生；
- metadata edit 为 0 或 1；archive move/commit/push 各一次；Draft Ready 一次或 Ready 零次；
- terminal retry 不重复任何已完成 mutation。

### 7.3 Negative matrix

覆盖多个 PR、fork、Closed/Merged、HEAD drift、scope drift、metadata preview drift、stale gate/Publication、archive
冲突、不同 PR binding 和 unknown transaction。

### 7.4 Distribution

运行 canonical/installed Finalizer suite、finish-family integration、preset all-platform reapply、package validator、
ownership、dogfood drift、byte parity、recursive sidecar-zero 与 task validation。完整 Release matrix 不执行。

## 8. Docs And Architecture

采用 `delta_first` task-owned RDT contribution；仅在实现确认合同发生变化时更新命中的 durable specs。Planning
Architecture 预期为 `no_architecture_impact`，因为 owner、public graph、transaction stages 和依赖方向均不变。

## 9. Rollback

回滚以本 task 的 canonical Finalizer runtime/tests/contract/RDT delta 为单位，再运行 preset apply 恢复生成副本。
不得只回退 dogfood/platform projection，也不得修改 #333 或 PR #337 的真实状态。
