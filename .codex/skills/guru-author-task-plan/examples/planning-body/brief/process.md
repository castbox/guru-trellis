# 简略来源的调查、裁剪与审核修订

本目录是教学材料，不是实际工具轨迹或真实用户答复。先读 [source 全文](source.md)，再形成 [Task PRD](task-prd.md)、[D1 PRD](delivery-prd.md)、[D1 design](delivery-design.md)、[D1 implement](delivery-implement.md)。示例正文不作为实际 Agent 测试输入的预写答案。

## 调查先于澄清

输入只有“显示已有output用途和默认目录，行为保持”。不能直接问用户默认目录是什么。Discovery应先查parser注册、build调用、现有测试、usage和canonical约束。source §2给出教学摘录：默认dist、已有目录失败、help被SUPPRESS隐藏、--help不执行build。因此当前事实足以形成要求，无真实产品选择，不编造一次用户确认。

如果实际事实不可查或冲突，则沿source §3留下具体gap，由原Clarify处理真实选择，未答时停止相关接受出口。Author可继续不依赖该答案的调查，不能把假定默认值写为要求。如何改argparse的help参数属于Author/Architecture技术细化，不要求用户提供方案。

## 整体、切片和裁剪

范围是一个可独立交付的help修复，选择full D1；首次无前序，无另留责任。为一个help文本拆成“先参数、后说明”不形成有意义独立交付，故不拆。仍保留D1的起点、排除项、Completion关系和实际验收安排。复杂部分/后续模式见 [详细例切片](../detailed/slices.md)，不能把它们当本例历史。

design保留九节，但接口只写argv→argparse help→stdout/exit0；无新数据schema，不造状态机。恢复/兼容/迁移逐项说明无持久化和无旧接口变化的理由。无规范性来源设计，design第3节写依据而不放空表。没有必要未决项，如实说明。

## 一次具体审核与修订

初稿I1曾计划把默认值从dist改为build并同步help，以“名称更清楚”。原审核应指出这违反“现有行为保持”和已查出的默认dist，不是等义措辞。Author应回到原要求，取消默认值改动；若真有改默认目录的意图须经Clarify，而不能以技术细化自批。

最终 [design 第4、5节](delivery-design.md#4-模块职责与设计取舍) 仅替换help参数，保留default/metavar/参数解析和build。最终 [implement I1/V2](delivery-implement.md#2-有依赖顺序的步骤与文件责任) 明确只改help，并复用原默认/显式/存在目录测试验证行为保持。这里展示具体初稿错误与最终落点，不声称真实owner已接受或测试已通过。

本例没有规范性来源设计和新机制；修订恢复原行为，原owner按实际影响刷新相关gates。新会话读取当前来源与这些必要引用；不得复用本例的教学快照当live事实。

本例没有跨批临时限制。原 owner 只维护 help 的实际差额并复用适用回归，不增设限制清单、空贡献或额外状态验证。
