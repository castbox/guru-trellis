# Design: canonical 与 dogfood 投影漂移修复

## 1. 设计原则

canonical source 是唯一长期写入权威，dogfood 与平台目录是 preset installer
生成的投影。本任务不得直接把 installed copy 作为新的并行 authority，也不得
修改 installer 规则来掩盖 source 漏同步。

该修复符合 `cohesion-change-isolation` 与 `minimum-necessary-complexity`：只补回
已在 #325/#327 审核合并的内容，并通过既有 conflict-preservation 合同解决一处
历史投影漂移，不新增行为、兼容层、schema 或迁移机制。

## 2. 修改边界

### 2.1 Canonical spec

从当前 dogfood spec 提取 #325 引入的最小 Finalizer provenance 合同差异，写入：

`trellis/presets/guru-team/spec/workflow/data-contracts.md`

只同步下列既有语义：

- Finalizer producer 读取 canonical bytes，但不调用完整 preset installer；
- target installed manifest 的唯一合法变化是最小 provenance 更新；
- immutable installed source 已满足绑定时无需 metadata tail；
- reprepare 与 recorded-tail 文案和已合并行为保持一致。

### 2.2 Canonical package test 与 installed conflict

当前 canonical 文件：

`trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py`

已经是目标 authority：它包含 #325 的 immutable provenance 与 manifest inventory
preservation 断言，也包含 #327 的 workspace-boundary fail-closed 回归。该文件不做
手工修改。

首次 apply 发现 installed test 不等于 manifest previous hash，也不等于 canonical，
因此产生 `.new` 并返回 conflict。三方历史证明 installed bytes 精确来自 PR #326
当时的不完整 dogfood 投影，而 `.new` 与当前 canonical 字节一致。受控恢复只允许：

1. 审核 installed 与 `.new` 的完整 diff；
2. 确认 installed-only 内容没有新语义，差异仅为缺失断言、缺失 #327 回归和旧格式；
3. 用已审核 `.new` 精确替换该 installed test，并删除这一处 `.new`；
4. 立即重跑 canonical apply，由 installer 重建 current manifest provenance。

任何其它 `.new`、未知 edit 或额外路径仍然阻塞，不复用这一结论。

## 3. 投影流程

1. 只修改 canonical preset spec；canonical package test 保持不变。
2. 对 canonical、installed、manifest previous hash 与首次 `.new` 做三方历史核对。
3. 显式解决已审核的单一 installed test conflict，不覆盖其它未知 edit。
4. 执行 all-platform preset apply，将 canonical 内容生成到 dogfood、installed、
   Shared、Codex、Cursor、Claude roots。
5. 删除由受控 known managed upgrade 产生且已审核的 `.bak` 后重新 apply；任何新
   `.new` 或未知冲突均立即阻塞，不静默覆盖。
6. 第二次 apply 验证幂等性，并运行 dogfood drift、ownership、source/installed 与
   platform parity 检查。

## 4. Architecture Impact

结论：`no_architecture_impact`。

- 不改变 Architecture Baseline、design constitution、domain ownership 或
  project change contract。
- 不改变 runtime data flow、public contract、stable id、schema、workflow route
  或 owner。
- 仅恢复 canonical 与派生投影的既有一致性，不创建 Architecture contribution
  或 ADR。

## 5. 兼容性与回滚

- 兼容性：恢复的是当前 `main` 已生效语义，合法结果是 canonical 与 installed
  收敛，不产生消费者可见行为变化。
- 失败行为：只有上述单一、已完成三方核对的 historical projection conflict 可
  显式解决；其它 ownership、manifest provenance、unknown edit 或 sidecar 检查
  失败时停止，不继续验证或扩大修改。
- 回滚点：实现提交前可按本 task 精确文件集合撤销；不得操作 #333 worktree。
- Release/部署：不适用。

## 6. 关键取舍

不直接编辑所有 installed/platform copies，因为这会继续保留多写者和未来
reapply 回退风险。使用 canonical-first 加正式 preset apply，才能同时修复当前
字节和后续更新路径。
