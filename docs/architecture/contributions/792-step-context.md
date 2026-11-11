# #792：当前步骤上下文与出口查询架构贡献

状态：已整合的历史贡献。来源为 Task `792-step-context` / generation `0`、Delivery
`4a341415-1863-4308-b8ec-336121e859d3` 的隔离拟写。原 Architecture owner 在完整候选 Check 后
通过 final_integration 整合并读回目标；本文保留 before/after 与取舍来源，不是第二共享 current。
当前完整定义读 [ARCH-CONTEXT-001](../03-domains/workflow-context.md)，决定读对应 ADR；
RDT 的实际晋升和后续正式质量/交付状态仍由各原 owner 的公共结果确定。

## 1. 适用来源与边界

固定 before 为 Git `05a16a5989669ca216d8ba34b9b419776410f04d`。直接需求为
[Issue #792](https://github.com/castbox/guru-trellis/issues/792)的五项行为及三项验收；
本批全部承担，没有延期必需实现。baseline 为 `guru-trellis-architecture`，constitution 为
`guru-trellis-design-constitution-v1`；原 [change contract](../06-governance/change-contract.md)
拥有九 concerns 与项目检查，本文不产生第二协议。

必要当前约束是 ARCH-FND-001/002、ARCH-DOM-016/038、ARCH-GOV-010/012，以及
[ADR-035](../adr/035-current-continuation-scope-routing.md)。#793 的 qualifier 适用合同保持；
本批不实施 #794 的 Check/Review 合并、身份组合或 #734，不批量迁移旧 Task。

## 2. Before 与本批实际源码差额

before workflow 内联完整 invoke/exit/target 标记、router/stop 行为及多处历史细节。
既有 discovery 按 Skill 返回 public contracts，尚无按出口取得直接 consumer 的入口。
原 phase index 提取区间夹带 continuation 和 Intake；原 installed graph validator、
compatibility snapshot/preview 都直接读取 workflow 标记。

本批源码候选把完整标记及 router/stop 行为移到
`trellis/workflows/guru-team/references/routing.md`。workflow 通过唯一
`guru-routing-reference` 声明该 extension-relative 资产；各 Skill Interface 仍拥有其
出口、consumer、I/O 和 projection。现有校验比较二者，不新增一张独立路由表。

原 `discover-skill-contract` 增加 `--exit`。当前执行 AI 输入实际 producer 和一个出口，
从 matching provider 取得唯一 consumer、直接输入/投影及必要入口。JSON schema consumer
另投影 repo-relative `consumer_schema_locator`，沿原 package 优先、shared consumers 根其次
规则定位实际 schema；原 `consumer_input` 和 producer `contract_root` 保持，不新增 schema
authority。普通 unknown、multiple、unmapped、缺 reference 或 graph/Interface mismatch
明确停止。无 exit 的原合同查询保持。
运行时只确定性提取和校验；条件 router、前置充分性、scope 与 semantic pass 仍由原 AI owner 判断。

Phase Index 与 Phase 1 相邻，唯一 continuation 位于该提取区间之外。正常入口保留当前
步骤、适用全局约束及原 producer 恢复定位；完整接收会话/phase/recovery 细节仍由同一
workflow 按实际条件加载。upstream extractor、hook、trellis-* 入口及其 API 不改。
legacy 正常路径只识别并转交，实际维护加载 managed legacy reference 和原 package 合同。

上述是本次源码检查可见的差额，不据源码或受管文件存在宣称 installed、实际 Agent、
远端项目或生产环境已采用。唯一验证观察位于
[#792 Test](../../requirements-design-test-contributions/792-step-context/test.md)，后续事实仍由其原 owner 维护。

## 3. Owner、当前执行与历史观察

| 对象 | 保持的唯一责任 |
| --- | --- |
| 全局顺序、mandatory invocation、typed exits/consumers、router/stop 条件 | Guru workflow 及其唯一 managed routing reference。 |
| 各 Skill 完整语义、入口前置、I/O/projection、private recovery | 原 Skill owner 与 Interface；查询不读取 private checkpoint 作为公共合同。 |
| query、reference 读取和客观图一致性 | 原 discovery/installed runtime；不解释条件或决定下游资格。 |
| phase/step/continuation 结构提取 | upstream native extractor；Guru 仅组织自己的 Markdown 正文。 |
| matching 分发、冲突、sidecar 与 Task/session 保留 | 原 preset/tools/upgrade owner；不手工复制受管投影或改业务状态。 |
| legacy conversion/archive/history/control retirement | 原维护 owner 的实际入口与准确来源，不由正常 runtime 接管。 |
| 隔离知识与共享晋升 | Task writer 准备完整候选；Architecture/RDT 各原 owner 在 final integration 分别单写。 |

正常新 source/installed runtime 与出口查询为 reference-only，没有旧 inline reader、
fallback 或双读。旧安装在原 owner 完整更新前继续使用自己的 matching provider，不能把
旧布局交给新 runtime。其 Task/Delivery、scope、selection、固定 B 和已发生副作用保持。

compatibility verifier 只对显式 `before_observation` 的旧 before-snapshot 保留原 inline
标记读取。这是已有只读历史输入覆盖，不用于当前 installed 成功或正常执行资格。
新 candidate preview 显式使用 matching source reference，installed snapshot 使用 matching
installed reference，不能混装。该原观察分支由 verifier owner 维护；当其受支持 before
样本不再含 inline 时，删除分支及对应定向用例。它不使本批成为完整矩阵任务。

## 4. 决策、代价与重评

采用 `target_native`。具体决定与替代比较见
[ADR-STEP-CONTEXT-LOADING](../adr/step-context-loading.md)；完整能力定义见
[ARCH-CONTEXT-001](../03-domains/workflow-context.md)。选择复用原命令、reader、native
提取和 preset，避免新增 wrapper、状态、缓存、ledger 或脚本语义 router。

收益目标是减少 AI 的查找和无关正文加载，不是由文件长度推导运行效能。确定性查询仍
读取并校验完整 matching 图；每次合法出口增加一个显式查询，维护者也要同步真实 reader、
reference 与受管资产。单一图正文避免手工维护另一映射。实际总耗时、加载内容与维护成本
需由真实观察说明，本贡献没有固定降幅、性能或生产效果结论。

若消费者不再需要该投影、native 提取接口变化、图与 Interface 的职责变化、真实 legacy
输入退出，或观察显示上下文成本被转移到重复查询/其他 owner，应由原 owner 重评。
不能为未知未来需求预留更通用 include、缓存或兼容层。

## 5. 原 concerns 的本批承接

| 原 concern | 适用性、理由与落点 |
| --- | --- |
| authority-binding | applicable；固定 before、Issue #792 与阶段适用 baseline/change contract 明确，正式当前资格仍由原 Architecture invocation 绑定。 |
| constitution-binding | applicable；实际命中 mature-practice-applicability、concept-semantic-completeness、cohesion-change-isolation、minimum-necessary-complexity、debt-one-way-convergence，分别对应官方扩展、完整 consumer、原 owner、最小投影和直接演进；不复制原则正文或评分。 |
| boundary-and-decision | applicable；加载/发现/分发改变，但生命周期与 AI 权威不变；唯一 target_native，ADR-035 保持，本次 ADR 只补加载组织。 |
| owner-and-single-writer | applicable；本节前述 workflow/Interface/runtime/native/安装/维护/晋升职责分别单写。 |
| compatibility-and-exit | applicable；正常 runtime reference-only；verifier 原 before 只读分支有明确 owner、退出和删除条件，无新 legacy authority。 |
| gap-and-deviation | applicable；本批针对全表必读及出口查询缺口，要求实现、真实消费和 matching 采用共同闭合；不据局部源码声称 GAP 已关闭或豁免其他范围。 |
| parallel-scope | applicable；只准备本 D1 完整目标，不竞争共享 roots、ownership、index 或其他 Task。晋升前仍核 live expected-current。 |
| evidence-and-freshness | applicable；before 不变，当前实际代码及拟写正文须一起进入完整 candidate；source、installed 与 Agent 证据分别判断。 |
| review-and-promotion | applicable；独立 Architecture 和 candidate Check 先读完整实现/拟写，原 final_integration 晋升/readback，之后 actual after 重绑最终 Check 和完整 committed Review。本文不补造任何结果。 |

## 6. 必要关系与采用限制

RDT 的实际目标为 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md`，
分别承接 R792-01..05/BEH792、D792-01..04/CON792、T792-01..06。它们的完整 proposed
正文位于本 Task 的 RDT 隔离贡献内，由原 RDT owner 在同一 final integration 实际承接，完整最终候选核验三层当前正文；不能从本贡献推断其晋升结果。

本批 Architecture 已整合本贡献、必要 ADR 和独立 DOMAIN 完整单元。根入口身份、
发现方法、既有 ownership 条目及共享索引不变，因此不向它们逐项登记。原 owner 若发现
真实同能力/关系重叠，按 current-knowledge 整合仍有效条件，不能仅凭路径分离直接晋升。

采用单位、普通错误和在途边界见 [MIGRATION-792](../../../trellis/presets/guru-team/MIGRATION-792.md)。
本贡献不预填 Check、Review、Completion、发布或 Release pass，不证明其他仓库或所有平台已采用。
