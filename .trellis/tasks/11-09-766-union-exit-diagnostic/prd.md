# #766 嵌套 union 字段诊断整体需求

## 1. 来源与术语

Direct Source：[Issue #766](https://github.com/castbox/guru-trellis/issues/766)，以当前完整正文为准。

| 来源章节 | 角色 | 用途 |
| --- | --- | --- |
| 背景与问题、当前证据与根因 | 历史事实及当前机制证据 | 界定普通输出组装错误与诊断选择偏差；不推断整个事故会话耗时 |
| 解决方案 | 约定设计 | 根据既有固定 `exit_id` 常量唯一匹配分支，复用校验器引用上下文和错误树 |
| DTO、兼容与范围边界 | 要求 | 保持合法性、公共结构及职责边界 |
| 最小验收 | 要求 | 生产 schema 复现、歧义回退与共享诊断回归 |

union 指 JSON Schema 的 `oneOf` 或 `anyOf` 组合。诊断选择仅确定应展示的失败约束；完整 schema 校验仍决定输入是否合法。

## 2. 背景与问题

`trellis/skills/guru-team/runtime/schema.py` 的 `_diagnostic_error` 按分支直接错误数量寻找唯一最近分支。真实 Author `semantic-result-2.0` 中，调用方给 `scope_requirements_ready` 输出误多传 `mode` 后，直接错误数为 `4、3、1、1、1`。两个内部 union 汇总与真实分支并列，使错误停留在 `owner_result.output`。

`_constraint_diagnostic` 已能将选中的 `additionalProperties` 错误定位到字段。当前缺口在此前的分支选择，增加 scope 输出字段会改变正确的拒绝合同。

## 3. 目标与非目标

目标是让普通调用方看到可纠正的字段位置和合同定位，同时保持完整校验的拒绝语义。Task 整体承担共享实现、直接回归和受影响受管副本同步。

不承担自动删除输入字段、自动选择出口、补造前序结果、新 DTO/schema 字段、任意 schema 推断框架、#765 或 #734/#736 整体治理。恶意输入防护、完整多平台安装升级和 Release 矩阵不在本范围。

## 4. 真实调用方、场景与流程

| 场景 | 调用方及前置条件 | 动作与处理 | 可观察结果 |
| --- | --- | --- | --- |
| S1 | Author 调用方组装合法 scope 输出 | 正常组装失误多传 `mode=workflow`，调用生产 `validate_json` | 仍拒绝，具体定位 `owner_result.output.mode`，提示未声明及原合同 |
| S2 | 同一调用方修正 S1 | 仅删除 `mode`，重新调用原校验 | 同一对象通过 schema 校验 |
| S3 | union 没有唯一可匹配出口 | 使用既有真实歧义回归样例 | 保留原歧义诊断和合同定位，不按顺序或相似名称猜测 |

## 5. 行为要求

- R1（S1）：对现有 schema 以固定 `exit_id` 常量区分的 union，优先根据实际出口值及 schema/相对 `$ref` 声明寻找唯一匹配分支，再复用既有字段约束诊断。
- R2（S3）：不能唯一匹配时保留原有歧义处理；不新增任意 schema 的出口推断规则。
- R3（S1/S2）：完整 schema 校验保持合法性权威。诊断匹配不能使无效输入通过，也不决定 workflow 路由。
- R4：保持 `schema_mismatch`、原退出码和 `code`、`field_path`、`remediation` 三字段错误结构。合法成功 DTO、闭合对象和现有公共字段不变。不得回显输入正文或敏感值。
- R5：复用共享实现及现有公开入口，不按 Skill/package 或具体出口硬编码，不另建 `$ref` 解析器。通过既有分发 owner 同步受影响 canonical、dogfood 和安装投影。

## 6. 约束与依赖

实现范围以共享 schema 诊断及其直接消费者为主。Author 原入口在生命周期查询前调用该校验；入口接线未改时，不要求创建业务 Task 或新增 native Agent 链证明诊断。若接线改变，补该变化对应入口验证。

沿用现有托管 Python、jsonschema 校验器及 referencing 上下文。无需数据迁移或新持久状态。AI 保持语义审核职责，脚本仅解释机器可判定的失败。

## 7. 可观察验收与验证方式

| 验收 | 对应要求 | 入口、输入及预期结果 |
| --- | --- | --- |
| AC1 | R1/R3/R4，S1/S2 | 生产 `validate_json` 加载真实 Author `semantic-result-2.0`，使用合法 `task_ref`、`requirements_locator` 及 scope 出口；额外 `mode` 必须拒绝且指向 `owner_result.output.mode`，说明未声明并定位合同。仅删除该字段后通过。 |
| AC2 | R2/R3，S3 | 复用既有无法唯一确定分支的样例，保留外层歧义诊断，不能误指具体出口。 |
| AC3 | R3/R4/R5 | 运行受影响共享诊断回归，覆盖嵌套 union、真实歧义、缺失字段和不回显值；检查三字段错误及拒绝语义。运行匹配的 source/installed 和漂移检查。 |

测试层级是共享校验及诊断，不将组件证据称为完整 Author 生命周期、生产效果、升级或 Release 验证。不增加 schema 字段静态快照测试。

## 8. 实际未决项

需求及规范性方案没有阻塞性未决项。实际实现与测试结果由后续 Delivery 提供；目前未宣称修复完成。
