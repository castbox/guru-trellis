# #850 设计完整差额

状态：integrated_pending_review。固定前驱为Git `a72981db56d2070d8140b468cab3a97ae82effd3` 的同名current单元。原语义owner为guru-maintain-requirements-design-test-ssot；以下是已写入并读回的完整变更章节/稳定单元，其余正文及历史观察保持。关联来源及替代范围见traceability.md；精确API仍由canonical packages与MIGRATION-850单写。

# 完整整合目标：docs/design/current/issue-content.md

## 来源、适用性与替代范围

适用基线为 Git `fd0ee32618433a92ae934e29afb5b72e7136b4f7`。需求关系为 `docs/requirements/current/issue-content.md` 的 R153/BEH153 与 R818/BEH818。本单元只承接 `.109` 设计入口所连接的 D153-01..03 / CON153-01..03 Issue 内容设计，不迁移 `.109` 对前驱的其他继承，不改历史 ADR、贡献或原验证结果。新要求的设计差额由下列 D818 身份承接。

原 Architecture 独立 final_plan 为 `baseline_current / no_architecture_impact / no_change`，公开 authority 为 `docs/architecture/README.md / guru-trellis-architecture / active`。#818当次设计沿既有owner、Markdown控制面与受管分发，没有新的运行依赖、数据状态或public I/O，当次未制造Architecture contribution或ADR。#850的真实合同与Architecture差额由其原owners另行承接，不继承这项历史no-impact结论。

## D153-02 / CON153-02：原入口执行及写入边界

Clarify、Readiness、Create Issue 的当前 SKILL 与适用合同完整加载同一内容正文，并在各自原门禁内使用。方法只通过必要薄引用承接，完整定义仍在 D153-01 的正文。独立 Wording 包、scanner、词表分类和专属回执退出；原内容 owner 亲自判断完整当前标题/正文与必要来源，不以词命中代替判断。Readiness 保留原十维，Create Issue 核对已审内容而不变成第二 writer。

草稿更新、已有正文修订、真实创建和只读请求各沿原动作、确认、live reread、刷新及重审路径。内容缺口不自行授权写入。原#153/#818当次没有新Skill、审核节点、typed exit、schema或最小DTO差额；#850当前后继合同由D850及MIGRATION-850承接，不把历史结论扩成当前无差额。对应 R153-02/04/05、R818-01..04；由 T153-02/03 和 T818-01/02 观察。

## D153-03 / CON153-03：受管分发及现有目标采用

既有递归 package/preset writer 分发完整正文、必要示例、当前入口及适用合同；受影响 managed spec 沿原机制安装。定向 fixture 实际执行 writer/reapply，核声明平台字节、引用、用户保留和 sidecar。正式 Task checkout 使用完整 matching source 的原 `guru-upgrade-tools`，按其 preview、审查、prepare、invoke 和 readback 更新，保留 Task/session 与用户内容。原管理机制处理冲突，禁止手抄受管副本。

源码、实际目标安装及 Agent 行为分别证明本层结果。`local_candidate` 不能建立 `formal_fork_source_lock`、其他业务仓采用或完整升级/Release 矩阵。对应 R153-03/05、R818-04；由 T153-04/05 和 T818-03/04 观察。

## D818-01 / CON818-01：原完整段落内修改方法

#818 在唯一正文原第2节修改整理与必要性判断，在第3节承接完整规则及验收，在第4节承接独立阅读与反查，在第5节定位当时四个原职责；历史含义保持，当前职责由R850/D850承接独立Wording退役。采用直接修改及薄引用，使一个 consumer 仍只需读取一份完整方法。原来源保留、局部完整性和必要保护继续有效；不以叠加摘要、平行准入流程或语义脚本承接方法。

该选择服务 R818-01..04，复用 T818-01/02 的原入口观察。后续若真实改变 owner、状态、I/O 或依赖，须回最早受影响的原 owner，本单元不预留另一机制。

## D850-01 / CON850-CONTENT：源身份及有界入口

