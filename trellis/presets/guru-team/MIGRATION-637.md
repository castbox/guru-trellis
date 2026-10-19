# #637：候选审核与验证复用的匹配迁移

本次直接演进现有 Markdown 控制面。唯一共享定义是
[Candidate Applicability And Coverage](spec/workflow/workflow-contract.md#candidate-applicability-and-coverage)。
Architecture、Check、TaskCommit、Branch Review、Delivery Review、Publication 和
Merge 保留原职责、公共 profile/exit、输入输出结构及确定性 runtime。
没有新增覆盖字段、reviewer 身份账本、兼容 reader、缓存或长期证明链。

## 旧条款退出与保留条件

| 原执行点 | 当前替代与保留 |
| --- | --- |
| Architecture 每个后继候选或阶段均重新派 fresh reviewer | 首次仍用独立子 Agent 和原 first-read order。合规独立 reviewer 可接续后继候选，并依次承担 Architecture 与 Branch Review；各阶段仍实际判断并正式调用。新架构事实需要相应独立评估，证据不足补审，组合影响无法界定则完整评估。 |
| Check finding 修复后 full-rerun、后继覆盖只能走引用对齐 | 所有九维度和完整当前 scope 继续成立。原覆盖、全部差额和受影响依赖形成当前 Check，变化、新增、缺失或不明的命令补跑；保留其它可验证事实。 |
| Branch finding 闭合后必须 distinct fresh reviewer 完整相同重审 | 实际独立 reviewer 验证闭合、修正差额及受影响覆盖，随后形成当前最终完整结论。同一合规 reviewer 可以执行这两个判断；闭合不是通过。 |
| 新 HEAD、阶段、reviewer 或目标前进触发全链重建 | 当前 owner 按共享合同判断真实影响。首次完整独立审核、精确当前范围和原结果绑定继续必需。无关 target 前进不触发整合；真实冲突读取双方语义、组合影响和未改 consumers。 |
| Delivery Review/Publication/Merge 重建已适用内容理解 | 各自判断当前 payload、Issue 语义、候选和 live facts，消费适用内容审核。原预览、required checks、expected HEAD、副作用确认和事务读回继续成立。 |

原 `delivery_promotion_reference_alignment` 仍限于它声明的引用/状态对齐输入。
一般后继内容变化使用原 full-review profile，不能扩大该窄入口的范围。
`delivery_base_continuity` 仍只是有界整合判断，不能替代首次完整 Review 或当前
正式 full_review。#636 的早期 Draft 分析仍不写最终 gate；最终 Check predecessor
及正式 Review 继续真实取得。

## `fresh_final_review` 的显式后继含义

保留原 schema/wire literal `review_intent=fresh_final_review`。在采用本完整匹配
合同后，它表示“finding 闭合之后，对当前精确候选形成的最终完整覆盖判断”。
它不再表示必须换一个 reviewer，也不要求无条件重读或重跑已覆盖内容。
这是一项明确的行为替代，不是等义润色或 enum 别名。

原 `introduced_head`、`fix_head`、后继 `closure_head`、`review_commit` 的 ancestry
与 recorder/checker 绑定继续执行。仍需真实闭合证据、当前完整覆盖和正式入口；
旧 pass、旧 token、修复声明或闭合结果不能转换成新 pass。原 owner 只在其现有
summary/evidence 中说明保留、失效与补充范围，不增加字段或保存 reviewer 过程。

初次 `implementation_required` 没有 passed full_review。commit/finding refs 只
定位对象和缺陷。可采用的原审核工作必须仍能通过实际 public 结果/调用对象、
精确 Git 和当前正文核验。原 reviewer 的理解可减少重复读取，但不能补造权威。
缺覆盖补覆盖，组合影响无法界定则完整审核。

## 完整安装与同 Delivery 在途恢复

旧安装继续使用其完整固定合同，或经原升级/工具维护 owner 成套切换 matching
workflow、preset managed spec、七个 packages 和受控 consumers。即使 wire 结构
相同，也不得仅替换一份 Skill 后悄然采用新语义。当前开发 Task 的 source 编辑、
dogfood apply 或验证位置安装不构成其活动 runtime 切换。

1. 由原 owner 核当前 TaskId/generation、DeliveryKey、planning_root、固定 B/H、
   实际阶段和未完成事务。身份保持，不新建 Delivery 或空提交。
2. 已执行的 commit、PR、Draft/Ready 或 merge 若丢失输出，先经匹配原 producer
   恢复真实结果；不得为切换重放副作用。已有语义输出只在当前适用时消费，
   缺失输出沿原 producer 重新实际判断及正式调用。
3. 完整安装切换后，原阶段 owner 读取合法公开结果、全部实际差额、当前正文和
   可核验原命令。若旧 pass 仍可定位，它仅提供原覆盖；当前结果必须重新判断。
   已消费 private checkpoint 不重建、不跨 owner 读取。原 private 状态仍只由其
   owner 按原恢复与退休合同处理。
4. same-tree 只刷新必要 binding，不证明工具链、环境或 required checks 未变。
   原工程结果不可得时补跑命中项。真实 authority、scope、设计前提或依赖变化
   回最早受影响 owner，不能靠切换合同豁免。

安装仍用官方 marketplace preview/显式应用和完整 preset apply/reapply。保留用户
内容与 managed hashes，逐项处理 `.new/.bak`。有冲突或不支持的旧输入时保留原
安装并沿原 owner 诊断；不新增 parser fallback 或自动迁移脚本。回退通过原升级
owner 的精确 write set 恢复完整旧安装，不把新结论当旧 pass。

## 验证与边界

定向验证分别报告 public wrapper/Git、实际独立 Agent、工程命令、安装投影及真实
远端结果。样本覆盖首次完整、同树/定位、无关目标前进、文档冲突组合、共享依赖
检错、缺命令补跑、private 退休和 finding 闭合。同构耗时分语义工作、命令执行、
正式记录和远端等待，不预设收益比例。scanner 或 fixture 不证明实际 Agent 判断。

命中组合采用 #636 已实际可用的 installed early TaskCommit/Publication/Review
接口。#638 未来接口明确未验证，由后交付项负责；本迁移不等待其关闭，也不声称
Backend 业务采用、生产效果或完整多平台 Upgrade/Release 矩阵已验证。
