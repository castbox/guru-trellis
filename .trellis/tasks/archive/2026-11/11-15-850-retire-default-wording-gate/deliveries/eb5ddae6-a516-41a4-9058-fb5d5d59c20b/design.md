# D1 设计：默认 Wording 退出与直接迁移

## 1. 设计目标、需求承接与内容基线

本设计承接本批 PRD 的 SC01–SC07、整体 R01–R04、AC01–AC05。D1 全量覆盖默认步骤退出、真实语义责任、显式只读、公共 API、在途及安装迁移，没有前序 Delivery。

开发基线 B 为 `a72981db56d2070d8140b468cab3a97ae82effd3`，来源是本 Task 原 Sync 固定读取的 origin/main。Planning H0 同为该 commit；内容候选由原 constructor 在实际实施后建立，不将 H0 当成最终实现 HEAD。PR integration 目标是 main，实际集成阻塞沿原 Reconcile owner。

阶段适用 Architecture 为 `docs/architecture/README.md / guru-trellis-architecture / active`；constitution 为 `docs/architecture/00-foundation/design-constitution.md / guru-trellis-design-constitution-v1 / current`；change contract 为 `docs/architecture/06-governance/change-contract.md / guru-trellis-architecture-change-contract-v1`。原独立 candidate_assessment 实际返回 architecture_impact / target_native；其直接责任是完整隔离贡献与 ADR、最终方案评估。该结果不代表 final_plan、实施或安装通过。

## 2. 当前系统、边界与目标差额

当前默认完整链是 Discovery→Clarify→Wording→Readiness，Readiness runtime/common.py 与 runtime/invoke.py 硬性要求 wording_current 并携带 Wording linkage。已有 Issue 的 runtime/issue_review.py 接 supplement_wording 与两种 Wording 返回。当前 Planning 是 Author→Wording→final Architecture→Approval；Wording content_changed 回 delivery_wording_reentry。Create Issue 直接消费 Readiness 的 reviewed_target，未读取 Wording private evidence，但其前序审查和评论仍依赖完整默认链。

目标是直接 Clarify→Readiness、Author→final Architecture→Approval；真实内容质量在原 owner 的完整判断中保留。退役同名 Wording Skill、scanner、词表、分类、专属回执、旧路由和无人消费资产。不得把扫描结果搬到 Clarify 或 Author。Task/Delivery 公共模型、selected scope、原正常 freshness 和其它阶段门禁保持。

## 3. 来源设计处置（唯一）

| 来源及原承诺 | 处置与本设计落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| #850 职责对照的七项语义责任 | retain；第4节原 owner 方法及第8节真实Agent验证 | 取消独立步骤不取消保义、完整条件、方案唯一性和可观察验收；不搬七字段 |
| #850 默认完整链、Planning、#819直接迁移 | retain；第4–6节同步改 consumer、API与回程 | 不只删调用；保留Readiness/Create/final Architecture/Approval本身判断 |
| #850 scanner和专属资产随依赖解除退出 | retain；第4、7节整包与受管路径退役 | 无独立当前质量职责；不保留optional scanner、wrapper或长期双读 |
| #850 显式只读措辞审核与语义未变/实质修改 | retain；第4–7节 bounded profile及原返工owner | 无Task绑定、无写入、无完整Intake扩张；本批不赋予只读请求修订权 |
| #850 公共API、在途、匹配安装切换 | retain；第5、7节当前版本与固定旧provider边界 | 原对象/实际义务接续，不伪造pass、不清空状态或重建Task |
| 当前 #93/#114 的独立强制词面机制；#819 的 Wording-only 补审路由 | change；删除默认步骤、迁移两类原补审到Clarify实际内容职责 | #850明确替代对应机制；历史材料与固定版本保原义，无需向旧Issue反向改文 |
| #154/#818 的来源、内容与清晰写作方法 | retain；只修改专属Wording引用及职责落点 | 单一方法与原审核充分性继续有效；不重做其它Issue能力 |
| 当前Architecture/RDT完整单元中的Wording owner条款 | change；第9节隔离贡献和ADR窄替代 | 原维护owner在实施后整合，当前阶段不直接写shared current |

## 4. 模块、职责与设计取舍

