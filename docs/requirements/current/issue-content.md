# Issue 内容的需求责任

#850由原RDT owner整合当前职责与关系，状态为integrated_pending_review，尚待TaskCommit及独立committed Review。固定前驱Git a72981db56d2070d8140b468cab3a97ae82effd3；来源、替代范围和本轮未验证边界见[本次追踪](../../requirements-design-test-contributions/850-wording-retirement/traceability.md)。旧观察保留原截止。

#819由原RDT owner在完整实施和真实工程结果后完成final_integration并读回；状态为integrated_pending_review，尚待TaskCommit及独立committed Review。固定before=4f2adef1f7b099f78bb8429e8b8facd66dce3bfc，来源与替代边界见[#819追踪](../../requirements-design-test-contributions/819-issue-review-intake/traceability.md)。以下旧观察保其原截止；本轮实际结果由[#819 Test](../../requirements-design-test-contributions/819-issue-review-intake/test.md)拥有。

#880由原RDT owner在真实 Agent eval、分发和本 checkout 工具采用后完成整合与读回；状态为`integrated_pending_review`，尚待TaskCommit及独立committed Review。固定前驱 Git `76198a53b4da989b66d2e5f135ff4d2b703ca3cf`；来源与工程边界见[#880追踪](../../requirements-design-test-contributions/880-issue-responsibility-acceptance/traceability.md)。

