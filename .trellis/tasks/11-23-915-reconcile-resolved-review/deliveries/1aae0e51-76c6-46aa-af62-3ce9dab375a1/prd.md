# D1 Reconcile 冲突接续修复需求

## 1. 整体来源与术语

本切片选择整体 PRD 的 AC915-1，覆盖 R915-1 至 R915-4。适用来源为 [Task 整体 PRD](../../prd.md)、[#915 的期望行为和验收](https://github.com/castbox/guru-trellis/issues/915)及 [Reconcile 详细合同的冲突解决后候选章节](https://github.com/castbox/guru-trellis/blob/8604558695dfd9d8ea2181406a87ece70d9eea63/trellis/skills/guru-team/packages/guru-reconcile-task-base/references/contract.md#L249)。本 Delivery 的规划目录为 `deliveries/1aae0e51-76c6-46aa-af62-3ce9dab375a1`。B 指原 Delivery 的固定内容基线，H 指原执行器返回的实际整合 HEAD。

## 2. 整体与本批目标、非目标

修正 `delivery_resolved_candidate` 入口和受管安装中的旧 Check 前置与旧 review profile 引用。使执行者可以依次创建整合提交、绑定候选、消费原投影并取得两个正式结果。D1 承担 #915 的全部范围。验证限于代表性的匹配安装和真实本地 Git 冲突。关联的 go-guru 案例只作为问题来源。

## 3. 本批起点、前序结果、依赖与剩余责任

开发从 `main@8604558695dfd9d8ea2181406a87ece70d9eea63` 开始，目标为 `origin/main`。没有前序 Delivery。当前已有整合执行器、投影命令、公开 Candidate 与 `begin_check`，以及合并后的 Branch Review owner。D1 完成实际入口修复和验证后，整体 Completion 核对同一验收的证据和正式 Delivery 结果。

## 4. 本批调用方、场景与流程

**S915-1** 由处理已审候选的 Reconcile 执行者触发。临时仓库两条分支从同一起点修改同一段架构正文。Git 报告冲突后，执行者按原入口解决并暂存。原执行器形成 H。原实施 owner 保留 B 和适用 Planning，以 H 更新候选。调用方转交实际输入和回执给投影，再将投影结果交给符合独立性的 Branch Review。审核通过后两个公开结果均绑定 H。

## 5. 完整行为、条件与约束

- 保留同一 Task 和 Delivery。原执行器按当前已解决索引与选定基线创建一次整合提交；其原同操作恢复语义继续适用。
- 原实施 owner 按合法阶段接续，以固定 B、实际 H 和完整内容绑定 `begin_check`。
- `project-resolved-full-review` 接收合同规定的当前输入、实际执行结果及审核 authoring。其输出供 `guru-review-branch:delivery_branch_review` 消费。投影前无需另跑独立 Check。
- 审核覆盖真实冲突解法、组合语义和受影响消费者。仍独立的原审核者可继续。可核验且仍适用的覆盖和验证应采用，变化、缺失或适用性不明的部分应补审。
- 新增或变更细节按现行详细合同。旧的 Check 绑定投影保留在适用的固定旧提供者边界内。详细合同的约定设计处置见本 Delivery design 第 3 节。

## 6. 本批验收、验证方式与未决项

**AC915-1**。用修复后的匹配安装执行 S915-1。保留起始提交、触发输入、关键调用结果和重跑入口。核对真实冲突、一个整合提交及父顺序、原 B 与 H 的候选绑定、实际投影调用和 Branch Review 对返回输入的消费。读取同一 H 的正式 Check 和 Branch Review 结果。审核记录区分采用的旧证据与实际补充。现有 Git 和公开命令测试可供复用；仍需实际独立审核证明语义部分。没有需求选择待定。

## 7. Canonical 引用与本轮差额

现行承载见 [要求](../../../../../docs/requirements/current/task-delivery-lifecycle.md)、[设计](../../../../../docs/design/current/task-delivery-lifecycle.md)、[验证策略](../../../../../docs/test/current/task-delivery-lifecycle.md)的提交后独立审核条款，以及 [Architecture ADR](../../../../../docs/architecture/adr/postcommit-independent-review.md)。现有联合审核责任、运行时接口和历史迁移已定。本轮差额是修正进入这些既有能力的受管指导，并提供本 Issue 要求的重跑证据。
