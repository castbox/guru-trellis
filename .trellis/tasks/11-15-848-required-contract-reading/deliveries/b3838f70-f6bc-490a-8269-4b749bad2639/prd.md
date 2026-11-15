# D1：长文读取方法与首读导航

## 1. 整体来源与术语

整体 authority 为 [Task PRD](../../prd.md)，接受版本 `sha256:a922f8c7e39c567fb2f954087826c16ddfe57888e7875d7df9bad65941eee3de`。本批 DeliveryKey 为 Task `848-required-contract-reading`、generation `0`、Delivery `b3838f70-f6bc-490a-8269-4b749bad2639`；planning_root 为本目录。

| 来源 | 位置与角色 | 本批用途 |
| --- | --- | --- |
| [#848](https://github.com/castbox/guru-trellis/issues/848) | 全文；要求、约定技术约束、既有诊断证据 | 本批完整行为与验收 |
| [接受评论](https://github.com/castbox/guru-trellis/issues/848#issuecomment-6891318170) | 完整复审结论；requirement | 保留名义请求、实际容量与跨调用补显的区别 |
| 整体 PRD §1—8 | 已接受整体范围 | 本批 scope_ref 选中 R1—R7、AC1—AC6 |
| canonical companion-scripts.md | Reading Required Contracts In Full / Intermediate Command Stdout 1.0；当前方法 | 原方法位置与完整 JSON/receipt 消费边界 |
| canonical guru-review-change/SKILL.md | provider-aware 首读入口；现状证据 | 独立入口实际调用方 |

内层、外层、实际容量及完整正文的含义沿整体 PRD §1、R1—R4；本批不新增不同定义。完整来源和必要现行合同已实际读取。

## 2. 整体与本批目标、非目标

整体目标是减少必需正文读取的可避免截断返工，并保持当前 AI 实际完整获得和理解正文。本批一次交付共享方法、首次长文前的短导航、匹配投影和真实采用验证，覆盖全部选定要求。

当前读法已有分段和两层预算原则，但先要求分段，缺明确外层参数位置与跨调用补显路径；独立入口首读长规范前未接入该短方法。修订在原 Markdown owner 完成，installer 仅分发导航。

本批保留整体非目标：不新增读取器、公共 Skill/schema、持久读取状态/gate，不改宿主全局配置，不承诺任意大容量，不削弱全文和原 mutation/receipt 恢复；不实施 #847，不扩为付费调用、多平台升级或 Release 矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首次 Delivery，无前序 delivered 结果。开发基线选择 `B=0fb7dc9aac817a684c2f95bebb6570061a5ef868`，当前规划起点 H0 与 B 相同。B 是固定内容起点，PR 目标 main 是独立角色；main 后续推进按原基线 owner 判断实际差额，不自动扩大范围。

源 Issue 的20,000／24,000合并显示失败、40,000仍同位置截断和原内存补显成功为既有诊断事实，不是本批修订后验收。尚需实际实施、原受管 owner 同步、AC1—AC6 验证及完整质量交付链。

本批不预留尚未分配的同范围实现给后继。宿主额外显示限制原因保持未知，但不阻塞按实际容量补显/补读的已接受目标。#847 无硬前驱关系，资源、元数据与操作保持独立；合并前停止等待协调器的 integration owner。

## 4. 本批调用方、场景与流程

| 场景 | 调用方与条件 | 本批行为与结果 |
| --- | --- | --- |
| D1-S1 | workflow/恢复 owner 面临必需长文 | 先核确需材料与已有完整上下文，再选择直接读取或容量回退，最终获得正文和文件尾 |
| D1-S2 | functions.exec 嵌套 exec_command | 每条内层覆盖其输出，外层覆盖所有输出及载体开销；输出 Markdown 正文并检查实际显示 |
| D1-S3 | 仅外层截断且完整原文仍在既有跨调用内存 | 下一独立调用从同一原内存按较小批次补显，无新读取命令 |
| D1-S4 | 内层已缺失或无原内存 | 按缺失部分补读；范围不明时用足额全文或连续相邻范围覆盖到文件尾 |
| D1-S5 | 新 Agent 无父历史，从直接独立 review 入口开始 | 先解析完整 provider，先读原短方法小节，再读同源必要长正文；target authority 单独读取 |
| D1-S6 | 原安装 owner 采用完整 matching 来源 | 安装/平台投影保持一致，用户内容保留，sidecar 按原 owner 处理，定向验证可核验 |

读取顺序为“必需材料和可复用完整内容 → 真实工具与预算 → 实际显示核验 → 按层级补显或补读 → 依赖正文的原判断”。没有新增状态机或授权载体。

## 5. 完整行为、条件与约束

- **D1-R1（整体 R1）**：当前 owner 实际获得必需全文并理解。完整原生注入和已读正文在当前仍完整可用时复用；预算增大不扩读范围。命令成功、raw stdout、路径和参数不能独立证明模型可见完整。
- **D1-R2（R2）**：工具能容纳时先显式足额预算直接读取。内层按每条预计输出，外层按全部输出和载体开销，不只取最大一条；超过缺省10,000不自动拆分。Codex 首次请求内层20,000、外层24,000；按实际内容调整，32,000／40,000仅示例。请求值不是固定阈值或宿主保证，不改全局配置；其它工具只用真实接口。
- **D1-R3（R3）**：exec_command 的 Markdown 输出采用 `.output` 正文，原生工具采用其实际载体；不能假设所有工具有同字段。正文输出不能代替预算，同次合并仅限确需且总量可完整容纳的材料。
- **D1-R4（R4）**：超实际容量、预算无法可靠覆盖或调整仍截断时，再按文件或连续相邻范围拆分，覆盖全文、文件尾及无末尾换行部分。名义值已高仍截断须保留事实，不盲目调大；固定行数不是合规条件。
- **D1-R5（R4）**：仅外层截断且原文在平台既有跨调用 owner 内存时优先补显，不重跑读取。exec 的 const 局部变量不算该内存；内层缺失、原结果丢失或内存不可用则补读，范围不明则全文或连续覆盖。functions.exec 确有 store/load 时原调用保存 output、后续补显、消费后释放；不新增缓存文件、内存服务或 ledger。
- **D1-R6（R5）**：原共享短方法承载唯一读法。原 AI-first 与 provider-aware 独立入口在首次长文前导航到该小节，只读小节而非整本。必要共享入口按实际调用关系适配，不复制方法，不要求独立操作先创建 Task/加载完整 workflow。Python 只分发文字。
- **D1-R7（R6）**：producer JSON、receipt 和 typed exit 用完整原始 stdout 在内存消费，不从按行显示片段重建；显示不全不重复 mutation。原 owner 的结果恢复与既有失败保留。
- **D1-R8（R7）**：原安装 owner 同步 canonical、dogfood/installed 和声明平台的受影响投影，定向 source/installed、reapply、drift、用户内容和 sidecar 验证各报告实际层级。真实新 Agent 采用与机械分发分开证明。

来源已有规范性技术约束，不按“建议”删去。后续 design §3 独占 retain/change/reject 的具体设计处置；本 PRD 不建立第二矩阵。本批无业务 API、数据库或持久数据迁移，公共 Skill I/O/typed exits 不变。

## 6. 本批验收、验证方式与未决项

| 本批验收 | 对应整体项/场景 | 入口、输入与可观察结果 |
| --- | --- | --- |
| D1-AC1 | AC1 / D1-S2 | 固定样本第二轮同形四份公开材料，经真实 tools 请求20,000／24,000，观察正文及文件尾。完整则记录一次；截断则保留原失败，并从原内存或连续补读补齐，不能缩短材料后冒称原合并通过。容量支持时观察超过10,000完整显示 |
| D1-AC2 | AC2 / D1-S4 | 对已观察内层超量，仅提高外层不能恢复内层缺失；连续补读可覆盖全文与文件尾。只验证此真实缺口，不扩压力矩阵 |
| D1-AC3 | AC3 / D1-S3 | 仅外层截断且原结果已保存时，下一独立调用从同一原内存补显，没有新的读取命令；同调用 const 不替代此证据 |
| D1-AC4 | AC4 / D1-S5 | 无继承新 Agent 经修订后的原独立入口，实际先读短小节，再按真实工具与材料选预算或分段读必要长文，不先读整本 companion-scripts。只报告实际观察层级 |
| D1-AC5 | AC5 / D1-S6 | 原 tools/installer 更新后，定向 source/installed、声明投影、reapply 和 drift 通过适用检查；保留用户内容并处置 sidecar。不声明完整多平台、升级或 Release 矩阵 |
| D1-AC6 | AC6 / D1-S1—S5 | 当前语义审查与必要回归确认全文/provider/JSON/receipt/mutation 恢复合同保持；无新增读取器、schema、持久 ledger 或脚本判断 |

当前无阻塞性需求未决项。新 Agent 行为和安装实际效果须实施后验证，参数效果与宿主容量未知保持观察边界。后续若发现真实范围选择，回原 Clarify；实现细化归原 Author/Architecture。

## 7. Canonical 引用与本轮差额

- `trellis/presets/guru-team/spec/workflow/companion-scripts.md#reading-required-contracts-in-full`：本轮修改的原 managed-spec 方法；Intermediate Command Stdout 1.0 保持原结果消费语义。
- `trellis/skills/guru-team/packages/guru-review-change/SKILL.md`：provider 与 target 分离，前置短导航改变首次读取顺序，其独立审核职责/前置不变。
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 的 AGENTS_AI_FIRST_BLOCK：原分发 owner 只增加导航，不执行读取决策。
- `docs/{requirements,design,test}/README.md` 与相应 current 发现合同：现行 RDT identity 为 guru-trellis-rdt；本能力的完整定义沿原 owner 准备隔离贡献，实际整合在批准 Planning、实施和工程验证之后。本轮不追加全局版本或共享逐项索引。
- `docs/{requirements,design,test}/current/review-sufficiency.md` 的 provider/真实行为/分发边界：本轮保留其审核职责，只有读取方法和首读导航差额，不以静态链接声称实际采用。
- `docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md`：由独立 Architecture owner authority-first 评估本候选；本 PRD 不预填 impact、path 或 pass。
- 原 TaskCommit、完整独立 Review、Delivery readiness、Completion、Closure/Finish 保持各自职责；本批需求齐全不构成这些结果。
