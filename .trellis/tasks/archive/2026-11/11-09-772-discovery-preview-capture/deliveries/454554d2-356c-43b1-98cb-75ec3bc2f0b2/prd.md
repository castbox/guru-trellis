# Discovery 大预览完整捕获与恢复：D1 需求

## 1. 整体来源与术语

整体权威为 `.trellis/tasks/11-09-772-discovery-preview-capture/prd.md` 的 accepted_scope，当前 scope_ref 选择 R1–R6 与 AC1–AC3。Direct Source 为 https://github.com/castbox/guru-trellis/issues/772 的完整正文（要求及验收）；现行 Discovery contract 和 companion-scripts 的工具预算、receipt规则是兼容约束。preview／展示／调用内存的定义沿整体PRD第1节。当前 planning_root 为 `.trellis/tasks/11-09-772-discovery-preview-capture/deliveries/454554d2-356c-43b1-98cb-75ec3bc2f0b2`。

## 2. 整体与本批目标、非目标

主入口尚未把已有完整捕获指引组织成可执行主路径，正常大预览展示截断后会停止。D1 全量交付：入口、正向步骤、可执行示例和安装投影，使当前AI完整取得全部候选信息后自主完成Discovery。继承整体PRD第3节的全部非目标：不改评分、20候选上限、public I/O、freshness、平台日志或业务实现，不加缓存、checkpoint或授权记录，不执行完整Release矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

首次D1，无前序Delivery。开发基线 main@fd52fbd69a8161d037bf6d4548b04b7247b60c03。现行preview、source reader和record/check/invoke均可用；真实预览可达462322字节。整体范围已接受，当前尚未实现。D1包括全部要求，无后续业务切片；整体Completion仍须检查验收、交付及来源闭环，不能以Delivery创建或合并代替。

## 4. 本批调用方、场景与流程

- S1：Discovery owner完成当前态调查后运行正常大preview；先完整捕获stdout并检查成功，再解析receipt.result，分批读取候选ID、路径、命中线索、问题和结果。
- S2：批次或字段过长时缩小展示，并按候选ID／字段补读；每个返回候选都有AI选择或排除理由。脚本不作语义选择。
- S3：仅展示截断时优先复用完整内存结果；结果丢失则用相同固定基线和查询恢复性重取，继续同一次Discovery，不向用户索取继续指令。
- S4：真正命令失败、来源缺失、stale/mismatch保留原错误与owner出口；展示截断不能代替这些事实。

## 5. 完整行为、条件与约束

R1：在SKILL主入口和Forward Behavior前置完整捕获、成功检查、解析result及按容量分批展示，并提供可运行示例。完整数据与模型展示分开。

R2：紧凑展示保留ID、路径、命中线索和足够内容；长内容按候选／字段补读。所有候选由AI判断，不静默过滤、不以脚本判断充分性。

R3：当前owner自动补取展示缺失信息，保持原基线、查询、原Discovery调用。截断不代表无候选、缺业务前置、semantic pass或最终阻塞。同范围恢复性重取不启动新宽泛调查。

R4：示例明确shell返回预算和外层展示预算。完整bytes捕获后再统一解码／JSON.parse，不能解析先已截断文本；不隐藏命令错误。

R5：选择和深读之后继续原Gate、record/check/invoke并消费实际typed exit。现行public I/O、评分、固定20上限、freshness与证据职责不变。

R6：通过原安装owner同步dogfood和声明平台；不新增预览缓存、tracked证据、runtime checkpoint或授权记录。规范性来源设计处置由本批design第3节唯一维护，当前requirements阶段不预写方案。

## 6. 本批验收、验证方式与未决项

- AC1：完整审读本批入口、步骤、示例；确认上述六条要求及S1–S4均有直接路径，失败出口不变。
- AC2：执行公开示例一次，输入真实正常大归档预览且超过选定展示预算；完整JSON可解析，紧凑批次未截断，全部候选可按ID定位和补读。复用Issue真实会话失败和恢复证据，不新增native评测或重演业务会话。
- AC3：原安装owner同步后运行受影响文档／示例、分发和dogfood drift定向检查，受管投影一致。

未修改的小输出、无候选、错误和record/check/invoke复用现有适用证据；实际改变时按影响补验。工具数据处理和静态分发证据不宣称生产会话效果已重验。无需求未决项，调用捕获和批次组织由本批方案确定。

## 7. Canonical 引用与本轮差额

- requirement/behavior：整体PRD第4–7节及Issue目标/验收；本批完整覆盖。
- design：`trellis/skills/guru-team/packages/guru-discover-change-context/references/contract.md` 的Forward Behavior、History Preview和Invocation；差额是前置捕获及恢复执行路径。
- test：同包tests/test_contract.py与公开示例；现有结构检查保持，补真实大预览示例执行。
- Architecture：`docs/architecture/README.md` 及其current/domain权威由独立Architecture owner先读再评估；不凭本PRD断言无影响。
- 共享预算：`trellis/presets/guru-team/spec/workflow/companion-scripts.md#reading-required-contracts-in-full`；复用两层预算，不另造共享规则。
