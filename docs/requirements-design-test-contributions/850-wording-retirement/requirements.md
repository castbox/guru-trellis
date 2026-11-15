# #850 需求完整差额

状态：integrated_pending_review。固定前驱为Git `a72981db56d2070d8140b468cab3a97ae82effd3` 的同名current单元。原语义owner为guru-maintain-requirements-design-test-ssot；以下是已写入并读回的完整变更章节/稳定单元，其余正文及历史观察保持。关联来源及替代范围见traceability.md；精确API仍由canonical packages与MIGRATION-850单写。

# 完整整合目标：docs/requirements/current/issue-content.md

### R153-04 / BEH153-04：原内容 owner 的完整判断

Clarify 负责正文写作与自检；独立 Wording 及其 scanner 已退出当前链，不增加替代语言关卡；Clarify 在原范围内亲自判断含义、完整条件和义务强度；Readiness 在原十维内判断完整性、独立交付单位与验收；Create Issue 在原创建门禁核对已审草稿及前序适用性，再沿原路径创建和回读。每个 owner 实际读取当前正文和必要来源，上游通过不能代替自己的判断。

局部修订的内容完整性判断覆盖完整 postimage，语言检查限本轮文本和必要上下文。普通遗漏回原受影响 owner；范围外既有缺口先说明影响，不能静默扩写或虚报完整。只读审核、讨论和查询不自动获得正文写入权。原 public I/O、typed exits、确认、freshness、刷新与恢复保持。

### R153-05 / BEH153-05：分层证明与受管采用

实际 Agent 写作/审核、机械分发、代表目标安装和外部写入回读分别提供证据。原 writer 分发完整正文、必要示例和当前内容入口投影，既有目标由原 tools owner 保护用户内容与 Task/session，并检查 reapply、drift 和 sidecar。原 #153 的 V1–V7 和真实 GitHub 对象是该次历史观察，不成为每个后继任务的固定样本或写入义务。

### R818-03 / BEH818-03：完整规则与独立理解

正文按唯一正文第3节组织完整规则，各原内容 owner 按第4、5节在各自范围独立理解并核对来源、入口和必要遗漏。规则清楚可读且仍完整时保留。识别真实入口不自动增加交付项，完成原始目标所需的适配也不能被精简删去。

## 关系与边界

