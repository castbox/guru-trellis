# #822 D1 五字段启用的流程验证与增量接续

## 1. 整体来源与术语

整体要求见 [Task PRD](../../prd.md) R1–R5。当前公共 accepted_scope 指向该 PRD，Delivery 的 scope_ref 选择 AC1 和 AC2。使用 [#822](https://github.com/castbox/guru-trellis/issues/822) 的行为、验收和顺序作为要求。使用 [业务 PR #1468](https://github.com/castbox/ai-chat-roleplay-backend/pull/1468) 和 [业务 Issue #1281](https://github.com/castbox/ai-chat-roleplay-backend/issues/1281) 作为案例背景与依赖证据。基线为 `ffbc25e32e65fa843c0ff0d75a9f16f0e0f0ea8f`。

## 2. 整体与本批目标、非目标

本批从受支持的 Agent 入口验证去敏五字段启用及其接续。根据当前行为证据只修补实际发现的恢复导航、增量规划或验证承接缺口。本批覆盖整体 R1–R5。原业务仓库、实际 Test 部署、生产启用和独立 CI 维护由原职责负责。

## 3. 本批起点、前序结果、依赖与剩余责任

本 Task 的 D1 无前序 Delivery。验收场景中的已交付计费实现由独立去敏案例复现。业务 PR #1468 合入 dev 是案例历史事实，原主线程和历史安装版本未知。当前流程已有明确对象续接、选中原切片、固定基线与证据适用性规则。本批先验证这些能力能否覆盖案例的正常调用。整体验收以实际观察和变化的受管投影为依据。

## 4. 本批调用方、场景与流程

**DS1 新启用切片。** 在已有已交付实现的样本 Task 中，用户请求按整体 AC1 启用五字段。Agent 读取实际前序结果与当前 scope，判断需新增切片，然后从原 Creation 进入 Author。Author 只展开本次配置差额及检查，采用仍适用的初始实现、资金精度、索引和预算证据。

**DS2 同切片接续。** 在切片已有规划或验证结果后，从另一个受支持的接续入口恢复同一 Delivery。Agent 核对明确 key、当前义务和原前置结果，按原 owner 补缺后继续。证据充分即转入提交与审核。进度以实际当前阶段及其剩余条件报告。

## 5. 完整行为、条件与约束

R1 与 R3 使用实际公共 Task/Delivery、唯一 continuation 和现有合同查询定位下一步。原切片或前序结果不能适用时，报告具体缺口并交对应 owner。R2 判断五字段差额对已有证据的影响，保留可定位引用。R4 检查当前必需的精度兼容、物理索引、预算配置和加载路径。只执行覆盖缺口的定向实验。R5 区分当前 Git、审核与流水线状态。现有必要阶段与公共接口保持。对当前差额的处理遵循原 Authority 所有权和受管投影。

## 6. 本批验收、验证方式与未决项

- **DAC1（AC1，DS1–DS2）。** 通过受支持入口执行去敏五字段案例，观察后续切片与已有切片恢复。确认增量计划、证据采用、定向验证及实际交付阶段。旧证据不足时核对缺口是否由对应检查补足。
- **DAC2（AC2）。** 对实际修订执行必要的包、安装及平台投影一致性检查。有兼容差额时核对迁移说明与有关行为。
- 当前未决项是案例中实际发生的承接缺口及其所在 owner。Implementation 按现有入口验证并收敛修订。历史原因保持未知。

## 7. Canonical 引用与本轮差额

[Task/Delivery 生命周期](../../../../../docs/design/current/task-delivery-lifecycle.md) 定义 Creation 和 Planning 进入、接续与 owner 边界。[行为验证方法](../../../../../docs/test/current/behavior-validation-method.md) 定义现有证据采用与必要诊断。Architecture 影响判断依据为项目 [Architecture Baseline](../../../../../docs/architecture/README.md)。当前提出复用既有机制，从正常行为观察确定局部差额。
