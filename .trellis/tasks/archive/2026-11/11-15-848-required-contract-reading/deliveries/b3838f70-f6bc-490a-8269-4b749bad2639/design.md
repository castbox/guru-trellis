# D1：长文读取方法与首读导航设计

## 1. 设计目标、需求承接与内容基线

本批承接 [PRD](prd.md) D1-R1—R8、D1-AC1—AC6，覆盖 [整体 PRD](../../prd.md) R1—R7、AC1—AC6。目标是让原 AI owner 在实际容量内完整获得必需正文，减少可避免的截断与重读；不承诺改变宿主容量。

固定开发基线 `B=0fb7dc9aac817a684c2f95bebb6570061a5ef868` 来自原 Sync 采用的 Git object；Planning H0 与 B 相同。候选内容范围是完整 B..后续 H 加实际 dirty 增量；PR 目标为 main。后续 target 演进由原 Reconcile 根据真实差额处理，不替换固定内容起点。

本阶段 authority 是 `docs/architecture/README.md` 的 guru-trellis-architecture、`00-foundation/design-constitution.md` 的 guru-trellis-design-constitution-v1、`06-governance/change-contract.md` 的当前 Planning 合同。独立 candidate_assessment 已通过原公开入口返回 baseline_current/no_architecture_impact：本候选只细化现有读取方法及首次导航，原 AI/installer、公共 I/O、状态和恢复职责不变。此结果只允许写方案，不能替代 final_plan 或最终实施审核。

## 2. 当前系统、边界与目标差额

无前序 Delivery。当前 canonical 方法位于 `trellis/presets/guru-team/spec/workflow/companion-scripts.md` 的 Reading Required Contracts In Full。它先要求连续行范围，再提醒两层预算。当前 workflow 的 Phase Index/continuation、22个 descriptor-bound Guru finish 入口先要求完整读取写作规范；独立 review Skill 先读 review-sufficiency，再解析 provider 和读写作规范。AGENTS_AI_FIRST_BLOCK 只分发写作规范导航。

本轮差额：原方法改为“确需范围和完整上下文复用 → 容量允许时足额两层预算直接读 → 按真实缺失层补显/补读”；上述首读入口只增加同源短节导航。独立入口先解析 provider 并读短方法，再读同源写作/审核方法，target authority 单独读取。

不修改 Trellis 上游、hook、官方 trellis-* entry、函数工具宿主、Skill Interface、schema、公共 DTO、typed exits 或 runtime parser。没有新增通用读取器、缓存服务或持久读取状态。

## 3. 来源设计处置（唯一）

