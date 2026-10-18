# #331 D1 当前有效知识设计

## 1. 设计目标、需求承接与内容基线

本批覆盖 Task accepted_scope 的 AC331-01..10，场景见本 Delivery PRD 第4节。开发基线和内容范围 B 均为 `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`，来源是用户指定 main；已由原 DeliveryProjection.content_base 核对。Planning H0 也是该提交，仅为起点。最终 H 由实施确定，PR 目标是 `castbox/guru-trellis:main`，不能用目标 ref 推进改变固定内容 B。

阶段适用 RDT 为 `current-main-0.6.17-guru.109`，Architecture 为 `.100`。constitution 是 `docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1`；change contract 为 `docs/architecture/06-governance/change-contract.md`。真实 candidate_assessment 选择 `architecture_impact`、`legacy_boundary_convergence`，命中 ADR-005/009/028/030。它要求完整正文、实际通用源和有退出的旧读取边界。尚无实施通过结论。

## 2. 当前系统、边界与目标差额

这是首次、全量 D1。现有 RDT `.109` 经 `.108` 等入口逐层继承贡献；`docs/architecture/06-governance/rules.md` 和 change-contract 先陈述旧晋升顺序，再追加 ADR-030 后继。项目 RDT spec 投影还持有 `.89/.86` 的过时版本。两套维护 Skill 已有独占职责、隔离贡献、晋升及阶段适用性，本批保留这些机制。

目标是让维护方按能力选取完整当前单元，再展开必要关系。新正文不是整个仓库历史的摘要，也不宣称一次迁完全部历史。实际迁移至少覆盖 Task/Delivery 生命周期、Completion/Closure、知识维护三个 RDT 单元，以及 Architecture 的晋升治理和两层栈关系。其它尚未迁移的对象继续由明确 legacy inventory 指向原完整来源，不能把未知内容标成已迁移。

## 3. 来源设计处置（唯一）

| 规范性来源及条款 | 原承诺与处置 | 本方案落点、理由和影响 |
| --- | --- | --- |
| RDT Skill references/contract.md 首段及追踪段 | retain：一个三层 authority、每项 requirement/behavior 有 design 与 test 关系；并行贡献隔离 | 第4/5/6节沿原四 profiles 管理完整单元，不引入第二维护方或独立生效结果。 |
| 同合同 Stage applicability | retain：阶段适用版本可取不可变版本/Git；无关 CURRENT 推进不使任务过期 | 第7节固定旧 Task 读取，晋升仍核对实际 expected-current。 |
| Architecture Skill references/contract.md Authority model/Independent assessment | retain：FOUNDATION/CURRENT/TARGET/GAP/PLAN/ADR/EVIDENCE 分工、fresh 独立评估 | 第4/6节同原 owner 及关口；新导航不作语义裁判。 |
| 同合同 Planning3.0/Pre-Check promotion4.0 | retain：candidate 与 final 两目的；独立 Phase2 评估后原 owner 晋升，最终 Check/committed Review 覆盖实际写入 | 第6节按 ADR-030，移除被替代的当前执行措辞但不改旧快照。 |
| Constitution 最小复杂度/职责隔离/债务收敛 | retain：实际 consumer、唯一正文、局部兼容和退出 | 第4/7节不用新服务、解析器、通用索引平台或无限双写。 |
| AGENTS 官方扩展与分发要求 | retain：Markdown 定义行为，脚本仅执行事实；canonical 同步安装副本 | 第8节完整 preset reapply/drift/代表性安装更新。 |

Issue #331 自身是目标及验收来源，没有预选目录或知识产品。以下布局是本次 Author 细化，不将其表述为用户预定设计。

## 4. 模块、职责与设计取舍

1. **可复用读写合同**：在 canonical RDT package 的 `references/current-knowledge.md` 定义完整单元、身份/状态/必要关系、查询和修订方法。Architecture 原 package 明确加载同一通用合同并保留其专属语义。两 package 的 SKILL.md/contract.md 连接日常 profiles。采用现有 package distribution，无新公共 Skill/API/schema。
2. **项目 RDT 正文**：`docs/{requirements,design,test}/current/` 按 `task-delivery-lifecycle.md`、`completion-closure.md`、`knowledge-maintenance.md` 三组组织。Requirements 含完整行为/条件，Design 含责任/契约，Test 含策略/场景/预期及真实结果的唯一 locator。`current/README.md` 是身份、状态、别名、位置、必要关系的导航，不重复正文。现有有效 REQ/BEH/DES/CON/TST/SCN 身份保留，新身份用主题稳定前缀。无需将长 package 规格逐字复制；完整接口规格仍由其现有 canonical source 拥有，单元须展开本能力行为及关联条件，不能只是链接集。
3. **Architecture 正文**：在现有 governance rules/change-contract 的同一正文位置收敛晋升及适用性定义，保留原 ARCH-GOV identity、ADR-005/028/030 来源；移除当前执行位置中已被窄替代的顺序，旧 Git authority 不改。新增 foundation `stack-selection.md` 只定义项目选择、适用范围、约束及差异。
4. **实际通用栈源**：`trellis/knowledge/technology-baselines/trellis-extension/versions/1.0/baseline.md` 是独立、版本固定的可复用 Trellis 扩展技术基线，旁置 README 导航。拥有技术栈选择、官方扩展面、Markdown/执行边界、平台分发和验证边界。源方和项目方均通过原 Architecture 维护 Skill，在各自正文边界写作；项目私有分支、Task、开发路径不得进入通用源。本项目 foundation 精确引用版本，不复制共享定义。
5. **迁移与采用**：`trellis/presets/guru-team/MIGRATION-331.md` 列新旧入口、迁移单元/前驱来源、切换、失败恢复、未迁移边界、在途使用方与退出。旧版版本入口保持字节不变；新 successor RDT `.110` 和 Architecture `.101` 仅在原 owner 晋升后生效。重构过时投影为解析实际 README authority 的定位文案，避免重复可变版本。

