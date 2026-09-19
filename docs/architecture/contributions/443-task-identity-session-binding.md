# #443 Task Identity Session Binding Contribution

## Scope

本 contribution 只定义 task identity-centered session binding capability，作为 #434 全局生命周期切换的前置能力。它不激活 #434，不创建第二 task ledger，不修改上游 Trellis task 状态集合，也不拥有 Completion、Finish、Cleanup 或 Issue closure。

## Authority and ownership

- `task.json`、task artifact locator、live branch/worktree、repository common dir 与 task/workspace mappings 是 task/workspace identity authority。
- `.trellis/scripts/common/active_task.py` 与 `session_storage.py` 是现有 session resolver/store；`guru-bind-task-session` 只在其上增加 lifecycle-aware binding projection，不复制 resolver。
- 新 package 是 session binding/rebind/switch/resume 的唯一 writer/validator。
- #438 保持创建期 attach owner；#436 保持 Reactivate generation、Finish/Cleanup receipt owner；#434 后续消费 public exits 与 route projections。

## Binding contract

每条 ignored binding 绑定：`session_id`、`task_ref`、`task_id`、workspace path、branch、base branch、task HEAD、lifecycle generation、current route 与 freshness timestamp。binding 丢失时，当前 session 必须重新读取并验证完整 identity；任一 task/repository/workspace/branch/base/mapping/session/lifecycle mismatch 均 zero-write stop。

同一合法 binding 重试返回同一 binding identity，不创建第二记录。Reactivate generation 变化时，旧 generation binding 不可用于当前 route；Finish/Cleanup receipt 仍由各自 owner 校验，session binding 不得绕过它们。

## Architecture path

`target_native`。新 package 以 Interface 1.4、独立 schema、typed exits 和 task-local contribution 进入 target boundary。未建立 legacy dual-read/dual-write，也未改变当前 workflow graph。实现完成后需通过 Phase 2、完整 Branch Review 与后续 #434 promotion/cutover owner 的独立审核。

## Validation boundary

本 contribution 的最小验证包括 package contract/runtime、A→B→A、跨 session rebind、Reactivate generation invalidation、mismatch zero-write、canonical/installed/platform projection、ownership 与 dogfood drift。完整 Release matrix、#434 production graph activation 和生产业务操作不属于本 contribution。
