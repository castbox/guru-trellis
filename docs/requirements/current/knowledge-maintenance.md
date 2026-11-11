# 当前适用知识的读取、修订与晋升

导航别名：`REQ-007/BEH-007`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。这些检索别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/requirements/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

本次 #649 最终整合的完整前驱：Git `4fea68613de4181d7cb55532b8758515472ba31b:docs/requirements/current/knowledge-maintenance.md`。贡献、#657 继承及原来源见 [#649 追踪](../../requirements-design-test-contributions/649-stage-result-convergence/traceability.md)。

知识单元：`RDT-REQ-KNOWLEDGE`。状态：`current`。authority identity：`guru-trellis-rdt`；精确内容由包含本文的完整 Git revision 与 locator 定位。前驱 RDT `.109`、Architecture `.100`；固定迁移源 Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`。候选正文须经原 owners 晋升才进入共享 authority，不因目录名 current 自动生效。

## 唯一 authority 与完整知识

`REQ-007/019/027..035`、`BEH-007` 保留身份，并按下述阶段适用性及 ADR-POSTCOMMIT-INDEPENDENT-REVIEW 承接当前时序。RDT 由唯一 `guru-maintain-requirements-design-test-ssot` 管理一个 Requirements/Design/Test repository authority。每个活动 requirement/behavior 均有 owning design responsibility/contract 和至少一个 test strategy/scenario/case，双向关系保持。Architecture 独占项目 FOUNDATION/CURRENT/TARGET/GAP/PLAN/ADR/EVIDENCE、constitution/决策/owner/兼容/历史；RDT 只继承其公开 locator/version/status，不读 private state，不复制架构正文。task-local PRD/design/implement 是 Task planning，不能冒充 repository authority。

`R331-01 / BEH331-01`：读者先按问题、Task、阶段和候选选择真正适用来源，再按能力/行为/接口/职责或稳定 ID 到完整单元。当前有效要求、已接受目标、未确认、历史和 superseded 内容分开；target 不冒充当前实现。读取必要关联（条件、否定、例外、顺序、依赖、设计、测试、Architecture），不无限展开所有链接。导航仅存 identity/alias/status/locator/关系，不是另一份业务摘要。搜索排名、日期和编号不决定 authority，命中标题或摘要不替代正文。解释旧决定或原因时按需读历史；普通当前查询不要求重放全部版本/贡献。

当前单元是原 owner 在已声明能力范围内合并的完整定义，历史 contribution 保留来源责任；晋升后后续查询不能仍靠贡献链补出遗漏规则。精确 public API/schema 仍由 canonical package 单写，单元展开能力行为并指向必要完整接口，不复制接口成第二来源。单元 revision 由完整 Git snapshot 与 locator 定位。根 authority identity 稳定，普通 Task 不强制递增全局版本或写根 README；只有入口自身身份、范围、状态、位置、查找合同或必要关系真实变化才改入口导航；独立主题不作共享逐项登记。真实 public API/schema 版本继续独立维护。

## 一致修订、身份与隔离

`R331-02 / BEH331-02`：原 maintenance owner 先读变更和受影响完整单元，判断 R/D/T/Architecture 关联、新增/修改/替换/删除/拆分/合并，再由对应 owner 写本 Task 隔离贡献。正常并行 Task 使用不同 `docs/requirements-design-test-contributions/<TaskId>/` 和 Architecture contribution locator，不互写对方，不竞争 shared current。必要时可由原 owner 判断窄 direct sync，但不能由 caller 自封同步。

展示顺序、移动或插入不改变既有身份。替换/删除保留旧 identity 的变更关系、历史和 successor；拆分/合并给真正新对象新 identity，保留前驱及各继承/替代范围。无关 ID 不批量重编号。只更新真实相关对象；无影响层说明依据，不为形式一致改全部文档。来源冲突由 AI 判断，不能脚本按最新 wins。完整 trace 是 requirement/behavior → design responsibility/contract → test strategy/scenario/case；关系表存 identity/locator，不重复来源 prose。

## 四 profiles、日常闭环与晋升

RDT 保持四 profiles：bootstrap_foundation 建立/复用/迁移兼容三层 authority；task_impact_sync3.0 对批准 delta 判断 no-op、完整 isolated candidate 或 revision；promotion3.0 在 final_integration 审查 contribution、subtraction、trace、历史和 Architecture inheritance 并实际写入；repair 修复具体 authority/navigation/迁移缺陷，不扩需求或改无关历史。bootstrap/repair 原合同不变。

Planning、实施、提交后独立完整 Review、Delivery Review、Completion 和 Finish 各自读取阶段适用的完整正文与必要关系。Planning 选择唯一 ssot_first、delta_first、bootstrap_or_repair_docs 或 no_docs_update_needed。实施先形成完整隔离候选；candidate_ready 只表示贡献和完整拟写可供原维护方整合，不表示共享 authority 已更新。无变化返回真实 no-change，不创建空 contribution、ADR 或提交。

`R331-04 / BEH331-04`、`R600-01..06` 与 `R638-01..07`：Planning 批准后，implementation 完成全部实现和真实工程验证。原 RDT/Architecture owners 在提交前 final_integration 读取完整 proposed targets、适用来源和实际 target，保留所有仍有效条件并整合。它们不要求尚未发生的独立 candidate Check 或提交前独立 implementation Architecture pass。原 owners 一次固定真实目标 branch/commit；不同单元保留未命中内容，相同单元比较 applicable base、双方 proposal、真实 current 和受影响未改 consumers。Git 文本合并不替代语义判断；需求前提改变回 scope/Planning，接口或验证义务改变回原责任方。

原 owners 实际写入并逐个读回 targets，判断 postwrite applicability。Architecture 输出 integrated_pending_review，RDT ssot_current 只证明已完成文档整合；它们不宣称独立质量通过。TaskCommit 将所有实现、正文、关系及导航真实 after 纳入精确本地提交。随后 implementation 用固定 B、实际 committed H 和完整 paths 构造候选并 begin_check；新的独立 reviewer 在同一次提交后完整 Review 中先读 before constitution/baseline/change contract，审真实 B..H 与未改 consumers，完成一次 implementation Architecture before/after，再完成原九维及完整 Branch Review。真正通过才顺序记录真实 check/full_review；不是两个独立审查步骤。

无影响走 no_change，无空贡献或提交。Architecture 只有真实 committed before/after 已独立通过且实际整合完成才是 reviewed_promoted。readiness/Publication/Completion/Finish 只接受适用 no_change 或 reviewed_promoted；integrated_pending_review、文件存在、导航或旧 pass 不能代替当前完整判断。修复由原 writer 形成后继提交；冻结候选审查期间不改正文。原覆盖、工程结果和 base 集成按唯一适用性合同判断，真实差额和影响必须覆盖。

expected-current mismatch 只影响本次实际写入，由原 owner 重读真实差额，不自动判全部在途 Task 过期。partial/output-loss 由原 owner读取同一明确 intent，完成已写 targets 的 readback并仅补 pending；真实冲突或不唯一时停止，不新建状态机、全仓 hash账本或第二 current。无关目标前进不要求 merge/rebase 或追赶 SHA。

## 阶段适用版本与实际变化

`BEH567-02/03` 保持，窄替代旧 `REQ-034` 的“一切 current 前进强制 sync”。原 owner 选择 Task plan/候选/阶段适用 RDT 和 Architecture，可以用 immutable version 或 Git history。无关共享 CURRENT、navigation、archive、remote ref 或 tool 前进不替代它，不强制贡献重写、业务门禁重跑或 branch 同步。明确适用于该 Task 的规则、失效假设、scope/dependency/solution 改变，仍回原 revision/assessment。promotion 自己仍读 live current 并校验本次写边界，两种时钟不能混淆。

`R578-01..04 / BEH578-01..04`：当前 semantic judgment 和工程命令事实分开。每次 owner 都新作当前完整判断并绑定当前 invocation；合法、可核查且实际 check定义、依赖、参数、预期、工具链和环境仍适用的工程事实可跨 owner/stage 使用。unknown/missing/真实变化才重跑受影响命令。不能借旧 semantic pass、同路径或相同 code tree 免当前判断，不读退休 private checkpoint 或造 cache/ledger。采用结果说明原来源和适用依据，不声称自己执行。

## Architecture 维护的既有判断边界

原 Architecture owner 在 Planning、合格的 implementation discovery、独立 committed Branch Review、publication 和 acceptance_finish 判定阶段适用性。项目正文唯一声明 constitution locator/version；Guru 只消费其五个 identity/short names，不复制原则正文、逐项评分或 verdict。无 Architecture 影响保持 no-impact/no_change 快速结果，不制造 contribution、ADR 或 project-check负担；有影响必须恰好选择 target_native、legacy_boundary_convergence、dedicated_refactor_slice 之一。

项目 change contract 必须承接真实 requirement/behavior、baseline/constitution、domain/integration/decisions/GAP、required concerns、current/target owners、single-writer、compatibility exit、parallel scope、偏离/删除条件、design responsibility、before/after、checks/evidence和promotion写边界。普通Task只写本方contribution；改变decision、原则例外/权衡、GAP lifecycle、owner/single-writer或compatibility exit才需要ADR candidate。implementation discovery 仅在实质边界变化时进入；提交后独立 Review 审完整固定范围，不能拿 Planning 或整合事实替代。

项目check的适用性、规则/decision/GAP关系、结果层次和证据缺口由该owner新判。适用blocking check失败或未验证不支持baseline_current；非blocking缺口明确保留，不用于关闭GAP或批准例外。新/恶化责任偏移回fitness_regression；authority冲突回architecture_conflict；缺必要合同/来源回contract_incomplete或原bootstrap/blocked；stale本次晋升写边界回sync_required。具体descriptor/DTO仍由Architecture canonical合同拥有，RDT不复制成第二判定器。

## 两层 Architecture 来源

`R331-03 / BEH331-03`：通用技术栈 baseline 有独立正文 owner 和明确 source locator/version；项目 Architecture 维护选择、范围、约束及差异。项目变更不授权修改共享定义或升级别的项目，项目私有 Task/分支/配置不能进入公共源。通过原 Architecture maintenance Skill 分别在各自边界写作，不引入第二 owner。真实 generic source 和项目投影分别由 [technology baseline](../../../trellis/knowledge/technology-baselines/trellis-extension/versions/1.0/baseline.md) 与 [stack selection](../../architecture/00-foundation/stack-selection.md) 定义；本层不重复其技术选择。

外部源须明确位置/版本/取得方式和缺口。来源明确的去敏副本/临时 fixture 可验证读取合同，不能冒充外部采用。缺必要源、断链、authority conflict 或未完成迁移时，说明具体对象、缺口与受影响结论，保留可读原源，进入原 Clarify/repair/blocked；推断不成为 confirmed/current。

## 迁移、退出与分发

`R331-05 / BEH331-05`：切换前明确 predecessor/版本/文件、稳定关系、替代范围、保留条件、失败恢复和 legacy inventory。完整性/追踪/真实场景核对未满足则旧 shared entry 保持，新正文 proposed，不宣称 current。正常恢复不改旧快照；晋升后 correction 走原 repair/新 successor，不回填不可变版本。

旧在途 Task 的实际 planning/gates 仍读原适用版本/Git authority；兼容只保留必要旧读取，不向旧 current 双写新能力。Task 完成、合法 Reactivate 改选或真实依赖改变后，该 Task 的旧普通读取退出；历史追溯可永久保留。尚未迁移主题必须明确走旧完整源，不能在导航中写已完成迁移。

canonical workflow/Skills/spec/preset 是长期源；dogfood 与 installed 是受管投影。matching installer/update/reapply 迁移必须处理用户修改、`.new/.bak`、mode 与漂移，不将 source 改动等同业务安装采用。公共 I/O 保持兼容；破坏变化需新版本/迁移。完整 Release/Upgrade matrix 由其专门 scope 负责，普通知识变更只做本 accepted scope 的最小可靠证据。

`R331-06 / BEH331-06`：实际采用必须有真实 Agent 同问题、同语义/预期、同模型/权限/起点、多次 old/new 对照。样本/必答事实/关联修订范围/次数/成本判据在实施前固定。导航/必要正文/重复/无关历史及注入/工具指令均计成本；总 input 与 cached 分列。报告逐样本正确性、读取量/步数、维护改动量、首次失败和修复。历史拼接查询须有实际收益；修订减少拼接或无关维护；兼容只要求正确。不能以更少字节抵消错误或漏条件，不能用静态链接/schema 或一次成功代替行为验证。

## 关系与完整规格

设计：[`RDT-DES-KNOWLEDGE`](../../design/current/knowledge-maintenance.md)。测试：[`RDT-TST-KNOWLEDGE`](../../test/current/knowledge-maintenance.md)。[迁移追踪](../../requirements-design-test-contributions/331-current-effective-knowledge/traceability.md) 定义来源和未迁移范围。原 [RDT Skill](../../../trellis/skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/SKILL.md)、[Architecture Skill](../../../trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/SKILL.md) 和本轮共享 current-knowledge 合同拥有各自公共规格与方法，不复制 private artifact。

## 约束、前提与原 owner 修订

来源：[本项完整来源](https://github.com/castbox/guru-trellis/issues/648)。本节补充原读取、适用性和质量职责，不替代上述 R331/R578/R600/R637/R638 的条件或公共接口。

**R648-01 / BEH648-01**：Author 读取适用约束的来源、对象、完整条件、否定和例外，在本批实际设计及唯一来源设计处置中说明行为落点。引用、retain声明或原则复述不证明符合；不复制基线全文或建立逐约束台账。

**R648-02 / BEH648-02**：Architecture 区分规范性约束、事实证据、已接受设计和关键假设。对影响可行性、职责、拒绝条件或阻塞依赖的前提读取原证据，前序ADR、批准、晋升与实现/测试一致不能豁免。合法例外按真实来源、范围及修订依据判断，不制定无条件文档优先级。比较原适用authority与候选，候选拟改baseline/ADR/预期不能自证；真实修订由原owner取得有效来源后处理。独立审核隔离通过叙述，同时取得必要约束和事实；缺事实保留不确定性并走原incomplete/blocked。

**R648-03 / BEH648-03**：实施发现已批准方案违约、关键前提不成立或无法满足原承诺时，即使scope未扩张也暂停受影响操作，返回条款来源、实际候选落点和影响。需求/约束有效而方案错，回原Author/Architecture修方案、保持accepted scope；承诺、规范来源或例外authority冲突，或确需改scope，回原Clarify，Architecture只提供具体架构冲突，不成为全部来源处理的新前置；规划有效而实现/断言错，回原implementation/Check。实施者不自行修改需求、baseline或错误预期。冲突已解决、受影响规划与审核及实际候选重新匹配后才恢复；无冲突工作按真实依赖继续，脚本通过和旧批准不足以恢复。

**R648-04 / BEH648-04**：Check/Branch Review先从有效合同确定应观察行为，再审实现、测试入口及断言。状态、开关、迁移或执行分支变化时，检查实际前后状态和真实受影响未改consumer，不机械生成全状态矩阵。有原证据的职责违规属于合同缺陷，不要求先发生生产功能故障。设计、实现和测试共同采用错误预期时，仍须指出共同错误，不迁就实现弱化断言。

**R648-05 / BEH648-05**：区分有效约束要求的依赖与机制无依据新增的限制。后者回原机制/Architecture，不能伪装成外部证据待补。task-free目标或执行涉及gate/admission/phase/switch/rollout时，执行owner识别保护对象、不变量、最小触发迁移、不适用operation、缺证据实际阻断范围和真实evidence owner/consumer。无依据跨能力前置导致停止受影响target write，走原evolution/scope route，不扩大编辑。同域A不改变不变量，缺同证据仍成功；B改变不变量，缺证据失败；共同错误限制A仍须检出。通用规则不带业务专属名称。

**R648-06 / BEH648-06**：新增证据否定原结论关键前提时，即使代码/测试未变也刷新受影响判断。其余覆盖与可核验工程事实按原适用性承接；组合影响不能界定时完整评估，不因阶段/reviewer变化无因重跑，不跨读或重建退休private状态。

**R648-07 / BEH648-07**：本项先冻结当前匹配版本，用保留失效关系的去敏真实Agent样本核验，再补实际方法/验证缺口。Agent自己读文件、作判断、写结果并调原wrapper，host期待不注入。改变方法后在相同或严格等价输入、模型、权限和起点复核，逐次审核条款、因果、预期和原owner路由；两边均检错记已有能力。Author落点、实施停点/分流/恢复、Check/Review、未改consumer和A/B在本项实际证明，不延期#649。保留失败和未验证边界；结构/出口/绿命令不独立证明效果。源码分发、实际Agent行为、安装采用分别报告。只用命中定向验证，最多一个代表clean，不扩完整Release/升级矩阵。

## R649：解除限制、当前说明与晚到事实

**R649-07 / BEH649-KNOWLEDGE**：原 maintenance owners 从真实解除条件及适用来源维护完整当前单元、使用指南和派生说明。删除或替换当前有效指令中的过期限制，并保留历史观察及其来源、适用阶段和截止点。局部缺口不扩为其它能力的全局否定。具体阶段限制与成果维度由 [生命周期](task-delivery-lifecycle.md#r649阶段限制与当前成果) 和 [Completion](completion-closure.md#r649阶段成果维度与缺口分类) 定义。

结果入口准确定位唯一实际 Test 与后续正式结果。晚到正式事实不要求回填受审正文自身最终结论；需要真实内容修订时，由原 owner 纳入完整候选、实际晋升及最终覆盖。#637 当前 Test 仅修正可证过期描述和观察截止点，并引用原正式结果；原命令、旧失败、当时未知及其它未证项目保持原义，不因 PR 合并全部转为通过。

本规则保留 R331／R578／R637／R638／R648 的完整来源、工程事实适用性、隔离贡献、原 final_integration 实际写入与读回、TaskCommit、完整 committed candidate 绑定和独立完整 Review。无变化不造空贡献或 ADR，稳定 identity 与原单写责任保持。

## 采用机制审核与决策纠正

**R-MECH-01 / BEH-MECH-ADOPTION**：原 Architecture owner 审核本次新增、修改、复用、扩大使用及直接影响的机制。将数据 authority、职责、协调、失败或生命周期约束带入当前路径的采用，即使共享实现无 diff，也须判断适用性；普通 helper 和无关依赖不逐个建单元。先从承诺的可观察最终结果及必要约束推导直接可行路径，再按完整设计宪法独立判断机制的必要性、范围、整体代价和可行替代。新增、修改、扩用及复用带来的额外协调默认不准入；原 Author 与独立审核主动尝试更简单路径并判断其可行性，原方案已最小或无可行替代时说明真实依据，不虚构替代。受理返回更快不自证最终完成更快，功能断言通过不豁免可避免的正常路径成本。不给予某一原则固定优先级，不以最短代码或更少 finding 证明质量。

**R-MECH-02 / BEH-MECH-PROTECTION**：新增或强化保护的提出方，包括作者、reviewer 和模板要求，说明真实要求或可信事实、现有保障缺口、补齐关系、收益、运行维护代价及合法请求影响。缺少签名、锁或重试本身不成立 finding。真实保密、权限和职责约束不以事故发生为前置。Protection 资格成立不自动成为方案批准，原 Architecture 仍按唯一方法判断简单替代、最小范围及完整正常完成成本。对安全、防御及失败保护的偏好须纠偏，不能以此取消有依据的保护，也不能声称已证明模型训练成因。

**R-MECH-03 / BEH-MECH-EVIDENCE**：适用 RDT/Architecture 已能回答能力、职责、条件和取舍时，不重复源码考古；实际行为、性能、全部相关消费者或文档冲突存在缺口时才定向查实现。正在审查的旧技术选择不能以自身排除替代；真实业务和外部合同保留，修订沿原受审变更合同实施，再按原阶段晋升。既有能力、平台原生能力和已安装依赖均须有当前适用依据；无直接 consumer 的抽象、包装、转换、配置和未来预留不进入实现。

**R-MECH-04 / BEH-MECH-UNCERTAINTY**：新保护缺证时补证、修订或撤回，不先升级为义务。旧保护缺证时不擅删，也不默认复用通过；只限制依赖该结论的采用或晋升，无关工作继续。必要性已证、可避免成本或缺陷已证、证据不足分别处理：已证缺陷沿原 owner 有界整改及适配消费者；缺证继续有界调查，不扩大机制。已有论证确实覆盖当前消费者、条件和代价时简短承接，真实前提或证据变化才补审，不因阶段或版本改变重做全部工程检查。

**R-MECH-05 / BEH-MECH-LEGACY**：纠正旧决策须识别同一决策的实际采用者、共享状态、数据、接口、配置和运行依赖。共存破坏同一约束、不兼容读写或使纠正失效时，承接必要适配与退出。可独立保留时，说明共存如何保持约束、剩余采用者、真实保留依据、owner、可执行后继交付或可观察触发条件及退出证据；未承接须如实标明，工期、改动量、链接或“下次再改”不代表安排。旧场景仍有依据时明确范围后保留，新消费者不扩入已判错模式。分析可大于实现范围，不自动授权跨仓迁移。

晋升完整单元保留决策行为、owner、范围、理由、代价、适用条件、重审触发及存量关系；使用既有正文/change contract，不新增评分、永久台账、审批链或公共字段。方法唯一正文在原 [Architecture contract](../../../trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md)、[Protection](../../../trellis/skills/guru-team/packages/guru-qualify-root-cause/references/contract.md) 与 [current knowledge](../../../trellis/skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md)。设计和测试分别由同名完整单元的 D-MECH 与 T-MECH 承接。

## R693：合同连续性与证据适用性

**R693-01 / BEH693-CONTINUITY**：执行链替换或入口扩大时，原 Author/Architecture 从实际入口追踪新生产者输出、持久完成状态及成功含义，核对仍在使用结果的消费者，包括无 diff 的读取器。复用调用须核参数实际对象、存在阶段、持久前提和顺序。Check/Branch Review 独立判断当前消费者可用性；类型、名称、生产者成功和旧 pass 不代替这些条件。差额回最早受影响原 owner。

**R693-02 / BEH693-EVIDENCE**：原 owners 对照测试声明边界与正式路径的入口/context/配置/依赖/状态/分支/观察点。边界前 fixture 和外部依赖替身可成立；边界内代产出、修正输出或绕过关键条件不能支持该边界的成功声明。入口、默认路径或启用范围变化后，分别判断旧事实保留、失效及补证范围。保留可核验且仍适用的局部证据，不将全部变化升级为全链 E2E。

**R693-03 / BEH693-HISTORY**：历史调查以当时实际规则、精确候选、条件、命令及可核验阶段结果为依据。分别表达合同失配、底层引入、影响扩大和证据适用范围；具体历史理由缺失时保持未知。源码缺陷、绿测试、空槽位或无 GitHub review 不证明某个 reviewer 未检查或如何采纳旧事实。不重建别的 owner 的 private state。

**R693-04 / BEH693-ADOPTION**：只在原方法和职责内补齐真实差额；方法由共享 workflow-contract/quality-guidelines 单写，项目指导由原 authority 承接，领域正文仍引用所属业务设计。公共源码、dogfood 和目标正式采用分别报告；后者仍由 accepted scope 的原 Task/Upgrade owners 承担。保留用户定制及在途 Task/会话，按原安装合同处理冲突/sidecar。安装成功不证明业务修复或环境效果。

对应设计为同名 Design 单元的 D693/CON693，验证为同名 Test 单元的 T693；原 R648/R-MECH 及全部前驱条件保持。

## R710：正常语义 authoring 与完整结果消费

来源仍为 [Issue #710](https://github.com/castbox/guru-trellis/issues/710)、固定前驱 Git `2fc49bda6552d1a8bf95dff243ab2de9a9ea8e30` 及 [#710 traceability](../../requirements-design-test-contributions/710-phase2-recorder-authoring/traceability.md)。本节保留正常语义 authoring、客观身份派生、完整结果合法消费及准确恢复义务；#794 窄替代重复 Check profiles 与时机。当前精确字段/argv/profile/exit 由 [Review package](../../../trellis/skills/guru-team/packages/guru-review-branch/references/contract.md) 单写；旧支持操作沿 [MIGRATION-794](../../../trellis/presets/guru-team/MIGRATION-794.md) 的 pinned provider 处置，不将旧结果改为新 pass。

**R710-01 / BEH710-AUTHORING**：新的独立 Review AI 实际读取完整 Skill、原 authoring 合同和最小语义示例，先完成当前 Architecture、九维、完整区间、finding、工程适用性及出口判断，再只 author 本轮语义内容。recorder 从合法入口和 live facts 派生客观结果身份；AI 不计算、复制或填写私有摘要或 HEAD 占位。完整结果示例只说明输出或合法消费，不能成为第二正常 authoring 路径。脚本、模板和 worker 身份不产生 semantic pass。

**R710-02 / BEH710-CONSUMPTION**：正式说明承接语义 authoring、原 recorder/checker/public invocation。checker 读取 recorder 实际产出的同一完整结果，invoke 消费真实结果和当前 profile；中间 receipt 不替代完整 owner result，caller 不重组结果。Task/Delivery/Planning、固定候选及合法原回执按其真实 consumer 传递，局部 token 不互换。当前支持 profiles 的成功、finding、规划回程和 blocked 仍有唯一实际 consumer。一次真实审查分别提供充分性与完整覆盖结论后才顺序记录两个必要公共槽，不复制空白 pass。

**R710-03 / BEH710-RETIREMENT**：record authoring 输入与 checker/invoke 完整结果消费是不同入口。MIGRATION-710 原正常输入收敛及 MIGRATION-794 的重复 Check 退休各有明确边界；保留原完整结果的合法消费与同 owner 精确恢复，不重新 record 旧语义。matching 切换不转换 pass、不长期双读；不能同步迁移的真实 consumer 回原 Author/Architecture 处理。

**R710-04 / BEH710-STALE**：普通字段、路径或候选身份失配保原 code、确定字段与原恢复 owner。摘要只证明不一致，不推断根因。业务内容变化拒旧结果，metadata 保原排除；不得重算摘要/HEAD 延续旧结论。输出丢失只从仍匹配的原语义、同候选和真实公共结果补缺步或恢复同结果；必要语义覆盖丢失须实际补审，不能制造 full_review。

**R710-05 / BEH710-EVIDENCE**：命令测试从正常语义输入经真实 recorder/checker/invoke，host 不代填私有身份。完整结果消费者单元只证明该入口。合同检查不替代 AI 亲读可执行性；正常 finding、planning rollback、blocked 与恢复分别验证，mock 或下游绿色不冒充实际 Agent。

**R710-06 / BEH710-FIRST-NATIVE**：当前真实 Agent 验证从正常安装 Skill 和合法已提交候选起点进入，原 Planning 与实际文档整合由其 owners 完成。host 只供合法事实和环境，不代填当前结果、私有摘要、内部选择或答案。首次输入、实际命令、完整结果承接、出口、失败及修订重跑如实区分；真实 finding 返回原 owner。原 #710 候选/最终专项轨迹和失败保留历史原义，不成为当前重复门禁或固定运行次数。

**R710-07 / BEH710-DISTRIBUTION**：原工具/preset owner 成套同步 canonical、dogfood、实际安装及声明平台，保留用户内容和 Task/session，按实际差额验证 reapply/drift/mode/sidecar。普通验证最多一个确有必要的代表 clean；源码、命令、真实 Agent、安装及业务采用分开。后继当前审查由原 owner 亲自执行，不新增交接 DTO、账本或业务迁移。

关系保持 D710/CON710、T710/SC710；原来源与历史专项观察保持，不将后续结果回写为先前通过。

## R711：独立知识单元与稳定发现

来源为 [Issue #711](https://github.com/castbox/guru-trellis/issues/711) 与 [本批追踪](../../requirements-design-test-contributions/711-knowledge-navigation-isolation/traceability.md)。本节收敛导航读写；上文完整定义、阶段适用、真实 API 版本、原晋升与质量边界继续适用。

- **R711-01 / BEH711-ENTRY**：根及 current 入口保体系稳定身份、适用范围/状态、真实版本引用、历史/未迁移边界与目录/稳定 ID 查找方法，不枚举全部单元。普通独立主题不更新共享登记、无关全局版本或合并历史，不将登记转移到下层 README、index/manifest/metadata 或每 PR 提交的生成索引。仅入口自身合同真实变化由原 owner 修改。
- **R711-02 / BEH711-UNIT**：按稳定能力/职责保持完整单元。日常正文与局部导航使用各自路径；修改既有能力沿原正文整合，不按 Issue 建第二 current。同一有效关系的真实重叠归关系原 owner，不能复制关系或拆散必要语义规避。
- **R711-03 / BEH711-DISCOVERY**：读者从适用稳定入口，经限定目录、稳定 ID/aliases/概念检索读取完整定义，核原 owner 晋升依据、来源/状态及必要 R/D/T/Architecture 关系。搜索命中、目录、排名、日期和更大版本不建立 authority；current、accepted target、未晋升 contribution、历史与被替代范围分开。改名保 ID，结构变化同步存活引用、前驱/后继与旧引用意义，不恢复共享登记。
- **R711-04 / BEH711-PROMOTION**：原 RDT/Architecture owners、隔离完整 proposed、final integration 实际写入/读回、TaskCommit、actual committed after 绑定及独立完整 Review；Planning 独立 Architecture 保留。贡献是候选或历史来源，不能冒充共享 current；普通当前读取不拼贡献链。
- **R711-05 / BEH711-OVERLAP**：同能力/正文/关系的任务比较适用 base、双方完整 proposal、真实 target 和受影响消费者，原 owner 保留全部仍有效条件并审组合定义。Git 自动合并只证明文本结果，不证明语义；不得未判断有效范围即取一侧。
- **R711-06 / BEH711-OWNERS**：共同方法同时覆盖 RDT 与实际命中的 Architecture 导航；只改相应读写合同/消费者，不扩大为业务代码冲突框架。AI 判断适用、替代与整合充分性，脚本只执行事实。
- **R711-07 / BEH711-CUTOVER**：安装规则与项目切换分开。原 owner 固定旧完整来源、旧入口/实际读写者、稳定 aliases、必要关系、未迁移范围及恢复条件；原质量链满足后才切换。未达条件保可读原 authority 和 proposed，不宣称消除共享登记。已切换新任务不双写旧索引；在途 Task 保阶段版本，最终集成触及已迁移单元则重读真实目标写当前单元。历史和原始证据保持，切换前失败保旧入口，切换后走原 repair/受审 successor。
- **R711-08 / BEH711-ADOPTION**：canonical 共同合同、原 Skills、managed spec、必要消费者及 matching dogfood/installed/声明平台投影成套采用，保用户内容、Task/session及原 sidecar/mode/drift规则。源码一致、实际 Agent 行为、项目文档切换和业务采用分别证明；公共 I/O/runtime 不变，不新增 registry、生成器或语义脚本。

关系：同能力 [D711/CON711](../../design/current/knowledge-maintenance.md)、[T711/SC711](../../test/current/knowledge-maintenance.md)；适用 Architecture 决策由原 Architecture owner 维护。完整采用与退出步骤见 [MIGRATION-711](../../../trellis/presets/guru-team/MIGRATION-711.md)。