| 模块／实际文件 | 输入、行为和唯一结果职责 |
| --- | --- |
| `packages/guru-clarify-requirements/{runtime,schemas,references,SKILL.md,interface.json}` | 全链保原意图/来源/范围判断并直接交Readiness；从实际source snapshot派生标题/正文身份；局部措辞只补真实缺口；新增独立只读profile不产生开工结果 |
| `packages/guru-review-change-request/{runtime,schemas,references,SKILL.md,interface.json}` | 自己执行原十维；full-chain消费当前Clarity；local只保context/requirements返回；真实措辞缺口交原Clarify的有界内容职责，回同次Readiness |
| `packages/guru-author-task-plan/` | 保唯一正文writer，明确七项责任的实际落点；plan_ready直达final Architecture；新content revision入口只判断并执行原最早依赖，不新增审核阶段 |
| `packages/guru-maintain-architecture-baseline/`、`guru-approve-task-plan/` | final_plan基于实际当前design与贡献，不再称Wording-current；独立两目的与Approval八维不变 |
| `packages/guru-create-issue/`与task-intake投影 | 消费新Readiness真实target；保完整草稿复核、评论生产/读回、duplicate和副作用边界；不创建Wording前序证据 |
| `packages/guru-discover-change-context/`、`guru-sync-base/` | 保事实及固定来源职责；更新full/local返回的引用和consumer，不取得内容充分性判断 |
| `packages/guru-review-change/` | 新增explicit_files/wording_only，snapshot选定Markdown全文，包含未变更文件；限定表述和保义审核，不继承range profiles的实现完整度与三视角前置；Issue/draft走Clarify专属只读profile |
| `packages/guru-review-contract-wording/`、registry及workflow旧wrapper | 删除整包、registration、默认mandatory/出口/consumer及无人消费脚本；其固定历史由原Git版本/历史材料定位，不继续作为当前provider |
| `consumers/workflow/stage0/`、workflow/routing及当前spec/docs | 同批更新source/route/schema/projection与恢复合同；每个当前出口唯一consumer；历史不可变材料不改标签 |
| `apply_guru_team_trellis_preset.py`、原tools owner | 更新受管desired inventory及旧wrapper退役；复用stale skill/overlay/legacy removal和sidecar，保Task/session与用户修改 |
| eval adapters、runtime/tests、preset integration tests | 迁移真正调用受影响entry的fixtures；删除只测退役scanner的测试；保留真实source/current/模式/用户内容与迁移断言 |

默认选择直接演进与同步consumer迁移。另一套scanner、receipt、fallback或长期adapter无法提供独立当前质量职责，会保留原问题，因此不采用。新source token只服务真实Readiness内容一致性，不能用作授权、语义pass或全链digest authority。

## 5. 接口与数据

### 5.1 全链源身份与Readiness

当前Clarify的target_content_sha256来自语义对象，不能冒充Wording原title/body内容身份。后继Clarify从原caller实际捕获的`owner_context.change_request`快照读取kind/repo/number或draft_id/title/body/updated_at。record/check核其与review_target的对象、body和更新身份一致，派生一个`source_content_sha256`，不调用scanner，不保存快照。计算由共享中性模块`trellis/skills/guru-team/runtime/content_identity.py`的纯函数`title_body_identity(title, body)`单写，沿现有Readiness的title/body组合identity规则。Clarify与Readiness调用同一函数，不复制第二算法。该模块无状态、路由或语义判断；Create原target计算的title/body组合项使用同一函数，其其它identity及恢复合同保持。

`clarity-current-4.0`保留原mode/base/target/continuation/source_selection/clarity/disposition，并增加该最小源内容token。Readiness将其与实际current target.content_sha256比较，保持checker对live Issue的实际读回；语义content_sha256和source token分开。录入错误对象/正文或正常stale返回原producer，不把缺失token补成pass。

全链Readiness保`ready/clarify_requirements/refresh_context/blocked`四出口，删除`review_wording`。ready只要求真实Clarity及本owner完整Gate；source target不一致回原owner刷新。`readiness-current-4.0`不携带Wording对象、scan或专属linkage；Create Issue仍只消费原reviewed_target。新ready aggregate为8.0、full-chain分支6.0；原三类public input发布2.0后继，Readiness public input aggregate从2.0升至3.0并选择新source profile及local return分支，原owner change-request-review发布4.0。原固定版本schema仅在存在明确历史验证consumer时保留；当前Interface不选旧分支。

### 5.2 #819局部路径