设计责任为 `docs/design/current/issue-content.md` 的 D153-01..03 / CON153-01..03、D818-01..03 / CON818-01..03；测试责任为 `docs/test/current/issue-content.md` 的 T153-01..05、T818-01..04。[#818 双向追踪](../../requirements-design-test-contributions/818-issue-minimal-sufficiency/traceability.md)定位本次来源与实际目标。

共同审核充分性的职责保持在 [R717](../../requirements/current/review-sufficiency.md)，其规范只定位原 Issue 方法，不取得第二内容 authority。Architecture 继承 `docs/architecture/README.md / guru-trellis-architecture / active`；#818的原独立 final_plan 为 no_architecture_impact/no_change，不产生空 Architecture contribution。#818当次没有新增Skill、公共字段、状态或外仓运行依赖，也未承接#819路由或完整安装/Release矩阵。#850的当前路由及合同差额分别由R850和对应D/T承接，不改变该历史结论。

## R850-01 / BEH850-CONTENT：原语义责任与显式只读

完整Intake由Discovery到Clarify，直接进入Readiness。原内容owner亲自保留来源含义、完整条件、义务强度、例外和可观察验收；独立Wording退出不削弱原门禁，也不新增替代语言gate、scanner或词表分类。

明确Issue/draft措辞请求由原Clarify standalone_wording_review只读完成，不要求Task/Delivery/session、完整Intake或ready。明确Markdown请求由原review-change explicit_files/wording_only读取全部选定当前正文，包括Git未变文件。报告具体位置、影响和原修订owner；必要来源缺失时blocked。合法建议、默认、引用、历史和literal不因词面阻塞。审核不授权正文修订、评论或发布。对应D850-01/T850-01。原range code review完整方法保持，有界结论不替代实现完整度判断。

## R850-04 / BEH850-ADOPTION：完整迁移与分层证明

当前producer/consumer、profile、schema及在途按匹配版本切换。固定旧provider已开始的副作用由原完整provider恢复同一操作后再更新，旧结果不改标签为新通过。原installer退役未改managed资产，用户修改/sidecar保原owner处理；Task/Delivery/scope/阶段/规划/session/配置/peer保持。源码、机械检查、实际Agent、目标安装与外部效果分层证明。真实不足保持未验证，local_candidate不证明formal_fork_source_lock或完整Release矩阵。对应D850-04/T850-04，历史原结果保其截止。

# 完整整合目标：docs/requirements/current/local-fix-intake.md

## R819-02 / BEH819-READINESS：已有Issue先行复核

模式选择和原Sync后，已有Issue由原guru-review-change-request亲自复核完整live正文、有效讨论/审核评论、必要前置交付和影响原判断的代码差额。充分且仍适用并满足前置时ready，经原router进入原Task创建；评论存在不是自动通过，没有评论也不独立阻塞。历史清楚自然语言评论不因模板、label、身份资格或期限被排除。

只有事实缺口交原Discovery；需求、范围或独立交付单位问题交原Clarify；仅措辞问题也交原Clarify，以review_focus=wording_only区分；需求问题使用requirements。原覆盖不足或影响不可界定时执行必要完整Discovery→Clarify→Readiness。确认必要前置未满足、真实选择未解或必要证据无法取得时按原blocked/等待说明恢复条件，不以重跑掩盖阻塞。对应D819-02、T819-03。

## R819-03 / BEH819-SUPPLEMENT：同次返回与最早必要依赖

Discovery与Clarify两个原owner以真实局部profile、必要输入和逐出口consumer进入，不要求先取得本轮完整前序receipts，也不伪造前序pass。各owner完成其适用完整方法后，将实际结果交回同一Issue、来源及continuation的Readiness。Discovery不替Readiness判断开工；Clarify确需事实时沿原context往返，结束后回判；wording_only发现真实需求变化时回原Readiness的requirements分支，不借措辞请求扩大范围。

多缺口按事实→需求→措辞的依赖顺序处理最早必要项，每次补足后由Readiness再判断剩余缺口；事实不变可直接ready，需求变化只刷新受影响的原内容判断，不能进入一个局部步骤就自动串完剩余全链。旧完整链仍须真实本轮结果。对应D819-03、T819-03/04。

## R819-04 / BEH819-BOUNDARY：来源、终点与后续门禁

局部返回保真实来源kind、selected_ref、commit；固定对象read不替owner选择Task集成branch，当前Create Task只接reviewed_base_source，selected_base_ref与delivery_target分别承担原职责。保同仓commit、acquisition等值、真实同步和原成功恢复条件，完整链不反拼旧transition。只有选定来源真实失效回原Sync；会话、Agent、时间或无关HEAD变化本身不使覆盖失效。

无Issue讨论仍经原标准调查/Clarify；只讨论或草稿在对应结果结束。需要创建须完整草稿Clarify/Readiness后进入R819-01创建和评论读回；只创建至created结束，还要求开工则正式Issue经Sync→先行复核。合法standalone_request/no_issue保完整原审核和Task创建，不造空Issue或评论。Task身份、checkout、分支/资源、副作用和后续规划/交付门禁保持。

公共profiles、逐出口schema、consumers、例子及恢复通过本项matching迁移和原installer同步；AI判覆盖/路线，脚本执行/校验客观事实，不增独立复核Skill、长期ledger或digest authority。对应D819-04、T819-03/04/05。完整当前定义由原RDT owner沿#819 final_integration整合，真实观察由本次Test单写；实施及验收状态不能由本条存在推出。

## R850-02 / BEH850-LOCAL：同次措辞补审

#819仅措辞缺口由Readiness以supplement_requirements及review_focus=wording_only交原Clarify，需求用requirements、事实归Discovery。保原Issue/base_source/continuation/真实gap；需要事实时原context往返保focus。原Clarify实际处理当前文字和来源含义，必要修订沿source_actions及回读，不扩大需求。真实supplemented仅回同次Readiness issue_review_return，再重读对象判断剩余缺口或ready。局部成功不自动串完整链，无独立Wording。对应D850-02/T850-02。

# 完整整合目标：docs/requirements/current/task-delivery-lifecycle.md

## 身份、整体责任与入口

`REQ-001/003/004/005/008/010`、`BEH-001..006`、`R531-01 / BEH531-OWNERS` 保持身份。Task 承担整个 accepted scope 的要求、来源和完成责任。Delivery 承担一个明确切片的独立规划、候选、检查、审核和交付结果。D1 与 D2 使用同一种公共 Delivery 模型；D2 不能覆盖 D1 的文档、历史或结果。公共 Task/Delivery 状态归官方 Trellis API，Guru 不另建状态机，也不写 schema-2 Task 的开发 `status`。

新变更先由原 mode owner 判断 standard intake 或 task-free；Issue 的存在、文件数和路径不能单独决定模式。标准 Intake 依次同步所选 base、发现当前变更上下文、澄清来源/要求，再由原Readiness复核当前内容与独立可交付性，再由原 Creation 创建 Task 和绑定的执行位置。信息查询不创建 Task。已绑定 Task 的变化走原当前 owner，不从 Intake 重建身份。缺失、重复或不唯一的公共身份、出口、consumer、安装合同或 checkout 关系须停止或进入其原恢复路线，不能由 inventory 的唯一候选猜选。

AI 判断 scope、来源、关联、finding、充分性和路线。确定性工具只执行明确动作、读事实或校验结构/内容绑定。mandatory step 由 global workflow 以稳定 Skill id 调用，step-local Skill 独占完整内部行为。semantic Gate 的脚本成功不代替语义判断。只处理诚实协作中的合法正常路径、普通错误与过期状态，不增加对抗伪造或未要求的并发/崩溃机制。公共 Skill/exit/schema/path 的破坏变化必须有显式迁移。

`R657-01 / BEH657-ADMISSION`：初始 Task 创建和原操作结果恢复保留原 checked created 与精确创建校验。既有活动 Task 经正式 TaskId/generation、合法 binding/rebind、唯一 checkout 及适用 session/explicit-task 解析后，由实际阶段 owner 判断写入；原 created DTO 或原机私有 runtime 不可得不能单独阻塞。正常无范围变化保留仍适用工程结果，真实缺失或歧义回原 owner。每批 source/test/task 写入前仍执行 live checkout boundary，不重建 Task 或空 Delivery，不补造初始创建、资源或历史 pass。

`R657-02 / BEH657-SELECTION`：创建和明确选择已有 Delivery 都保留原 created DTO，其含义是实际 key/root 已建立或选定。唯一 consumer fresh 读取同 key 的公共 current phase；只有 planning 中真实初始需求义务且符合 Author profile 前置时进入 initial Author；已有 Planning 恢复实际 Author/Architecture/Approval，当前 approved 进入 Activation，缺失或过期结果回原 producer。其余活跃阶段回原 continuation。保留 key、phase、规划、历史及仍适用结果；不能以 created 名称重置阶段或以 phase 冒充门禁。输出丢失经原 producer 恢复同结果，后续按真实阶段承接。

## 切片建立与唯一 Planning

`R531-02 / BEH531-PLAN` 与 `R292-01..12/14/15` 保留。原 Clarify 接受整个 Task 要求后，原 `guru-create-delivery` 在首次 Planning 前建立或明确选择 DeliveryKey、scope_ref 和上游 planning_root。创建只建立 Delivery，不另建 Task/branch/worktree。方案返工、base 变化或同一 PR 更新保留同 Delivery；确有后续独立工作才建立下一切片。局部 provider 缺口仅阻塞实际依赖它的场景，已经确认必要且独立的工作继续，consumer 不接管 provider。

唯一 `guru-author-task-plan` 写 Task 整体 PRD，以及选定 Delivery 的 PRD、design、implement 和 context manifests。Task 整体文档不冒充 D1 计划。Author 先充分读取真实来源，区分要求、已有规范性设计、建议、实现证据和历史；无法取得必要来源时说明缺口并沿原澄清路线。不能通过省略条件或把技术细化当需求改变来制造通过。

`R154-01..05 / BEH154-01..05` 保持。Task PRD 陈述整体要求；Delivery PRD 陈述本批目标、起点、前序事实、依赖及剩余责任。design 展开真实职责、契约、行为、条件、失败、兼容、来源承诺处置和可验证设计；唯一逐项规范性来源设计处置只在 design 维护。implement 明确有依赖顺序、验证、停止/恢复、唯一 Delivery Policy 与唯一 Docs SSOT Plan。full、partial、后续和返工均保留整体与本批区别；已有 detailed 承诺不能缩成标题或链接。章节、适用字段、裁剪和深度由 Author 的现行 planning-body/templates 定义。

Planning 在实质 solution 写入前先取得真实 candidate 的独立 Architecture assessment；Author 消费实际结果完成方案。最终文档由Architecture final_plan和Approval依次审核；Author在原写作和自检中承担完整语义责任，独立Wording不再是当前前置。无真实 candidate 不产生候选通过。Architecture/Approval 不代写 Author 正文；Brainstorm 仅在原 owner 之下复用方法。Approval 的当前正式结果交原 Activation；文件存在或 public phase 不是批准。

原 `guru-activate-delivery` 读取三份当前中文规划、明确切片及相邻 Approval 实际 freshness，完成当前计划展示/接受边界后，唯一使用公共 planning writer 记录真实 Planning 结果。调用方不能从文件重算 token 冒充 Approval。恢复读回同 operation/result，不重复公共写入；真实计划变化回最早受影响 Planning owner。授权仅存在会话，不写入任何 artifact。

## R679：明确接收会话、首失败与文档展示

**R679-01 / BEH679-RECEIVE**：主会话承接创建结果或独立审核会话接收明确 TaskId/generation、DeliveryKey 和 planning_root 后，普通执行接收先核接收者自己的身份、唯一 checkout 与公共 current。存在 context 而缺 Task 绑定时，经原 Identity/Ensure/Bind 恢复该明确对象；同 Task 缺选择时，经原 Creation Selection 选择明确的非终态切片。匹配事实复核复用，不重复写；恢复后重读 key、generation、phase、scope、root，并回原未完 profile/purpose。已有 Planning 不重跑初始 Author，必要前序缺失或过期回原 producer。新绑定不是切片选择，也不是阶段通过。真正无 context 沿原 explicit-task 校验。独立 Architecture final_plan 使用下述 R694-01 的只读对象入口；其他入口不用显式 key 隐藏有 context 的缺失、冲突或错误。

**R679-02 / BEH679-FIRST-FAILURE**：接收调用区分 no_current_task、no_current_delivery、current、terminal_delivery、error，以及不同选择和真实 generation/phase/scope 失配。诊断指出本次首先失败条件与原 owner；恢复后再读其余条件。不同合法选择不覆盖，终态不重开，损坏/不可读/API不支持或 checkout 歧义不当作缺绑定。原 Author/Architecture planning 校验保拒绝强度、错误 code 和出口形状，细化具体 field_path/remediation；早于 Delivery guard 的真实 API 错误也保留。精确诊断与 matching 迁移见原 package 及 MIGRATION-679，不新增状态模型。

**R679-03 / BEH679-STANDALONE**：standalone_request 是来源 profile，执行 mode 独立。Readiness 使用真实Clarify producer请求身份、mode及当前源内容身份，调用方定位可不同；源title/body identity与Clarify semantic identity分开，沿当前后继合同绑定完整draft authority。旧Wording recipe只保其固定provider的历史含义，不是当前reader。普通消费者构造错误后，当前 Agent 重读未改 source/适用 producer，完整重建 consumer 并重审自身十维，再消费原 record/check/invoke 的真实结果。不得只补字段、改 producer、手写派生 linkage 或 receipt；真实 source/authority 或前序变化回原 producer。精确字段和可执行 recipe 仍由原 Readiness package 单写。

**R679-04 / BEH679-ARTIFACTS**：明确选定 Delivery 的展示把真实完整 key 传原 resolver，展示实际 planning_root 中存在的文档。尚无或无当前 Delivery 的 Task-only 停点，只展示该精确 TaskRef 内存在的整体根 PRD，不猜选、构造 key 或创建空切片。Finish 后明确切片使用实际 archive TaskRef/key。实际 resolver 调用和正常缺文件行为须验证，文本一致只证明分发。

上述行为保持 R531/R657 的 Task/Delivery 公共模型、单 writer 与原义务，Architecture first-read/独立性和适用结果保持。不能修改 context 环境借用别的会话，不能从 inventory 唯一项或 phase/文件推导身份与 pass。对应职责见 D679-01..04，验证见 T679-01..06；本批来源与窄补充边界见 [#679 追踪](../../requirements-design-test-contributions/679-session-continuation/traceability.md)。

## R850-03 / BEH850-PLANNING：默认退出与同切片修订

Author完成完整规划和自检后，独立Architecture final_plan直接进入Approval，candidate_assessment仍先于实质solution。Approval亲自判断可实施性，缺口交原Author返工，不继承上游通过。原content_changed由Author delivery_content_revision读真实change_refs和当前文档，在同Task/Delivery修订；等义只刷新直接依赖，需求/机制/Architecture/验收实质变化回最早owner。保scope/key/phase/selection和适用结果，不清空规划、不重建身份、不首次激活；固定旧操作按原provider恢复后匹配采用。对应D850-03/T850-03。
