# #553 实施前基线冲突整合

Direct Source：[Issue #553](https://github.com/castbox/guru-trellis/issues/553)，2026-10-14 live OPEN 正文“目标”“验收”“独立范围与非目标”为本 Task authority；无新增产品决定。TaskId `553-preimplementation-reconciliation`，generation 0。

## 问题与当前证据

当前 canonical 使用 Task schema 2 / Delivery API 1；完整旧 dogfood 保留旧 Task owner，不能混用输入或结果。当前合同明确的受控组合为 CLI tar `5aeeb81ca72508081b7dd94ddb7a19f69444714f78b3a38858d908196cc77916`、Core tar `45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967`。本轮已核对安装包 713/270 文件字节与权限，并在该组合复现真实双分支冲突：原 `execute-base-candidate` 返回 conflicted；零 unmerged 的合法已解决 active MERGE_HEAD 再交 ordinary post_plan executor，仍重新 merge 并返回 reconciliation_failed。原 resolved 路径只从完整 Check 接入。

这是实施前新规划尚未实现时的基线承接缺口。完整业务 Phase 2 不能提前通过；旧测试通过不是缺口不存在的证据。根因修复资格与后续完成证明分别由各原 owner承担。

## 需求和验收

- R553-01：当前固定组合支持同 Task/gen/Delivery 的已批准活动规划修订 → 新 base pair → 合法文档冲突 → 原 Reconcile AI 解决并审查候选 → 精确本地双父 merge commit → 原 Activation 恢复实施。该环节不能要求未实现业务范围通过 Check。
- R553-02：基线验证只证明双方 authority 保留、当前规划适用、整合内容正确；不产生业务 Phase 2、TaskCommit、Branch Review 或 Delivery批准。实施后各 owner仍完成完整审查。
- R553-03：保留 TaskId/generation、适用 Delivery identity、规划与后续 consumer；不重复创建 Task/Delivery，不因 base 前进自动扩大 scope或全链重规划。
- R553-04：提交只包含受审 integration tree；无关 staged、unstaged、untracked 和并行内容在提交及同操作恢复后保持。
- R553-05：提交前核对实际 HEAD、selected base、MERGE_HEAD、零 unresolved、受审 tree/paths和父顺序。普通 stale/mismatch、未解决冲突、真实authority变化沿原 owner返回；Git副作用仅消费精确当次对话确认。
- R553-06：同请求 stdout丢失恢复原 commit，不新增第二 commit；原实施后 resolved_candidate 与无冲突行为通过原回归。
- R553-07：同步 canonical workflow/Skill/必要 runtime、schema、consumer及 dogfood/声明平台投影；执行定向 package/runtime、代表性 installed 接续、reapply/drift验证。静态、fixture、当前AI、installed/native和业务恢复证据分别报告，不声称完整多平台或Release矩阵通过。

每条 R553 的实际证据由 implement.md 所指唯一 Test记录；fixture语义输入、当前AI审查、installed continuation和业务恢复分别报告。

## 排除边界

不修改、升级、提交、发布或清理 backend #148；不向该会话发消息、不动其stash/worktree。不升级或清理业务仓，不关闭CMS Issue #1。不改上游/global/node_modules，不增加锁、TOCTOU、攻击/恶意输入防御或非常规加固；不跑完整多平台/Release矩阵，不开始其它Issue。

原 #407、#530 只提供各自承接约束。#547/#548 已交付不是本问题的替代机制；原业务历史手动恢复不是正常 Reconcile闭环证明。

## 已知安装验证边界

当前完整旧 dogfood 的 ordinary reapply 已返回 upstream_delivery_migration_required；D2历史迁移由原 Upgrade owner承担。本Task不半升级、删除历史或扩大为业务仓升级。当前支持的新schema2组合在独立完整安装样本核验投影；保留旧dogfood的现状验证与未切换事实，不将它记为新模型同步通过。此记录不是改写R553-07或自动豁免，最终Check/Completion须按适用当前组合与原安装边界分别判断。