现有Issue先行Readiness仍可直接ready，不要求本轮完整链。新local owner schema2.0删除supplement_wording。`supplement_requirements`明确携`review_focus=requirements|wording_only`及原gap；该字段直接约束Clarify补审范围。Clarify local输入/语义owner发布2.0后继并保同Issue/base_source/continuation。真实措辞缺口只做保义、条件与清晰度审查，不改已确认范围；发现实质scope缺口按原Clarify判断处理。

local return2.0只保actual context_result或requirements_result两分支；Clarify完成后仍`supplemented`，Readiness重新判断剩余义务。Discovery context-return必须原样携带review_focus/gap到同一次Clarify。现有Issue ready1.0仍仅含原Issue/source/selection，可保持其wire；aggregate8.0选择该未变分支，不为形式新增字段。

### 5.3 显式只读与Planning返工

Clarify新增`standalone_wording_review`1.0：mode=standalone，target为明确Issue或调用期draft正文，输入保本次review_request。Issue分支为repo_ref/number；draft分支为caller_locator/title/body。当前owner实际读取对象及必要来源，只在本次措辞范围判断；不要求Discovery receipts、Task、Delivery或session，不创建/修改对象。出口`reviewed`带当前可读结论及具体发现到唯一user-response consumer；`blocked`保实际缺失对象/来源。该结果不进入Readiness或Task graph。显式文件走原review-change新增的`explicit_files`1.0：`mode=standalone`、`repository`、非空精确Markdown `paths`、固定`review_focus=wording_only`。该profile捕获选定文件的完整当前bytes，包括没有Git差额的文件；当前working_tree+paths只捕获相对HEAD的差额，不能承接此能力。public input aggregate发布2.0并加入该分支，现有working_tree/committed_range wires保持。其step-local方法只审核选定全文的表述、完整条件和含义保留，保原reviewed/blocked user-response出口；不机械继承range profiles的实现完整度、测试与三subagent前置。未改变的range profiles仍执行原完整独立审核方法。不创建另一Skill、Task/session、Intake或写入。

Author aggregate发布3.0，新`delivery_content_revision`1.0承接真实`task_ref/delivery_key/change_refs/mode`，原owner先判断语义未变或实质影响。语义未变只重审实际变化及刷新直接依赖；实质变更先按变化类别回requirements/candidate Architecture/原scope owner。原`delivery_wording_reentry`退出当前aggregate；其它八类中未改变的输入/结果保持wire。plan_ready本身保持最小key/ref，workflow直接加载final Architecture，再将实际final result投影到原Approval。

Clarify clear发布delivery-index4.0及full-chain5.0；现有public-clear-output-4.0的path/id和历史含义保留，不用新必填源token覆盖。Clarify public input aggregate从现有4.0升至5.0，新增standalone_wording_review及更新local profile分支；Readiness public input aggregate从2.0升至3.0，原三类source profile使用2.0后继并选择local return2.0。对应Interface、runtime选择、shared consumer、graph及实际fixture同步选择后继，旧已发布schema不静默改义。shared semantic-owner envelope发布3.0并选择匹配当前profile；private非active owner发布6.0以绑定源snapshot且不改旧3/confirmation5的历史含义。被改变的current aggregate/profile/consumer同时切换，fixed旧安装从原完整版本读旧schema；不让旧公共envelope落入新runtime。原命令transport不改。

### 5.4 资产与副作用边界

不增加持久状态表、授权字段或scan账本。source/semantic token只校相邻内容一致性；public输出只留唯一consumer必需字段。shared Interface metamodel仍服务其真实其它packages；旧stage literal不激活retired步骤，不因文本命中机械重写所有历史schema。删除所有无独立consumer的专属schema/示例/配置/测试/注册。

## 6. 状态、顺序、正常与失败流程

1. draft／no-Issue正常完整链：Sync→Discovery→Clarify clear→Readiness。current_issue全链同理。ready只交原Task intake router；proposed draft交原Create Issue，创建/评论读回后只创建请求结束，还要工作则正式Issue重新Sync→先行Readiness。
2. existing Issue：Sync→Readiness。事实缺口→Discovery→原Readiness；内容/措辞缺口→Clarify适用focus→原Readiness。多缺口每次只补实际最早缺口，不自动串剩余完整链。必要full-intake消费原Sync transition，不能反拼三字段source。
3. Planning：Creation→Author requirements→candidate Architecture→Author design/implement→final Architecture→Approval→展示/接受→Activation。实施本Issue前仍使用本checkout当前旧workflow的Wording步骤；源合同修改与匹配安装后才切换目标路径，不提前跳门禁。
4. 显式只读：按对象路由→原owner读取及判断→user-response。实际修订另循原写入边界；没有自动写入。
5. 原owner发现stale source/key/generation/scope/phase或必要事实缺失时保持原错误与恢复consumer。取消的是Wording专属前置，不取消身份、实际阶段、来源和原质量检查。

