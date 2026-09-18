# #436 Post-Delivery Completion、Issue Closure 与 Finish 持久化

合同版本：`2026-09-18-r3`。本任务规划绑定 `castbox/guru-trellis#436`，承接 #435 的
`delivered` result；本阶段只形成规划，不授权 `task.py start`、实现、commit、push、PR、merge、Issue
closure 或 cleanup。

## 1. 目标与边界

建立一个可重复、可恢复且职责单一的 terminal lifecycle：

```text
#435 delivered / evidence-refresh
  -> guru-review-task-completion
  -> guru-complete-task-closure
  -> guru-finish-task
  -> guru-cleanup-task-resources
```

同一 task 可以经历多个业务 Delivery。`delivered` 只说明一个业务 slice 已合并，不能推断 task
complete、Issue closed、archive、Finish 或 Cleanup。Completion 必须 fresh 汇总 accepted scope、所有
Delivery facts、当前需求权威、验证与外部证据；不能由 PR Ready、merge、deploy、测试通过、Issue 状态或
archive 反推。

正常结束的 archived task 可以由 `guru-reactivate-task` 重新绑定到同一个 task identity；它不是
`guru-restore-archived-task` 的 merge 前 Phase 2 回退，也不创建替代 task。

## 2. 需求

### R436-01 Task Completion

新增 `guru-review-task-completion` semantic Skill，独占当前 task 是否完成的判断。它必须 fresh 读取：

- accepted task scope、current requirement/design/test authority 与 Architecture/RDT identity；
- 全部历史 Delivery facts，包括跨分支、已删除 remote branch、Reactivate 后新 workspace 的事实；
- 当前 task/workspace/binding、remaining work、实现与验证结果；
- Issue/source reference、外部 evidence 与其 freshness。

它只返回以下 closed typed exits，并为每个 exit 声明独立最小 DTO 与唯一 consumer：

- `remaining_work`：保持 active，回到当前 task 的既有实现/计划 owner；
- `evidence_pending`：保持 active，进入 evidence-refresh owner；
- `additional_delivery_required`：保持 active，进入 Delivery/Planning owner；
- `requirements_revision_required`：回到需求澄清/Planning owner；
- `implementation_revision_required`：回到 Phase 2 实现 owner；
- `completed`：把 completion approval 交给 Closure；
- `blocked`：进入唯一 terminal stop。

除 `completed` 外不得触发 Closure、Finish 或 Cleanup。`evidence_pending` 的 evidence-refresh 入口可被
Reactivate 的只补验证路径复用，但不预填 `completed`，不伪造新的 Delivery result。

### R436-02 Issue Closure

新增 `guru-complete-task-closure` semantic Skill，独占 Completion approval 后的 Issue disposition 与
Issue mutation：

- no-Issue、reference-only、follow-up、parent 或其它不应关闭的来源返回 `no_mutation`；
- exact source Issue 才允许独立 close mutation；
- mutation 前必须展示精确 repo、Issue number、action、reason 与预期结果，并取得当前对话确认；
- provider uncertainty、output loss、stale identity 只能恢复同一 closure transaction，不重复 close；
- Closure 不创建 Issue，不决定 Completion，不调用 Finish，不触发 Cleanup。

Delivery PR 与业务 Merge 均只使用 `Refs`，不携带 closing keyword，也不拥有 Issue closure。

### R436-03 Official Finish 持久化

新增 `guru-finish-task` semantic Skill，只在 Closure completed 后运行，负责：

- 将 active task 归档并生成 `finish-summary` 与 terminal metadata；
- 退出 current task binding，完成必要 history/index/journal bookkeeping；
- 准备只包含本 task 生命周期净差异的 expected-head-bound bookkeeping commit/PR；
- 审核 bookkeeping diff 与 PR payload，不重新执行业务 Delivery Review 或完整业务 Branch Review；
- 在 bookkeeping merge 成功并于目标基线验证 archive identity 后，才返回 `success`。

Finish bookkeeping PR 是行政收尾，不是业务 Delivery：不产生 Delivery result、不进入 Delivery discovery、
不触发 Completion、不携带 closing keyword、不创建 task，也不递归生成 Finish PR。归档目录移动、commit
或 PR 创建本身都不代表 Finish success。

### R436-04 Cleanup

新增 `guru-cleanup-task-resources` deterministic/semantic 边界明确的 Skill，仅消费当前调用产生的
`guru-finish-task:success` DTO。它 fresh 发现本轮 task 所有 owned branch、worktree 与 runtime resources，
展示精确删除目标并取得独立确认，然后只删除无 active consumer 的本轮资源。

