# D1 按既有出口标识定位 union 诊断

## 1. 整体来源与术语

本批消费整体 [Task PRD](../../prd.md) 的当前 accepted_scope，选取 R1–R5、AC1–AC3。公共 DeliveryKey 为 `766-union-exit-diagnostic / 0 / 88802bbb-f0f0-475a-9f38-6553a7236b1c`，planning_root 为本目录。

[Issue #766](https://github.com/castbox/guru-trellis/issues/766) 的“解决方案”是规范性设计约束；“DTO、兼容与范围边界”和“最小验收”是要求。事故记录是历史证据，不作为整个会话耗时的因果结论。union、诊断选择和合法性判断沿用整体 PRD 第1节定义。

## 2. 整体与本批目标、非目标

当前直接错误数选分支会把真实 Author `output.mode` 错误遮蔽为外层 union 汇总。本批完整交付共享诊断改进、直接回归与受影响安装投影，使调用方能在原入口纠正普通组装错误。

本批覆盖整体全部要求，不留待后继切片。保留全部非目标：不修改成功 DTO、schema 字段、错误结构、route authority，不自动修复输入，不新增任意 schema 推断器，不承担其它 Issue 或完整升级/Release 矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首个 Delivery，尚无前序交付。固定开发基线为 `main@8d97fe5401345180ce294e2f729ec33071b37f62`；目标分支为 `main`。现有 `_constraint_diagnostic` 已支持字段错误，当前缺少唯一 `exit_id` 分支优先选择。

依赖现有托管 Python、jsonschema/referencing 和 preset 分发 owner。实现后需原 Check、独立完整 Branch Review、交付审核及实际 PR 合并。整体 Completion 仍须核对全部 AC 与投影；本批交付本身不等于 Task 已完成。没有另行分配的功能责任。

## 4. 本批调用方、场景与流程

- D1-S1：Author 调用方组装 `scope_requirements_ready` 输出，保留合法 task_ref/requirements_locator，普通失误多传 `mode=workflow`。生产 `validate_json` 完整校验失败后选择具体诊断，继续拒绝并定位 `owner_result.output.mode`。
- D1-S2：调用方仅删除同一对象的额外 mode，再调用原校验；对象通过。
- D1-S3：已有无法唯一确定出口的样例进入共享校验；保留原歧义处理和合同定位，不按顺序或相似名称猜测。

## 5. 完整行为、条件与约束

- R1：对已有固定 `exit_id` 常量区分的 union，优先使用实际出口值和 schema/相对 `$ref` 声明唯一定位分支；选定后复用字段诊断。
- R2：无法唯一匹配时保留原选择/歧义处理；不建立通用推断框架。
- R3：完整 schema 校验决定合法性。诊断选择不放行无效输入、不决定 route、不自动删字段或切换出口。
- R4：保留错误码、退出码、三字段错误和合法成功 DTO；闭合对象继续拒绝额外字段，不回显正文或敏感值。
- R5：复用原引用解析上下文及错误树，不另建解析器，不按 package 或具体出口硬编码。沿原 owner 同步 canonical/dogfood/安装投影。

来源设计的唯一处置将在本批 design 第3节记录。当前仅完成需求与候选，不提前宣称 Architecture 或方案通过。

## 6. 本批验收、验证方式与未决项

| 验收 | 要求/场景 | 生产入口和预期观察 |
| --- | --- | --- |
| AC1 | R1/R3/R4；D1-S1/S2 | `validate_json` 加载真实 Author semantic-result-2.0；多传 mode 仍为 schema_mismatch，field_path 精确到 owner_result.output.mode，remediation 说明未声明及合同。仅删 mode 后通过。 |
| AC2 | R2/R3；D1-S3 | 复用既有 tied alternatives，仍报告原歧义，不误指具体出口。 |
| AC3 | R3/R4/R5 | 运行现有共享诊断回归，涵盖嵌套、歧义、缺失字段和不回显值；检查原三字段/拒绝语义及受影响投影漂移。 |

不为字段不变新增静态快照测试。入口接线未改变时，无需真实业务生命周期或 native 链；接线改变则补相应入口验证。上述是预期，尚未执行修复验证。无阻塞性需求未决项。

## 7. Canonical 引用与本轮差额

- `.trellis/spec/workflow/companion-scripts.md` 的 Error Handling、Shared Skill Runtime Dispatcher 和 Python Runtime Constraints：保持共享客观校验与托管运行时；仅细化失败诊断的选择。
- `.trellis/spec/workflow/quality-guidelines.md` 的 Test And Validation Value、Validation Scope Ownership：用生产 schema 及原函数观察行为，不以新矩阵扩大范围。
- `.trellis/spec/workflow/clear-technical-writing.md`：持续使用当前写作规范。
- `trellis/skills/guru-team/runtime/schema.py` 与其 `tests/test_public_contract_diagnostics.py`：生产实现及直接回归位置。
- `docs/architecture/README.md`：Architecture authority 发现入口；架构差额由独立 owner 按真实候选评估，不用 Task 自述代替。