单一纯函数runtime/content_identity.py::title_body_identity计算源标题/正文组合身份，供Clarify、Readiness及Create对应组合项复用。源身份与Clarify semantic identity分开；原owner读取真实对象，recorder/checker只校验客观绑定，不保存完整快照或把token当语义authority。

Clarify standalone_wording_review消费完整当前Issue/draft与必要来源，reviewed/blocked止于用户答复。review-change explicit_files/wording_only捕获选定完整bytes/mode，AI审核后以同snapshot验证连续性，未变文件也进入捕获。两入口不建Task/绑定、不改正文或报告；修订归原writer。对应R850-01/T850-01。

## D850-04 / CON850-ADOPTION：匹配分发与历史退出

MIGRATION-850单写前代path/id保留、后继版本及当前consumer映射，旧schema存在不激活双读。原tools owner以完整matching source执行preview/prepare/invoke/readback/reapply，不手抄managed副本或改manifest隐藏差额。原managed removal退役包/命令/wrappers；resolver、installed/native、平台bytes/mode、sidecar与Task/session/peer分别读回。不增加状态模型、collector或授权持久化；安装不等于业务完成或Review pass。对应R850-04/T850-04。

# 完整整合目标：docs/design/current/local-fix-intake.md

## D692-01 / CON692-OWNERS：保留调用图，在原 owner 内减少重复

selector依据实际行为影响选择原route。Create Issue完成D819-01正式内容/评论读回后，仅创建在created结束；还要开工则交原Sync，再由D819-02 Readiness先行。必要完整链中的Discovery仍核新身份、完整live正文、当前base及事实差额，并亲自完成适用duplicate/history和充分性；D819-03局部调查只补真实指明缺口并回同次Readiness。两者都不重复广搜仍适用完整内容，created不携带调查缓存。

普通完整链Clarify使用当前Discovery public output；局部Clarify采用D819-03真实缺口/返回合同。两者都读可核验完整来源，自行判断intent、role、disposition、scope，不借读producer私有结果，不重复询问证据已回答的问题。Author 依现有模板区分整体要求、本批要求、design 与 implement，复用已接受定义的必要引用，完成当前正文责任；来源处置仅在 design 唯一位置维护。Author完成方案后，由独立 Architecture final_plan、Approval、展示接受与 Activation 依次承接，各阶段仍作自己的判断。真实事实失效回原 producer/最早 owner；同源普通装配恢复不新增确认。

事实复用仍在原step-local Markdown完成，不新增恢复层、跨Skill capsule或统一缓存。#819已按其实际规划改变已有Issue入口、局部public I/O及评论恢复；这些新责任由D819单写，不能把原#692的固定调用图当作新profile的前置。其余调用图/接口变化仍回原规划及迁移合同。

## D819-02 / CON819-READINESS：原owner先行与逐出口

原workflow在Sync后薄路由：明确已有Issue进入原Readiness的existing_issue_intake，其他标准对象/原confirmation保原入口。Readiness拥有完整当前覆盖、变化影响、前置与路线的semantic判断；record/check/invoke只绑定原对象/来源/实际结论。ready仍只交原Task intake router；事实补审及带review_focus的需求/措辞补审、必要完整链、基线刷新和blocked各有唯一consumer。

新来源DTO保kind/selected_ref/commit。read复制真实git_object来源；实际sync将selected_base/decision_head归一为synced_branch，不从read或本地HEAD猜provenance。精确规格由canonical包及MIGRATION-819单写。对应R819-02和T819-03/04。

## D819-03 / CON819-SUPPLEMENT：原profile与同次回判

Discovery、Clarify分别拥有issue_readiness_supplement输入与真实结果；Clarify以review_focus=requirements|wording_only限定本次判断，不新增owner。局部前置由仍适用审核和本轮事实满足，不用旧完整链transition替代。supplemented结果仅携必要对象、来源、continuation及该次结果/来源摘要，回Readiness的issue_review_return；来源kind和精确对象不丢失、不重解成集成branch。

