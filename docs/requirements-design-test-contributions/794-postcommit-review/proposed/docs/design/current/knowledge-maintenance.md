# 当前知识单元与原维护方设计

导航别名：`REQ-007/BEH-007`；`R331`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。这些检索别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/design/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

本次 #649 最终整合的完整前驱：Git `4fea68613de4181d7cb55532b8758515472ba31b:docs/design/current/knowledge-maintenance.md`。贡献、#657 继承及原来源见 [#649 追踪](../../requirements-design-test-contributions/649-stage-result-convergence/traceability.md)。

知识单元：`RDT-DES-KNOWLEDGE`。状态：`current`。authority identity：`guru-trellis-rdt`；精确内容由包含本文的完整 Git revision 与 locator 定位。固定前驱 RDT `.109` / Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`。需求：[RDT-REQ-KNOWLEDGE](../../requirements/current/knowledge-maintenance.md)；测试：[RDT-TST-KNOWLEDGE](../../test/current/knowledge-maintenance.md)。稳定 `REQ-007 / BEH-007` 的design责任沿原RDT/Architecture owners延续。

## 稳定设计身份

`DES-007` 保留RDT/Architecture各自唯一authority与最小spec projection。`DES-026..034` 的双维合同、constitution、责任/check/contribution边界继续由Architecture正文和原package拥有；本单元迁移其日常知识读取/适用性/晋升关系，不改写项目具体架构答案。`DES-027` 的当前晋升顺序由D638/ADR-POSTCOMMIT-INDEPENDENT-REVIEW承接，`DES-033` 的无条件current推进stale片段按ADR-028/R567替代，其余有效条件保持。

## D331-01 / CON331-01：完整单元与薄导航

原RDT维护Skill的 `references/current-knowledge.md` 单写可复用读取/修订合同，由原package distribution安装。两维护Skill按原职责加载同一通用合同；没有新公共Skill、schema、service或parser。项目根为docs/requirements/current、docs/design/current、docs/test/current；按task-delivery-lifecycle、completion-closure、knowledge-maintenance三个capability/responsibility组织完整正文。

每层 current/README 提供限定目录、稳定 ID/alias 查找方法与明确 legacy 边界，不逐项枚举所有单元。单元标明适用版本/状态、完整定义/条件、必要关系、来源和替代范围；目录名current不具有semantic authority。共享根入口使用稳定 authority identity guru-trellis-rdt，仅在入口自身身份、范围、状态、位置、查找合同或必要关系真实变化时由原 promotion owner 修改；普通晋升不强制全局递增或总README写入。未切换前candidate保持proposed；不能以新导航或新CURRENT自证正确。当前正文revision用包含其完整内容的Git snapshot，不另造无限版本副本。历史版本和contributions只读来源，普通当前查询不要求拼接它们。

能力正文展开完整行为、异常/否定/继承条件，细粒度公共API仍由canonical package拥有。读者按问题/阶段选单元并展开必要R/D/T/Architecture关系，不机械递归所有链接。navigation中不重复business summary，来源history也不复制成current本文的第二份规则。

## D331-02 / CON331-02：关联修订与结构身份

原task_impact_sync从批准delta及实际适用authority判断no-op、isolated contribution、窄direct sync或revision。每个Task拥有独立contribution目录，默认manifest/requirements/design/test/traceability五件套，互不竞争shared正文。写作owner在本delta准备完整目标内容，主promotion owner再在live current上合并；脚本不推断conflict或最新有效规则。

稳定REQ/BEH/DES/CON/TST/SCN/CASE身份与展示顺序分离。移动/插入保持原ID；替换/删除留旧→后继与历史；真实拆分/合并才分配新身份，并记录前驱/范围。原trace保留；新关系映射不批量重编号无关对象。维护一层时判断其它层和Architecture的真实影响，无影响据实保留，不为格式完整批量修改。

## D331-03 / CON331-03：两层Architecture来源

原Architecture owner在generic source边界维护版本固定通用栈定义，在project边界维护选择/范围/约束/差异。实际generic源为 `trellis/knowledge/technology-baselines/trellis-extension/versions/1.0/baseline.md`，项目投影为 `docs/architecture/00-foundation/stack-selection.md`。二者在Architecture正文定义适用关系，本RDT只定位，不复制技术条款或独立批准。

项目差异仅修改项目投影；共享变更由源方owner在源范围审查，不隐式升级其它项目或写入Task/branch/客户配置。外部source缺失需说明位置/version/取得方式及受影响结论；去敏fixture证明合同而非外部真实采用。FOUNDATION/CURRENT/TARGET/GAP/PLAN/ADR/EVIDENCE分区、constitution和single-writer不变。

## D331-04 / CON331-04：晋升和阶段适用性

原 RDT/Architecture semantic owners 及四 profiles 保持。RDT impact/promotion3.0、Architecture 非 Planning6.0/Delivery4.0 与直接 consumers 成套采用。Planning3.0/Delivery1.0、bootstrap/repair 保原合同；真实 API 版本独立于知识身份。精确 source 使用完整 Git revision/locator，局部一致性 token 不成为 semantic authority。

`D638-02 / CON638-CANDIDATE`：实施完成全部代码、完整隔离 targets 及真实工程结果，RDT impact 的 candidate_ready 交原维护方，不进入独立 candidate Check。Planning 独立 candidate/final Architecture 保留。只有实质边界扩张才刷新 implementation discovery；它不成为普通整合的重复前置。

`D638-03 / CON638-INTEGRATION`：原两维护 owners 在 final_integration 一次固定真实 target branch/commit，读 applicable before、完整 proposal、实际 current 和必要关系/导航，保留双方有效条件。普通 mismatch/partial/output-loss 留原 writer；completed读回、pending只补未冲突内容、conflict或intent不唯一停止。RDT 原写作仍核完整三层 trace 和 Architecture inheritance，不由 wrapper 写正文。Architecture 以 before_authority/candidate、promotion_targets、post_candidate 和实际 readback 绑定结果，只返回 integrated_pending_review；项目 checks 的独立实现判断留提交后 Review，不伪造 precommit review。

整合实际 after 进入 TaskCommit 精确本地提交。implementation 用原公开 constructor 固定 B、H 和全部 paths，再 begin_check；原 guru-review-branch 同时拥有 check/full_review。该新的独立 reviewer 先读原 authority，再审完整 committed before/after、消费者，完成一次 implementation Architecture 和九维/完整区间审查。通过后顺序 record check（Planning predecessor）与 full_review（该 check predecessor），只在两投影都完成才返回 passed。Architecture reviewed_promoted 来自真实整合和此同次独立 before/after；readiness 不消费 pending。固定候选不在审查时被修改；原 writers 修复后继提交，合法原覆盖和工程事实按 ADR-034 采用，缺口或无法界定影响补足完整判断。

输出丢失核同 key/B/H/候选和真实 public results，仅补尚缺投影或恢复同一结果；丢失必要语义不补造pass。没有另一 Check checkpoint、第二 current 或审计账本。工程事实仍按 R578/唯一候选适用合同判定义、输入、依赖、环境、工具链、参数和期望；未知/失效才补命中项。

`D638-01 / CON638-IDENTITY`：完整单元与关系保持稳定ID，authority identity= guru-trellis-rdt；普通晋升允许同 identity，只校真实目标内容。根导航只在入口自身合同真实改变时写入，独立主题不登记共享列表，不追加每Issue业务摘要。Architecture使用独立稳定 identity guru-trellis-architecture。bootstrap仍要求其真正distinct successor，历史和真实接口版本不改义。

## D331-05 / CON331-05：迁移、恢复与分发

迁移清单逐项定位B的实际predecessor条款、完整目标、继承/替代及尚未迁移范围。未review/切换前保留旧README，候选标proposed。legacy普通读取的consumer是固定旧authority的在途planning/gates，owner不再向旧current双写新能力；Task结束/合法改选/真实依赖变化后退出其旧普通读取，历史仍可追溯。普通源缺失、断链/冲突/未迁完回原repair/Clarify，不能靠推断填confirmed。晋升后correction沿原repair/新successor，不改历史快照。

canonical packages/workflow/spec/preset拥有长期内容，dogfood/installed经完整apply更新；matching update/reapply保留用户修改并逐项处置sidecar/mode/drift。命中公共I/O按MIGRATION-638显式版本化并成套直接迁移，不加长期双reader或额外installer机制。当前代表性clean与旧匹配更新不等于完整Release matrix、外部业务配置重建或业务采用。

## D331-06 / CON331-06：真实对照与结果归属

实施前冻结V331-A..D的问题、必答事实、必要条件、关联修订范围、模型/权限、3次old/new和成本判据。用真实B旧语料与actual新正文；写作实验使用同语义临时副本，双方面对相同正常起点。host期待表不注入受测Agent，另一侧答案/轨迹不预载。

脚本仅收集原生session events/命令/实际输出字节/usage/改动paths，不做semantic评分；AI逐次判完整性和成本类别。总input包含共同注入，cached单列不扣减造收益；必要正文、导航、重复和无关历史分开。读取/定位改善与维护改动均报告，失败保留首次结果及修复，同口径变更须双方重跑。兼容子项不强求节省，错误不以低成本抵消。无需新telemetry平台或长期raw traces。

唯一实际#331结果由 [contribution test.md](../../requirements-design-test-contributions/331-current-effective-knowledge/test.md) 拥有；三层当前Test单元只拥有策略/场景/预期与结果定位。migration核对/定向tests、一个代表性clean+matching update/reapply/drift证明各自层次，真实Agent证据不能由schema/目录通过代替。

## D648：约束、关键前提与原 owner 承接

需求R648-01..07的完整定义由Requirements同单元拥有；本节定义本仓原模块的职责落点。公共I/O、profile、typed exit、schema、runtime状态、阶段、single-writer和授权边界不变。没有新的Architecture决策，因此no-impact不建立空贡献或ADR。

**D648-01 / CON648-SOURCE**：原Author planning-body/authoring和Delivery design模板承接R648-01。实际设计说明约束如何限定机制、分支、拒绝与依赖；唯一来源处置引用原承诺和具体落点。原Author收尾Gate按既有选择合同，对照live selected scope_ref anchors与design/Delivery Policy的本批承诺。完整来源的条件和例外按其适用性保留，不因读取而自动成为本批交付承诺；正文承诺写宽时按实际选择纠正，真实范围变更仍回原owner。事实或假设不足留原缺口，不能由脚本补成已确认设计。

**D648-02 / CON648-PREMISE**：原Architecture contract与独立读取路径承接R648-02。规范约束、原证据、接受设计和假设分开，before_authority仍是候选比较来源。原native staging提供真实authority、完整候选、原始事实与未改consumer；不能通过隔离隐藏必要约束，也不能把答案或旧pass注入。

**D648-03 / CON648-REENTRY**：原实施协调承担受影响操作停点与原owner路由。scope不变的方案修订使用原当前阶段合法rework和同Delivery Planning continuation；不新建身份或改accepted_scope。真正authority/scope问题回原Clarify，规划有效的实现/断言修复留原implementation/Check。新候选依原资格/机制入口处理；恢复必须与受影响最新规划、判断和实际候选匹配，无冲突工作仅按真实依赖继续。global workflow只定位触发与重入，step-local方法归原Skill。

**D648-04 / CON648-EXPECTATION**：原独立 Review 从有效合同确定预期，再核代码/测试和真实消费者，在同次完整判断覆盖九维、精确 committed B..H 和受影响未改 consumer。测试私有固定值不能替代源约束；绿测试与一致设计不豁免职责缺陷。

**D648-05 / CON648-APPLICABILITY**：原task-free pre-write/evolution gate判断gate保护语义及依赖必要性。样本以同域catalog的展示重命名A和生效目标选择B表达operation差异，具体业务名不进入公共方法。原实现/测试共同过度限制A时，owner在剩余受影响target write前停止，并沿原机制/evolution/scope consumer处理。A/B实际调用与state前后由测试记录，AI说明不适用理由、必要阻断和evidence职责。

**D648-06 / CON648-COVERAGE**：单一Candidate Applicability And Coverage定义继续拥有复用规则。原owner读取新原证据后判定哪些前提失效、哪些覆盖仍有效；代码/测试未变不豁免，整体版本或身份变化不自动重跑。同一合规独立reviewer可接续，当前阶段结果仍实际发生。

**D648-07 / CON648-VALIDATION**：原Architecture/Check semantic_authoring与原native Adapter扩展本项写作、实施、Review和task-free事实。测试私有运输只执行真实Agent请求、落其原字节、记录原wrapperstdout及状态变化；它不选语义结论或改public DTO。声明多owner连续性时，用同一stateful fixture消费实际前序stdout。预置合法前置只证明起点，不冒充本轮前序判断。RDT完整隔离proposed由原final_integration整合读回后进入TaskCommit，再绑定完整committed candidate进行独立Review。

## D649：当前成果收敛与结果引用

**D649-06 / CON649-KNOWLEDGE** 承接 R649-07。原 RDT contract／current-knowledge 和 Architecture contract 在其既有职责中读取真实解除条件，更新当前定义、指南、派生说明，保留历史阶段观察。当前 R/D/T 单元展开行为，公共 Skill 内部步骤仍由各原 package 单写；spec 只作最小定位。

隔离贡献提供九个完整 proposed targets，保留原身份及所有有效前驱条件。当前 final_integration 在 TaskCommit 前写 shared current 并读回；其后同 B 的完整 committed after 进入一次独立 Review。#649 原专项时机及观察保留历史意义。

#637 Test 的有限修正只使用原 archive 正式结果、PR #644 和已证 main ancestry；保留原命令、失败、未知、legacy reapply 阻塞及其它未证边界。#649 唯一实际结果记录各运行的真实层次、cutoff 和失败，不从相同 exit 或最后一次重跑推导成功。

## D-MECH：采用机制与原 owner 承接

**D-MECH-01 / CON-MECH-ADOPTION** 承接 R-MECH-01/03/04。原 Architecture contract 单写采用机制审核方法，按实际行为、状态、依赖和直接消费者确定对象，含无 diff 的复用。先从支持调用方取得承诺结果的完整路径推导直接可行方案，再判断额外协调的必要性、职责与作用范围、整体代价、替代和证据；完整宪法不排名。默认不准入与主动尝试删除、收窄或替代的方法只由原 Architecture contract 单写，独立审核自行判断可行性；原方案已最小时说明依据，不虚构替代。Author 在原候选与方案比较中消费，Approval 在原设计充分性等维度核落点，Check/Branch Review 审完整实际候选及受影响未改消费者，不复制另一套问卷。受审旧技术选择可被质疑，真实约束及原 change contract 继续有效。

**D-MECH-02 / CON-MECH-PROTECTION** 承接 R-MECH-02。原 root-cause contract 的 Protection 分支拥有提出方举证；作者、reviewer、模板提出保护都须说明真实缺口、补齐、收益和整体代价。Protection 资格只承担原准入职责，不替代 Architecture 对简单替代、最小范围和正常最终完成成本的判断；Root Cause 与 Author 在原消费点引用唯一方法，不复制新清单。原正常场景、solution/root qualification 及 finding 出口不变；脚本不从缺签名/锁/重试或安全词汇生成结论。新保护缺证不先成为义务，旧保护缺证只限制依赖结论，不自动删除或视为通过。

**D-MECH-03 / CON-MECH-KNOWLEDGE** 承接 R-MECH-03..05。原 current-knowledge 单写文档优先取证、完整决策单元和存量处置关系。RDT 足够时不追全部源码；行为、性能、消费者完整性或冲突有缺口才定向查。必要性已证、缺陷已证与缺证分别承接：已证问题由原 owner 有界纠正并适配必要消费者，缺证保留有界调查且不扩大采用；不将机制用途或 CURRENT 自证视为充分依据。纠正决策区分必须同步适配、可独立分期和场景保留，在原单元/change contract 承接真实 owner、共存依据、剩余消费者、可执行交付/触发及退出证据，不建永久迁移台账。

项目方法投影由原 Architecture contribution/final_integration 写 change-contract。六个 RDT 完整拟写由原 RDT owner 保留有效前驱，由原 final_integration 写入读回，经 TaskCommit 以同 B 绑定完整 committed after，再由同次独立 Review 覆盖 Architecture 及完整质量职责。公共 I/O、schema、runtime、状态、原则、single-writer 和阶段保持；canonical 经原 preset 完整分发，既有业务安装采用另行证明。

## D693：原方法与原消费者

**D693-01 / CON693-METHOD** 承接 R693-01/02。唯一合同连续性方法位于 [Candidate Applicability And Coverage](../../../trellis/presets/guru-team/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage)，唯一测试边界方法位于 [Test And Validation Value](../../../trellis/presets/guru-team/spec/workflow/quality-guidelines.md#test-and-validation-value)。原 Author 在候选/方案中具体承接，Architecture 判断实际消费者和复用对象前提，Check/Branch Review 各自独立核当前结果与证据范围。step-local references 只加载并消费，不复制方法；无新阶段、public I/O、schema 或脚本语义判定。

**D693-02 / CON693-HISTORY** 承接 R693-03。原当前调查 owner 以固定源码、当时安装规则、公开规划/阶段/交付及原命令形成有来源说明；原阶段对象、已知条件、执行/采用和记录缺口分别表达。不能恢复的 reviewer 理由不由后来规则或代码缺陷补齐。具体静态观察和未知项只由配对 Test contribution 拥有，不建立长期审核台账。

**D693-03 / CON693-ADOPTION** 承接 R693-04。Delivery 原 owner 在真实 payload 中限制 consumer/entry/安装范围，读取原 Policy 保留后端正式采用的整体责任。项目 Architecture change-contract 消费同一方法，RDT 与 Architecture 各自准备完整隔离拟写，原 final_integration/readback 后 TaskCommit，再由 implementation 绑定全部 actual committed after，独立完整质量链覆盖。完整 preset 分发受管副本；目标项目按原正式 Upgrade owner 采用，不复制业务领域定义。

三层稳定关系及本批来源见 [#693 traceability](../../requirements-design-test-contributions/693-contract-evidence-adoption/traceability.md)；原 D648/D-MECH 与前驱晋升/兼容条件保持。

## D710：语义 authoring、完整结果与原消费者

R710/BEH710 的正常 authoring、客观身份派生、完整结果合法消费和恢复由当前 [Review contract](../../../trellis/skills/guru-team/packages/guru-review-branch/references/contract.md) 承接。MIGRATION-794 明确旧 Check profiles 及 provider 边界，MIGRATION-710 和原结果保历史含义。这里不重复字段、算法或具体 argv。

**D710-01 / CON710-AUTHORING**：原 Review AI 实际完成一次当前完整语义判断，只写原 recorder 的最小语义输入；recorder 派生客观身份。最小示例是正常入口，完整结果示例只供消费说明，不形成双 authoring 或新 wrapper。

**D710-02 / CON710-CONSUMPTION**：record/check/invoke 独占各自输入和输出。原 receipt 定位本次完整结果，checker 验证该结果，invoke 消费真实完整文件；receipt/绿色状态不替代 owner result。公共候选/局部 token 按原 consumer 分离。真实 check 与 full_review 分别绑定一次实际判断的充分性和完整覆盖，由原 public API 顺序记录；成功只交原 Delivery Review，绝不回 TaskCommit 或提前 Publication。

**D710-03 / CON710-RETIREMENT**：record完整输入退休与完整结果消费/恢复分开；MIGRATION-794 定位旧受支持操作的固定完整provider及同操作恢复。新链直接选择新 Review 合同，不从旧Check结果换owner/version造pass；既有真实已完成结果只按其原语义读取。无长期双parser或第二状态。

**D710-04 / CON710-STALE**：保客观错误code/field、capture ancestry、路径覆盖、业务bytes/modes和metadata排除。实际内容改变使旧结果失效；缺步或输出丢失只核同对象、仍适用语义及真实 public facts 后恢复原结果。丢失语义覆盖重新实际审查，不重绑旧摘要延续结论。

**D710-05 / CON710-BOUNDARY**：正常语义输入命令链与完整结果consumer单元各测真实入口。eval只运输Agent原字节，fixture不代当前owner生成结论。成功、finding、planning rollback、blocked/resolved及缺步恢复按当前实际profile验证，命令层不宣称native效果。

**D710-06 / CON710-FIRST-NATIVE**：新的独立 Review 从完整 committed candidate 入口实际读取 authority、候选及 consumers，先 Architecture 后九维/完整Review，原wrapper由该Agent调用。host不代填语义/摘要/答案，首次失败、修订与未验证如实保留。#710原候选/最终专项轨迹和次数是历史证据，不成为新链重复阶段。

**D710-07 / CON710-ADOPTION**：原tools/preset owner成套同步matchingsource、Task/session和受管平台，按差额验证source/installed/reapply/drift/mode/sidecar；定向安装、命令和实际Agent/业务采用分开。当前完整知识仍由原writer在final_integration真实读写，不生成共享导航登记。

## D711：目录发现、局部导航与原 owner 切换

承接 R711-01..08；来源与逐项关系见 [#711 追踪](../../requirements-design-test-contributions/711-knowledge-navigation-isolation/traceability.md)。原 D331/D638 的完整正文与候选/最终边界保持。

**D711-01 / CON711-DISCOVERY**：canonical 原 RDT `references/current-knowledge.md` 单写稳定发现和隔离导航。RDT 根/current 入口保体系信息及 `current/**` 范围；Architecture 根沿 FOUNDATION/CURRENT/TARGET/DOMAIN/INTEGRATION/GOV/GAP/PLAN/ADR/EVIDENCE 职责目录查找。原 Skills/contract 与 managed RDT spec 消费同一方法。读取端用 `rg --files` 和稳定 ID/概念限定搜索，再读完整单元并核来源/晋升与状态；原 Author、实施、Check、Review 的阶段责任保持。

**D711-02 / CON711-WRITE**：独立单元只写原能力正文、自身目录局部导航及真实受影响关系。root/current README 不枚举单元，不向共享 manifest、system/ownership/ADR index 或生成索引转移登记。根自身合同变化才进入 reviewed targets。原完整单元保稳定 ID/aliases、semantic owner、适用来源/晋升依据、定义、关系与替代范围，精确接口仍由原 canonical package 单写。

**D711-03 / CON711-OVERLAP**：原维护 owner 在 final integration 比较 applicable base、双方完整 proposal 和一次固定真实 target，核组合及受影响未改消费者。Git 自动合并不供语义 pass；保留双方仍有效条件。同一关系不复制或拆散，真实范围/机制/验证变化回原 owner。原 actual write/readback、after 重绑和最终完整质量链继续。

**D711-04 / CON711-MIGRATION**：MIGRATION-711 拥有可执行采用步骤；knowledge-navigation-1 只标文档组织边界。原 owners 先在隔离 proposed 准备完整目标，逐项核旧 alias 并只补原单元缺口，保原路径和历史。未达条件仍读旧 authority；满足后原 final integration 切换，后续不双写旧共享索引。在途旧读取保其阶段版本，触及已迁移目标的最终写入整合当前单元。改名/替换/删除保 ID、存活引用及旧意义；失败沿原 repair/successor，不改不可变来源。

**D711-05 / CON711-DISTRIBUTION**：原 tools owner 从完整 matching source 同步受管 dogfood/installed/声明平台，普通 apply 保其原前置与 sidecar，安装器不迁移业务文档。公共 README 只引用迁移 locator；runtime/profile/API/schema 与 workflow bytes 不变，无新索引服务/生成器/registry/语义脚本。实际 native、两序合并、安装和采用分层记录，不扩完整多平台 Release 矩阵。
