# D1 Planning union 诊断实施与验证计划

## 1. 输入与引用

整体范围为根 `prd.md` 的 accepted_scope；本批要求、场景和验收由同目录 `prd.md` 完整定义。读取同目录 `design.md` 第3节唯一来源设计处置、第4/6节算法和第8节验证后实施。真实独立 candidate_assessment 为 no_architecture_impact；Wording-current final_plan、Approval 和当前对话的规划接受仍须完成。

必须读取 `trellis/skills/guru-team/runtime/schema.py`、`runtime/tests/test_public_contract_diagnostics.py`、真实 Architecture aggregate 4.0 及其 Planning 示例。`clear-technical-writing.md`、`quality-guidelines.md` 的 Test And Validation Value/Python Syntax Check/Validation Scope Ownership、`subtraction-first-compatibility.md` 与本批所引完整 authority 约束本轮工作。正文规则与模板只由原 Author package 单写，不复制到运行脚本。

起点 B/H0 为 `0fb7dc9aac817a684c2f95bebb6570061a5ef868`，PR 目标 `main`。没有前序 Delivery，也没有已实现修复或已通过验收。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置 | 原 owner、文件与具体行为 | 完成观察 |
| --- | --- | --- | --- |
| I1 | 当前 Planning 被接受并 Activation 成功 | implementation owner 重读计划、实际 Task/Delivery/checkout；每次写入前执行原 check-task-checkout-boundary | 同一 key/generation、scope/root 与 implementing 匹配，无并行改动被覆盖 |
| I2 | I1 | 在现有 `test_public_contract_diagnostics.py` 增加两种 Planning 布局的合法→错层→仅修层级断言，使用真实 aggregate/生产 validate_json | 两种用途独立覆盖；观察真实字段、拒绝语义及用途提示，不复制选择算法 |
| I3 | I2 的断言与源代码已读 | 在共享 `schema.py` 的原 `_diagnostic_error` 用同对象 const 声明匹配替换 exit_id 专用段，按 design 第4/6节保留全部原回退 | 不改 validator、约束提示 owner、loader、DTO、schema或业务路线；现有出口仍由同一机制处理 |
| I4 | I3 与 V1/V2 工程结果 | 原 source-owned guru-upgrade-tools 对本 checkout preview，完整读取其当前合同、精确 source/public API与实际写集；展示确认后 prepare/invoke 同一 operation | canonical/installed 一致，Task/session/用户/peer 保持；local_candidate 的 source-lock 限制明示 |
| I5 | I4 | 执行 V3/V4，原 RDT owner 的 task_impact_sync 重新判断实际差额与 no-change；Architecture 若机制或边界扩大回原 owner | 工程证据真实、知识结论与实际 diff 一致，无共享正文待首次集成遗漏 |
| I6 | I5 | 原 TaskCommit owner 审查精确 stage/commit 计划并另获确认；提交后 implementation 用公开 constructor 绑定完整 B..H/begin_check | 不造空提交，不推断 pass；新独立 reviewer 在同一次完整 committed Review 先作 Architecture before/after，再完成 Check/full Review |
| I7 | 实际完整 Review passed | 原 Delivery Review/readiness→Publish→Merge，每个精确外部副作用独立展示；合并前停止交协调器 | PR Refs-only；整体 Completion→Closure→Finish 由原 owners 后续核全部范围 |

I2 与 I3 可在同一次有界开发中采用测试先行；不要求为形式重复红绿、撤回修复或冻结 mutable 值。任何新增必要文件先说明直接 consumer；不添加通用分支推断器、wrapper、状态或报告台账。

## 3. 验证入口、输入与预期观察

**V1/V2（D1-AC1–AC3）**：从 repo root 执行共享诊断模块：

```bash
PYTHONPATH=trellis/skills/guru-team .trellis/guru-team/runtime/resolve-python.sh . trellis/skills/guru-team/runtime -m unittest discover -s trellis/skills/guru-team/runtime/tests -p test_public_contract_diagnostics.py -v
```

新增断言加载当前真实 aggregate 4.0，并以实际 Planning 示例的合法字段为 fixture；fixture 只建立 schema 边界前的合法输入，不制造 validator 输出。final_plan 的顶层路径移到 candidate 后仍抛 schema_mismatch/原非零退出码，field_path 指实际 candidate/design_locator，remediation 不要求切换用途。candidate_assessment 反向场景同样检查。只修层级、用途不变时通过。既有测试继续检测 exit_id、嵌套 union/相对引用、真实歧义、字段与值不回显；若旧覆盖存在本次实际缺口，只补其独立断言，不扩 schema 组合矩阵。