Clarify需要上下文沿原needs_context/context_request/context_ready回原局部Clarify；结束才交Readiness。Clarify wording_only亲自读取完整当前标题/正文及必要来源，判断具体歧义、条件与保义，不执行词表或scan；真实需求变化回Readiness的requirements分支。各次Readiness重判必要后续，不让局部成功落入普通默认全链。缺必要真实结果回原producer，不建coverage缓存。对应R819-03和T819-03/04。

## D819-04 / CON819-BOUNDARY：消费、刷新与迁移

新ready向原Create Task当前profile2.0/共享creation3.0投影reviewed_base_source；Task集成selected_base_ref、未来delivery_target和原Issue disposition仍由原owner分别审定。精确来源commit与acquisition.decision_head等值；synced来源branch身份检查为新建/恢复共用，新建额外核local HEAD，已成功恢复不因后来ref前进失效。固定对象read不要求local main等于旧commit或primary clean。

必要全链继续消费真实Sync transition，不从最小三字段反拼摘要或前序。缺调用期结果恢复原读取/同步事实；真实基线失效由原Sync产生新事实后回判。讨论/草稿/只创建/创建并开工/no_issue保R819-04终点及全部Task后续门禁。

MIGRATION-819记录#819当次七包、workflow/graph、schema/Interface/consumer/examples及受管投影的历史迁移；#850当前后继合同与独立Wording退役由MIGRATION-850承接；原工具owner保Task/session、用户内容、mode和sidecar。旧Creation固定provider恢复沿MIGRATION-813，不转换旧pass、不重复对象、不新增长期dual-reader。对应R819-04和T819-04/05；原owner整合/readback后仍待TaskCommit及独立committed Review。

## D850-02 / CON850-LOCAL：原 owner 薄回程

Readiness拥有覆盖、gap/focus和route判断；supplement_requirements后继到Clarify保同Issue/source/continuation，Clarify以requirements|wording_only执行适用方法。必要Discovery local context-request/ready保focus再回同Clarify。真实supplemented到issue_review_return仅薄投影result_summary为requirements_result，保source_refs/source_selection；旧wording_result不进入当前return。source/内容变化回最早owner，不改hash/state续旧pass，不增独立措辞owner或缓存。对应R850-02/T850-02。

# 完整整合目标：docs/design/current/task-delivery-lifecycle.md

## Creation 与 Author/Activation

`D531-02` 承接 `D292` 的唯一 writer 分工。Creation 从 Task 整体 accepted scope、历史切片与未分配范围判断本 slice，执行明确 create/select，仅分配稳定 Delivery 身份和 public planning_root。create/select 输出丢失由同 owner 以相同 operation/UUID 恢复；新的空切片不能掩盖旧身份。无 context 只在原明确 key 的合法公共校验条件下使用调用期关系，有 context 则必须符合实际 current，不用 fallback 隐藏 stale/冲突。

唯一 Author 写四种实际正文（Task PRD、Delivery PRD/design/implement）及本切片 manifests。`D154-01/02 / CON154-01/02` 拥有 source-sufficiency 调查、内容深度和来源承诺处置；详规由 [planning-body](../../../trellis/skills/guru-team/packages/guru-author-task-plan/references/planning-body.md) 及该 package templates 单写。RDT 当前正文不复制模板。每个承诺的 retain/refine/replace/defer/reject 处置在 design 唯一位置明确，技术展开不改变 source 目标。Policy/Docs Plan 同样只在 implement 唯一位置拥有。

Architecture 候选评估先于 Author 实质 solution；Author完成当前方案后，原Architecture final_plan紧邻Approval。Author负责正文和自检；Architecture/Approval亲自判断、不代写文档，也不索取Wording-current事实。Activation 独占公共 planning role，消费真实 approved DTO 的局部 freshness，调用公共 record_gate 产生新的 planning-accepted result。该 receipt 交 implementation及合并Review的check predecessor；Approval freshness 不成为公共 Gate result identity 或跨阶段 authority。

