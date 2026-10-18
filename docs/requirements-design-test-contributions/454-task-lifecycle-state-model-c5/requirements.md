# #454 C5 Session And Resource Control Requirements Contribution

状态：`reviewed_promoted`，successor 为 `current-main-0.6.17-guru.63`。本 contribution 只承接 C5 path-free session adapter 与 resource ownership ledger
substrate；expected current 为 `current-main-0.6.17-guru.62`。它不激活 production workflow，不交付完整 Skill
package，也不重做 C1、C2、D0、C3 或 C4。

- `R454-C5-01`：session domain payload 必须严格同构于 `TaskLifecycleDTO`；official record 只能包含
  `schema_version`、`task_id`、`lifecycle_generation`。TaskRef、branch、path、HEAD、ownership、semantic pass 与授权
  不得进入 session authority。
- `R454-C5-02`：Guru session adapter 必须调用 Fixed Fork official schema-2 repository/common-dir store，不复制
  `.trellis/scripts/common/**` 或创建第二 store。context key 缺失或不可用时不得写 record，返回
  `explicit_task_mode`；session write failure 不回滚已成立 lifecycle。
- `R454-C5-03`：同一 task 可由多个 session 继续；同一 session 可 A-to-B-to-A 受控切换。Reactivate 后旧
  lifecycle generation record 必须失效；consumer 每次按 stable TaskId fresh 解析 TaskRef。
- `R454-C5-04`：resource ledger 必须位于 Git common-dir，并按 `TaskId + lifecycle_generation` 隔离。每个 resource
  incarnation 记录 acquisition origin、ownership、portable ref、binding epoch/revision、state 与 responsibility role；
  不保存当前 checkout locator authority。
- `R454-C5-05`：unknown/unprovable ownership 固定投影为 caller-owned。active ledger missing 与 ledger conflict
  必须区分；active missing 可在 current binding/live resource 验证后以 caller-owned 重建，terminal missing 固定进入
  manual cleanup selection，不补写 Guru ownership。
- `R454-C5-06`：C4 `OwnershipPort` 的 current/snapshot/restore/establish/rebind/unresolved-ref 操作由同一 ledger
  实现。已建立 state 必须校验 epoch、revision、branch 一致性；该校验不得变成从 path、branch name、Issue 或目录
  猜测 task 的严格 selector。
- `R454-C5-07`：rebind 必须保留旧 resource incarnation。旧 Guru-owned resource 进入 `cleanup_pending`；旧
  caller-owned resource 保持 retained/manual-only；同一 portable ref 在前一 incarnation 收敛前不得复用。
- `R454-C5-08`：Finish seal input 必须携带 exact `finish_head`，封存当前 generation 的完整 responsibility inventory，
  将最后一个 current bundle 的 Guru-owned resource 的 `expected_cleanup_head` 固定为该 HEAD。普通 Cleanup 只消费
  `guru_owned + cleanup_pending` 并验证 sealed HEAD；caller-owned、unknown ownership 与
  `refs/heads/guru-task-lifecycle/*` retained control refs 不得进入普通 deletion set。
- `R454-C5-09`：remote resource identity 必须包含 portable `remote_name`、repository 与完整 branch ref；零个或一个
  remote 可承担 `current_delivery` role。Cleanup 用 remote name 与 repository identity 定位并验证完整 remote ref；
  Publication 尚未发生时 remote set 可以为空。同一 current remote incarnation 在再次正常发布时保留原 resource id、
  origin 与 ownership，以 caller 已验证的当前 HEAD 单调推进 cleanup HEAD；相同 HEAD 重试不改 ledger，旧 HEAD
  回退或 remote identity/ownership 漂移拒绝。Guru-owned remote 首次记录时必须已有 exact published HEAD；
  conservative recovery 的 caller-owned remote 可暂时缺少 HEAD，后续已验证的 HEAD 只更新同一 incarnation。
- `R454-C5-10`：自动 discovery 只在恰好一个 valid candidate 时自动选择；零个或多个进入 selection-required。
  用户可选 discovered candidate 或显式指定未列出 target，两条路径在 mutation 前使用同一 fresh validation。
- `R454-C5-11`：`guru-establish-task-identity` 在 C5 只作为 planned stable ID。不得创建 canonical package tree、
  interface、command、workflow edge、installed copy 或平台 projection；E434 独占激活。

C6-C7、D443、D436、E434、#434 activation 与完整 Release matrix 不属于本 contribution 的完成声明。
