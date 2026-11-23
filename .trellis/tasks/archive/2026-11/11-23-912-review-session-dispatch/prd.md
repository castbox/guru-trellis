# 正式步骤跨会话交接整体需求

## 1. 来源与术语

[Issue #912](https://github.com/castbox/guru-trellis/issues/912) 定义交付要求和验收。#651、#679、#694 分别说明独立评审载体、接收会话续接及 final_plan 只读入口。接收会话是实际调用正式入口的会话。Task 绑定和 Delivery 选择分别记录该会话的任务及交付对象。

## 2. 背景与问题

go-guru #542 的新 Architecture 候选评审和 Branch Review 子会话均在正式入口上遇到缺少匹配会话状态的问题。派发交接了候选对象，却未安排在首次调用前完成接收会话前置。经正式 Bind 和 Selection 后，同一 Architecture 评审取得正式结果。

## 3. 目标与非目标

覆盖现行支持的跨会话首次派发、替换接续和主会话接回。修复需要接收会话绑定或选择的入口及派发职责冲突。沿用现有会话隔离、语义 owner 和身份校验。独立只读和仅提供工程证据的入口沿用各自合同。

## 4. 真实调用方、场景与流程

S1 主会话派发新的独立 Architecture 候选评审者或正式 Branch Review 评审者。
S2 实际正式调用者替换或主会话接回原结果，准备继续同一 Task 或 Delivery。
S3 接收会话已绑同代 Task、已选匹配 Delivery，或已有不同合法选择。

## 5. 行为要求

R1 派发明确实际调用者、原入口、目标 Task/generation、注册 checkout 及适用 DeliveryKey，在首次依赖会话状态的正式调用前执行当前会话续接。
R2 缺 Task 时按原 owner 核对身份和 checkout，建立必要绑定。仅缺 Delivery 选择时选中明确的已有 Delivery。复用匹配状态。保留不同、过期和真实冲突的具体诊断与原 owner。
R3 派发允许原 owner 执行必要会话状态写入。独立评审维持候选与语义判断边界。正式结果交原消费者。
R4 核查规划、实现、审核、交付和收尾的真实派发与接回，按实际入口的 Task-only、Delivery 或显式只读合同处理。

## 6. 约束与依赖

现有 Identity、Ensure、Bind、Selection 和正式阶段 owner 承担既有职责。保留 final_plan 的只读显式对象入口及工程协作者职责。

## 7. 可观察验收与验证方式

AC01 同一已选 Delivery 的主会话从正常派发启用两个新的独立评审者，分别在候选评审与提交后 Branch Review 的首次正式调用以前满足各自前置，再产生该候选的正式结果。
AC02 验证仅缺 Delivery 选择、复用匹配状态、保留其他合法选择及 Task/显式只读适用边界。
AC03 枚举现行实际派发和接回入口，确认调用会话、所需状态、检查时机与原 owner。为独立差异补充定向验证，共享路径复用证据。

## 8. 实际未决项

需求范围和验收已明确。具体落点由 Delivery 方案和独立 Architecture 评审收敛。
