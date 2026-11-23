# 正式步骤跨会话交接需求

## 1. 整体来源与术语

整体 accepted_scope 指向 Task 根 PRD。本 Delivery 承接 AC01、AC02、AC03。[Issue #912](https://github.com/castbox/guru-trellis/issues/912) 是直接来源。接收会话是运行正式入口的实际会话。

## 2. 整体与本批目标、非目标

在需要会话状态的正式调用前完成接收会话前置，覆盖首次派发、换人和接回。保留只读显式对象、工程证据和原语义审批的既有职责。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首个切片。当前主分支 workflow 已规定规划接续。独立候选评审和提交后 Branch Review 的实际派发仍需统一执行前置。当前依赖是原 Identity、Ensure、Bind、Selection 及只读 continuation。交付和验收完成后无后继切片。

## 4. 本批调用方、场景与流程

S1 新独立评审者在首次依赖会话状态的调用前核对实际接收会话。S2 替换执行者或接回者按自身当前事实续接。S3 仅缺选择、匹配和不同选择分别进入原补齐、复用或冲突路径。

## 5. 完整行为、条件与约束

R1 派发携带对象、原入口及适用写入边界。R2 接收会话按原入口需求读取 Task 或 Delivery 状态，必要时经原 owner 建立或选择。R3 读回匹配事实后执行原步骤，独立评审保留候选约束。R4 核对所有现行派发及接回点，有差异时按原职责承接。

## 6. 本批验收、验证方式与未决项

AC01 新评审会话经正常派发完成候选 Architecture 和提交后 Branch Review。AC02 定向核验仅缺选择、复用、冲突、Task-only、显式只读。AC03 盘点实际入口、调用者、检查时机及续接职责。无范围未决项。

## 7. Canonical 引用与本轮差额

现行 workflow 的 Explicit receiving-session continuation 定义原接续顺序。Architecture 与 Branch Review Skill 拥有阶段条件。既有 Task/Delivery RDT 和 workflow-context 架构单元承接行为和验证差额。
