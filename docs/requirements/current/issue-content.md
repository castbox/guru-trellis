# Issue 内容的需求责任

#819由原RDT owner在完整实施和真实工程结果后完成final_integration并读回；状态为integrated_pending_review，尚待TaskCommit及独立committed Review。固定before=4f2adef1f7b099f78bb8429e8b8facd66dce3bfc，来源与替代边界见[#819追踪](../../requirements-design-test-contributions/819-issue-review-intake/traceability.md)。以下旧观察保其原截止；本轮实际结果由[#819 Test](../../requirements-design-test-contributions/819-issue-review-intake/test.md)拥有。

Identity：`RDT-REQ-ISSUE-CONTENT`；状态：`current`。导航别名：`R153`、`BEH153`、`R153-01..05`、`BEH153-01..05`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。来源为[#153 需求来源](../../requirements-design-test-contributions/153-issue-content-ssot/requirements.md)与 [#818](https://github.com/castbox/guru-trellis/issues/818) R1–R4。

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

### R153-04 / BEH153-04：四个原 owner 的完整判断

Clarify 负责正文写作与自检；Wording 在原措辞门禁内检查完整语义并保持完整 title/body scan；Readiness 在原十维内判断完整性、独立交付单位与验收；Create Issue 在原创建门禁核对已审草稿及前序适用性，再沿原路径创建和回读。每个 owner 实际读取当前正文和必要来源，上游通过不能代替自己的判断。

局部修订的内容完整性判断覆盖完整 postimage，语言检查限本轮文本和必要上下文。普通遗漏回原受影响 owner；范围外既有缺口先说明影响，不能静默扩写或虚报完整。只读审核、讨论和查询不自动获得正文写入权。原 public I/O、typed exits、确认、freshness、刷新与恢复保持。

### R153-05 / BEH153-05：分层证明与受管采用

实际 Agent 写作/审核、机械分发、代表目标安装和外部写入回读分别提供证据。原 writer 分发完整正文、必要示例和四入口投影，既有目标由原 tools owner 保护用户内容与 Task/session，并检查 reapply、drift 和 sidecar。原 #153 的 V1–V7 和真实 GitHub 对象是该次历史观察，不成为每个后继任务的固定样本或写入义务。

## #818 的方法责任差额

### R818-01 / BEH818-01：必要性先于表达充分性

Issue 创建、修订或原审核中，原 owner 先判断新增要求、机制和验证义务是否为原始目标及实际支持场景所需，再检查表达充分性。必要性及结果与机制的区别只由唯一正文第2节定义；实现、测试、文档和旧审核不能自行授权新要求。

### R818-02 / BEH818-02：完整收敛扩张及派生义务

原写作与审核 owner 发现无依据或已排除的扩张时，按唯一正文第2节收敛该要求及其派生义务，不将其转移给后继阶段。该收敛保留原始需求明确的保护和真实兼容责任；需要真实范围选择时仍沿原 Clarify，而不是据无依据内容制造选择。

### R818-03 / BEH818-03：完整规则与独立理解

正文按唯一正文第3节组织完整规则，四原 owner 按第4、5节在各自范围独立理解并核对来源、入口和必要遗漏。规则清楚可读且仍完整时保留。识别真实入口不自动增加交付项，完成原始目标所需的适配也不能被精简删去。

### R818-04 / BEH818-04：围绕主要结果验收

Issue 验收按唯一正文第3节优先证明主要结果，并覆盖与实际后果相称的必要保护。后续实施和发布阶段保持原职责；不因本项而新增固定矩阵、评测平台或审核轮次。真实 Agent 结果与受管采用分别证明 #818 AC1、AC2，分发通过不替代行为证据。

## 关系与边界

设计责任为 `docs/design/current/issue-content.md` 的 D153-01..03 / CON153-01..03、D818-01..03 / CON818-01..03；测试责任为 `docs/test/current/issue-content.md` 的 T153-01..05、T818-01..04。[#818 双向追踪](../../requirements-design-test-contributions/818-issue-minimal-sufficiency/traceability.md)定位本次来源与实际目标。

共同审核充分性的职责保持在 [R717](../../requirements/current/review-sufficiency.md)，其规范只定位原 Issue 方法，不取得第二内容 authority。Architecture 继承 `docs/architecture/README.md / guru-trellis-architecture / active`；原独立 final_plan 为 no_architecture_impact/no_change，不产生空 Architecture contribution。没有新增 Skill、公共字段、状态或外仓运行依赖；#819 路由与完整安装/Release 矩阵不进入本能力差额。

## R819-01 / BEH819-COMMENT：最小审核评论

原Create Issue保完整草稿审核；创建并读回正式标题/正文与已审内容一致后，发布本次实际审核结论并读回，才完成创建。原Clarify在主动复审且本次发布/修订范围明确时发布或更新准确结论；局部审核不写成完整开工pass，纯只读不写评论。

两入口共用Clarify-owned一份评论正文规则。评论说明实际对象/覆盖、结论和影响开工的未决/前置，代码基线只在影响判断时说明；不要求固定模板、label、身份资格、期限、hash链或长期ledger。结果不确定时沿原owner找回同一已成功Issue/comment，不重复创建或发布。完整内容方法继续由原issue-content正文拥有，评论规则不替代它。

评论仅供原Readiness复核，当前适用性和分流由R819-02/03/04及其原owner拥有，不自动放行Task。对应D819-01、T819-01/02；#818内容方法与本次入口/评论差额分开，不追溯润色旧Issue或历史验证。
