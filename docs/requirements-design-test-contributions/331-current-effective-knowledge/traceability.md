# #331 追踪、迁移清单与来源核对

状态：`promoted_source`。比较来源全部固定在 Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`（B）的实际文件；RDT current `.109` 通过既有immutable前驱继承下列有效合同。本轮已纳入 RDT `.110`，关联 Architecture `.101`；原比较起点 `.109/.100` 保持为历史来源。本文件存来源/关系和替代范围，不成为另一份业务规则。

## 新增差额的双向关系

| Requirement / behavior | Design / contract | Test / scenario | Current正文 |
| --- | --- | --- | --- |
| R331-01 / BEH331-01 | D331-01/04 / CON331-01/04 | T331-01/04/05 / V331-A/D/E | [Requirement](../../requirements/current/knowledge-maintenance.md)、[Design](../../design/current/knowledge-maintenance.md)、[Test](../../test/current/knowledge-maintenance.md) |
| R331-02 / BEH331-02 | D331-02/04 / CON331-02/04 | T331-02/03/05 / V331-B/C/E | 同一KNOWLEDGE三层单元；[Completion修订对象](../../requirements/current/completion-closure.md) |
| R331-03 / BEH331-03 | D331-03 / CON331-03 | T331-04/05 / V331-D/E | KNOWLEDGE三层；[generic source](../../../trellis/knowledge/technology-baselines/trellis-extension/versions/1.0/baseline.md)、[project](../../architecture/00-foundation/stack-selection.md) |
| R331-04 / BEH331-04 | D331-01/04 / CON331-01/04 | T331-01/03/05/06 / V331-A/C/E/F | KNOWLEDGE及[LIFECYCLE](../../requirements/current/task-delivery-lifecycle.md)三层 |
| R331-05 / BEH331-05 | D331-05 / CON331-05 | T331-03/04/05/06 / V331-C/D/E/F | KNOWLEDGE三层；[MIGRATION-331](../../../trellis/presets/guru-team/MIGRATION-331.md) |
| R331-06 / BEH331-06 | D331-06 / CON331-06 | T331-01..06 / V331-A..F | [Test策略](../../test/current/knowledge-maintenance.md)、[唯一实际结果](./test.md) |

三层主题的唯一locator为 `docs/<requirements|design|test>/current/<topic>.md`。下表LIFECYCLE、COMPLETION、KNOWLEDGE分别指task-delivery-lifecycle、completion-closure、knowledge-maintenance同名三层文件。对应unit identity是RDT-REQ/DES/TST-主题；原条目identity不改，unit identity只是容器，不替换原ID。

## 实际前驱 → 完整当前单元

来源列给出B内精确文件与条款；对于contribution，原 requirements/design/traceability/test分别拥有其层次，实际历史结果仍由原test单写。新单元展开能力行为与责任/预期；canonical公共规格仍由原package独占，属于必要关系而非待拼接业务delta。

| 旧稳定identity / exact predecessor | 目标 / 迁移范围 | 保留条件、替代范围及历史关系 |
| --- | --- | --- |
| REQ-001/002/003/004/005/008/010，BEH-001..006；`docs/requirements/versions/current-main-0.6.17-guru.53/requirement-main.md` §目标/生命周期；DES-001..005、CON-001/002及TST-002/003/004/007、CASE-001/002、SCN-001..004见该版三层及trace | LIFECYCLE / authority、入口、AI/脚本、Planning/实施/Review | 身份/职责/兼容/正常路径条件保留；旧Task级开发Planning/Finalizer顺序仅在已被R531/ADR-030取代范围退出，历史不改。具体公共schema/source算法未迁为新正文。 |
| R531-01/02/03/04/05/08、BEH531-OWNERS/PLAN/REWORK/CANDIDATE/FACT/DEPENDENCY；`531-task-delivery-lifecycle/requirements.md` 表对应行、design D531-01..05/08、trace、test T531-02..05/08 | LIFECYCLE / 整体与slice、D1/D2、唯一writer、返工/撤回、clean/dirty、事实恢复、局部依赖 | D2不覆盖D1、保留scope/identity/history；停不是交付；局部provider不阻断独立必要工作；原事务零重复mutation，历史事实不等gate。 |
| R292-01..12/14/15、BEH292-WRITER/SOURCE/DISPOSITION/PROFILES/CHAIN/PURPOSE/RECOVERY/BRAINSTORM/PREWRITE/POLICY/DELIVERY/DEPENDENCY/DISTRIBUTION/HANDOFF；`292-unique-planning-author/{requirements,design,traceability}.md` | LIFECYCLE / 唯一Author和独立gates、source角色、处置/Policy/Docs Plan | 唯一writer/目的/语义条件保留；Task级开发profiles及BEH292-EXECUTION的resume_execution由R531迁为Delivery同owner路径。历史9profiles/接口不当当前替代规格。 |
| R154-01..06/BEH154-01..06；`154-planning-body-contract/requirements.md` 全表、design D154-01..03/CON154-01..03、trace/test T154-01..05 | LIFECYCLE（正文行为）/ KNOWLEDGE（分发） | 四类正文的完整来源/深度/条件、详细承诺、唯一来源设计处置、独立下游实际读取及受控匹配采用保留；完整字段/templates继续canonical单写。 |
| R530-01..06 / BEH530-CONTINUE/IDENTITY/READONLY/RECOVER/FULLREVIEW/DISTRIBUTE；`530-clean-committed-reentry/requirements.md` 全表及trace | LIFECYCLE / clean首次完整Review，dirty仍exact commit | 仍freshCheck/currentidentity/独立完整Review；零空或重复commit；实际stale/base变化回原owners，不复用旧commit。 |
| R535-01..05 / BEH535-EMPTY/QUALIFY/GATES/PROFILES/DISTRIBUTE；`535-review-zero-candidates/requirements.md` 全表、trace D535/CON535/T535 | LIFECYCLE / Review正常空集和完整gate | 零候选与非空全rejected分明；空集不决定passed/ready；原profile/Docs/Architecture/freshness及distribution要求保留。 |
| BEH567-01..07；`567-fixed-development-baseline/requirements.md` 全表、design/trace | LIFECYCLE / B/H/target分离、正常零Reconcile；COMPLETION/KNOWLEDGE / 适用性 | 默认追赶、祖先/latesttarget资格等窄片段被替代；真实scope/dependency/solution/立即适用规则、actual conflict/requiredCI集成失败/已证服务器要求/主动同步及同操作恢复全部保持。 |
| R600-01..08 / BEH600-01..08；`600-promotion-before-check/requirements.md` 全表、design D600-01..04/CON600、trace/test T600 | LIFECYCLE及KNOWLEDGE / before/after、晋升/最终Check、Review、恢复、分发 | 独立Phase2先、原owner晋升、最终Check、commit、独立committed Review。仅替代post-Review首次晋升，不弱化独立性/expected-current/validation；三类在途版本成套迁移细规继续MIGRATION-600，不复制旧parser。 |
| R531-06 / BEH531-COMPLETION、D531-06/T531-06；`531-task-delivery-lifecycle/{requirements,design,traceability}.md` 对应行 | COMPLETION / 整体收尾、无Delivery证据/验证 | Completion/Closure/Finish/Cleanup/Reactivate分别拥有实际事实；纯证据/收尾不造空Delivery，旧pass不代替新whole判断。 |
| R436-01..05、R454-D436-01..05及D454/T454同号；`436-post-delivery-completion-finish/requirements.md` 与 `454-task-lifecycle-d436/{requirements,design,traceability}.md` | COMPLETION / 终态五owner、exactsource动作、archive/ledger/新generation | 整体scope、精确资源/回收consumer/隐私/原事务保持；旧TaskLifecycle输入由R531上游公共模型承接；exactsource必close及Finish仅CLOSED由R547窄替代。R436-06/R454-D436-06的历史activation/composition证据保持历史。 |
| R434-01/02/03/05；`434-task-delivery-lifecycle/requirements.md` 对应条；其design/trace | LIFECYCLE / Refs-only和slice结果；COMPLETION / archive/Reactivate/旧closeout | business merge不完成Task、不关Issue、不归档；bookkeeping不递归Delivery；source discovery不能由空summary排除；旧closeout用pinned旧完整版本或显式逐事实处置，不虚构交付。 |
| R547-01..08 / BEH547-SCOPE/DISPOSITION/RESULT/ARCHIVE/COMPLETION/PROJECTION/RECOVERY/ADOPTION；`547-retain-source-open/{requirements,design,traceability}.md` 全表 | COMPLETION / retain_open及完整action set | exact_source资格不等close意图；OPEN/no_mutation/source_result=null、混合集aggregate/source分离、blocked零事务、普通drift回Closure、Finish状态核对、matchingconsumer边界全部保留。 |
| R383-01/02/06/07/08/09；`383-causal-completion-semantics/requirements.md` 表及canonical `trellis/presets/guru-team/spec/workflow/causal-completion-semantics.md` §Ownership/Evidence/Completion equivalence/Semantic changes | COMPLETION / scope感知、证据层次、因果/补证/严格等价；KNOWLEDGE / commonauthority | diagnosis/mitigation/feature/implementation-only与生产根因目标区分；未知不虚假完成，不危险replay，不自动grant生产权限。commonprose及admission的完整规范仍canonical单写。 |
| BEH-557-01..04；`557-manual-merged-delivery-recovery/requirements.md` 表；canonical Merge `delivery_merged_recovery` / Completion人工合并段 | LIFECYCLE / 原Merge事实恢复；COMPLETION / actual-vs-published完整差额和CI | unique公开关系、普通two-parent merge、零重复merge、输出丢失/base推进/branch删除事实保留；MERGED不等actualcandidate gatepass，squash/rebase未支持。 |
| BEH569-01..11；`569-fixed-cutoff-history-query/requirements.md` 表；canonical Completion §Bounded history consumption | COMPLETION / consumer实际cutoff与有界补事实 | 当前公共facts足够无额外history前置；new同Task事实才补缺，外部ref无关前进不追赶；完整query扫描/Git临时对象算法归原Merge package/旧authority，未迁为本主题实现正文。 |
| REQ-011/BEH-008、DES-005/009、TST-010/SCN-003；`.53` 三层对应identity和trace | COMPLETION / 历史、archive、exact资源 | Task history可追溯，不覆盖peer；retiredworkspace mapping/Finalizer整段owner由现官方Task/session及D531终态owners替代，旧source/Git历史保留。 |
| REQ-007/BEH-007、DES-007、TST-006/SCN-006；`.53` 三层及trace；canonical RDT SKILL.md/contract.md §authority/Profiles/Stage applicability | KNOWLEDGE / 三层唯一authority/完整trace/四profiles | 只读Architecture公共identity；隔离contribution、subtraction/history、AI判断、最小output和原repair全部保持；新增current完整单元，不另立owner/状态机。 |
| REQ-027..035、DES-026..034及原TST-018..026/SCN-024..033；`.53` 对应条/trace；canonical Architecture contract §Authority/Independent assessment/Stage-applicable/Pre-Check promotion | KNOWLEDGE / 原架构维护职责、路径、checks、阶段适用和晋升关系 | 项目constitution/分区/requiredconcerns/singlewriter/checks/ADR触发/兼容/独立before-after保留；REQ-034无关current前进强制sync片段由R567/ADR-028替代，DES-027旧晋升顺序由R600/ADR-030替代。具体项目架构规则/descriptor仍Architecture单写。 |
| R578-01..05/BEH578-01..05；`578-cross-owner-validation-facts/{requirements,design,traceability}.md` 全表及Architecture contract §Engineering execution facts | LIFECYCLE/KNOWLEDGE / 当前judgment与可采用工程事实 | current独立checkset/result必新作；真实definition/dependency/expectation/toolchain/params/environment适用才采用，unknown/missing/变化补受影响检查；不读retiredprivate，不造cache/ledger。 |

上表contribution短locator均相对于本目录的父目录 `docs/requirements-design-test-contributions/`。`.53`仅定位最早通用identity，B的后继合同在本表后续行显式覆盖冲突；它的历史软件版本、计数、测试结论、Finalizer/retiredtask入口都不被迁为当前事实。RDT `.109` 的其余有效要求保持在legacy源。

## 结构调整与稳定引用

本迁移是原稳定条目移动/等义合并到能力容器，没有删除原identity，也不按展示顺序重编号。旧版本和contribution locator保持原字节。原BEH-001..008/DES-004/005/007/009关系分别可到达对应完整单元；publicAPI/source算法仍通过canonical规格引用。R331/BEH331/D331/CON331/T331是本Issue新能力身份，不占用/替换旧条目。未来真实替换/删除/拆分/合并由原owner记录前驱/后继及窄范围，不修改无关ID。

## 未迁移的 legacy 范围

`legacy_unmigrated` 是未进入本轮完整主题正文的明确范围，并非已迁移或被废弃。三个层各有同一范围的 [.109 Requirements](../../requirements/versions/current-main-0.6.17-guru.109/requirement-main.md)、[Design](../../design/versions/current-main-0.6.17-guru.109/design-main.md)、[Test](../../test/versions/current-main-0.6.17-guru.109/test-strategy.md) 入口；所需能力仍读其实际前驱完整源和canonical规格，不凭新导航猜答案。

| Legacy scope identity / 边界 | 原authority locator | 状态/关系 |
| --- | --- | --- |
| RDT109-INTAKE-DETAIL；Issue内容规范/duplicate/readiness/Sync authority细则 | `.109`及153/250/290/295/396/548 contributions与各canonical package | legacy_unmigrated；本轮只迁移正常生命周期调用/责任，不迁移每项Intake详细决策和恢复算法。 |
| RDT109-INSTALL-UPGRADE；source lock/固定Fork、平台选择/安装迁移/旧版本族/legacy维护 | `.109`及329/378/452/481/490/495/503/521/556/566/577/575 contributions与原packages | legacy_unmigrated；本轮受管分发/旧Task读取义务保持，未将完整升级或业务采用迁成三主题能力。 |
| RDT109-GIT-DETAIL；对象摘要、history query扫描、Reconcile/Git/provider事务细算法 | `.109`及311/338/342/344/347/350/358/376/557/569/589与原packages | legacy_unmigrated；本轮迁其适用性/事实/consumer行为，完整具体算法继续原source单写。 |
| RDT109-QUALIFICATION；normal/solution/root-cause候选准入详规 | `.109`及382/466、canonical qualification packages和causal spec | legacy_unmigrated；本轮只迁正常路径/共同证据/当前owner义务，不另写准入方法。 |
| RDT109-RELEASE；正式软件四轴、source adoption、candidate matrix/tag/Release/smoke | `.109`及260/267/332/335/392/410/467/575与private release owner | legacy_unmigrated；真实软件版本/历史计数/矩阵结果不从正文迁移推断。 |
| RDT109-EVOLUTION-TARGET；下一阶段产品目标 | `docs/requirements/evolution/README.md`及该目录唯一主定义 | accepted_target；非当前runtime事实，未迁入本轮current正文。 |
| RDT109-OTHER；表内未明确列出的其余稳定identity/细项 | 同层immutable `.109`及其完整继承源 | legacy_unmigrated；不能以搜索未命中或导航遗漏认定删除/完成。 |

## 切换和旧读取退出

原RDT owner逐条核对本表的条件/否定/例外/顺序及R/D/T关系，独立Phase2/真实Agent/安装证据满足后才晋升共享三层入口到reviewed successor；Architecture沿自身原owner同步公开identity。未满足时旧README仍为authority、新正文仍proposed，缺口回原repair/Clarify，不称切换成功。

旧Task planning/candidate/gates实际固定的immutable版本或Git B继续可读；不因共享CURRENT无关推进而重写其contribution或重跑businessgate。兼容仅保留此只读consumer，不向旧current双写新能力；该Task结束、合法Reactivate改选或真实依赖变化后退出其旧普通读取。历史追溯永久保留不等无限双写。晋升后普通correction走原repair/新successor，不改旧snapshot；尚未切换的candidate可在本Task范围修订而不触碰旧authority。

实际逐条核对、引用/历史字节检查和未验证边界由唯一 [test.md](./test.md) 记录。此清单和文件存在本身不证明实际晋升、真实Agent正确、安装更新、Delivery或wholeTask完成。
