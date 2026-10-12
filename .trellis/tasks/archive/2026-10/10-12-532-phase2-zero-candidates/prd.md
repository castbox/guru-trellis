# #532：完整 Phase 2 真实零候选初检

## 来源与目标

Direct Source：[castbox/guru-trellis#532](https://github.com/castbox/guru-trellis/issues/532) 的“目标与修复边界”与“验收”。当前来源更新时间为 2026-10-12T10:09:24Z；实现开始时重新读取来源。历史诊断只证明非空约束，不作为修复后公开链路成功证据。

目标：Check owner 完整审阅规划、diff、代码、测试、Docs 和 Architecture 后没有真实缺陷候选时，以 `candidate_classifications=[]` 走通原 recorder → checker → public initial_check。空集合只表达审查观察，不决定 passed。

## Accepted scope

- R1：Check SKILL 和 contract 定义两个确定分支。候选集合为空时不调用三个 qualification owner；有实际候选时按当前资格判断顺序调用，root owner 只接收前两 owner 返回的 eligible refs。不得把 reviewed_paths、业务功能或 no-defect 占位项当作缺陷候选。
- R2：原 schema/runtime 接受空数组，继续拒绝非数组；保留候选唯一性和 findings/scope decisions 的真实 candidate_ref 引用一致性。三个 qualification Skill 的非空输入合同保持。
- R3：保留九项语义审查、Docs/Architecture 前置条件、内容 freshness、四个正式出口与唯一 consumer、execution checkpoint 生命周期。正常缺失证据或 stale 状态不能因空数组获得 passed。
- R4：共享 schema/runtime 的 initial_check、finding_fix_rerun、planning_reentry、resolved_reconciliation 四 profiles 使用同一逻辑。保持 reconciliation 的原私有结果与 target-owned projection，不新增正式出口。
- R5：同步 canonical、dogfood、一个代表性 installed 环境；示例、测试和 eval 分别表达真实空集合与实际非空候选最终无 findings。执行 apply/reapply 和 overlay drift 定向验证。

## 可观察验收

| ID | 场景与入口 | 预期观察 |
| --- | --- | --- |
| AC1 | 完整真实审查无候选，经原 recorder/checker/public initial_check | 原数组为空；在前置条件全部满足时取得正式 passed，handoff 与 checkpoint 生命周期正确；无虚构候选、无 tracked 证明文件 |
| AC2 | 真实非空观察经适用 qualification 全部 rejected | 原 classifications 保留拒绝理由和 witness，无 findings；与 AC1 使用不同真实语义事实 |
| AC3 | 有可复现当前范围缺陷并经完整 qualification | finding 引用真实 qualified candidate，取得原 implementation_required；涉及规划缺口的候选由原 planning_stale 路由承接 |
| AC4 | 零候选但正常缺失必需验证或 Architecture 前置条件 | owner 停在原阻塞/Architecture 回程；不能选择 passed |
| AC5 | 正常 recorder 后受审内容发生变化 | 原 freshness checker 拒绝 stale；不手改 hash/state 制造案例 |
| AC6 | 四 profiles 与原消费者 | 空集、非空无 findings、有效 finding 的定向结果保持 profile-specific route；resolved_reconciliation 使用原投影 |
| AC7 | canonical/dogfood/一个 installed 环境的真实入口 | 原公开链路结果一致；preset apply/reapply 与 overlay drift 通过；sidecar 逐个说明 |
| AC8 | 分层报告 | schema/单元/契约、真实公开链路、安装与重应用分别列实际结果及未验证边界 |

## Delivery 与外部边界

本 task 只有一个完整 Delivery slice：R1–R5 与 AC1–AC8。独立交付条件是现有 Check 生命周期内修复并通过该验证集，不依赖 #531 模型迁移完成。task 内无隐藏剩余切片。

#292 保留其原实现、安装与恢复验收；#530 保留 clean 已提交候选进入 Branch Review；#531 保留 Task/Delivery 重构与后续迁移。本 task 不修改它们的状态、工作树或 Closure。完整多平台矩阵由专门 upgrade/release owner 承担；本 task 不宣称原会话恢复、版本发布或业务部署完成。

不重构 Task/Delivery，不新增状态 authority、审计 ledger、授权存储或资格判断空集出口，不改 upstream trellis-*、全局 npm，不添加攻击/伪造/对抗、锁/压力竞态或非常规 crash consistency 机制，不清理现有资源。

## Docs SSOT Plan

策略：`ssot_first`。Check 行为唯一源为 `trellis/skills/guru-team/packages/guru-check-task/SKILL.md` 和 `references/contract.md`；先改合同，再改其确定性校验。运行安装副本由 preset 同步，不拥有第二份行为定义。

RDT 使用 task-owned `docs/requirements-design-test-contributions/532-phase2-zero-candidates/` 的 requirement.md、design.md、test.md、traceability.md 记录增量与唯一 Test 结果；共享 current 由原 RDT promotion owner 串行晋升，禁止手改历史版本。Architecture 的影响、贡献和 ADR 由独立 owner 的实际判断决定。规划文档不作为长期运行 authority，测试结果不得倒填为规划已通过。
