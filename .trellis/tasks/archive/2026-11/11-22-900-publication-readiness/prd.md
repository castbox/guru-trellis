# 将 Delivery Review 的 PR readiness 判断并入发布入口

## 1. 来源与术语

| 标识 | 来源与章节 | 角色与用途 |
| --- | --- | --- |
| S1 | [#900](https://github.com/castbox/guru-trellis/issues/900) 的行为要求与验收 | Direct Source，定义本 Task 的范围和验收。 |
| S2 | [#736](https://github.com/castbox/guru-trellis/issues/736) 第 8 项的 readiness 合并要求及 AC7 的发布部分 | S1 选定的上位要求。 |
| S3 | [#900 评审评论](https://github.com/castbox/guru-trellis/issues/900#issuecomment-7078987199)、[#794](https://github.com/castbox/guru-trellis/issues/794) | 审核证据与历史前置。保留提交后的独立审查和后续合并确认。 |
| S4 | [当前 workflow](../../workflow.md#36-delivery-review-and-publication)、[生命周期需求](../../../docs/requirements/current/task-delivery-lifecycle.md#交付事实与整体完成)及[设计](../../../docs/design/current/task-delivery-lifecycle.md#本地待审提交与旧-draft-恢复职责) | 当前运行分工与兼容依据。 |

readiness 是 AI 对当前 Delivery 切片能否独立发布的语义判断。Publication 是发布入口及其远端事务。Merge 拥有独立的合并判断与写入。

## 2. 背景与问题

#794 已将 Check 和 Branch Review 合为一次提交后独立审查。当前调用方还要单独进入 Delivery Review，取得其 readiness、中文 PR 载荷及 `ready`，随后才可进入 Publication。#900 将这段发布准备收敛到一个公开入口。

## 3. 目标与非目标

本 Task 交付发布入口的语义判断、准确预览及后续发布动作，并迁移受影响的正常、返工、续接合同和声明平台投影。独立候选审查、架构资格、Merge 独立确认以及 Task Completion 后的原 Closure 保持各自的职责。归档合并评估和其它 #736 交付由原范围承担。

## 4. 真实调用方、场景与流程

- SC1 正常发布。标准 Guru workflow 的调用方持有通过独立审查的固定已提交候选，从发布入口取得 readiness 和实际预览。确认对应预览后才执行适用的 push 与 PR 操作。满足当前合并前置时，把结果交给原 Merge。
- SC2 前置失效或 readiness 未通过。发布入口停止待执行远端写入，并携当前问题返回相应的审查、架构、规划、实现或范围职责。
- SC3 续接在途发布。调用方恢复同一 Delivery 时先回读发布状态和已有 PR，区分完成与待执行动作。已合并的 PR 进入原 Merge 恢复。

## 5. 行为要求

- R1 发布入口采用当前适用的独立审查和架构资格结果。AI 按批准范围、实际交付与验证、剩余 Task 责任及未验证边界判断独立可发布性。
- R2 readiness 通过时展示实际中文 PR 标题和正文、切片交付、剩余责任及未验证项。有适用的来源 Issue 时沿用 `Refs`。关闭来源 Issue 由 Task Completion 后的原 Closure 判断并执行。
- R3 push 与 PR 操作绑定已审候选和本次预览。完成该次确认后才执行。候选或发布事实变化使结果失效时，返回受影响职责重新取得结果。待执行的远端写入或确认过的预览发生实质变化时，重新展示并确认。
- R4 审查或架构资格缺失、失效时回原职责。readiness 发现规划、实现或范围问题时回对应职责。满足当前合并前置后才交原 Merge，由其独立确认合并。
- R5 合法在途操作沿同一 Delivery 和已有 PR 恢复。原事务回读已完成动作。待执行动作按当前前置和确认边界继续。发现该 PR 已合并时直接交原 Merge 恢复入口。
- R6 同步受影响的公开合同、正常和返工续接入口、实际前置、最小调用示例、结果与失败消费、兼容迁移和声明平台投影。

## 6. 约束与依赖

原 Branch Review 提供当前固定候选的独立审查结果，原 Architecture 提供适用的资格结果。方案阶段由 Author 和 Architecture 确定正常入口、公共合同迁移与在途恢复的实现，并核对受影响的当前需求、设计、测试及架构定义。基线上的旧 Draft 和已合并恢复能力是本次兼容依据。

## 7. 可观察验收与验证方式

- AC1 对应 R1–R4、R6 和 SC1。通过正常公开入口提交通过独立审查的固定候选。调用方直接取得 readiness 判断与准确预览。比较确认前后的目标远端状态，确认后写入与预览一致。达到合并前置时，原 Merge 入口可直接消费结果。
- AC2 对应 R3–R6 和 SC2、SC3。通过该入口观察审查或架构资格失效以及 readiness 未通过时的适用回程。覆盖本次影响的在途恢复，观察调用复用已有 PR，回读已完成动作并按当前资格与确认边界续接待执行动作。已合并回程可采用仍适用的原验证证据。

## 8. 实际未决项

整体需求未发现需要在此阶段确认的产品选择。具体合同版本与恢复迁移方案由 Delivery Planning 展开。
