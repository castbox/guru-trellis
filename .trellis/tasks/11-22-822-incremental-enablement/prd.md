# #822 Task 内小范围启用的增量接续

## 1. 来源与术语

| 来源 | 角色 | 用途 |
| --- | --- | --- |
| [Guru Trellis #822](https://github.com/castbox/guru-trellis/issues/822) 的行为要求、验收、实施顺序与关联 | 直接需求 | 定义 Task 内后续启用、接续、证据复用及交付边界 |
| [业务 Issue #1281](https://github.com/castbox/ai-chat-roleplay-backend/issues/1281) 与 [业务 PR #1468](https://github.com/castbox/ai-chat-roleplay-backend/pull/1468) | 历史事实与案例来源 | 提供已合入实现、Test 启用条件及配置差额背景 |
| [#819](https://github.com/castbox/guru-trellis/issues/819)、[#736](https://github.com/castbox/guru-trellis/issues/736)、[#692](https://github.com/castbox/guru-trellis/issues/692)、[#818](https://github.com/castbox/guru-trellis/issues/818)、[#850](https://github.com/castbox/guru-trellis/issues/850) | 相关交付与约束 | 复用适用的 Intake、上下文、验收和写作职责 |

Task 表示已接受的整体范围。Delivery 表示 Task 内一个可独立判断的交付切片。

## 2. 背景与问题

业务案例的计费运行实现已合入 dev，后续在 Test 采用新配置前仍需核对实际依赖。#822 记录补丁准备到定向检查约 31 分钟、Delivery 创建到激活约 25 分钟。时间来自结果文件。历史主线程及安装版本缺失，无法还原逐阶段耗时或归因。本 Task 通过当前基线验证接续与证据复用的剩余差额。

## 3. 目标与非目标

既有实现已经交付、后续配置差额明确且证据可定位时，Agent 应从当前义务继续，完成必要的增量规划和验证后进入交付。整体 Completion 核对 R1–R5 和 AC1–AC2。

交付对象为 Guru Team 流程。本 Task 的验证使用去敏案例。业务仓库配置写入、实际 Test 或生产部署、独立 CI 修复以及其他部署由原业务或发布职责承担。

## 4. 真实调用方、场景与流程

**S1 后续启用。** 用户从受支持的 Agent 入口请求启用已有实现。前序 Delivery 已交付，启用目标和证据可定位。Agent 确认当前 Task 与实际 Delivery 结果，判断剩余义务，再用原 Creation 和 Planning owner 处理后续切片。必要检查满足后进入提交和审核。

**S2 恢复当前切片。** 工作在一个已选 Delivery 内中断后，Agent 从原 continuation 读取同一 Task、Delivery 和当前阶段。已完成且仍适用的调查、规划和检查继续供对应 owner 使用。证据失效或覆盖存疑时补当前缺口，完成后返回原阶段。

## 5. 行为要求

- **R1 接续身份。** 原 continuation、Delivery 和规划 owner 按实际 Task、Delivery 与现有结果判断义务。恢复已有切片时保留身份、阶段与适用结果。仅在确需后续切片时采用原创建入口。换会话或执行者以及后续切片成立本身不要求重查未变事实。
- **R2 增量规划。** 规划正文具体写本批目标、配置差额、边界、缺口和执行安排。逐项判断前序 evidence 对当前版本、条件和依赖的适用性。引用可定位的已有能力和证据，只补受影响或覆盖存疑的部分。
- **R3 恢复导航。** 采用现有 `discover-skill-contract` 和原 owner 的恢复入口定位下一 owner、profile、输入来源、schema 或模板。导航适配限本场景证实的缺口。
- **R4 定向验证。** 原验证 owner 选择最小充分检查和停止条件。五字段案例检查资金精度兼容、必要索引、模型预算及配置加载的适用性和实际缺口。新增诊断须回答具体未决问题。证据充分即进入交付。合并后的自动 CI/CD 按原流程执行。
- **R5 进度如实。** 说明当前结果、剩余阻塞与下一动作。规划、提交、审核、合并、CI、部署和实际生效各按实际进度报告。

## 6. 约束与依赖

沿用当前必要的规划、架构、批准、措辞质量和交付职责。#850 已将日常措辞质量纳入现有职责。使用 #736、#819 和 #692 已交付且仍适用的能力。#736 整体完成、历史主线程和现场版本均非本 Task 的前置。保留公共 API 语义，实际调整时同时明确兼容或迁移。

AI 判断范围、证据适用性、充分性和路由。脚本负责确定性定位、投影与校验。持久化载体沿现有职责使用。改动受管投影时，由原安装 owner 同步。定向验证以差额为界，采用仍适用证据。

## 7. 可观察验收与验证方式

- **AC1（S1、S2；R1–R5）。** 用受支持的 Agent 入口观察已有计费实现交付后，Test 五字段的去敏启用及同一工作的接续。输入为 `exact_text_pricing_version="exact_billing_r4"` 及既有 Test 文字模型的 `context_window_tokens=1048576`、`reply_reserve_tokens=0`、`budget_version="test-gemini-3.5-flash-lite-context-v1"`、`budget_counting_method="provider-context-rejection-v1"`。观察 Agent 识别剩余义务、采用适用证据、只补增量规划和检查。验证充分后，流程进入对应交付阶段，进度与实际阶段一致。
- **AC2（R3–R4）。** 核对实际受影响合同、canonical 源、dogfood 和声明平台投影一致。验证方式由改动和已知证据决定。若涉及公共合同，核对明确的兼容或迁移。回归和证据失效补测按实际影响选择，不以固定矩阵或耗时作为验收。

## 8. 实际未决项

当前基线的五字段接续还缺真实 Agent 路径证据。Delivery Planning 选择正常入口和有效观察条件，按实测确定存在的承接缺口。历史归因保持未知。
