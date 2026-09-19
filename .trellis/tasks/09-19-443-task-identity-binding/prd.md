# #443 Task identity-centered multi-session binding

## Goal

为 Guru Team 建立以稳定 task identity 为核心的短期 session binding 能力，使同一 task 可以跨 session 继续执行，也允许同一 session 在 task A 与 task B 之间受控切换并准确返回，同时支持 binding 丢失后的 fresh rebind。该能力作为 #434 全局生命周期切换的前置 capability，但不激活 #434。

## Requirements

1. **稳定身份**：task identity 是唯一长期主身份；Issue、规划、Delivery、archive、Reactivate、Finish/Closure 历史均归属于它。session、branch、worktree 是可更换承载资源。
2. **短期 binding**：一个 task 可先后绑定多个 session；一个 session 可按明确 current route 承接多个 task。binding 只存在 ignored runtime/private 状态，携带 task/session/repository/workspace/branch/base/lifecycle freshness，不进入 task artifact、public DTO、Issue ledger 或授权记录。
3. **受控 rebind**：binding 丢失时，必须 fresh 校验 task metadata、repository common dir、task/workspace mapping、branch/worktree/HEAD/base、task 阶段、lifecycle generation 与当前 session identity；任一不一致均 fail closed。合法重试幂等且不重复创建或迁移资源。
4. **受控切换与返回**：A→B→A 每个 task 保留独立 identity、Issue、workspace、branch、route 和历史；B 的旧 pass、Finish/Cleanup receipt 或 stale binding 不得驱动 A。
5. **跨 session resume**：session 2 只能基于 live facts 重新验证并绑定同一 task；session 1 的确认、授权、semantic pass 与 checkpoint 不作为 session 2 当前授权或 pass。
6. **生命周期隔离**：Reactivate 生成新的 lifecycle-aware binding，使上一 generation 的 binding、Finish success、Cleanup receipt 失效；Finish/Closure/Cleanup owner 不被 rebind 绕过。
7. **#434 接口**：提供最小 public input、typed exits、consumer projection 与 global route 映射，能区分续接、跨 task 切换、Reactivate rebind 和 stale stop；不提前修改 #434 production graph。
8. **分发一致性**：canonical package、registry/schema、installed package、Shared/Codex/Claude/Cursor projection、preset reapply 与 dogfood drift 保持一致。

## Acceptance Criteria

- 同一 task 可通过两个不同 session 的 fresh identity 校验继续执行，且不创建第二 task/Issue/branch/worktree。
- binding 丢失可恢复；task、repo、branch、worktree、mapping、base、lifecycle 或 session 任一 mismatch 时零写入停止。
- 同一 session 从 A 切换到 B 并返回 A，A/B 的 runtime binding 与 route 不串线。
- Reactivate 后旧 generation binding/receipt 无法驱动当前 task。
- 缺少 session context、未知 task、错误 repo/workspace、stale binding 均有明确 typed stop。
- package/local tests、跨 package fixture、projection parity、ownership、`git diff --check` 和 task validation 通过。
- 明确记录 #434 production graph、完整 Release matrix 与生产业务操作未在本 Issue 实施。

## Issue revision: authorized manual recovery

新增 `manual_recovery` 入口：当 task artifact、task identity、repository/common directory、branch、worktree、HEAD 与 base 可由 live facts 验证，但 task/workspace mappings 与 session binding 同时缺失时，用户明确授权后只重建最小 ignored mappings 与当前 session binding。恢复不得创建 task、Issue、branch、worktree，不修改 tracked task artifact，不伪造 semantic pass、授权、Completion、Finish、Closure、PR 或业务交付事实；恢复后必须重新通过 boundary validator。缺少 session context、身份冲突、多候选 task 或错误 workspace 时 zero-write fail closed。

新增验收：完整 mapping 丢失场景可幂等恢复，恢复动作不会自动成为 task activation 或 lifecycle completion。
