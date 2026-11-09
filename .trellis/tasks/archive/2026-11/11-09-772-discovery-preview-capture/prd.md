# Discovery 大历史预览完整捕获与截断恢复：整体需求

## 1. 来源与术语

| 来源 | 章节／角色 | 本 Task 用途 |
| --- | --- | --- |
| https://github.com/castbox/guru-trellis/issues/772 | 完整正文；Direct Source 要求及原始会话证据 | 唯一整体范围与验收依据 |
| `trellis/skills/guru-team/packages/guru-discover-change-context/references/contract.md` | Forward Behavior、History Preview、Invocation；现行合同 | 保留 AI 判断、公开 I/O 和失败出口 |
| `trellis/presets/guru-team/spec/workflow/companion-scripts.md` | Reading Required Contracts In Full、Intermediate Command Stdout；共享规则 | 内外工具预算及 receipt.result 读取 |

preview 指原公开历史预览命令的完整 JSON 回执。展示指工具实际交给模型的文本；展示可以少于完整捕获数据。完整数据只保留在当前调用内存。

## 2. 背景与问题

Issue 记录 Backend #1175、Mobile #407 两次正常 preview 返回成功后，模型因展示截断而停止 Discovery。原 owner 使用内存中的完整 JSON、紧凑候选摘要及补读后均能返回 context_ready。Codex 日志持久化截断属于独立平台事实，日志摘录不能作为完整 JSON 重放。

main@fd52fbd69a8161d037bf6d4548b04b7247b60c03 的合同后段已有完整捕获指引，但主入口和正向步骤未提供直接可执行路径。本次正常预览也达到 462,322 字节、20 个候选，说明大结果是正常输入。

## 3. 目标与非目标

让 Discovery 在正常展示预算下完整取得候选事实，完成每个候选的 AI 判断、选中证据深读及原 Gate、record/check/invoke。展示截断时自主恢复，不请求用户继续。

范围为 canonical Skill、正向步骤、可执行示例、必要共享引用及原安装 owner 管理的 dogfood／声明平台投影。整体完成包括定向验证、交付和 Task 闭环。

不调整评分或相关性、固定候选上限、freshness、public DTO；不修改业务仓库、Codex 工具或日志机制；不新增缓存、checkpoint、tracked 预览证据、授权记录、锁或重试框架。不执行完整多平台安装矩阵或 Release Gate。

## 4. 真实调用方、场景与流程

| 场景 | 调用方／前置与触发 | 行为及可观察结果 |
| --- | --- | --- |
| S1 大预览 | 当前 Discovery owner 完成当前态调查后运行公开 preview | 完整捕获 stdout，确认成功后解析 receipt.result；模型逐批读取全部候选的 ID、路径、命中线索、问题及结果 |
| S2 信息过长 | 紧凑批次或候选字段仍超展示容量 | 缩小批次或按候选／字段补读；AI 完成每个返回候选的选择或排除判断 |
| S3 仅展示截断 | 命令已成功，展示缺少信息 | 优先复用内存完整结果；丢失时保持原固定基线与查询同范围重取，再继续同一次 Discovery |
| S4 实际失败 | 命令失败、真实来源缺失或 stale/mismatch | 保留真实状态，沿现有 owner 出口处理；不以捕获示例掩盖失败 |

## 5. 行为要求

- R1（S1）：主入口和正向步骤前置完整捕获→成功检查→解析 receipt.result→分批展示的路径，并提供可执行示例。数据捕获与模型展示分离。
- R2（S1/S2）：展示保留候选 ID、归档路径、命中线索及足够内容。剩余长字段可定位补读。每个返回候选均由 AI 判断；脚本不选择候选、不判断充分性、不静默丢弃候选。
- R3（S3）：展示截断不等于业务前置缺失、无候选、semantic pass 或最终阻塞。当前 owner 自动补取并继续原固定基线、原查询；恢复性同范围重取与重新宽泛调查明确区分。
- R4（S1/S4）：示例区分 shell 返回预算和外层展示预算；不能对先已截断的文本 JSON.parse。捕获完整 bytes 后统一 UTF-8 解码，或使用保留字符边界的流式解码。正常失败保持原处理。
- R5（全部）：候选判断后继续原 Gate、record/check/invoke 并消费实际 typed exit。public I/O、评分、20 候选上限、freshness 和证据职责保持现有合同。
- R6（全部）：通过原安装 owner 同步 dogfood 和声明平台。使用调用内存及已有读取机制，不新增预览缓存或状态。

## 6. 约束与依赖

Markdown 负责过程与语义判断，脚本仅捕获、解析、展示确定性事实。复用现有公开 preview、source reader 和 record/check/invoke；不调用私有 runtime 构造派生字段。共享工具预算规则是唯一共享来源，Skill 定义自己的直接执行路径。

原 Task/session 必须在投影同步时保留。没有数据／schema 迁移或部署配置变化。完整安装矩阵由专门升级或 Release Gate 承担。

## 7. 可观察验收与验证方式

| 验收 | 要求／场景 | 入口、输入与预期结果 |
| --- | --- | --- |
| AC1 | R1–R5；S1–S4 | 完整审读主入口、正向步骤和示例；先完整捕获再解析、全部候选判断、自动同范围恢复、两层预算及原失败出口均明确 |
| AC2 | R1–R4；S1/S2 | 执行公开示例一次，使用超过选定展示预算的正常真实大归档预览；完整 JSON 可解析，紧凑批次未截断，全部返回候选按 ID 可定位补读 |
| AC3 | R5/R6 | 原安装 owner 同步投影，运行受影响文档／示例、分发及 dogfood drift 定向检查；受管内容一致 |

未修改的小输出、无候选、命令错误及 record/check/invoke 逻辑复用现有适用证据。若实际改变这些行为，按影响补验。复用 Issue 已有真实会话失败和恢复证据，不重演两个业务会话，不新增 native Agent 评测或完整 Intake consumer 验收。工具示例与静态／分发验证不宣称生产会话效果已重验。

## 8. 实际未决项

无需求未决项。具体捕获工具、分批容量和字段补读安排由 Delivery Author／Architecture 在上述边界内细化。