Cleanup 必须保留用户原有 checkout、其它 task 资源、archive 与仍有 consumer 的 runtime 状态。Cleanup
失败不撤销 Completion、Closure 或 Finish；旧 Finish success 不得被 Reactivate 后的当前 Cleanup 消费。

### R436-05 正常结束 task 的 Reactivate

新增 `guru-reactivate-task` semantic Skill，独占正常结束 archived task 的重新激活：

- fresh 验证 exact archived task identity、原 accepted scope、archive Git version、历史 Delivery、当前
  baseline 与恢复原因；Issue reopen 只能触发核对，不能自动恢复；
- 保留原 task identity 与 Issue 关联，不创建 follow-up 或替代 task；
- 原 branch/worktree 可复用时验证后复用，不适合或已清理时从当前目标基线准备新的 branch/worktree；
- 写入前展示 task、archive/active path、目标基线、branch/worktree、binding 和文件变更，确认后才执行；
- 将唯一同身份 task 从 archive 移回 active，更新 metadata、mapping 与 session binding；
- 历史 Completion、Closure、Finish、Review 仅作历史事实，本轮必须 fresh 重跑；Issue reopen 不由该 Skill
  隐式执行。

恢复后有业务变更时走 #435 新 Delivery；只有验证补充且无业务 diff 时，走 evidence-refresh -> Completion，
不生成空业务 PR 或 Delivery result。再次完成后重新走 Completion -> Closure -> Finish -> Cleanup。

### R436-06 生产图与迁移边界

本任务只交付 additive Skill/package/schema/consumer、lifecycle SSOT、canonical/installed/platform
projection 与定向测试。#434 之前：

- production workflow 保持现有 22 mandatory invokes / 98 exits 与旧 Publication/Finalizer/Merge/Restore
  edge；
- 不允许旧 Merge result 自动进入新 Completion；
- 不允许新 Finish 消费旧 Finalizer archive residue；
- 不创建 old-output adapter、dual runtime graph、第二 lifecycle owner 或 ledger。

## 3. 验收标准

- [ ] 一个 task 完成两个顺序 Delivery 后，Completion 汇总全部 Delivery，remaining work 不被提前标记完成。
- [ ] Completion 的 7 个 typed exits、最小 DTO、唯一 consumer、freshness 与 fail-closed 规则闭合。
- [ ] evidence pending 更新与 Reactivate 只补验证路径不创建空 Delivery、不生成业务 PR。
- [ ] additional delivery、requirements revision、implementation revision 与 blocked 均返回最早受影响 owner，保持 task active。
- [ ] no-Issue/reference-only/follow-up/parent 路径不 mutation；exact source Issue 只由 Closure 在独立确认后关闭。
- [ ] Closure output loss 与 provider uncertainty 恢复同一 transaction，不重复 close。
- [ ] Finish 仅在 Closure completed 后开始；bookkeeping PR allowlist 不含业务代码、其它 task、共享 journal 或 runtime。
- [ ] bookkeeping merge success 前不允许 Finish success 或 Cleanup；目标基线 archive、active removal 与 metadata 一致。
- [ ] Finish PR 不进入 Delivery discovery、不产生 Delivery result、不关闭 Issue、不创建自身 task/Finish PR。
- [ ] Cleanup 只消费当前 Finish success，精确处理 owned branch/worktree/runtime，失败不回滚前序结果。
- [ ] 正常结束 archived task 的 Reactivate 保留原 identity，能复用或重新准备 workspace，且不产生 active/archive 双副本。
- [ ] Reactivate 后业务变更使用新 Delivery；旧 merged PR、旧 branch、旧 Finish success 不阻塞或污染本轮。
- [ ] 旧格式正常结束 archive 可承接；同月/跨月再次归档不产生重复目录、嵌套目录或重复 task。
- [ ] source/installed package tests、Completion/Finish integration、bookkeeping allowlist/expected-head、projection parity、preset reapply、dogfood drift、task validation 与 `git diff --check` 通过。
- [ ] #434 激活前 production workflow 与旧 lifecycle edge 保持不变；完整 Release/multi-platform matrix 不在本任务范围。

## 4. 非目标

- 不修改 #435 Delivery Review/Publish/Merge readiness、payload、merge trailer 或 Delivery identity。
- 不实现 #434 production graph atomic activation、旧 edge retirement 或最终计数切换。
- 不拆出独立 Acceptance Issue，不创建 follow-up task，不新增通用 Finish checkpoint/recovery framework、pinned generation、故障注入或自动异常恢复矩阵。
- 不重构 Phase 0/普通 Planning、CI auto-merge、GitHub ruleset、Release、业务仓生产操作或完整兼容性 Release Gate。
- 不关闭本 Issue，不执行 commit、push、PR、merge、tag、Release 或 cleanup，除非后续分别获得明确授权。