来源为 [#848](https://github.com/castbox/guru-trellis/issues/848)“目标与处理顺序”“保留的合同与范围”及[接受评论](https://github.com/castbox/guru-trellis/issues/848#issuecomment-6891318170)。下列技术承诺均 retain；没有 change/reject 或待上游改义的承诺。

| 原承诺 | 处置与具体落点 | 理由与影响 |
| --- | --- | --- |
| 先确认确需并复用当前完整材料，不因预算扩读 | retain；§4 M1、§6 P1 | 保持真实阅读范围 |
| 容量允许时两层足额预算直接读取，外层按总量和开销 | retain；M1、P2、V1 | 修订原方法顺序，不能只取最大一条 |
| 初始20,000／24,000；32,000／40,000仅调整例子 | retain；M1 参数例子 | 不制造固定阈值、宿主保证或全局设置 |
| exec_command 输出 .output；其它工具用真实载体 | retain；M1、P2 | 减少载体开销，仍须独立配置预算 |
| 超容量、不确定预算或调整仍截断才分段 | retain；M1、P4 | 保留实际失败与文件尾，不盲目抬值 |
| 仅外层截断且有原跨调用内存时优先补显 | retain；M1、P3、V3 | 不重跑读取；const 局部变量不算持久于下一调用 |
| 内层缺失/原文丢失/内存不可用则补读；范围不明连续覆盖 | retain；M1、P4、V2 | 不把提高外层当作找回内层数据 |
| functions.exec store/load 仅真实存在时用，消费后释放 | retain；M1 跨调用例子 | 使用既有平台内存，不新增服务或文件缓存 |
| AI-first 和 provider-aware 独立入口在首次长文前读短节 | retain；M2—M4 | 导航只定位，不复制方法正文或要求完整 workflow/Task |
| producer JSON/receipt/typed exit 保持完整内存消费；不重放 mutation | retain；M1、P5、V6 | prose 补读与结构化结果恢复分开 |
| 同形失败、跨调用补显和无继承新 Agent 真实验证 | retain；§8 V1—V4 | 不换短材料制造合并成功，不注入预期行为 |
| 原受管同步与定向 source/installed/drift；无完整矩阵 | retain；M5、§7、V5 | 区分源码、模型行为与本 checkout 实际采用 |

## 4. 模块、职责与设计取舍

| 模块/owner | 实际文件与变更 | 输入、输出及边界 |
| --- | --- | --- |
| M1 原 Markdown 读法 | `trellis/presets/guru-team/spec/workflow/companion-scripts.md` 的原短节 | AI 读取必需材料及真实工具定义后选择预算/分批；输出为其实际获得的完整正文，不产生新 DTO |
| M2 原 AI-first 分发 | `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 的 AGENTS_AI_FIRST_BLOCK | 在现有写作条款前增加短节导航；Python 不计算可读长度、不决定充分性 |
| M3 原 workflow/launcher | `trellis/workflows/guru-team/workflow.md` 的 Phase Index/continuation；`trellis/presets/guru-team/overlays/` 的22个已有 finish entry | 在首次长文要求之前定位 installed 原短节；Markdown、JSON、TOML 保持各原格式，不新增入口/owner |
| M4 原直接独立入口 | `trellis/skills/guru-team/packages/guru-review-change/SKILL.md` 顶部 provider/首读段 | 先确定完整 source/installed provider，在其 workflow-spec root 读短方法，再读写作与 review-sufficiency；原独立审核前置、专业方法及 perspectives 不变 |
| M5 原 installer/tools | 上述 canonical 经 `guru-upgrade-tools` 同步本 checkout；原分发测试 `test_clear_technical_writing.py` | 完整匹配来源、原 manifest/hash/sidecar 和用户内容保留；生成投影，不手工改安装副本 |
| M6 原文档 owner | `trellis/workflows/guru-team/README.md` 与 `trellis/presets/guru-team/README.md` 的读取方法导航及采用说明；RDT 原 owner 的独立能力贡献及真实晋升 | 说明唯一方法、采用入口、验证边界；不追加公共 Skill/schema 或共享逐项索引 |

只改共享方法而不加导航，仍使直接入口在长文之后才遇到读法；只把长规范拆小会保留外层总量和首读缺口。新增 reader、固定行数或持久 ledger 增加状态与维护成本，无法替代 AI 对工具实际容量的判断。选择在原职责内改正文及薄导航；同一导航句可在已有 native adapter 中分发，完整方法仍只有一份。

M3 的22个入口都有相同首读要求，均属于真实消费者。M4 是本轮直接独立来源入口。普通其它 Guru Skills 经 AGENTS/workflow 的原入口获得该方法；不因本项批改全部公共 Skill，也不改变其 scope。

## 5. 接口与数据

没有新公共 API、字段、schema 或状态。现有接口链保持：原 workflow/profile 输入 → 原 Skill 定位完整 provider/必需正文 → 原语义判断与既有出口/consumer。M1 只改变获得正文的方法。

Codex 例子使用已暴露的真实位置：functions.exec 首行 `// @exec: {"max_output_tokens": 24000}`，每条 tools.exec_command 参数 `max_output_tokens: 20000`，显示 `text(result.output)`。外层覆盖该次全部输出及开销。其它工具没有这些参数时不套用。

跨调用 prose 例子在原调用用 `store("required-contract-text", result.output)` 保留完整返回，下一独立调用 `load` 并按实际容量连续显示；完成后 `store("required-contract-text", null)` 释放引用。key 只为例子，非公共名字、读取台账或必用机制。当前平台没有 store/load 时采用原连续补读。

receipt、JSON 和 mutation 的原恢复合同不使用这个 prose 例子的截片重构方式。完整原始 stdout 留在原 owner 内存；结果丢失由其原 recovery 恢复。

## 6. 状态、顺序、正常与失败流程

没有新增生命周期或持久状态。

1. **P1** 当前 AI 确定确需材料，复用当前完整且适用的正文/原生注入。首次长文前经入口导航完整读取同源短方法。
2. **P2** 工具容量和预算可覆盖时，显式配置每条内层及编排外层总预算，读取正文并观察实际文本和文件尾。
3. **P3** 只有外层显示截断、内层原文完整且仍在原跨调用 owner 内存时，从原内存缩小显示批次；不重跑读取。
4. **P4** 内层截断、原文丢失、内存不可用或无法可靠预算时，补读缺失范围；缺失范围不明则从文件首行连续覆盖到实际末尾，包括无末尾换行。名义请求已高仍失败保留事实，不反复盲调。
5. **P5** 实际全文获得后，原 owner 才执行依赖它的判断。prose 完整性由 AI 判断；结构化结果仍按完整原 stdout、原 recorder/checker/typed exit 合同消费。

所需文件缺失或 provider 不完整时，回原安装/来源 owner，暂停依赖它的正文或判断；恢复后完整读取继续，不新增确认或 fallback provider。该规则复用现有前置，不新增 gate。

## 7. 恢复、兼容、迁移与集成

没有 Task/Delivery、业务数据或 public I/O 迁移。本批只更新原方法和导航；旧历史及原实验保留原观察。原首读入口使用 source root `trellis/presets/guru-team/spec/workflow` 或 provider 的 installed `.trellis/spec/workflow`，不能借 target 中另一版本方法替代。

源码完成后，用完整 canonical source 的 `guru-upgrade-tools` 对当前专用 checkout 执行原 local_candidate 路径。实际 preview、一次 prepare、精确写集确认、invoke、目标自身 resolver/installed/native/drift 和 peer preservation 逐步执行。该模式保留 `formal_fork_source_lock` 未验证边界，不能声称正式 source_locked 采用或发布。准备阶段固定 source_ref 为当时实际 HEAD，冻结 canonical 工作树；来源实质变化先回原工具 owner 重新审查，不改旧计划。

目标写集只允许 workflow、受管规范/Skill/平台投影、AGENTS 原有界块、原安装 manifest 与 checkout-local runtime pointer；Task、Delivery、session、公共/私有 controls、配置与 peer tools 保留。AGENTS custom base 使用当前原全文，原 renderer 只更新 Guru block。未知编辑或 sidecar 冲突按原 owner 处理；禁止手工覆盖受管副本来绕过安装。

后续 main 真实冲突由原 Reconcile/安装 owner 处理。#847 保持独立；本批 commit、push/PR、工具写入及合并各自保留原精确动作确认。合并前等待协调器，Delivery 合并不证明整体 Completion。

## 8. 验证设计

| ID | 对应 AC | 层级、入口和输入 | 预期观察与边界 |
| --- | --- | --- | --- |
| V1 | D1-AC1 | 临时真实 transport：固定公开源码 `8c158381b5bdb61fd961cbb89e23c2d1f659c9aa` 的 clear-technical-writing.md 与 guru-review-change 的 contract.md、review-method.md、interface.json；同样两组材料，内层20,000/外层24,000，输出 .output | 保存两份完整原结果于已有调用内存；观察实际模型可见文本及文件尾。仍截断保留初失败，后续原内存分组或连续补读补齐；不能改短样本后称原合并一次成功。记录实际超过10,000完整显示的可得观察，不强制宿主容量 |
| V2 | D1-AC2 | 临时定向诊断：同一已观察内层超量的必要正文，保持内层缺失，外层足额；再用连续范围补读 | 外层增加不补回内层已缺失文字；原缺失及文件尾经连续范围实际获得。只测本项真实缺口 |
| V3 | D1-AC3 | V1 的原完整内存对象，下一独立 functions.exec 用 load 补显，不启动新读取命令 | 跨调用原文可用且补显完整；局部 const 或重跑 shell 不算。消费后释放内存引用 |
| V4 | D1-AC4 | tools 同步后，用无继承 generic Agent 从 installed guru-review-change 实际独立入口只读审核固定文件 `trellis/presets/guru-team/scripts/python/guru_platform_inventory.py`，正常完整审核所需方法 | prompt 只指定原入口/对象/只读权限，不注入预算、顺序或预期 findings。保留实际首次工具动作与结果；观察原短方法先于写作/审核长正文，按实际接口预算/分段且不先读整本 companion-scripts。原 Skill 所需独立 perspectives 保持；审核结果不替代本 Task 正式 Review |
| V5 | D1-AC5 | 长期分发回归扩展原 test_clear_technical_writing fixture：真实安装/reapply 后解析 AGENTS、workflow、各 native overlay payload 与 source/installed 独立入口引用；原 tools 本 checkout 实际采用 | 引用解析到对应同源短节，导航在首个长文要求前，正文由原 managed-spec 分发，用户字节和 reapply idempotence 保留。source/installed、3平台 dogfood/drift、mode/sidecar 定向检查；不等于完整矩阵 |
| V6 | D1-AC6 | 原 semantic check 和 source/installed package validators，必要 runtime 回归按实际差额选用；Python 内存 compile、JSON/TOML parse、git diff --check | 原 public graph、完整结果消费与 mutation 恢复保持；脚本只分发文字。机械通过不证明 V4 或修复宿主限制 |

V1—V3 为本次临时诊断，不变成长期压力测试。V5 复用真实分发 fixture 检查 consumer 可解析引用，不增加固定预算值自证断言。V4 是实际 Agent 行为，不以链接测试替代；原失败与最终结论分开。达到这些验收及受影响回归的足够证据即停止，不追加没有具体缺口的反复红绿、回退或任意长度实验。基础设施反复失败时由原 owner 重评能观察同一行为的入口，并保留无法完成的具体验收缺口。

## 9. Canonical 引用、本轮差额与实际未决项

核心 method、entry、installer 和分发测试位置见§4；原 README 只解释采用和限制，不复制方法。RDT 使用 guru-trellis-rdt 的 current 完整单元发现合同，本轮由原 RDT owner 为 required-contract-reading 准备独立 requirements/design/test 完整候选及必要关系，批准 Planning、实施和真实工程验证后 final_integration/readback，再纳入 TaskCommit 和独立 committed Review。具体 strategy 与 writer 只在 implement §6 定义。

Architecture baseline/current constitution/change-contract 已实际读取。独立 candidate 结论为 no impact，因此本候选不造空 Architecture contribution 或 ADR；final_plan 仍由独立 owner 对最终设计实际判断。若实现扩大 owner、状态、公共接口、持久化或 source 假设，则回原 Architecture/Planning。

Evolution 已确认目标的对应为：EVO-001 保完整来源语义，EVO-003/004 保唯一 authority/owner，EVO-005 减少无效重读，EVO-007 同步声明投影；EVO-002 沿原独立架构合同，EVO-006 保原生命周期，二者不新增职责。本轮不实施 Evolution target 的其它候选能力。

没有阻塞性产品或技术选择。真实工具容量、Agent 首次采用与安装效果待实施观察；formal source lock、完整多平台升级/Release 和宿主内部原因保持未验证边界。