## 7. 恢复、兼容、迁移与集成

`MIGRATION-850.md`在实施时发布明确的current-only公共切换表、实际旧入口和恢复边界。无长期旧runtime reader、adapter、双写、wrapper或扫描兼容。

| 实际在途位置 | 新路径接续与证据 |
| --- | --- |
| full Intake待Wording | 从当前对象和原Clarify覆盖回原Clarify发布后继源身份，再进入Readiness；已有来源/语义覆盖仍适用则只补实际新增源身份判断，不重启Sync/Discovery访谈 |
| 已有适用Wording/内容判断，待Readiness | Readiness按current对象复核其有效内容覆盖；需要后继Clarity源身份时回原Clarify，不把旧Wording结果改标签成新pass |
| #819 supplement_wording或其返回未消费 | 从原Readiness的同Issue/base/continuation/gap重建Clarify wording_only调用；旧wording_result不进入新return schema |
| 旧content_changed到Author | 原Author读取实际change_refs及当前三文档，进入同Delivery content_revision；按影响刷新直接依赖，不丢scope/key/selection，不首次激活 |
| Planning已有有效结果，接近final/Approval | 复用适用覆盖，原owner只刷新受改变合同/内容影响的判断；新路径不索取Wording proof |
| 固定旧provider已开始Issue创建、评论或其它副作用 | 先用该完整固定provider完成/恢复同一对象，再沿原tools owner匹配更新；不把未完成旧envelope给新runtime，不重复远端动作 |

canonical source保持唯一源头。已有checkout沿原`guru-upgrade-tools`完整source合同preview/prepare/invoke/readback/reapply，不能手抄dogfood。退休Skill包及平台文件使用原stale managed删除；未改managed文件可删，用户改动保留并按原sidecar/冲突owner处理，未知内容不静默覆盖。旧根wrapper加入原已知legacy managed removal，已有不明hash保持原冲突路径。安装保TaskId、generation、accepted_scope、DeliveryKey、phase、规划结果、session和用户配置；本D1已在implementing时的更新不能重建slice。

已发布旧源码/归档保持固定Git身份；只作为历史或明确固定provider恢复使用，支持在该操作完成并匹配更新时退出，不构成新current双链。其它Task不强制升级或修改其metadata，本Task最终写入shared单元前原owner重读真实target并语义整合。

## 8. 验证设计

| 验证 | 需求／入口与输入 | 必须观察、层级及限制 |
| --- | --- | --- |
| V01 | AC01/04；生产Sync/Discovery/Clarify/Readiness wrappers，current_issue/proposed_draft/standalone_request | 实际producer输出直接达到ready及唯一consumer，非预造transition；Create写前target和最小评论承接真实Readiness。mock GitHub不算live写入 |
| V02 | AC01/04；existing-Issue先行、两补审、多缺口、必要full-intake及context往返 | focus/gap/source/continuation保留，补审回同次Readiness，无Wordingproof或剩余全链自动执行 |
| V03 | AC03/04；同Delivery content revision及受支持旧待办接续 | scope/key/phase/selection与有效规划保留；语义未变只刷新直接依赖，实质变化回原owner；用正常旧provider输出/操作，不手改artifact/hash制造场景 |
| V04 | AC02/03；真实Agent原入口分别审核Issue/draft与规划、显式文件 | 输入含正常需求弱化、条件缺失、来源语义丢失、验收不明，以及无受控词命中的缺口；观察具体发现和原修订owner。清楚建议/default/quote/history/literal不因词面阻塞；被测Agent不取得预期finding |
| V05 | AC03；无Task的standalone_wording_review与review-change路径 | 对含未变更文件的选定Markdown全文完成有界结论，核snapshot覆盖完整bytes；对象bytes与Task/session不写入、不进入完整Intake；场景所需来源不可读时实际blocked |
| V06 | AC04；source package/interface/schema/consumer与动态discovery | 全部当前出口唯一consumer，退役专属命令不可用，实际新profile可调用；失配回原producer。保其它Task生命周期/qualification恢复消费者 |
| V07 | AC05；原installer/tools matching更新、reapply、managed退役和user-edit sidecar | source/installed/声明平台bytes+mode、真实旧文件退出、用户内容保留、Task/session前后不变、drift和sidecar结果分开；至少一个匹配目标，最多一个clean throwaway，不扩Release矩阵 |
| V08 | 全部；RDT/Architecture proposed→final_integration/readback→TaskCommit后独立Review | 完整current正文/必要关系反映实际迁移；不能由源码green或贡献存在推定晋升/Completion |