选择人工可读 Markdown 单元及薄导航，原因是现有 consumers 已按 locator/version/profile 读取，且 AI 已负责语义关联。全文搜索只是发现工具；不用自动按日期选权威、向量库、双向链接解析器或新知识状态机。公共路径新增是 additive，既有 source/Task/Delivery/exit/schema 不变。单元快照用 Git 定位，不保留另一套可变历史正文。

## 5. 接口与数据

公共 Skill 输入/出口保持现有 profiles/DTO。原 RDT `task_impact_sync` 先选阶段适用 authority，再按问题/稳定 ID 读取相应完整单元；原 `promotion` 把隔离 delta 语义合并成完整单元并核对 R/D/T 关系。Architecture 使用其原 candidate/final/phase2/branch_review/promotion 入口，加载通用基线和项目投影的明确 locator/version。缺口仍走原 revision/repair/blocked 出口。

单元正文至少可辨认 identity、适用版本/状态、完整定义、必要关系、来源和替代范围。此为 Markdown 内容职责，不制造 JSON 总对象或额外 required fields。导航只承载 ID/alias/status/locator/relations；其 content 不独立授权规则。替换/删除保留前驱与后继位置；拆分/合并分配真正新身份，旧身份可定位到变更关系，无关 ID 不变。

贡献仍在 `docs/requirements-design-test-contributions/<TaskId>/` 和 `docs/architecture/contributions/<TaskId>.md`。原 promotion owner 读实际共享目标，核对贡献 base，串行合入完整定义。两个正常任务互不写对方贡献。历史 contribution 不删除、不回填改写为新 current；新 current 的来源可追踪到其具体条款。

## 6. 状态、顺序、正常与失败流程

查询：判断 Task/阶段/候选适用性 → 从对应导航或稳定引用选完整单元 → 读必要 R/D/T 与 Architecture 关系 → 区分 current/accepted target/unconfirmed/history/superseded → 输出带约束答案。只有解释原因或旧版本才展开历史，不将回放全链当普通查询前置。

修订：定位行为及关联 → 判断新增/修改/删除/替换/拆分/合并及 Architecture 影响 → 写本 Task 隔离 delta 与完整目标内容 → 原 owners 检查语义/追踪/冲突 → 独立 Phase2 读完整候选及 proposed targets → 原 owners 按 expected-current 晋升 → 核对实际写入及适用性 → 最终 Check → commit → 独立完整 committed Review。workflow 仅调用原 owners，不复制其内部方法。

来源缺失、断链、范围冲突或未迁移时，说明具体对象与受影响结论，保留原来源，转原 repair/Clarify，不猜出“最新正确答案”。正常 expected-current 改变由原 owner 比较真实差额；无关推进不触发旧 Task 重写。无攻击、锁、压力、crash 扩展。

## 7. 恢复、兼容、迁移与集成

迁移前以 B 固定旧 RDT `.109`、Architecture `.100`、其完整贡献和 stable refs。迁移清单逐项注明实际 predecessor locator/条款、目标单元与有效约束/后继。仅在 AI 完整性核对、追踪检查、真实 Agent 样本和安装验证满足后，将共享 README 指向 reviewed successor。切换未成时 README 维持旧 authority，候选标为 proposed，不能声称 current。

旧 Task 的实际使用方为引用旧 RDT/Architecture 版本的在途 planning/candidate/gates；它们仍使用相应 immutable snapshot/Git B。兼容范围只读旧知识，不向旧 current 继续写新能力。该 Task 结束、reactivate 合法改选或原 owner 判断真实依赖改变后，旧普通读取退出；历史追溯永久保留，不等同无限双写。

共享晋升失败只写未冲突的原 intent；来源不唯一则停在原 owner。尚未切换可删除本 Task 候选并保留旧入口；已切换的 ordinary correction 走原 repair/新受审 successor，不重写已固定快照。不是业务数据/生产配置迁移，无数据库回滚协议。preset update 沿匹配源码 reapply，保留用户指令，逐个处理 sidecar，禁止只 patch 安装副本。