`D657-01/02 / CON657-ADMISSION/SELECTION`：初始 Task Creation checked created 只服务原创建区间；既有续接通过原身份/绑定/checkout owner 后，实际阶段 owner 承担写入资格。Delivery created wire 不变，原 workflow consumer 读取公共 current phase 和实际未完成义务后按唯一 continuation 进入原 owner；Planning 只有初始需求义务才进入 initial Author，已有工作恢复适用 Author/Architecture/Approval，当前 approved 进入 Activation。query 只提供客观可用性，scope/gate 充分性仍由原语义 owner判断；不新增 phase cache、router Skill、DTO 或状态 authority。初始创建精确 validator 不放宽。

## D679：接收者前置事实与原 owner 接续

**D679-01 / CON679-RECEIVE** 承接 R679-01。普通执行的原 workflow created consumers、唯一 continuation 与 Planning 编排显式调用原 Identity/Ensure，然后按接收者自身事实进入原 Bind 和 Selection。当前各 Planning Skills 在自己的 entry 中核相同前置；Architecture 在原 baseline-first 之后按 purpose 核接收事实；final_plan 按 D694-01 只读核对象，其他 purpose 保原恢复。workflow 只拥有跨 Skill 顺序，step-local Skills 仍拥有内部判断和写入。adapter.current 的有 context / 无 context 边界不变，不新增绑定 writer、wrapper、状态或全局映射。

**D679-02 / CON679-DIAGNOSTIC** 承接 R679-02。Author/Architecture 原 planning guard 按公共 kind、selected key、generation、phase、scope 顺序检查；更早的 resolve/API 首失败保原具体条件。外层 stale_identity/出口不变，session.task、session.delivery、delivery.phase、current.error/current.kind/current.key、delivery_key.lifecycle_generation 和 delivery.scope_ref.authority 定位实际条件。runtime 只报客观事实，不 bind/select 或决定语义 route。Approval/Activation 保原 guard，由明确 caller 接续承担补缺与错误分流。

**D679-03 / CON679-PROJECTION** 承接 R679-03。当前Readiness recipe从真实Clarify transition投影locator/mode/continuation及源内容身份，standalone请求身份与source对齐，caller locator保自己的合法值。前驱Wording recipe保持固定旧provider的历史含义，不作当前fallback。normalization 保持；原 recorder 派生、checker receipt 和正式 invoke 唯一出口承接。原 native runner 从实际 public profile 选择提示，不替 Agent 构造身份、判断通过或修复 consumer。

**D679-04 / CON679-PRESENTATION** 承接 R679-04。Human artifacts 调用方提供真实 TaskRef/key；原 Approval package-owned resolver 继续解析精确切片。Task-only 直接检查精确根 PRD；archive 使用实际归档 ref/key。原命中测试执行文档 argv 并观察实际路径/缺文件/不创建与不选择，而非仅断言字符串。

原#679当次不改公共schema/typed exits/phase/helper参数，不新增兼容双读或Architecture authority；当次workflow、五Planning packages、Readiness与直接consumers成套采用，历史诊断迁移见MIGRATION-679。#850当前后继与退役包退出改由MIGRATION-850及原packages定义，不保留五包作为当前安装前置。历史归档不为工具安装转换；含旧数据的 checkout 沿原 tools-only owner维护工具，普通preset检查继续严格。RDT完整拟写先原final_integration/readback及TaskCommit，再完整committed candidate和一次独立质量链；source/package、installed、Agent 及外部采用分别证明。

## D850-03 / CON850-PLANNING：原 writer 与直接 consumer

Author requirements_ready经candidate assessment回solution_planning，plan_ready直接交Architecture final_plan，其实际结果紧邻Approval；默认链无Wording/receipt。Approval修订薄投影真实revision_actions到Author，由原owner按实际修订出口刷新依赖，不由脚本选择等义或实质route。delivery_content_revision承接原wording reentry的内容修订，保同Delivery/change_refs，不恢复退役字段/reader。原Activation、TaskCommit、committed Candidate及一次独立Check/fullReview顺序保持；token不作跨阶段批准或授权。精确版本由packages/MIGRATION-850单写。对应R850-03/T850-03。