长期回归覆盖实际路由、源identity、返回、恢复与安装退役。V04/05的实际Agent观察为本Task验收，不新增通用评测系统/固定数量门槛。采用适用既有覆盖并补受影响producer/consumer；退役scanner的自证测试随资产删除。无强制旧版red或重复回退；已有观察不足以确认新测试reach时才做有界对照。

## 9. Canonical 引用、本轮差额与实际未决项

本批PRD第7节定位RDT/Architecture实际current单元。RDT strategy为delta_first：原RDT owner在phase2准备`docs/requirements-design-test-contributions/850-wording-retirement/`的完整差额/追踪，整合Issue-content、local-fix-intake及task-delivery必要关系，不写根索引或全局版本。

真实Architecture隔离贡献为`docs/architecture/contributions/850-wording-retirement.md`，必要ADR候选为本planning_root的`architecture/adr-wording-retirement.md`。贡献拥有拟变更完整职责定义，包括Architecture change-contract的完整Change paths and lifecycle及Current Planning boundary章节、runtime-location的明确Git对象与实际副作用完整章节，以及ARCH-INT-044和ARCH-DOM-061完整单元；#819历史before原文保留。ADR窄替代旧独立Wording决定；原Architecture owner在工程完成后final_integration写shared current并读回，提交后新独立Review审实际before/after。Planning阶段不直接改shared authority。

### 项目 change contract 的九项 concern

本节是本Task设计对`guru-trellis-architecture-change-concerns-v1`的适用判断，直接供原Architecture project-check和实施核对使用；不建立另一份gate账本，也不声明工程通过。

| Concern | 适用性 | 本Task理由与落点 |
| --- | --- | --- |
| authority-binding | applicable | 第1节绑定planning3.0两目的、阶段适用baseline及原change-contract；非Planning沿原6.0/Delivery4.0，不用候选结果替代最终结果。 |
| constitution-binding | applicable | 原constitution current保持；本次职责收敛、最小纯函数、有界原owner入口及current-only切换按其五原则评估，真实取舍由本设计及ADR拥有。 |
| boundary-and-decision | applicable | 第2–5节改变默认Wording边界与直接consumer；ADR-850窄替代其独立机制，不改需求及终态权威。 |
| owner-and-single-writer | applicable | 第4节明确Clarify/Author/Readiness/Architecture/Approval及原tools各自职责；Planning只写隔离提案，RDT与Architecture各晋升自身正文。 |
| compatibility-and-exit | applicable | 第5、7节声明真实后继版本、同批consumer切换、固定旧操作恢复及managed退役；无当前旧envelope reader或长期双链。 |
| gap-and-deviation | applicable | 本批不新增永久GAP；既有GAP006/008的历史与原退出合同保持，实际新偏移由原Architecture判定，不从本规划推定closed或通过。 |
| parallel-scope | applicable | 仅本Task规划/贡献及已批准canonical内容可写；其它Task、共享journal与#853在途内容不进入本批写集；shared current只能原维护owner在合法边界整合。 |
| evidence-and-freshness | applicable | 第1节固定B/H0与目标，第5节分开源/语义身份，第8节区分生产wrapper、真实Agent、安装及外部证据；实际当前design/贡献由原owner绑定，token不作语义authority。 |
| review-and-promotion | applicable | 真实贡献和必要ADR已隔离；工程充分后原owner按真实expected-current整合并逐个readback，仅为integrated_pending_review；TaskCommit后一次独立完整Review判断实际before/after。 |

本方案没有未解决的产品范围选择。实际final_plan/Wording/Approval尚须原owner基于本文执行；V01–V08尚未完整验收，已有helper局部工程事实不构成完整实现或安装通过结论。实现发现新的实质consumer、来源义务或兼容机制时回原受影响规划/架构owner，不能自行增加兜底。