## 8. 验证设计

以下样本与判据在实施前固定。基线语料取 B 的真实 canonical 文档与必要历史，新侧取实际迁移正文；需进行写作实验的临时副本保留同一正常起点、语义和预期。测试 owner 的必答表不注入受测 Agent。每组 old/new 各3个独立 native Codex 会话，共24次；固定同一模型/配置，查询 read-only、修订 workspace-write，双方权限相同。模型不得读另一侧结果；工具输出/注入/指令均计量。不得通过把答案放进提示缩短新侧。

| ID/场景/AC | 固定问题或修订输入 | 必答事实、必要条件与范围 | 判据 |
| --- | --- | --- | --- |
| V331-A / S01/02 / AC01/02/09 | 查询多轮 Task/Delivery 生命周期；说明晋升与最终 Check/Review 的执行顺序和旧规定替代范围 | 整体 Task 与 slice 分开；Creation/Planning/Activation/Check/Commit/Review/Delivery/Completion/Closure/Finish 的原职责；ADR-030 Phase2→promotion→最终 Check→commit→独立 Review，ADR-028 适用性；必要来源可追溯 | 每次答案正确完整；三次中位文档加载字节与历史拼接步骤均下降，分别报导航/必要正文/重复/无关历史。 |
| V331-B / S03/04 / AC03/04/09 | 在临时正常仓库中为 Completion 的补充验证说明插入独立知识条目，并拆出“Closure 不等于 Finish”子条目；不改变运行 API | 正确修改相关 Requirement/Design/Test，判断 Architecture 是否受影响；保留旧身份映射/新子身份与无关 ID；不改业务脚本或历史快照 | 每次一致修订；真实改动正文/关系及无关修改可核对；新侧中位历史拼接步骤减少或无关维护减少。 |
| V331-C / S05/07/08 / AC05/07/08/09 | 两个 Task 分别增加已有验证场景说明与稳定引用，按正常贡献→晋升顺序执行；旧 Task 保持 B 适用版本，新查询按 successor | 两贡献隔离；晋升后完整单元含两项增量及原约束；旧 Task 不因无关推进重写；同一含义/条件/来源不丢；历史可读 | 每次正确；新侧减少晋升后查询的历史拼接。正常兼容子项仅要求正确，不强求节省。 |
| V331-D / S06/09 / AC06/08/09 | 查询并补充通用栈/项目投影的一个项目差异；另给正常缺失源/断链/未完成迁移条件 | 精确源/version；源 owner 与项目 owner 分开；差异只落项目；来源缺失指明受影响结论并原 repair、不报告完整；不把 target/inferred 当实现 | 两侧用语义等价两层 fixture（旧结构/新结构），完整来源来自实际通用源；三次每次正确；兼容/缺口只要求正确。 |

每次保存临时原始 JSON events、实际命令/路径/输出字节/最终答案/usage；AI owner逐次判断完整性。总 input_tokens 含平台公共注入，cached_input_tokens 单列，不从总量扣除。工具实际加载内容与定位步数是主要可控读取成本。重复/历史类别由 AI 据读取轨迹分类，脚本只收集。无导航生成器，生成成本为首次人工迁移、每次关联导航修订及 reapply；实际改动量另报。失败保留首次结果和修复；改变样本/环境须双方同口径重跑。最终唯一 Test 记录全部24次的简要结果/成本/失败和限制，完整 traces 不进 repo。

V331-E 对真实迁移逐条核对清单、前驱/后继与 R/D/T 关系，执行两 package focused tests、公共 package/source validators、workflow/overlay 检查。V331-F 完整 preset apply 到 dogfood，运行 drift，检查 sidecars；一个代表性 clean throwaway 安装实际包，再从旧匹配安装更新/reapply，保留用户指令并核对公共入口和新引用。此非完整多平台 Release matrix，也不证明生产业务采用。

## 9. Canonical 引用、本轮差额与实际未决项

RDT 原 writer 在 `docs/requirements-design-test-contributions/331-current-effective-knowledge/` 写本轮 R331/BEH331→D331/CON331→T331 及迁移关系。新正文需吸收受选历史来源的全部仍有效约束。Architecture 原 Author 写真实 `docs/architecture/contributions/331-current-effective-knowledge.md` 与 ADR-031 候选，说明 current authority 组织和兼容退出；Phase2 独立评估后原 owner 按 ADR-030 晋升，最终 committed Review 覆盖所有写入。

现有命中包括 `.109` 三层 versions 及其 reviewed contributions、Architecture `.100`、ARCH-GOV-008/009、ADR-028/030、两个 canonical Skill、workflow 与 docs/architecture spec projections。本批改变组织、读取和晋升后的完整正文维护，不改变 public runtime I/O。没有产品范围未决项；source 缺失或无法完成真实对照会阻塞相关 AC，不以计划填充替代证明。
