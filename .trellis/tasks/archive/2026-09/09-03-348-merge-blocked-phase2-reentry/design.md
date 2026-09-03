# #348 技术设计

## 设计原则

保留 `merge_blocked` 的安全终止语义；仅由 semantic owner 在当前 task scope、PR identity 和 finding 充分绑定后选择 re-entry。脚本只执行确定性读取、校验、恢复和记录，不判断 finding 是否属于 task scope。

## 组件边界

1. `guru-merge-task-pr`：读取当前 Merge gate 结果，区分 task-work finding 与外部 blocker，并输出最小 re-entry handoff 或原有 blocked DTO。
2. 独立 recovery owner/consumer：承接 re-entry，重新读取 live Git/GitHub/Trellis facts，完成 archive-to-active 的事务恢复和 authority 清理。
3. workflow：为 re-entry 增加唯一 Phase 2 target；原 `merge_blocked -> task-pr-merge-blocked` 保持不变。
4. task/archive adapter：封装 canonical archive locator、active locator、状态转换、重复恢复检测和冲突 fail-closed；不暴露手工 `mv` 作为用户操作。
5. runtime mapping/authority invalidation：只写 ignored owner-private mapping；旧 gate、check、review、publication、finalization 状态按 identity 失效并要求 fresh 重跑。
6. preset/projection：同步 canonical package、installed `.trellis/guru-team`、workflow、schemas、platform overlays、README/spec、examples/evals。

## 数据流

`merge gate finding`
-> semantic scope classification
-> `task_work_reentry_required`（最小 DTO）或 `merge_blocked`
-> fresh recovery validation
-> archive task restore + status transition + mapping repair + old-authority invalidation
-> `guru-resume-implementation` / Phase 2 target
-> full downstream rerun

DTO 不包含 machine-local path、用户授权、完整 payload、旧 checkpoint 或 merge authorization。路径由 recovery owner 根据当前 task/archive identity 重新解析。

## Fresh 校验与写入顺序

校验必须覆盖：PR state/base/head/expected head、remote/local branch、Issue scope/closure intent、archive commit、task status/finish summary、runtime mapping 唯一性、worktree tracked/untracked 冲突和 active consumer 占用。

恢复写入按一个 owner transaction 处理：

1. 读取并锁定当前 identity 的恢复事实；
2. 若已恢复且事实完全一致，返回同一成功结果，不重复移动或改写；若存在冲突，零业务写入并 blocked；
3. 恢复 canonical active task locator并更新 `task.json` 为 `in_progress`，移除 `completedAt`；
4. 更新 ignored runtime mapping；
5. 清除旧 authority；
6. 返回唯一 Phase 2 route。

仓库正常协作模型不新增 hostile-input、分布式锁或非常规 crash-consistency 机制；但 stdout 丢失和普通中断必须可由同一 identity fresh recovery 重新判定。

## 兼容性

- 当前 stable graph 保持原 `merge_blocked` terminal route，外部 blocker 不改变行为。
- 新 route 只在完整 task-work finding 证据存在时可达。
- #248/#261 后续 cutover 可替换 owner，但必须继续满足本 Issue 的 acceptance；本实现不等待其落地。
- 已有 `return_to_task_work` 不复用为 Merge recovery route，避免跨 owner 伪造 handback。

## 失败与回滚

任何 identity、scope、head、dirty state 或 active consumer 不一致均在业务写入前 blocked。恢复事务若在正常中断后再次调用，必须通过当前事实判断已完成状态；冲突状态不得覆盖。恢复后的下游失败只重新进入 Phase 2，不回滚到 requirements/planning，也不自动执行 merge。

## 架构影响

这是跨 package、workflow、runtime、schema、preset 和多平台投影的 workflow contract 变更，需在规划阶段调用 `guru-maintain-architecture-baseline:task_impact_sync(stage=planning)`。在该 gate 通过前，不开始实现。
