# 当前知识单元与原维护方设计

本次 #649 最终整合的完整前驱：Git `4fea68613de4181d7cb55532b8758515472ba31b:docs/design/current/knowledge-maintenance.md`。贡献、#657 继承及原来源见 [#649 追踪](../../requirements-design-test-contributions/649-stage-result-convergence/traceability.md)。

知识单元：`RDT-DES-KNOWLEDGE`。状态：`current`。authority identity：`guru-trellis-rdt`；精确内容由包含本文的完整 Git revision 与 locator 定位。固定前驱 RDT `.109` / Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`。需求：[RDT-REQ-KNOWLEDGE](../../requirements/current/knowledge-maintenance.md)；测试：[RDT-TST-KNOWLEDGE](../../test/current/knowledge-maintenance.md)。稳定 `REQ-007 / BEH-007` 的design责任沿原RDT/Architecture owners延续。

## 稳定设计身份

`DES-007` 保留RDT/Architecture各自唯一authority与最小spec projection。`DES-026..034` 的双维合同、constitution、责任/check/contribution边界继续由Architecture正文和原package拥有；本单元迁移其日常知识读取/适用性/晋升关系，不改写项目具体架构答案。`DES-027` 的当前晋升顺序由D638/ADR-KNOWLEDGE-FINAL-INTEGRATION承接，`DES-033` 的无条件current推进stale片段按ADR-028/R567替代，其余有效条件保持。

## D331-01 / CON331-01：完整单元与薄导航

原RDT维护Skill的 `references/current-knowledge.md` 单写可复用读取/修订合同，由原package distribution安装。两维护Skill按原职责加载同一通用合同；没有新公共Skill、schema、service或parser。项目根为docs/requirements/current、docs/design/current、docs/test/current；按task-delivery-lifecycle、completion-closure、knowledge-maintenance三个capability/responsibility组织完整正文。

每层current/README仅列identity、alias、status、locator和必要关系，另定位明确legacy范围。单元标明适用版本/状态、完整定义/条件、必要关系、来源和替代范围；目录名current不具有semantic authority。共享根入口使用稳定 authority identity guru-trellis-rdt，仅在关系、身份或状态真实变化时由原promotion owner修改；普通晋升不强制全局递增或总README写入。未切换前candidate保持proposed；不能以新导航或新CURRENT自证正确。当前正文revision用包含其完整内容的Git snapshot，不另造无限版本副本。历史版本和contributions只读来源，普通当前查询不要求拼接它们。

能力正文展开完整行为、异常/否定/继承条件，细粒度公共API仍由canonical package拥有。读者按问题/阶段选单元并展开必要R/D/T/Architecture关系，不机械递归所有链接。navigation中不重复business summary，来源history也不复制成current本文的第二份规则。

## D331-02 / CON331-02：关联修订与结构身份

原task_impact_sync从批准delta及实际适用authority判断no-op、isolated contribution、窄direct sync或revision。每个Task拥有独立contribution目录，默认manifest/requirements/design/test/traceability五件套，互不竞争shared正文。写作owner在本delta准备完整目标内容，主promotion owner再在live current上合并；脚本不推断conflict或最新有效规则。

稳定REQ/BEH/DES/CON/TST/SCN/CASE身份与展示顺序分离。移动/插入保持原ID；替换/删除留旧→后继与历史；真实拆分/合并才分配新身份，并记录前驱/范围。原trace保留；新关系映射不批量重编号无关对象。维护一层时判断其它层和Architecture的真实影响，无影响据实保留，不为格式完整批量修改。

## D331-03 / CON331-03：两层Architecture来源

原Architecture owner在generic source边界维护版本固定通用栈定义，在project边界维护选择/范围/约束/差异。实际generic源为 `trellis/knowledge/technology-baselines/trellis-extension/versions/1.0/baseline.md`，项目投影为 `docs/architecture/00-foundation/stack-selection.md`。二者在Architecture正文定义适用关系，本RDT只定位，不复制技术条款或独立批准。

项目差异仅修改项目投影；共享变更由源方owner在源范围审查，不隐式升级其它项目或写入Task/branch/客户配置。外部source缺失需说明位置/version/取得方式及受影响结论；去敏fixture证明合同而非外部真实采用。FOUNDATION/CURRENT/TARGET/GAP/PLAN/ADR/EVIDENCE分区、constitution和single-writer不变。

## D331-04 / CON331-04：晋升和阶段适用性

原 RDT/Architecture semantic owners 及四 profiles 保持。RDT impact/promotion2.0、Architecture 非Planning5.0/Delivery3.0、Check private6.0 与直接 consumers 成套采用新时机；Planning3.0/Delivery1.0、bootstrap/repair 不改义。真实 API版本独立于稳定知识身份。精确 source 使用完整 Git revision/locator；局部目标内容一致性不成为 semantic approval或全链 authority。

`D638-02 / CON638-CANDIDATE`：implementation 先以固定 B、实际 HEAD 和全量 paths 调原 candidate/begin_check（implementing→checking）。独立 Architecture phase2 读 immutable before authority、完整 implementation 和 proposed targets，可返回真实 reviewed_candidate。RDT phase2 impact 的 candidate_ready 定位完整隔离贡献，no_change保持实际空影响。原 Check delivery_candidate_check 仍完整检查九维与受影响未改 consumers。通过时其原 role 以 rework(target_role=implementation, affected_results=[readiness]) 返回 implementing，不写 public Check gate，再发 candidate_checked；不清 Planning 或真实历史，不授权旧结果用于当前候选。

`D638-03 / CON638-INTEGRATION`：唯一 workflow consumer 调原两 promotion owners 的 final_integration。一次固定真实目标 branch/commit，只读写命中单元及必要关系/导航；相同单元比较适用 before、本方完整 proposed 和真实 target，保留仍有效条件与双方变化。组合改变原已审内容时按唯一 Candidate Applicability And Coverage 补独立审核全部差额、组合语义及未改消费者，前提/义务变化回最早原owner。没有真实 Git阻塞不 merge/rebase或追目标。original owners 写完整 reviewed组合并读回，不从期望 DTO 推断实际成功。

实际写入后 implementation 以同 B、实际 HEAD 和全部实际差额重新 candidate/begin_check（implementing→checking）。最终 Architecture/Check 使用新 content_ref；旧写前 candidate 不能验证 after bytes。仅最终 Check record_gate（checking→reviewing）供 TaskCommit和完整独立 committed Review消费。no_change也走合法回程，无空贡献、ADR或commit。Ready/Finish不消费候选状态。

partial/output-loss 只恢复同一可唯一 intent：completed读回、pending补写、conflict停原owner。candidate_checked 丢失时按实际 phase/写入事实回原 Check、implementation或maintenance，不从phase补造pass；同 DeliveryKey与B保持。当前语义每次新作，工程事实按R578/ADR-029及唯一候选适用合同核真实定义、依赖、环境、工具链、参数/期望后采用，缺失/未知/变化才补命中检查。无需长期 cache、账本或授权持久化。

`D638-01 / CON638-IDENTITY`：完整单元与关系保持稳定ID，authority identity= guru-trellis-rdt；普通晋升允许同 identity，只校真实目标内容。根导航只在定位/身份/状态改变时写入，不追加每Issue业务摘要。Architecture使用独立稳定 identity guru-trellis-architecture。bootstrap仍要求其真正distinct successor，历史和真实接口版本不改义。

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

**D648-04 / CON648-EXPECTATION**：原Check/Branch Review从有效合同确定预期，再核代码/测试和真实消费者。完整当前Check、精确committed B..H Review和受影响未改consumer各自保持。测试私有固定值不能替代源约束；绿测试与一致设计不豁免职责缺陷。

**D648-05 / CON648-APPLICABILITY**：原task-free pre-write/evolution gate判断gate保护语义及依赖必要性。样本以同域catalog的展示重命名A和生效目标选择B表达operation差异，具体业务名不进入公共方法。原实现/测试共同过度限制A时，owner在剩余受影响target write前停止，并沿原机制/evolution/scope consumer处理。A/B实际调用与state前后由测试记录，AI说明不适用理由、必要阻断和evidence职责。

**D648-06 / CON648-COVERAGE**：单一Candidate Applicability And Coverage定义继续拥有复用规则。原owner读取新原证据后判定哪些前提失效、哪些覆盖仍有效；代码/测试未变不豁免，整体版本或身份变化不自动重跑。同一合规独立reviewer可接续，当前阶段结果仍实际发生。

**D648-07 / CON648-VALIDATION**：原Architecture/Check semantic_authoring与原native Adapter扩展本项写作、实施、Review和task-free事实。测试私有运输只执行真实Agent请求、落其原字节、记录原wrapperstdout及状态变化；它不选语义结论或改public DTO。声明多owner连续性时，用同一stateful fixture消费实际前序stdout。预置合法前置只证明起点，不冒充本轮前序判断。RDT以隔离完整proposed目标进入candidate Check，原final_integration整合读回后以实际after重新candidate/begin_check，原最终Check/committedReview不省略。

## D649：当前成果收敛与结果引用

**D649-06 / CON649-KNOWLEDGE** 承接 R649-07。原 RDT contract／current-knowledge 和 Architecture contract 在其既有职责中读取真实解除条件，更新当前定义、指南、派生说明，保留历史阶段观察。当前 R/D/T 单元展开行为，公共 Skill 内部步骤仍由各原 package 单写；spec 只作最小定位。

隔离贡献提供九个完整 proposed targets，保留原身份及所有有效前驱条件。候选 Check 之后，原 final_integration 才写 shared current 并读回；implementation 以同 B、实际 after 重绑，最终 Check 与独立 committed Review 覆盖真实内容。没有新的晋升时机或状态。

#637 Test 的有限修正只使用原 archive 正式结果、PR #644 和已证 main ancestry；保留原命令、失败、未知、legacy reapply 阻塞及其它未证边界。#649 唯一实际结果记录各运行的真实层次、cutoff 和失败，不从相同 exit 或最后一次重跑推导成功。

## D-MECH：采用机制与原 owner 承接

**D-MECH-01 / CON-MECH-ADOPTION** 承接 R-MECH-01/03/04。原 Architecture contract 单写采用机制审核方法，按实际行为、状态、依赖和直接消费者确定对象，含无 diff 的复用。先判断当前必要性、职责与作用范围、整体代价、替代和证据，再解释设计依据；完整宪法不排名。Author 在原候选与方案比较中消费，Approval 在原设计充分性等维度核落点，Check/Branch Review 审完整实际候选及受影响未改消费者，不复制另一套问卷。受审旧技术选择可被质疑，真实约束及原 change contract 继续有效。

**D-MECH-02 / CON-MECH-PROTECTION** 承接 R-MECH-02。原 root-cause contract 的 Protection 分支拥有提出方举证；作者、reviewer、模板提出保护都须说明真实缺口、补齐、收益和整体代价。原正常场景、solution/root qualification 及 finding 出口不变；脚本不从缺签名/锁/重试或安全词汇生成结论。新保护缺证不先成为义务，旧保护缺证只限制依赖结论，不自动删除或视为通过。

**D-MECH-03 / CON-MECH-KNOWLEDGE** 承接 R-MECH-03..05。原 current-knowledge 单写文档优先取证、完整决策单元和存量处置关系。RDT 足够时不追全部源码；行为、性能、消费者完整性或冲突有缺口才定向查。纠正决策区分必须同步适配、可独立分期和场景保留，在原单元/change contract 承接真实 owner、共存依据、剩余消费者、可执行交付/触发及退出证据，不建永久迁移台账。

项目方法投影由原 Architecture contribution/final_integration 写 change-contract。六个 RDT 完整拟写由原 RDT owner 保留有效前驱，先接受独立 Architecture/候选 Check，再由原 final_integration 写入读回、同 B 的实际 after 重绑及最终 Check/完整 committed Review。公共 I/O、schema、runtime、状态、原则、single-writer 和阶段保持；canonical 经原 preset 完整分发，既有业务安装采用另行证明。
