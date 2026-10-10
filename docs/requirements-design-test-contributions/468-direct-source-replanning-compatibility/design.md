# #468 设计责任增量

状态：`candidate`；继承 `current-main-0.6.17-guru.80 / active`。本文件导航职责与实现合同，不复制各 Skill 的步骤。
Architecture candidate：[task-owned contribution](../../architecture/contributions/468-direct-source-replanning-compatibility.md)；独立原 owner 的 assessment、review 与后续 promotion 决定其状态。

| Responsibility | 唯一 owner、实现 locator 与 consumer |
| --- | --- |
| D468-01 | 原 `guru-clarify-requirements`、Planning、Check、Delivery、Completion、Reactivate 的 canonical `SKILL.md` 负责本阶段 Direct Source/必要事实/重开判断；`trellis/workflows/guru-team/workflow.md` 只编排既有 typed exits 与 earliest-owner 回程。Source 仍是 #454 封闭 union，无 coordination/related 字段、查询编排或 revision registry。 |
| D468-02 | 原 `guru-activate-task` 独占 `resume_execution` / `recover_execution`。单一 aggregate input/output schema 升为 2.0，原 activate/recover_activation payload 与含义保留；新增 execution_resumed 最小 output 由 workflow 原 Phase2 router 消费。共享 `runtime/task_lifecycle/composition.py` 校验 current planning、status、TaskId/generation、binding、session/current checkout 与 continuity；脚本不决定 route intent。Planning approved 仍只有 phase-1-task-activation consumer，由 workflow 根据 live lifecycle 进入首次激活或活动恢复执行。 |
| D468-03 | 原 activation package `runtime/execution_result.py` 拥有 gitignored 短期完成结果 checkpoint；仅服务原 owner 的实际输出丢失恢复及 current Phase2 handoff/Check，不记录 approval 或对话接受。`recover_execution` 只读验证同次 resume 结果；`guru-check-task` 仅在正式 current passed 结果产生后调用原 owner helper 退休对应 checkpoint。失效与 semantic DTO 丢失仍回原 producer fresh re-entry；无第二状态机或全链 replay。 |
| D468-04 | Marketplace workflow、canonical package/spec 与 preset 投影是长期源头；installed/platform 副本由原 preset apply 更新。RDT task-isolated contribution 由既有 maintenance owner 审查、串行 promotion；promotion-created diff 重新通过 fresh Phase2、TaskCommit 与完整 independent Branch Review。 |

兼容边界：`activate` 只写 planning→in_progress；`resume_execution` 不写 task status；首次输出丢失 recovery 与活动重规划 recovery 分开表达。原 Completion/Closure/Finish/Cleanup/Reactivate owners 和 #464 局部失效不增加新的公开路由或领域模型。其已支持场景复用定向证据，实际结果只由 [Test](./test.md)拥有。
