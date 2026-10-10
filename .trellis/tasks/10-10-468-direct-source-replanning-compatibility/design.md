# 设计候选：Direct Source 与活动重规划承接

## 当前对象与受影响执行图

main@8dfa2a35bd2ccae236f7b8bc679f107f3ec1ffde 的 Planning approved 唯一 consumer 是 phase-1-task-activation。当前 guru-activate-task 的 task_activation profile 只有 activate 与 recover_activation；prepare_activation_inputs 接受 planning，activate_task_status 只写 planning -> in_progress，recover_activation_inputs 接受 in_progress。Planning checkpoint 在正常 public projection 后删除。当前 continuation 区分 semantic output 丢失 fresh owner re-entry 与 deterministic mutation 输出丢失原 owner recovery。

活跃 task 经 current Clarification 返回 Planning、获批后的 approved 到达同一唯一 consumer，但 status 已是 in_progress。直接 activate 拒绝；recover_activation 的 published semantic 是首次 status mutation 后输出丢失，无法表达新规划接续。

本候选直接演进现有 workflow、Planning/Lifecycle owner；不新增 Skill、任务状态或 source 字段。

## DR468-01：需求事实与依赖判断

Direct Source 沿 current task.json.source.repo_ref + number 读取，accepted scope 与 source disposition 分离。Coordination、Related Work、Follow-up 只在 live scope 或 stage 原有 evidence 中按明确用途判断。纯信息变化不影响 scope；必要条件变化复用 #464 局部失效和 earliest owner re-entry。脚本不解释 Issue 自然语言，不增加拓扑字段、Issue 查询编排、revision binding 或 dependency registry。

Issue 重开先从原 TaskId 与 live lifecycle facts 区分 active、未完成 closeout transaction、正常归档并符合 Reactivate entry。原 owner 处理冲突；不根据 Issue state 自动加 generation 或新建任务。

## DR468-02：同一 approved consumer 的两种执行承接

保持 guru-approve-task-plan:approved DTO 和唯一 phase-1-task-activation consumer。该 workflow target 由 AI 依据 current lifecycle 分支：planning 首次 activation；in_progress 活动重规划恢复执行。两个分支均先消费 current approval、完成 current plan 展示与对话接受、通过 task_activation pair guard，然后调用同一 guru-activate-task semantic owner。script 不决定 route intent，也不判断用户回复。

直接演进 guru-activate-task 的单一 public input 至 2.0：
- activate 与 recover_activation 的输入形状及语义保留。
- 增加 resume_execution，用同一最小 activation 输入消费 current planning_result_id、TaskId/generation/TaskRef、base continuity、session outcome；仅接受 in_progress，完成正式执行承接而不写 task.status。
- 增加 recover_execution，仅恢复同一次已完成 resume_execution 的结果；不作为 pending 新规划的代替。
- activated 输出保留 1.0 identity projection；新增 execution_resumed 输出为 task_id/task_ref/lifecycle_generation，唯一 consumer 为现有 Phase2 execution target 的显式 workflow router。
- aggregate input/output schema id 版本化，interface / examples / projections / consumer contracts / registry 同步。不保留第二 parser 或 fallback；controlled consumers 原地更新。旧 activate/recover_activation payload 在单一新 schema 下仍保持原语义，活动任务不得被静默当作首次 recovery。

Shared composition 复用 TaskId/generation、C4 branch binding/resource ownership、C5 official session/current checkout、planning-content freshness 与 continuity validator；新增明确 in_progress prepare-resume helper，不通过 recover_activation helper伪装新功能。

## DR468-03：正常 continuation 和结果丢失

只新增一个 Lifecycle owner-private、gitignored、短生命周期 execution-result checkpoint：记录该 owner 实际完成的 activate 或 resume_execution 操作与当前 planning_result_id，并绑定 TaskId/generation/TaskRef、当前 branch-binding revision 和执行时 continuity。字段仅用于恢复同一次结果及检测正常内容/身份/base 变化；不记录语义 pass、用户接受、回复、时间、来源、digest 授权或过程。

首次执行或恢复执行成功后，由原 owner 的 deterministic recorder 写结果；recover_execution 读取并验证该 owner 的 resume_execution completion 与 current live binding/planning/continuity，返回 execution_resumed，既不改 task metadata，也不重新记录或推进。真实首次 recover_activation 保持原合同；不能用 resume checkpoint 冒充首次输出丢失。

唯一 [trellis-continuation] 在普通 Phase2-to-Completion 路由前明确处理活动重规划：
- 当前 adjacent approved DTO 仍在：回 phase-1-task-activation 展示/接受，再调用 resume_execution。
- 尚未完成执行承接且 approved 丢失/过期：回原 Planning owner fresh re-entry，当前对话接受不可确认就重新展示；文件存在和 in_progress 都不是 pass。
- execution-result 与 current plan 同步、operation 为 resume_execution，且输出丢失：进入原 owner recover_execution。
- planning 内容或 requirement authority 改变：先由 AI 按 #464 判断语义影响，material 变化回最早受影响 owner；不得仅因 hash 变化执行整链 replay，也不能从旧 checkpoint 推导新批准。
- checkpoint 缺失时以原 stage 的实际正式结果/事务为依据；若重规划承接无法证明，返回 fresh Planning。已存在的 Check/Commit/Delivery/closeout continuation 不回退或重新激活。

checkpoint 的直接 consumer 是执行结果恢复及 current Phase2 handoff/Check。当前 Phase2 checked passed 已产生其原 producer checkpoint 后，调用原 execution owner 的确定性 retirement helper 删除对应结果；失败、输出丢失或内容不匹配保留给原 owner。无永久 ledger、逐轮历史、跨阶段 receipt chain或重规划授权标记。

## DR468-04：SSOT、投影与测试

Markdown 更新 current Clarification/Planning/Check/Delivery/Completion/Reactivate 的必要说明，复用原 typed routes。Repository Docs strategy 为 delta_first：本任务隔离 RDT contribution；Architecture candidate 位于 docs/architecture/contributions/468-direct-source-replanning-compatibility.md，绑定九项 concern、current authority、owner/data lifecycle 和 project-check protocol，ADR 当前候选为不需要并由独立 owner 复核；不直接写 shared current。promotion 后的 diff 必须重新完成 fresh Phase2、TaskCommit、完整 independent Branch Review。

canonical 源为 trellis/workflows/guru-team、trellis/skills/guru-team、trellis/presets/guru-team；dogfood 由官方 preset apply 投影。platform entry 只加载和路由，不复制 local owner 步骤。安装副本不携带 tests；canonical tests 与代表性 installed wrappers 分别验证。

测试以生产 Planning recorder/checker/public wrapper -> Lifecycle public wrapper -> live task/control-state before/after 为主，测试预期来自需求行为。扩展当前 tests/test_contract.py 和 lifecycle composition tests，新增定向正常边界用例；semantic Issue 角色与 earliest-owner 判断使用 current Clarification、Check、Completion、Reactivate owner 实际审查及其原 package 的 formal invocation，不能用脚本模仿 AI 判断。

## 备选与约束

直接重复 activate 会违反现有 status contract；使用 recover_activation 代替新恢复会改变已发布语义；只凭 in_progress 手写 Phase2 资格会跳过新 approved consumer。新独立 Skill/任务状态机、永久 revision binding/授权缓存均增加第二 owner 或无必要状态。上述候选直接演进 existing owner，执行结果 checkpoint 只解决新要求的真实正常结果丢失窗口。

当前设计尚需独立 Architecture assessment、Planning normal/solution/root qualification、wording 和 Planning Approval；本文不声明候选通过，也不授权实现。
