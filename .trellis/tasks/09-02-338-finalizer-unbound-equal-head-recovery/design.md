# #338 技术设计：ordinary transaction 的 equal-HEAD PR 接管

## 1. Design Boundary

本设计在 Finalizer package 内增加一个窄分类分支，不放宽 fresh existing-PR adoption，也不改变普通首次发布
对零未绑定 Open PR 的要求。

```text
rebuilt current plan
  -> read current owner transaction
  -> ordinary/push_content/unbound exact-plan transaction?
       -> resolve unique live PR + remote HEAD
       -> classify equality recovery
       -> preview existing_pr_recovery
       -> execute: atomically rewrite owner transaction binding
  -> existing recovery preflight
  -> optional metadata convergence
  -> archive -> push_archive -> Ready handling -> ready_for_merge
```

## 2. Classification Order

`finalization_existing_pr_recovery_context()` 增加一个位于普通 preflight 之前的 current-transaction 分支：

1. `reprepare_required` 继续拥有最高优先级。
2. 无 transaction 时继续使用 #208 strict-ancestor fresh adoption；equal-HEAD 仍拒绝。
3. current transaction 已是 `existing_pr_recovery` 时继续使用 #251 bound recovery。
4. current transaction 为 `ordinary_publication/push_content` 且未绑定 PR 时，仅在 exact-plan identity
   校验通过后调用 equality classifier。
5. 其它 ordinary stage、已有 binding、identity mismatch 或 unknown state 保持阻断。

该顺序防止 `allow_equal` 成为通用开关。equal-HEAD 资格来自 current ordinary owner transaction，而不是
来自 Open PR 自身。

## 3. Equality Classifier

新增 package-private helper，输入为 current plan、validated ordinary transaction、唯一 live PR 与 remote
HEAD。输出复用 current `existing_pr_recovery` preview shape：

```json
{
  "mode": "existing_pr_recovery",
  "pr": {"number": 337, "url": "https://github.com/castbox/guru-trellis/pull/337"},
  "initial_state": "ready",
  "initial_is_draft": false,
  "pre_push_remote_head": "<publication-head>",
  "publication_head": "<publication-head>",
  "ancestry": "equal",
  "push_required": false,
  "metadata_update_required": true,
  "ready_action": "preserve_ready"
}
```

Helper 复用 current PR identity、close-scope 与 metadata comparison primitive。它必须额外验证 ordinary
transaction 的 plan identity、未绑定状态与 `next_transition=push_content`。

## 4. Transaction Conversion

执行器消费已通过 preview/gate 的 equality recovery 后，调用一个单一 transaction-conversion helper：

- 以 current ordinary transaction 为 preimage；
- 设置 `mode=existing_pr_recovery`；
- 写入 `pr` 与 `adopted_pr`；
- 保留 task/repo/base/branch/review/publication/plan/payload/scope identity；
- `pre_push_remote_head=publication_head`；
- `next_transition=bind_pr`，随后复用 current binding transition 推进到 `archive`；
- 在任何 PR edit、archive 或 Ready mutation 前重新读取并验证 live identity。

Current schema 已承载该形状，因此不迁移 schema。若实现证明 schema validator 无法表达该转换，停止并重新
审查公共兼容合同，不在本 task 静默改变 schema 语义。

## 5. Metadata And Remaining Mutations

绑定后完全复用 #208 的 mutation owner：

1. equality recovery 的 push action 固定为 skip；
2. live title/body 存在字节差异时执行一次 current Publication metadata update；
3. update 后 reread，验证 payload、scope、PR identity 与 HEAD；
4. archive move 与 archive commit/push 各执行一次；
5. initial Ready 使用 `preserve_ready`，initial Draft 使用 `mark_ready`；
6. terminal 验证 local/remote/PR HEAD 与 Ready 状态，输出 `ready_for_merge`。

PR metadata edit 与 close-scope验证必须共用 live reread，防止末尾 LF 收敛误改变 Issue disposition。

## 6. Recovery And Drift

Transaction conversion 完成后，所有 retry 进入现有 bound recovery。每个 transition 依据 transaction 与 live
facts 判断已完成动作，不依据调用次数或旧 preview 推断。

Preview 与 execute 之间的 PR number/URL、Draft state、HEAD、title/body 或 close scope 漂移必须在 conversion
或首个 mutation 前阻断。Conversion 后的漂移沿用 existing recovery reason code 和 current preflight。

## 7. Test Design

### 7.1 Focused contract tests

- current rejection test 保留为“无 transaction 的 fresh equality 仍拒绝”。
- 新增 ordinary/push_content/unbound exact-plan equality preview positive cases。
- 覆盖 Ready/Draft、metadata equal、title drift、末尾 LF body drift。
- 覆盖 ordinary stage mismatch、已有 pr/adopted_pr、transaction identity drift、multiple/fork/scope/head drift。

### 7.2 End-to-end package fixture

以 #333 / PR #337 去敏拓扑运行 preview、gate-compatible execution、transaction conversion、metadata
convergence、archive、push_archive、Ready handling 与 terminal projection。Fake Git/GitHub adapter 记录
push、PR create/edit、archive commit/push 与 Ready mutation 次数。

### 7.3 Installed and projection checks

从 installed wrapper 运行同一 focused fixture；随后执行 canonical-to-installed/platform parity、preset
reapply、ownership、dogfood drift 与 recursive sidecar scan。完整 release matrix不属于本设计。

## 8. Docs SSOT Plan

采用 `delta_first`：Phase 2 先写 task-owned RDT contribution，再更新 Finalizer canonical contract 与直接
命中的 durable workflow specs。Promotion diff 必须重新进入 Phase 2、task commit 和 independent Branch
Review，之后才进入 Publication。

## 9. Architecture Result

Planning impact 为 `no_architecture_impact`。变更保留 Finalizer 单一 owner、package-local runtime、existing
recovery transaction、六个 exits 与 Merge dependency。`minimum-necessary-complexity` 通过窄 predicate 和
schema reuse 落实；没有 architecture contribution 或 ADR。

## 10. Rollback

回滚以本 task 的 canonical package/spec/RDT delta 为单位，再运行 preset apply 恢复 generated copies。
不得仅回退 dogfood/platform副本，不修改 #333 或 PR #337 的真实状态。
