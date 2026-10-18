# #443 Task Identity Session Binding Requirements contribution

状态：`reviewed_promoted`。本 contribution 已提升到 `current-main-0.6.17-guru.57`；`.56` 为 immutable predecessor。

- `R443-01`：task identity 是唯一长期主身份；Issue、规划、Delivery、archive、Reactivate 与 Finish/Closure 历史归属同一 task。session、branch、worktree 与 runtime mapping 只是可替换承载资源。
- `R443-02`：session binding 是 ignored owner-private 短期状态，由 official Trellis `active_task` / `session_storage` authority 承载；不得进入 tracked task artifact、public DTO、Issue ledger、授权记录或第二 binding store。
- `R443-03`：resume/rebind 必须 fresh 验证 task artifact、repository common dir、branch、worktree、HEAD、base provenance、task/workspace mappings、session context 与 lifecycle generation；任一 mismatch 在写入前 fail closed。
- `R443-04`：同一 task 跨 session 继续和同一 session 的 A→B→A 切换都必须重新验证目标 identity；不得把另一个 task 的 route、checkpoint、Finish/Cleanup receipt 或旧 semantic pass 带入当前 task。
- `R443-05`：Reactivate generation 变化使旧 binding 与旧 terminal receipts 失效；session binding owner 不接管 Reactivate、Completion、Closure、Finish 或 Cleanup 的语义与 mutation。
- `R443-06`：manual recovery 只在 task artifact、live Git/worktree、base provenance 与 session context完整一致时重建最小 task/workspace mapping 和当前 binding；不创建 task、Issue、branch、worktree，不修改 tracked task artifact，合法重试幂等。
- `R443-07`：package 提供 `session_resumed`、`session_rebound`、`task_switched`、`reactivate_rebound`、`session_manually_recovered` 五个成功出口与 `binding_blocked`；每个出口只投影唯一 consumer 必需的最小字段。
- `R443-08`：`guru-bind-task-session` 以 active/deferred 完整进入 canonical、installed 与声明平台 projection；#434 前 production workflow 保持 22 mandatory invokes / 98 exits，不能把 package 存在解释为 route 已激活。

完整 Release matrix、#434 graph activation、真实生产 binding 操作和当前任务的 commit/push/PR/merge/cleanup 均不由本 contribution 自动授权。