Identity：`RDT-REQ-ISSUE-CONTENT`；状态：`current`。导航别名：`R153`、`BEH153`、`R153-01..05`、`BEH153-01..05`、`R880`、`BEH880`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。来源为[#153 需求来源](../../requirements-design-test-contributions/153-issue-content-ssot/requirements.md)、[#818](https://github.com/castbox/guru-trellis/issues/818) R1–R4及[#880](https://github.com/castbox/guru-trellis/issues/880) R1–R7。

本单元由原 RDT owner 在 #818 批准 Planning、实际实现及工程结果完成后，于 `codex/818-issue-minimal-sufficiency` 的 final_integration 实际整合。整合前重读真实目标、适用来源及必要关系，写后逐项 readback；整合状态为 `integrated_pending_review`，尚待 TaskCommit 与独立 committed Review。该事实不产生 Check/Review pass 或 Task Completion。原基线为 Git `fd0ee32618433a92ae934e29afb5b72e7136b4f7`；本次来源及精确替代范围见 [#818 贡献](../../requirements-design-test-contributions/818-issue-minimal-sufficiency/traceability.md)，普通当前读取无需拼接提案。

## 适用来源、唯一正文与历史边界

适用基线为 Git `fd0ee32618433a92ae934e29afb5b72e7136b4f7`，repository authority 为 `guru-trellis-rdt / active`，发现合同为 `knowledge-navigation-1`。完整内容方法由 [canonical Issue 内容规范](../../../trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md)单写。本单元拥有能力责任、条件和 R/D/T 关系，不复制该方法。运行者读取完整 matching provider 的安装正文及其必要来源，不能用知识导航代替加载。

本次迁移只承接 `.109` [需求入口](../../requirements/versions/current-main-0.6.17-guru.109/requirement-main.md)所连接的 R153-01..05 / BEH153-01..05 Issue 内容责任，并增加 R818-01..04 / BEH818-01..04。本轮 final_integration 后，本单元承担该能力的当前完整定义；旧 `.109` 保留其固定历史及未迁移范围的读取。`.109` 对 `.108` 的其他继承、其他能力、固定旧阶段读取及 #153 原始贡献/结果均保持原义。历史内容不因本次迁移获得 #818 的实现或验证结论。

## 既有能力与条件

### R153-01 / BEH153-01：基于真实入口确定差额

修改 Issue 写作能力前，原 owner 调查现有入口与可查仓库事实，复用已经正确工作的能力。调查结果只界定真实差额，不把某次草稿通过解释为不存在其他遗漏，也不以新规范为由重做原 scanner、executor 或恢复机制。

### R153-02 / BEH153-02：来源与最终正文

创建或完善请求进入原 Clarify 后，Clarify 读取完整当前来源及必要条件，保留仍有效承诺并整合本轮明确变化和必要评论。最终正文承担本 Issue 的行为、条件和验收；建议、历史和候选保持各自来源角色。真实范围选择仍归原 Clarify，技术细化仍归原规划 owner，不能以整理正文改变职责。

### R153-03 / BEH153-03：创建和修订共用内容 authority

创建与修订共用唯一 Issue 内容规范。适用内容、复杂度裁剪、来源规则及清晰写作规范按该正文加载，不另造格式或语言权威。规范缺失时暂停依赖判断，沿原安装或原 owner 恢复并完整读取后继续；无需新增审批。简单完整正文无需为形式重写，历史 Issue 不追溯润色。

### R153-04 / BEH153-04：原内容 owner 的完整判断

Clarify 负责正文写作与自检；独立 Wording 及其 scanner 已退出当前链，不增加替代语言关卡；Clarify 在原范围内亲自判断含义、完整条件和义务强度；Readiness 在原十维内判断完整性、独立交付单位与验收；Create Issue 在原创建门禁核对已审草稿及前序适用性，再沿原路径创建和回读。每个 owner 实际读取当前正文和必要来源，上游通过不能代替自己的判断。

局部修订的内容完整性判断覆盖完整 postimage，语言检查限本轮文本和必要上下文。普通遗漏回原受影响 owner；范围外既有缺口先说明影响，不能静默扩写或虚报完整。只读审核、讨论和查询不自动获得正文写入权。原 public I/O、typed exits、确认、freshness、刷新与恢复保持。

### R153-05 / BEH153-05：分层证明与受管采用

实际 Agent 写作/审核、机械分发、代表目标安装和外部写入回读分别提供证据。原 writer 分发完整正文、必要示例和当前内容入口投影，既有目标由原 tools owner 保护用户内容与 Task/session，并检查 reapply、drift 和 sidecar。原 #153 的 V1–V7 和真实 GitHub 对象是该次历史观察，不成为每个后继任务的固定样本或写入义务。

## #818 的方法责任差额

### R818-01 / BEH818-01：必要性先于表达充分性

Issue 创建、修订或原审核中，原 owner 先判断新增要求、机制和验证义务是否为原始目标及实际支持场景所需，再检查表达充分性。必要性及结果与机制的区别只由唯一正文第2节定义；实现、测试、文档和旧审核不能自行授权新要求。

### R818-02 / BEH818-02：完整收敛扩张及派生义务

原写作与审核 owner 发现无依据或已排除的扩张时，按唯一正文第2节收敛该要求及其派生义务，不将其转移给后继阶段。该收敛保留原始需求明确的保护和真实兼容责任；需要真实范围选择时仍沿原 Clarify，而不是据无依据内容制造选择。

### R818-03 / BEH818-03：完整规则与独立理解

正文按唯一正文第3节组织完整规则，各原内容 owner 按第4、5节在各自范围独立理解并核对来源、入口和必要遗漏。规则清楚可读且仍完整时保留。识别真实入口不自动增加交付项，完成原始目标所需的适配也不能被精简删去。

### R818-04 / BEH818-04：围绕主要结果验收

Issue 验收按唯一正文第3节优先证明主要结果，并覆盖与实际后果相称的必要保护。后续实施和发布阶段保持原职责；不因本项而新增固定矩阵、评测平台或审核轮次。真实 Agent 结果与受管采用分别证明 #818 AC1、AC2，分发通过不替代行为证据。

## 关系与边界

设计责任为 `docs/design/current/issue-content.md` 的 D153-01..03 / CON153-01..03、D818-01..03 / CON818-01..03、D880-01..04 / CON880；测试责任为 `docs/test/current/issue-content.md` 的 T153-01..05、T818-01..04、T880-01..05。[#818 双向追踪](../../requirements-design-test-contributions/818-issue-minimal-sufficiency/traceability.md)和[#880追踪](../../requirements-design-test-contributions/880-issue-responsibility-acceptance/traceability.md)定位各次来源与实际目标。

共同审核充分性的职责保持在 [R717](../../requirements/current/review-sufficiency.md)，其规范只定位原 Issue 方法，不取得第二内容 authority。Architecture 继承 `docs/architecture/README.md / guru-trellis-architecture / active`；#818的原独立 final_plan 为 no_architecture_impact/no_change，不产生空 Architecture contribution。#818当次没有新增Skill、公共字段、状态或外仓运行依赖，也未承接#819路由或完整安装/Release矩阵。#850的当前路由及合同差额分别由R850和对应D/T承接，不改变该历史结论。

## R819-01 / BEH819-COMMENT：最小审核评论

原Create Issue保完整草稿审核；创建并读回正式标题/正文与已审内容一致后，发布本次实际审核结论并读回，才完成创建。原Clarify在主动复审且本次发布/修订范围明确时发布或更新准确结论；局部审核不写成完整开工pass，纯只读不写评论。

两入口共用Clarify-owned一份评论正文规则。评论说明实际对象/覆盖、结论和影响开工的未决/前置，代码基线只在影响判断时说明；不要求固定模板、label、身份资格、期限、hash链或长期ledger。结果不确定时沿原owner找回同一已成功Issue/comment，不重复创建或发布。完整内容方法继续由原issue-content正文拥有，评论规则不替代它。

评论仅供原Readiness复核，当前适用性和分流由R819-02/03/04及其原owner拥有，不自动放行Task。对应D819-01、T819-01/02；#818内容方法与本次入口/评论差额分开，不追溯润色旧Issue或历史验证。

## R850-01 / BEH850-CONTENT：原语义责任与显式只读

完整Intake由Discovery到Clarify，直接进入Readiness。原内容owner亲自保留来源含义、完整条件、义务强度、例外和可观察验收；独立Wording退出不削弱原门禁，也不新增替代语言gate、scanner或词表分类。

明确Issue/draft措辞请求由原Clarify standalone_wording_review只读完成，不要求Task/Delivery/session、完整Intake或ready。明确Markdown请求由原review-change explicit_files/wording_only读取全部选定当前正文，包括Git未变文件。报告具体位置、影响和原修订owner；必要来源缺失时blocked。合法建议、默认、引用、历史和literal不因词面阻塞。审核不授权正文修订、评论或发布。对应D850-01/T850-01。原range code review完整方法保持，有界结论不替代实现完整度判断。

## R850-04 / BEH850-ADOPTION：完整迁移与分层证明

当前producer/consumer、profile、schema及在途按匹配版本切换。固定旧provider已开始的副作用由原完整provider恢复同一操作后再更新，旧结果不改标签为新通过。原installer退役未改managed资产，用户修改/sidecar保原owner处理；Task/Delivery/scope/阶段/规划/session/配置/peer保持。源码、机械检查、实际Agent、目标安装与外部效果分层证明。真实不足保持未验证，local_candidate不证明formal_fork_source_lock或完整Release矩阵。对应D850-04/T850-04，历史原结果保其截止。

## #868 本次整合与关系

原RDT owner在批准规划、实际实现及真实工程结果后，于固定前驱Git `b85ea7bdf80db97ba8aceb1298dd61ed5f1ebeec` 的Task隔离checkout完成final_integration和读回。状态为`integrated_pending_review`，尚待TaskCommit及独立committed Review；不产生质量或Completion通过。来源和替代范围见[#868追踪](../../requirements-design-test-contributions/868-issue-acceptance-boundary/traceability.md)。既有来源、完整条件及旧观察截止保持。

## R868-01 / BEH868-BOUNDARY：Issue结果与边界

原Clarify从有效来源确定目标、消费者、自身可独立交付及验证的边界，再在边界内最外沿有效切面表达必要结果。API、CLI、workflow、文档、代码、配置、协议或数据状态均为合法交付。候选分成结果、支撑证据和无依据扩张；能映射目标不证明有独立验收价值。删除后不影响必要承诺判断的条目合并或删除，不固定条数、一目标一条或多义务挤一条。必要失败、安全、兼容和规范性技术承诺仍保留。唯一内容方法由Clarify-owned issue-content承载，跨阶段验证只引用原quality-guidelines。对应D868-01、T868-01。

## R868-02 / BEH868-PREWRITE：所有创建入口首次写前

受支持Agent创建入口不因Task、阶段、Issue-only或草稿来源豁免。原Clarify、Readiness和Create Issue在各自门禁实际判断最终完整正文；上游通过、现成草稿与创建意图不能替代。未合理精简先沿原owner回程，修订通过前不创建，不先创建后补救。实质变化刷新直接受影响判断，执行器仍原文提交；成功后的输出丢失恢复原对象。对应D868-01/02、T868-01/02/04。

## R868-03 / BEH868-CONTINUING：每轮审核及正文写回

所有相关原写作/审核owner在本轮输出前按共同验证方法判断拟新增、恢复或强化义务；无依据或重复候选不能成为Finding、风险、返工、依赖、强制follow-up或gate，不改名或转移。每次写回前核完整postimage及受影响安排。模式、阶段、换Agent或恢复会话不豁免；真实原范围缺陷与失效证据仍定向修复，真正范围变化回Clarify。对应D868-02、T868-02。

跨阶段R868-04/BEH868-EVIDENCE由[原验证方法单元](behavior-validation-method.md)拥有；本单元不另立方法。对应[D868-01/02](../../design/current/issue-content.md)、[T868-01/02/04](../../test/current/issue-content.md)。

## R880-01 / BEH880-RESPONSIBILITY：责任层可组合

Issue 根据有效需求、实际消费者和自身承诺，判断可观察结果覆盖哪些必要责任层。组件或服务合同、调用方或界面合同、跨组件业务结果以及发布或环境结果可以组合，不能按标题词强制唯一分类。组件责任不自动包含调用方接入、整站联调或整体部署；调用方责任不能以替身成功冒充被调用组件或完整链路通过。

## R880-02 / BEH880-NECESSARY：必要承诺不得误删

有效需求明确要求真实联调、共享环境或指定目标环境，或者只有该环境才能判断承诺时，Issue 保留该结果、必要环境条件和归属。最小验证不能删除这项承诺；部署、共享环境或其它外层通过也不能替代未覆盖的组件合同。

## R880-03 / BEH880-SEPARATION：结果、证据、部署与业务发布分离

验收定义 Issue 需要观察的交付结果，验证证据证明该结果，服务版本部署、共享 test 环境部署和目标环境运行验证属于相应的部署、环境或发布责任。普通 Issue 不默认逐 Issue 部署共享 test 环境；业务对象中的“发布模板”“发布配置”“同步配置”等操作不因名称自动成为服务部署。

## R880-04 / BEH880-SCENARIOS：验收场景按独立风险收敛

每个场景对应一个独立的可观察结果或风险；一个场景可以包含判断该结果所需的多个条件、输入和例外。同一行为不得因创建、复审、验证方法或阶段不同拆成多个重复场景。补充测试方法、工程检查或一致性验证不自动成为新的行为场景；其他入口或阶段只在存在必要差异时增加场景。

## R880-05 / BEH880-OWNERS：原创建与审核职责落实

Clarify、Readiness 和 Create Issue 继续消费同一共享内容正文，并在各自原门禁检查完整标题、正文和验收。普通内容缺口返回原 writer；评论、上游通过、现成草稿或创建意图不能替代最终正文判断。该责任不新增平行 writer、审批阶段或公共 I/O。

## R880-06 / BEH880-DISTRIBUTION：单一来源与受管采用

Issue 结果、证据、责任层与场景集合规则由 `issue-content.md` 单写；跨阶段验证责任、证据去重与复用继续由 `quality-guidelines.md#test-and-validation-value` 单写。原 owner 只补必要引用或检查，不复制第二套正文。受影响 RDT/current、canonical、dogfood、声明平台和安装投影沿原 owner 同步。

## R880-07 / BEH880-VERIFY：分层验证

真实 Agent 行为观察复用现有 Issue 内容 eval／fixture 和原 Clarify／Readiness 入口。固定文本、引用存在、评论存在、分发成功或脚本通过不能替代行为判断。行为、工程、分发和本目标采用分别报告；不要求完整多平台 Release 矩阵、其他业务仓库采用或逐 Issue 部署共享环境。对应 D880-01..04、T880-01..05。
