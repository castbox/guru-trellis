# #847 Planning union 字段诊断整体需求

## 1. 来源与术语

Direct Source：[Issue #847](https://github.com/castbox/guru-trellis/issues/847)，以完整当前标题、正文和已接受复审评论为准。

| 来源 | 章节 | 角色与用途 |
| --- | --- | --- |
| Issue #847 | G03 的问题范围 | 要求及历史事实：区分共享诊断缺陷与普通调用错误，保留各项责任 |
| Issue #847 | 当前缺陷与复现 | 缺陷证据：双向 Planning 错层及合法输入对照 |
| Issue #847 | 根因与推荐方案 | 因果证据及建议：在原共享 owner 内细化 const 定位；明确的回退和职责约束仍须保留 |
| Issue #847 | 兼容边界与验收 | 要求：合法性、错误结构、引用解析、验证与同步边界 |
| [复审评论](https://github.com/castbox/guru-trellis/issues/847#issuecomment-6890790098) | 完整评论 | 要求及复审事实：承接对称场景、既有 const 声明及不能唯一定位时的原回退 |
| `.trellis/tasks/archive/2026-11/11-09-766-union-exit-diagnostic/prd.md` | 第 5–7 节 | 前驱约束：保留出口定位、字段诊断、相对引用和真实歧义回归 |

union 指 JSON Schema `oneOf` 或 `anyOf`。诊断选择仅在完整校验失败后选择展示的约束，不决定输入合法性或业务路线。`final_plan` 和 `candidate_assessment` 是既有 `planning_purpose` 值。

## 2. 背景与问题

当前 `trellis/skills/guru-team/runtime/schema.py` 的 `_diagnostic_error` 优先按 `exit_id` 常量匹配分支，随后使用唯一最少错误数和 `best_match` 回退。Architecture Planning 输入没有 `exit_id`；真实 aggregate 4.0 使用 `planning_purpose` 常量区分两种设计路径布局。

final-plan 的顶层 `design_locator` 被误放入 `candidate.design_locator` 时，完整校验正确拒绝。实际用途分支有多余与缺失字段两项错误，另一个用途分支只有 const 错误，因此当前诊断误导调用方切换用途。反向错层也有对称问题。期望保留用途，指出实际布局错误。

Issue 的旧安装为 `0.7.0-guru.8@8c158381…`，复审固定源码为 `ac1c823857ad6695c106daeedd25aafce4c50934`。这些是历史证据，不用当前规则否定旧故障。此次采用 `0fb7dc9aac817a684c2f95bebb6570061a5ef868` 的实际源码；已读共享实现仍有同一缺口。历史隔离分支实验不代表候选算法已实现或安装已验证。

## 3. 目标与非目标

整体目标：修复共享诊断器的误导方向，让普通调用方在错误布局被拒时看到可纠正的字段，同时保留完整校验与既有回退。

Task 承担共享实现、双向真实 schema 回归、受影响既有回归、canonical 与安装副本的原 owner 同步，以及相称 source/installed 和 drift 证据。整体 Completion 核对这些责任，不以提交或 PR 合并替代。

不承担 #848、全部 G03 返工消除、所有调用错误自动修复、新 DTO 字段、放宽闭对象、自动删字段或切换用途、新 wrapper 或语义 gate、任意 JSON Schema 推断框架、第二套引用解析器、完整业务交付或云端调用、多平台 Throwaway/升级/Release 矩阵。排除恶意输入、伪造 artifact、竞态压力与无来源加固。

## 4. 真实调用方、场景与流程

调用方是按既有 Architecture public input 组装 Planning 输入的 Agent。原入口先执行完整 schema 校验；失败后共享诊断器解释失败，调用方修正原输入并重试原入口。

| 场景 | 前置条件与动作 | 处理及可观察结果 |
| --- | --- | --- |
| S1 | 合法 `stage=planning / planning_purpose=final_plan`，顶层设计路径被普通组装错误移入 `candidate` | 仍拒绝；定位 `candidate` 多余或 `design_locator` 缺失，不要求切换用途 |
| S2 | 合法 `candidate_assessment` 原使用 `candidate.design_locator`，路径被误移到顶层 | 仍拒绝并定位实际字段，不要求改为 `final_plan` |
| S3 | 仅修正 S1/S2 的字段层级，保持用途和其余合法字段 | 原生产 schema 校验通过 |
| S4 | 声明缺失、冲突或不足以唯一确定分支 | 保留现有最少错误选择和 `best_match`；原本真实歧义仍在 union 层级报告 |
| S5 | 既有 #766 出口、嵌套 union、相对引用或普通字段错误 | 保留已有诊断及不回显提交值约定 |

## 5. 行为要求

- **R1（S1/S2）**：既有 const 声明足以将当前输入唯一定位到一个分支时，优先解释该分支的真实字段错误。保留用途；不按 Skill、两种用途字面值或新增注解硬编码。
- **R2（S4）**：不能唯一定位时保留原最少错误选择和 `best_match`。不得将所有未命中变成笼统 union 提示，不抹去原本真实歧义。
- **R3（S1–S5）**：完整 schema 校验继续决定合法性。诊断只解释已失败校验，不决定业务路线、成功出口或补造前序结果。错误布局继续拒绝，合法输入和成功 DTO 保持。
- **R4（S1–S5）**：保留 `schema_mismatch`、原非零退出码和 `code/field_path/remediation` 三字段错误结构。提示指出实际字段及原合同，不回显提交值；闭对象与用途不放宽。
- **R5（S5）**：保留 #766 的 `exit_id` 定位、嵌套 union 与现有相对引用解析。提取及递归限于当前真实 schema 和必要既有引用结构，由 Delivery 规划细化；不另建引用解析器或任意 schema 推断框架。
- **R6**：由原受管工具升级 owner 同步 canonical 与受影响安装副本，验证 source/installed 场景及适用 drift。源码变更不能代替 installed 采用证据。
- **R7**：保留 G03 责任映射：`freshness_identity` 外溢按 producer→consumer 投影纠正；qualifier 多传 `checkout_head/diff_locator`、漏 `planning_paths` 按当前实际 profile 组装；已有 Task 的 authority 使用 `active_task`；具体 revision 原因留 findings，稳定 route code 使用 `design_revision`；兼容运行器和 `repo_locator` 遵循原入口/locator 合同。不统一放宽参数。只有发现与本次同一选择机制有直接证据的诊断差额，才在该机制范围处理；不得推断其它现象有共同根因。

## 6. 约束与依赖

生产入口为共享 `validate_json`，实际 schema 是 `trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/schemas/public-input-delivery-task-impact-sync-4.0.schema.json`。复用当前 jsonschema 校验器已解析的 schema/错误树及 referencing 上下文。AI 保留语义 gate；脚本只做确定性解释、执行及事实校验。

本次不改变业务 DTO、持久化格式或生命周期，因此没有数据迁移。共享诊断及回归由原 owner 复用，canonical/runtime 与安装副本通过原升级入口维护。具体提取方案由 Author/Architecture 细化，不要求用户提供代码。

## 7. 可观察验收与验证方式

| 验收 | 要求/场景 | 入口、输入与预期观察 |
| --- | --- | --- |
| AC1 | R1/R3/R4，S1/S3 | 生产 `validate_json` 加载真实 aggregate 4.0：合法 final-plan 通过；错层仍非零，定位 `candidate` 或 `design_locator`，不要求切换用途；仅修层级后通过 |
| AC2 | R1/R3/R4，S2/S3 | 同入口：合法 candidate-assessment 通过；反向错层拒绝并定位实际字段，不要求 `final_plan`；仅修层级后通过 |
| AC3 | R2/R4/R5，S4/S5 | 运行受影响 #766 出口、嵌套 union/相对引用、真实歧义及字段回归；确认常量未唯一命中时保留原回退、错误结构和不回显值 |
| AC4 | R6 | 原升级 owner 同步后，在 source/installed 验证上述行为和适用 drift，无未经处理的受管冲突 |
| AC5 | R7 | 独立审核核对责任映射及实际 diff；未新增无依据 DTO、参数放宽或其它调用错误自动修复 |

只新增真实缺口所需断言，复用适用回归，不扩成任意 schema 组合矩阵。以上定义验收，当前未执行修复后验证。组件/schema 证据不称为完整 Architecture 生命周期、生产效果或 Release 资格。

## 8. 实际未决项

整体需求与验收没有阻塞性未决选择。const 提取的具体实现、Delivery 设计/执行计划及修复后的测试/安装证据由后续原 owners 完成；本 PRD 不预填通过结果。
