# 当前适用知识的读取、修订与晋升

本次 #649 最终整合的完整前驱：Git `4fea68613de4181d7cb55532b8758515472ba31b:docs/requirements/current/knowledge-maintenance.md`。贡献、#657 继承及原来源见 [#649 追踪](../../requirements-design-test-contributions/649-stage-result-convergence/traceability.md)。

知识单元：`RDT-REQ-KNOWLEDGE`。状态：`current`。authority identity：`guru-trellis-rdt`；精确内容由包含本文的完整 Git revision 与 locator 定位。前驱 RDT `.109`、Architecture `.100`；固定迁移源 Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`。候选正文须经原 owners 晋升才进入共享 authority，不因目录名 current 自动生效。

## 唯一 authority 与完整知识

`REQ-007/019/027..035`、`BEH-007` 保留身份，并按下述阶段适用性及 ADR-KNOWLEDGE-FINAL-INTEGRATION 承接当前时序。RDT 由唯一 `guru-maintain-requirements-design-test-ssot` 管理一个 Requirements/Design/Test repository authority。每个活动 requirement/behavior 均有 owning design responsibility/contract 和至少一个 test strategy/scenario/case，双向关系保持。Architecture 独占项目 FOUNDATION/CURRENT/TARGET/GAP/PLAN/ADR/EVIDENCE、constitution/决策/owner/兼容/历史；RDT 只继承其公开 locator/version/status，不读 private state，不复制架构正文。task-local PRD/design/implement 是 Task planning，不能冒充 repository authority。

`R331-01 / BEH331-01`：读者先按问题、Task、阶段和候选选择真正适用来源，再按能力/行为/接口/职责或稳定 ID 到完整单元。当前有效要求、已接受目标、未确认、历史和 superseded 内容分开；target 不冒充当前实现。读取必要关联（条件、否定、例外、顺序、依赖、设计、测试、Architecture），不无限展开所有链接。导航仅存 identity/alias/status/locator/关系，不是另一份业务摘要。搜索排名、日期和编号不决定 authority，命中标题或摘要不替代正文。解释旧决定或原因时按需读历史；普通当前查询不要求重放全部版本/贡献。

当前单元是原 owner 在已声明能力范围内合并的完整定义，历史 contribution 保留来源责任；晋升后后续查询不能仍靠贡献链补出遗漏规则。精确 public API/schema 仍由 canonical package 单写，单元展开能力行为并指向必要完整接口，不复制接口成第二来源。单元 revision 由完整 Git snapshot 与 locator 定位。根 authority identity 稳定，普通 Task 不强制递增全局版本或写根 README；只有定位关系、身份或状态真实变化才改导航。真实 public API/schema 版本继续独立维护。

## 一致修订、身份与隔离

`R331-02 / BEH331-02`：原 maintenance owner 先读变更和受影响完整单元，判断 R/D/T/Architecture 关联、新增/修改/替换/删除/拆分/合并，再由对应 owner 写本 Task 隔离贡献。正常并行 Task 使用不同 `docs/requirements-design-test-contributions/<TaskId>/` 和 Architecture contribution locator，不互写对方，不竞争 shared current。必要时可由原 owner 判断窄 direct sync，但不能由 caller 自封同步。

展示顺序、移动或插入不改变既有身份。替换/删除保留旧 identity 的变更关系、历史和 successor；拆分/合并给真正新对象新 identity，保留前驱及各继承/替代范围。无关 ID 不批量重编号。只更新真实相关对象；无影响层说明依据，不为形式一致改全部文档。来源冲突由 AI 判断，不能脚本按最新 wins。完整 trace 是 requirement/behavior → design responsibility/contract → test strategy/scenario/case；关系表存 identity/locator，不重复来源 prose。

## 四 profiles、日常闭环与晋升

RDT 保持四 profiles：bootstrap_foundation 建立/复用/迁移兼容三层 authority；task_impact_sync2.0 对批准 delta 判断 no-op、完整 isolated candidate 或 revision；promotion2.0 在 final_integration 审查 contribution、subtraction、trace、历史和 Architecture inheritance并实际写入；repair 修复具体 authority/navigation/迁移缺陷，不扩需求或改无关历史。bootstrap/repair 原合同不变。

Planning、实施、候选 Check、最终 Check、Branch Review、Delivery Review、Completion、Finish 都读取阶段适用的完整正文与必要关系。Planning 选择唯一 ssot_first、delta_first、bootstrap_or_repair_docs 或 no_docs_update_needed。Phase2 先执行策略并形成完整隔离候选；有变化时 candidate_ready 仅表示贡献和完整拟写可供候选检查，不表示共享 authority 已更新。无变化返回真实 no-change，不创建空 contribution、ADR或提交。

`R331-04 / BEH331-04`、`R600-01..06` 与 `R638-01..07`：原 implementation 在 implementing 以固定 B、实际 HEAD 及完整差额构造 candidate/begin_check，进入 checking。独立 Architecture phase2 和原 Check delivery_candidate_check 读取晋升前适用 authority、完整 tracked/untracked implementation、完整 proposed targets 与受影响未改 consumers。候选通过时原 Check 用既有 rework(target_role=implementation, affected_results=[readiness]) 返回 implementing，再输出 candidate_checked；它不写最终公共 Check。Planning 和真实历史结果保留，历史不自动获得当前适用性。

candidate_checked 的唯一 consumer 调原两 maintenance owners 最终整合。原 owners 一次固定真实目标 branch/commit，逐一读取命中单元。不同单元推进不改本方未命中内容；相同单元须保留真实 current、本方来源和双方仍有效条件，生成唯一完整组合正文，必要时按原候选适用性合同补审全部差额及受影响未改 consumers。不得只靠 Git 自动合入、目录或版本数字宣称语义兼容。推翻需求前提回 scope/Planning；改变实现、接口或验证义务回相应原质量 owner。

原 owners 亲自写已审内容并读回所有 targets，判断实际适用性。随后 implementation 以同 B、实际 HEAD 和全部晋升/关系/导航 paths 重建 candidate/begin_check。原 Architecture 对实际候选作匹配 phase2 判断；最终 Check 只能消费新 content_ref，记录真实公共 passed，之后精确 TaskCommit、独立 committed Architecture/完整 Branch Review 覆盖实际内容。无知识写入也走合法候选回程，不制造空文件或空提交。Ready/Publication/Completion/Finish 只接受真实 no_change 或 reviewed_promoted，候选出口不能代替最终 gate。

expected-current mismatch 只影响本次实际写入，由原 owner 重读真实差额，不自动判全部在途 Task 过期。partial/output-loss 由原 owner读取同一明确 intent，完成已写 targets 的 readback并仅补 pending；真实冲突或不唯一时停止，不新建状态机、全仓 hash账本或第二 current。无关目标前进不要求 merge/rebase 或追赶 SHA。

## 阶段适用版本与实际变化

`BEH567-02/03` 保持，窄替代旧 `REQ-034` 的“一切 current 前进强制 sync”。原 owner 选择 Task plan/候选/阶段适用 RDT 和 Architecture，可以用 immutable version 或 Git history。无关共享 CURRENT、navigation、archive、remote ref 或 tool 前进不替代它，不强制贡献重写、业务门禁重跑或 branch 同步。明确适用于该 Task 的规则、失效假设、scope/dependency/solution 改变，仍回原 revision/assessment。promotion 自己仍读 live current 并校验本次写边界，两种时钟不能混淆。

`R578-01..04 / BEH578-01..04`：当前 semantic judgment 和工程命令事实分开。每次 owner 都新作当前完整判断并绑定当前 invocation；合法、可核查且实际 check定义、依赖、参数、预期、工具链和环境仍适用的工程事实可跨 owner/stage 使用。unknown/missing/真实变化才重跑受影响命令。不能借旧 semantic pass、同路径或相同 code tree 免当前判断，不读退休 private checkpoint 或造 cache/ledger。采用结果说明原来源和适用依据，不声称自己执行。

## Architecture 维护的既有判断边界

原 Architecture owner 在 Planning、合格的 implementation discovery、Phase2、独立 committed Branch Review、publication 和 acceptance_finish 判定阶段适用性。项目正文唯一声明 constitution locator/version；Guru 只消费其五个 identity/short names，不复制原则正文、逐项评分或 verdict。无 Architecture 影响保持 no-impact/no_change 快速结果，不制造 contribution、ADR 或 project-check负担；有影响必须恰好选择 target_native、legacy_boundary_convergence、dedicated_refactor_slice 之一。

项目 change contract 必须承接真实 requirement/behavior、baseline/constitution、domain/integration/decisions/GAP、required concerns、current/target owners、single-writer、compatibility exit、parallel scope、偏离/删除条件、design responsibility、before/after、checks/evidence和promotion写边界。普通Task只写本方contribution；改变decision、原则例外/权衡、GAP lifecycle、owner/single-writer或compatibility exit才需要ADR candidate。Phase2读取完整candidate，Branch Review对完整已提交范围独立重算，不能拿前次pass替代。

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

本规则保留 R331／R578／R637／R638／R648 的完整来源、工程事实适用性、隔离贡献、candidate Check、原 final_integration 实际写入与读回、实际 after 重绑、最终 Check 和完整 committed Review。无变化不造空贡献或 ADR，稳定 identity 与原单写责任保持。

## 采用机制审核与决策纠正

**R-MECH-01 / BEH-MECH-ADOPTION**：原 Architecture owner 审核本次新增、修改、复用、扩大使用及直接影响的机制。将数据 authority、职责、协调、失败或生命周期约束带入当前路径的采用，即使共享实现无 diff，也须判断适用性；普通 helper 和无关依赖不逐个建单元。找到设计依据后，仍按完整设计宪法独立判断必要性、范围、整体代价和可行替代，不给予某一原则固定优先级，不以最短代码或更少 finding 证明质量。

**R-MECH-02 / BEH-MECH-PROTECTION**：新增或强化保护的提出方，包括作者、reviewer 和模板要求，说明真实要求或可信事实、现有保障缺口、补齐关系、收益、运行维护代价及合法请求影响。缺少签名、锁或重试本身不成立 finding。真实保密、权限和职责约束不以事故发生为前置。对安全、防御及失败保护的偏好须纠偏，不能以此取消有依据的保护，也不能声称已证明模型训练成因。

**R-MECH-03 / BEH-MECH-EVIDENCE**：适用 RDT/Architecture 已能回答能力、职责、条件和取舍时，不重复源码考古；实际行为、性能、全部相关消费者或文档冲突存在缺口时才定向查实现。正在审查的旧技术选择不能以自身排除替代；真实业务和外部合同保留，修订沿原受审变更合同实施，再按原阶段晋升。既有能力、平台原生能力和已安装依赖均须有当前适用依据；无直接 consumer 的抽象、包装、转换、配置和未来预留不进入实现。

**R-MECH-04 / BEH-MECH-UNCERTAINTY**：新保护缺证时补证、修订或撤回，不先升级为义务。旧保护缺证时不擅删，也不默认复用通过；只限制依赖该结论的采用或晋升，无关工作继续。已有论证确实覆盖当前消费者、条件和代价时简短承接，真实前提或证据变化才补审，不因阶段或版本改变重做全部工程检查。

**R-MECH-05 / BEH-MECH-LEGACY**：纠正旧决策须识别同一决策的实际采用者、共享状态、数据、接口、配置和运行依赖。共存破坏同一约束、不兼容读写或使纠正失效时，承接必要适配与退出。可独立保留时，说明共存如何保持约束、剩余采用者、真实保留依据、owner、可执行后继交付或可观察触发条件及退出证据；未承接须如实标明，工期、改动量、链接或“下次再改”不代表安排。旧场景仍有依据时明确范围后保留，新消费者不扩入已判错模式。分析可大于实现范围，不自动授权跨仓迁移。

晋升完整单元保留决策行为、owner、范围、理由、代价、适用条件、重审触发及存量关系；使用既有正文/change contract，不新增评分、永久台账、审批链或公共字段。方法唯一正文在原 [Architecture contract](../../../trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md)、[Protection](../../../trellis/skills/guru-team/packages/guru-qualify-root-cause/references/contract.md) 与 [current knowledge](../../../trellis/skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md)。设计和测试分别由同名完整单元的 D-MECH 与 T-MECH 承接。

## R693：合同连续性与证据适用性

**R693-01 / BEH693-CONTINUITY**：执行链替换或入口扩大时，原 Author/Architecture 从实际入口追踪新生产者输出、持久完成状态及成功含义，核对仍在使用结果的消费者，包括无 diff 的读取器。复用调用须核参数实际对象、存在阶段、持久前提和顺序。Check/Branch Review 独立判断当前消费者可用性；类型、名称、生产者成功和旧 pass 不代替这些条件。差额回最早受影响原 owner。

**R693-02 / BEH693-EVIDENCE**：原 owners 对照测试声明边界与正式路径的入口/context/配置/依赖/状态/分支/观察点。边界前 fixture 和外部依赖替身可成立；边界内代产出、修正输出或绕过关键条件不能支持该边界的成功声明。入口、默认路径或启用范围变化后，分别判断旧事实保留、失效及补证范围。保留可核验且仍适用的局部证据，不将全部变化升级为全链 E2E。

**R693-03 / BEH693-HISTORY**：历史调查以当时实际规则、精确候选、条件、命令及可核验阶段结果为依据。分别表达合同失配、底层引入、影响扩大和证据适用范围；具体历史理由缺失时保持未知。源码缺陷、绿测试、空槽位或无 GitHub review 不证明某个 reviewer 未检查或如何采纳旧事实。不重建别的 owner 的 private state。

**R693-04 / BEH693-ADOPTION**：只在原方法和职责内补齐真实差额；方法由共享 workflow-contract/quality-guidelines 单写，项目指导由原 authority 承接，领域正文仍引用所属业务设计。公共源码、dogfood 和目标正式采用分别报告；后者仍由 accepted scope 的原 Task/Upgrade owners 承担。保留用户定制及在途 Task/会话，按原安装合同处理冲突/sidecar。安装成功不证明业务修复或环境效果。

对应设计为同名 Design 单元的 D693/CON693，验证为同名 Test 单元的 T693；原 R648/R-MECH 及全部前驱条件保持。
