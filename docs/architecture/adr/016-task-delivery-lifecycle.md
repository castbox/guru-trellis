# ADR-016: Separate business Delivery from task completion and finish

状态：`accepted`（`current-main-0.6.17-guru.67`）。来源：Issue #434 `2026-09-18-r4` 与 task-owned
[Architecture contribution](../contributions/434-task-delivery-lifecycle.md)。
predecessor 为 `current-main-0.6.17-guru.66`；由 expected-current-bound serialized
Architecture promotion 接受，post-promotion gates 仍需独立验证。

## Context

当前 closeout 将 Publication、push/PR、archive、Ready 与 Merge 连接为一次
terminal transaction。task 在业务 Delivery merge 前归档；Merge 后发现 task work
时必须恢复 archive。Issue closure intent 也在 whole-task Completion 之前编码。
该模型无法表达一个 active task 的多次顺序业务 Delivery，也把正常完成后的再次工作
与 merge 前提前归档回退混为同一恢复语义。

## Decision

1. 业务 Delivery、Task Completion、Issue Closure、Official Finish 与 Resource
   Cleanup 成为五个顺序概念，各由独立 semantic/action owner 承接。
2. 每次 Delivery merge 只产生一次 Delivery result；task 保持 active，Issue 保持
   Open，Delivery PR 固定使用 `Refs`。
3. `guru-review-task-completion` fresh 判断 remaining work、evidence、additional
   Delivery、requirement/implementation revision 或 completed。只有 completed 进入
   explicit Closure。
4. Closure 完成后，`guru-finish-task` 通过独立 bookkeeping commit/PR 将唯一 archive
   持久化到目标基线；该 PR 不是业务 Delivery，不再次触发 Completion。
5. Cleanup 只消费同一 lifecycle generation 的 Finish success。旧 Finish success
   不能删除 Reactivate 后的资源。
6. 已正常结束的 task 使用新的 `guru-reactivate-task`，保留 task identity，并按真实
   缺口进入 requirements、Planning、implementation、validation 或 evidence refresh。
   旧 `guru-restore-archived-task` 不复用、不改名。
7. #435/#436/#443 先交付 additive package capability；#443 的 Session Binding capability 是 activation hard prerequisite；#434 在全部 package、schema、consumer、
   installed/platform projection 就绪后一次性切换 global graph 并退休旧 active edges。
8. current main 不保留 old/new 双图、旧 output adapter、schema dual-read 或通用旧链迁移
   runtime。在途旧链固定旧版本完成或人工处置。
9. #454 C2-C7/D443/D436 改变 TaskId/source、path-free session、branch binding、resource ledger 和终态 ResultRefDTO；#434 只连接现行接口与全局路由，不恢复 task_workspace mappings。六个 planned IDs 在有真实 package/interface 前不能作为激活前置通过。

## Rejected Alternatives

- 继续扩展旧 Finalizer：保留交付、归档和完成的职责耦合。
- 每个 task 持久化 graph version 并长期双路由：引入无退出双图和第二测试矩阵。
- 将旧 Restore 改名为 Reactivate：入口对象、阶段语义、workspace 策略和 exits 均不相同。
- 让 Delivery PR 使用 closing keyword：把一次 Delivery 错当 whole-task completion。
- 新增独立 Acceptance：Issue #434 明确由 Completion 承担最终 semantic judgment。

## Consequences And Adoption Gate

目标图能表达多次 Delivery 和正常结束后的同 identity Reactivate，但激活必须等待 #435、#454 D443/D436 与 Phase E 必需 package 的完整接口、切换前 active registry 32 packages / 142 exits / 102 commands（另有非激活 source exits）和 installed projection reconciliation。切换会删除旧 current owner/edge，旧版本 task 不能在新 main 上依赖旧
Restore 自动迁移。采用前必须证明 source/installed/four-platform graph closure、mixed graph
fail-closed、A/B multi-delivery、Completion/Closure/Finish/Cleanup、Reactivate、preset reapply
和本地 canonical workflow 样本 + preset 的代表性 clean throwaway。远端 marketplace 安装不在 #434 验收范围；完整多平台 Release Gate matrix 由专门 Release Issue 独立执行。

接受本 ADR 需要 expected-current-bound Architecture promotion；promotion 本身不证明后续
Phase 2、Branch Review、远端发布、正式 Release 或业务生产验证完成。
