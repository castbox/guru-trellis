# D1 Planning union 字段诊断需求

## 1. 整体来源与术语

整体 authority 是 `.trellis/tasks/11-15-847-planning-union-diagnostic/prd.md`，accepted revision 为 `sha256:836691ca52d402266cc07a1aa060b4a9275bb6ee603d3c21595fe9906d8bcab2`。本批 Delivery 为 `85d5b984-11d3-4a4c-81d3-118e2160ca42`，generation 0，planning_root 为 `deliveries/85d5b984-11d3-4a4c-81d3-118e2160ca42`，scope_ref 选中 R1–R7 与 AC1–AC5。

| 来源 | 章节/角色 | 本批用途 |
| --- | --- | --- |
| [#847](https://github.com/castbox/guru-trellis/issues/847) | 完整正文；要求、历史及推荐方案 | 诊断缺口、双向复现、回退和验收 |
| [已接受评论](https://github.com/castbox/guru-trellis/issues/847#issuecomment-6890790098) | 完整评论；要求及复审事实 | 保留对称场景与不能唯一定位时的原回退 |
| 整体 PRD | 第1–8节；已接受整体范围 | 本批覆盖、兼容边界及非目标 |
| `.trellis/tasks/archive/2026-11/11-09-766-union-exit-diagnostic/prd.md` | 第5–7节；前驱约束 | 原出口定位、引用与歧义回归 |

union、用途和诊断选择沿整体 PRD 第1节定义。来源方案的最终取舍由本批 design 第3节独占；此处不预填方案通过。

## 2. 整体与本批目标、非目标

当前共享诊断器能按 exit_id 常量优先定位输出分支，但没有该字段的 Planning 输入会落入错误数量选择。final-plan 错层时实际分支错误更多，提示因此可能要求改变本来正确的用途；反向错层同样受影响。

本 D1 全量承担 #847：在错误布局继续被拒的前提下定位实际字段，保留合法性、用途、既有回退及 #766 行为，并完成直接回归和 canonical/installed 同步。独立交付结果是可由原调用方使用的正确诊断，而非自动修正输入。

整体 PRD 第3节的非目标全部保持：不做 #848、全部 G03 修复、DTO/闭对象放宽、新 wrapper/语义 gate、任意 schema 推断、第二套引用解析及完整多平台/Release矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首次 Delivery，没有前序 delivered 结果。开发起点和 Planning H0 为 `0fb7dc9aac817a684c2f95bebb6570061a5ef868`；PR 目标为 `main`。两者角色不同，后续 target 前进不自行改写内容基线。

依赖已有 jsonschema/referencing、生产 `validate_json`、Architecture aggregate 4.0、共享诊断测试和原受管工具升级 owner。此次不修改 Task/Delivery API或业务数据，不需要数据迁移。尚未实施、执行修复后测试或更新 installed。

D1 没有延期给后继的实施责任。整体 Completion 仍须核对实际全部验收、Delivery 事实及未验证边界；Delivery 合并本身不构成整体完成。Closure/Finish 属于后续原 owners。

## 4. 本批调用方、场景与流程

调用方是组装 Architecture Planning 输入的 Agent。原流程为组装→生产完整 schema 校验→失败时共享诊断→调用方修正原字段并重试；本批不接管用途或业务路线。

| 场景 | 前置、动作 | 本批处理与观察 |
| --- | --- | --- |
| D1-S1 | 合法 final_plan 输入，将顶层 design_locator 误移入 candidate | 拒绝不变，报告 candidate 多余或 design_locator 缺失，不要求改用途 |
| D1-S2 | 合法 candidate_assessment 输入，将 candidate.design_locator 误移到顶层 | 拒绝并定位真实字段，不要求改 final_plan |
| D1-S3 | 仅纠正上述层级 | 原用途保持，合法对象通过同一生产 schema 校验 |
| D1-S4 | const 声明缺失、冲突或不足以唯一定位 | 原最少错误与 best_match 回退保持；真实歧义不被猜测性选择抹去 |
| D1-S5 | 原 exit_id、嵌套 union/相对引用及普通字段错误 | #766、字段诊断与不回显提交值约定保持 |

## 5. 完整行为、条件与约束

- **D1-R1 / R1**：只有既有分支 const 声明足以唯一定位当前输入时，才优先解释该分支的真实字段错误。不按具体 Skill 或两种用途字面值硬编码，不新增 discriminator、branch ID 或 schema 注解。
- **D1-R2 / R2**：声明不足、冲突或不唯一时，保留原最少错误选择和 best_match；不得统一退化为笼统 union 提示，原本真实歧义保持。
- **D1-R3 / R3/R4**：完整 schema 仍决定合法性；错误继续非零、schema_mismatch，公共三字段错误结构与合法成功 DTO 保持。提示命名实际字段和合同，不回显输入值。用途、闭对象、前序结果和业务路线不由诊断修正。
- **D1-R4 / R5**：复用当前校验器已解析的 schema/错误树及既有相对引用上下文。const 提取与递归限于当前真实 schema 和必要引用，保留 exit_id、嵌套 union、真实歧义与字段回归，不引入任意推断或第二解析器。
- **D1-R5 / R6**：原工具升级 owner 同步 canonical 与受影响 installed，验证实际 source/installed 场景及 drift；不手工覆盖受管副本。
- **D1-R6 / R7**：整体第5节的其它 G03 责任映射保持。freshness_identity、qualifier profile、active_task authority、稳定 design_revision 和入口/locator错误按原合同纠正，不统一放宽。若出现同一诊断选择机制的新直接证据，只处理该机制差额，不推断共同根因。

## 6. 本批验收、验证方式与未决项

| 验收 | 要求/场景 | 原入口、输入及预期结果 |
| --- | --- | --- |
| D1-AC1 / AC1 | D1-R1/R3；S1/S3 | validate_json + 真实 aggregate 4.0：合法 final_plan 通过；错层拒绝并指 candidate/design_locator，不改用途；仅修层级后通过 |
| D1-AC2 / AC2 | D1-R1/R3；S2/S3 | 同入口检查 candidate_assessment 的合法、反向错层和修正输入；只将实际字段错误解释得可纠正 |
| D1-AC3 / AC3 | D1-R2/R3/R4；S4/S5 | 复用共享诊断回归，保留出口、嵌套 union/相对引用、歧义、字段、错误结构及不回显值；新增真实缺口所需断言 |
| D1-AC4 / AC4 | D1-R5 | 原升级同步后，source/installed 运行双向场景与适用 drift，受管冲突按原 owner 处理 |
| D1-AC5 / AC5 | D1-R6 | 独立完整 Review 核对实际 diff 与调用消费者，确认无错误放宽或无依据范围扩张 |

足够层级为生产共享 validator/schema 和受影响 installed 入口；不要求完整业务生命周期、云端调用或多平台矩阵。永久回归以双向缺口和适用旧测试为限；不新增重复诊断实验。当前需求阶段无未决选择，具体算法和命令留给经独立 Architecture 的方案规划。所有验收尚待执行，未预填通过。

## 7. Canonical 引用与本轮差额

| Authority | 已读对象与用途 | 本轮差额 |
| --- | --- | --- |
| requirement/behavior | `docs/requirements/current/local-fix-intake.md` R692-03/04；原诊断失败仍失败与受管分发边界 | 不改 Discovery 的绑定诊断；只补 shared schema union 的实际字段选择 |
| design | `docs/design/current/local-fix-intake.md` D692-02/03/04；当前调用者消费与原 owner 分发 | 不新增路由、存储或 wrapper，保留原共享 owner |
| test | `docs/test/current/local-fix-intake.md` T692-02/04；直接行为与 source/installed 证据边界 | 本批用真实 aggregate 双向错层补共享测试，不借用旧结果声称通过 |
| Architecture | `docs/architecture/README.md` 及 `docs/architecture/06-governance/change-contract.md`；阶段适用发现与 concern/owner 规则 | 独立 candidate_assessment 待执行；其结论决定实际 Architecture 工作，不预建空 contribution/ADR |
| canonical contracts | `trellis/skills/guru-team/runtime/schema.py`、真实 aggregate 4.0、`runtime/tests/test_public_contract_diagnostics.py` | 原共享实现与测试直接承接，合法性和公开 DTO 不变 |

RDT/Architecture 的实际维护判断与 Docs Plan 在原后续职责完成；本 requirements 写作不改共享导航或 current authority。