**V3（D1-AC4）**：I4 后用目标自身安装环境：

```bash
PYTHONPATH=.trellis/guru-team .trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime -
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

首条 Python 从 stdin 执行 V1 的同形观察序列，import 目标 installed `runtime.schema.validate_json`，加载 `.trellis/guru-team/skills/packages/guru-maintain-architecture-baseline/` 下的真实 aggregate/示例。先核实际模块路径来自目标 installed，再观察两合法、两错层及修正后结果；不借 source runtime 代替 installed。记录真实命令与输出，不新增长期测试 harness 或复制诊断实现。检查受影响声明平台投影 bytes/modes、原工具 owner 的 postvalidation/native 结果及递归 `.new/.bak`；冲突不算通过。

**V4（D1-AC5/质量）**：执行 `quality-guidelines.md#python-syntax-check` 的原内存编译命令及其它本次变更的 Guru Python；执行：

```bash
python3 .trellis/scripts/task.py validate .trellis/tasks/11-15-847-planning-union-diagnostic
git diff --check
```

源码/runtime、installed、受管分发、AI 完整 Review 和 GitHub 外部事实分别报告。上述计划没有预填 pass；不执行完整多平台 Throwaway、云端业务、生产效果或 Release 矩阵。原始失败保留，修复后的成功注明观察层级。

## 4. 停止条件与适用回退点

- 缺真实 schema/依赖、Task/Delivery/checkout 不匹配或旧结果过期时，停在原 identity/阶段/依赖 owner，不修改 binding/hash 伪造接续。
- 若必须引入新的 parser、DTO、业务路线、持久状态或更宽 schema 推断才能实现，停止该扩展并回 Author/Architecture；真实范围选择交 Clarify，不在实现中猜测。
- 工程测试失败时保留失败输入，定位当前修复/测试/设施问题，不放宽业务断言。验收所需缺口未解决就不宣称通过。设施反复失败时重评同问题的复现方式，不能把设施失败当作目标缺陷复现。
- Tools 中断沿同 operation 的公开恢复入口，不重做 prepare/backup、不删除他人资源。没有业务数据/部署变化，因此无数据回滚协议；对本次未提交代码的修订仅处理自己范围，不 revert 并行改动。
- 当前验证集已足以回答验收且无剩余因果/reach疑问时结束验证；新诊断实验必须指明现有证据不能回答的问题与决策作用。

## 5. Delivery Policy（唯一）

**full**：D1 全量覆盖根 PRD R1–R7、AC1–AC5，没有延期实施或验收责任给后继切片。独立交付条件是双向字段诊断与全部保留行为成立，canonical/installed 同步及相称验证完成，实际独立 Check/full Review 与 readiness 通过。此时才能发布本批 PR，合并仍须协调器处置。

没有阶段性功能限制或待解除开关，不新增限制账本。Delivery 合并不代表 Task Completion；whole-Task owner 仍核实际所有义务、证据层级及未验证边界，Closure/Finish 分别处理源 Issue 和最终归档。

## 6. Docs SSOT Plan（唯一）

选择 **no_docs_update_needed**。本批修复共享诊断器对既有 const/字段约束的失败解释，不改变需求范围、入口、public I/O、生命周期或 Architecture 决策。原 requirement/design/test authority 的相关完整单元是 PRD 第7节的 `local-fix-intake.md` R692/D692/T692：其 Discovery 绑定诊断和分发职责保持，不把本次 schema 选择写成新的 Intake route。完整 schema/错误结构与测试定义由原 canonical runtime/schema/tests 单写；Task PRD 与本批规划承接具体缺口及验收。

原 writer 为 `guru-maintain-requirements-design-test-ssot`。I5 在实际代码、测试及安装结果后，用其原 task_impact_sync 对照差额确认 no-change；直接 consumer 是后续 Check、独立完整 Review、Delivery Review 和 Completion。没有真实知识差额就不建空 contribution、ADR、共享导航或全局版本更新。

若实施中出现改变当前完整知识定义的真实差额，回原 RDT/Author 判断必要维护与受影响规划。若其合法结论要求 delta，则在同 Task 隔离贡献准备完整拟写，经原 final_integration/readback 纳入 TaskCommit，再由独立 committed Review 审真实 after；不能让独立 Review 首次整合或在 Finish 追加业务修订。Architecture candidate assessment 已无影响，Wording-current final_plan 仍由独立 owner 核当前设计。
