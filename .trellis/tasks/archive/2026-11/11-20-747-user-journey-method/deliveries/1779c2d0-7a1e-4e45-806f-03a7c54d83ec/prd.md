# D1 连续操作与阶段交接

## 1. 整体来源与术语

整体 PRD 位于 [Task 范围](../../prd.md)。本批 scope_ref 指向该已接受范围的 JQ-R1、R2、R5、R6、AC1、AC2、AC6、AC7 和 AC8。直接来源为 [#747](https://github.com/castbox/guru-trellis/issues/747) 的交付切片、行为要求、约束与兼容、方案与职责、实施顺序、验证和验收。术语继承整体 PRD。来源设计处置见本批 design 第3节。

## 2. 整体与本批目标、非目标

本批使 Clarify 从真实入口推导连续正常动作，使 Author 明确阶段交接业务条件，并使原 Architecture 和 Approval 核对条件能否成立。各适用原审核职责独立形成关键检查问题。D2 的验证顺序和证据有效性留给后继切片。流程、owner、公共接口和整体排除项沿用整体要求。

## 3. 本批起点、前序结果、依赖与剩余责任

当前没有前序 Delivery。main 已有 Clarify 来源和正常场景规则、Author 写作合同及 #717 共用审核充分性规范。在当前正文承接新方法。V1 使用中性多阶段编辑材料和真实原生 Agent。D2 可以采用独立且来源明确的已定义旅程，不依赖富媒体样本的产品答案。Task 整体 Completion 还需要 D2 的交付结果。

## 4. 本批调用方、场景与流程

- JQ-S1。Clarify 遇到有多阶段操作的来源，通过真实入口识别具体起点、阶段、允许动作、等待期间的正常再次操作及成功、失败或放弃结果。由原入口处理真正未决的产品选择。
- JQ-S2。Author 展开跨状态、持久化或资源交接，在所属正文说明条件、时序、writer/reader 及失败后归属。Architecture 和 Approval 先从适用权威形成检查问题，再判断候选能否兑现。
- JQ-S5。现有 reviewer 在其规定的首读顺序中形成行为和关系问题，然后对照候选及后读总结。沿用各阶段独立性和原证据复用合同。

## 5. 完整行为、条件与约束

Clarify 只展开适用的动作和结局。无交互任务使用其真实调用方。既有行为作为事实，待决产品选择保持待决；新增场景沿原资格规则。

Author 根据本批实际行为区分局部确认、后台任务完成、可靠保留、最终提交等阶段。交接涉及状态或资源时，写明跨阶段条件、先后动作、实际 writer/reader 和失败后归属。Architecture 与 Approval 按各自权限检查正常操作中条件能否维持，技术交接修订由技术 owner 处理。通用锁、并发压力和异常 crash 协议在范围外。

原 reviewer 从当前来源或职责 authority 自行形成问题。调用方提供必要来源与候选，不预置 findings 或通过叙述。共用方法保留顺序、隔离、已有适用证据、资格规则、角色和轮数。相关结果落在已存在 PRD/design/implement 正文，保留历史原义并记录必要证据范围。

## 6. 本批验收、验证方式与未决项

- V1 实际原生 Agent 按 Clarify/Author 方法读冻结中性材料。应展开上传中再次编辑、局部确认后退出、恢复与最终保存，区分事实、真实未决和设计职责；从实际动作与资源归属发现候选引用交接空档。同一 V1 素材另由未参与写作的原生 Agent 按原 Approval 审核方法核对候选。独立评价者对照两份实际原始记录，覆盖 JQ-AC1/2 和本批 AC6/8。
- V5 执行所影响规划正文、审核充分性和包的定向分发、安装/reapply 检查。V6 以 local_candidate 运行原 Upgrade Tools 和受管所有权、drift、工具 smoke。两项证明 JQ-AC7 的 D1 投影，不代替语义观察。
- 当前没有待定产品选择。原生入口或受管投影缺口保留原结果。依赖缺失的验收保持待验证，独立工作继续。

## 7. Canonical 引用与本轮差额

[要求](../../../../../docs/requirements/current/behavior-validation-method.md)和[审核要求](../../../../../docs/requirements/current/review-sufficiency.md)承接正常连续动作与独立问题推导。[设计](../../../../../docs/design/current/behavior-validation-method.md)和[审核设计](../../../../../docs/design/current/review-sufficiency.md)承接原方法的各自落点。[测试](../../../../../docs/test/current/behavior-validation-method.md)和[审核测试](../../../../../docs/test/current/review-sufficiency.md)承接 V1 与必要分发。[架构域](../../../../../docs/architecture/03-domains/review-sufficiency.md)记录原 owner 的方法消费和交接责任。本批推进上述单元的必要差额。
