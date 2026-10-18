# #436 Post-Delivery Completion And Finish Test contribution

状态：`reviewed_promoted`。`T436-01..56` 是需求阶段的验收矩阵，不等同于每个编号已有一条自动化测试。当前只声明下列已执行证据；semantic 判断仍由 AI owner 完成，脚本与 fixture 不替代 live authority review。

## 当前自动化覆盖

- Completion package：12 tests。覆盖 `completed` 对 authority、全部 Delivery 与 evidence 的非空、精确双向绑定、非空 `remaining_work_refs` 拒绝，以及 `completed -> Closure` authoring-seed 投影；未把其余六条 semantic route 都声明为 runtime 场景覆盖。
- Closure package：9 tests。覆盖 no-mutation、`exact_source + no_mutation` fail-closed、错误 repo/Issue recovery facts fail-closed，以及 OPEN/CLOSED recovery fact 都重新读取 exact live Issue 后决定是否关闭；新增 `closure:v3` 对 source Issue/disposition 的绑定与错误 disposition 恢复拒绝；provider 使用 fake `gh`，不构成 live GitHub 证据。
- Finish package：10 tests。覆盖 `resume_finish` 返回完整 `task_ref`、`closure_exit`、`closure_ref`、`source_issue` 自投影，其它 task archive allowlist 拒绝、bare/qualified closing keyword 拒绝、merge 前 base-head 复核，以及 fake remote/provider 下单一 bookkeeping commit/PR/merge、目标分支 archive post-check、Closure 绑定校验与 lifecycle generation 输出。
- Cleanup package：8 tests。覆盖 empty/already-absent owned set、缺失 Finish receipt 时 `remaining_resources` continuation identity、独立确认前保留资源、exact Finish-owned remote branch 与 remote-tracking ref 删除、成功后最小 ignored terminal receipt 的 stdout-loss recovery、`lifecycle_generation` 与 terminal archive 交叉校验，以及当前执行 checkout/unbound worktree 拒绝。
- Reactivate package：11 tests。覆盖 source/consumer projection、exact workspace reuse、新 workspace 创建、`reuse_exact`/`create_new` complete transaction post-state 的 stdout-loss recovery、task/archive/mapping locator identity、旧 Finish receipt 失效、fresh lifecycle generation 输出，以及 bookkeeping merge 后 branch fast-forward ancestry。
- Cross-package contract：`test_post_delivery_public_contract_projections_are_closed` 验证五个 package 的每个 exit 使用独立 schema/example，所有 artifact/schema 已声明，skill authoring seed 与目标 input required fields 闭合，workflow projection 含 `exit_id`，zero-payload stop 只有 `exit_id`。

## 分发与边界证据

- source/installed package validation、Shared/Codex/Claude/Cursor public projection parity、dogfood overlay drift 与 preset managed-backup recovery 已执行。
- installed production graph 仍为 22 mandatory invokes / 98 exits；五个 package 保持 `workflow_integration_state=deferred`，#434 前不激活新 edge。
- Delivery/active-task-continuation integration 已执行。既有 Finish-family suite 仍有 3 个与 #436 无关的基线失败：旧 `archived_ready` exit 集合预期和旧 Finalizer eval file schema；本任务不修改旧 Finalizer 合同来掩盖这些失败。

## 未验证边界

- 未执行真实 GitHub Issue close、真实 bookkeeping PR/merge 或生产资源 Cleanup。
- 未执行完整多平台 Release/upgrade matrix；本 Issue 只承担普通 Issue 的定向 install/reapply/parity 门禁。
- #436 的 RDT/Architecture shared current 已在 `current-main-0.6.17-guru.56` 完成前一轮串行 promotion；本轮 P1 修复只在该已提升 topology 内做 additive correctness fix，未执行 #434 production graph activation，也未创建新的 shared-current promotion。
