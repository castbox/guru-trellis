# D1 Issue 验收边界与持续去重设计

## 1. 设计目标、需求承接与内容基线

本设计承接本批 PRD 的 D1-S1–S4、D1-AC1/AC2 及整体 R1–R7。开发基线 B 固定为 `b85ea7bdf80db97ba8aceb1298dd61ed5f1ebeec`（创建时 main）；Planning H0 同 B，只是起点观察。最终内容范围为完整 B..最终 TaskCommit HEAD 加实际内容增量，不能以选定文件遗漏同范围内容。交付目标独立选择 `castbox/guru-trellis:main`。

真实独立 Architecture candidate_assessment 已返回 `baseline_current / no_architecture_impact`，baseline=`guru-trellis-architecture`、constitution=`guru-trellis-design-constitution-v1/current`，change-contract=`guru-trellis-architecture-change-contract-v1`。候选保持原 owner、public I/O、状态与分发边界，无需 Architecture contribution/ADR；该结果仅覆盖预写候选，完整设计仍须独立 final_plan，不据此预填实现或最终审核通过。

## 2. 当前系统、边界与目标差额

D1 无前序。当前 Clarify-owned `issue-content.md` 已有来源保留、必要性和主目标优先；Readiness 十维与 Create Issue 原创建门禁已消费它。workflow Gate 已将正常创建请求路由到原 Create Issue，不允许以手工 GitHub 路由绕过；本批先核对实际入口，现有正确路由复用，不为形式新增节点。

差额是结果／证据分类、最外沿有效切面、停止外推、写前精简及任意后续轮次去重的具体方法。目标是原 Agent 在原语义步骤完成这些判断，不改创建执行器的原文字节语义，不增加评分、状态、字段、wrapper 或脚本自然语言分类器。

## 3. 来源设计处置（唯一）

来源均为 [#868](https://github.com/castbox/guru-trellis/issues/868) 当前“修订范围与职责”“非目标”及相应行为要求；整体 PRD 与 implement 引用本表。

| 原承诺 | 处置 | 本设计落点、理由与影响 |
| --- | --- | --- |
| Issue 方法由 Clarify-owned issue-content 单写 | retain | 第4节修改原完整段落，目标/边界/结果/写前责任在一份正文收敛，不建第二内容规范 |
| 跨阶段验证必要性、边界、去重与复用由 quality-guidelines 原小节承载 | retain | 第4节在 Test And Validation Value 展开共用方法，review-sufficiency只定位它，不复制规则 |
| Clarify 在原整理与自检执行，不新增持久映射或证明表 | retain | 原 SKILL/合同以短引用明确执行点，判断留当前 owner，不改 recorder/schema |
| Readiness 保留十维及 clarify_requirements 回程 | retain | 原 SKILL/contract 与 existing-Issue入口只指向同一方法，缺口仍回原 Clarify |
| Create Issue 原样提交；不合规 refresh_review | retain | 原创建 Skill 在首次provider写入前完成自身语义核对，回程不变；runtime/invoke.py不增裁剪分支 |
| 所有受支持创建入口共享原 owner，Task/模式/输入来源不豁免 | retain | 第6节核实际workflow与声明平台路由，用既有正确图承接；不把步骤细节复制进launcher |
| 后续各轮及写回前禁止义务叠加，真实原范围缺陷仍可修复 | retain | 共同验证方法及共同审核加载点承接；原 owner在当前判断中区分缺陷与扩张，不增专用审核阶段 |
| 复用现有教学与 Skill eval，不建评测平台 | retain | 第8节用事实输入、真实native owner与外部独立评估；必要只扩已有fixture/staging，不加入语义判断 |
| 原工具 owner 同步受管副本并保护Task/session与用户内容 | retain | 第7节完整 matching source 的 guru-upgrade-tools；不手抄managed投影或修改manifest掩盖差额 |
| 不新增 public DTO/schema/运行状态，不执行完整安装/发布矩阵 | retain | 现有接口与退出不变，只做差额所需定向验证；local_candidate证据边界单独报告 |

没有 change/reject 的来源设计，无需新增上游范围处置。

## 4. 模块、职责与设计取舍

### 4.1 Issue 内容方法

直接修改 `trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md`：
- 在原整理流程先确定消费者与自身责任边界，形成结果候选，再分离支撑证据、删除无依据/重复义务。
- 在原内容与裁剪部分定义有效切面、技术交付和来源约束；不再将代码/内部状态观察一概排除，也不固定一目标一条。
- 在原审核／修订部分明确首次写入前和每次正文写回前的完整正文检查；各原 owner 的表只定位责任，不复制方法。
- 在原教学示例中整合一个简短去敏复合场景，原两个目标对应必要结果，测试方法和合法内部承诺有各自去向。

### 4.2 共用验证与审核方法

由 `trellis/presets/guru-team/spec/workflow/quality-guidelines.md#test-and-validation-value` 单写责任边界内的最小充分证据、禁止调用链外推、有效覆盖复用、实际缺口最小补证和每轮新增义务的必要性判断。明确它适用于各原写作/审核 owner，不因模式、阶段、换 Agent 或恢复而豁免；语义判断不产生新的逐项证明表。

`review-sufficiency.md` 在原形成覆盖和审核新增条件处薄引用该节，原 owner 按既有 mandatory loading 读取。这样可覆盖 Architecture/Approval/Check/独立/Branch/Delivery/Completion，而不逐包复制大段政策。只有真实漏接引用时才修对应入口。

### 4.3 原内容与创建 owner

对 Clarify 的 SKILL/contract、Readiness 的 SKILL/contract及必要 issue-intake、Create Issue 的 SKILL 作最小必要引用和执行点修订。原 Create Issue 必须亲自审最终正文，已有ready或创建意图不能代替，语义不合规先refresh_review；executor继续原字节提交及唯一对象恢复。

流程、preset/workflow README、overlays、.agents与Codex入口均检查实际调用关系。已正确路由的文件保持，不新增上游trellis-* overlay或把dogfood当canonical。

### 4.4 取舍与成本

采用原正文直接收敛和薄引用，运行成本为原owner必要语义判断及缺口定向验证；不增加长期状态、额外审批轮次或维护服务。相比创建器自动裁剪，保留源语义和writer职责；相比新增统一审核gate，避免重复审核与恢复链；相比只做目标映射，能识别“属于目标但仅为验证过程”的多余条目。无runtime兼容双链或新状态迁移。

## 5. 接口与数据

生产 public Skill、profile、DTO、schema、typed exit 和consumer不变。输入仍是原来源/草稿及当前事实；输出仍是现有Clarify clear/refresh、Readiness ready/clarify_requirements、Create Issue created/refresh_review等。字节/digest校验仍只证明客观一致，不证明语义。

现有 Intake native 投影缺少当前 Skill 明文要求的公开方法，须在现有 adapters/eval/intake_authoring.py、eval_support.py 及必要既有transport测试中补齐固定公开合同集合及实际字节传递；保持 evals、私有runtime和预期隔离，不扩flow回环、命令集合、schema或runner生命周期。所需方法的必要来源依赖（如Author planning-body）同样按明确public locator传递，不让缺文件假冒行为阻塞。

eval侧仅使用现有corpus、facts fixture、native adapter和独立semantic assertions；如果新增事实样本需要已有测试staging登记，只做确定性装配，不选择语义pass或改生产runtime。评测原始输出位于仓外临时run root，长期Test文档只保留有直接consumer的必要结果和未验证边界。

## 6. 顺序、正常与失败流程

1. 原 Agent 读取有效完整来源及相同provider共享规范，确定自身边界与已有覆盖。
2. Clarify 在最终草稿中保留结果及真实承诺，删除无依据/重复义务；Readiness独立按原十维复核。
3. Create Issue 在首次GitHub创建前核对当前完整待写正文及前序适用性。不合规走原refresh_review并由原writer修订，不能先发布再修。
4. 成功创建后仍沿原回读、评论和恢复合同；输出丢失恢复同一Issue，不再次创建。
5. 后续任意原审核在本轮输出前审拟新增/恢复义务；无依据或无独立价值即移除其阻塞后果。写回前核完整postimage，不让旧义务改名恢复。
6. 真实原范围缺陷或失效证据由原owner定向修复；确需范围改变仍回Clarify，已排除扩张不反复询问。

没有新增公共状态转换。普通缺来源、stale、hash mismatch和真实创建失败沿原owner恢复，不构造攻击、竞态、锁、crash或故意篡改场景。

## 7. 恢复、兼容、迁移与采用

业务恢复与public兼容沿原接口，无数据迁移或第二执行路径。公共内容方法变更通过完整matching source采用，源码修改不等于已安装环境更新。

正式Task checkout含当前Task/session，故由原 `guru-upgrade-tools` 完整preview→prepare→invoke→readback同步，不以普通apply触发历史任务迁移或手工覆盖managed副本。开发脏候选仅用原 `local_candidate`，如实保留formal_fork_source_lock未验证边界；不改版本号冒充新release。逐个处理真实.new/.bak，核受管字节/mode、目标resolver、installed/native入口、Task/session/配置及peer保持、同操作reapply和drift。只处理本任务受影响差额。

知识维护为delta_first：主会话原RDT owner先形成完整已变责任提案和追踪，真实工程验证后在TaskCommit前整合原current能力单元并readback。不登记根/current README，不复制 unchanged authority到第二current。Architecture当前no-impact不制造空贡献；若真实发现新边界变化，回原owner刷新，不能用旧结论放行。

## 8. 验证设计

| ID | 对应范围 | 入口、输入与预期观察 | 证明边界 |
| --- | --- | --- | --- |
| V1 | D1-AC1／S1-S4 | 在原Skill eval或其已有原生执行机制中让真实Agent处理两目标混合草稿、合法技术承诺、充分证据、真实遗漏与跨界E2E意见；观察完整修订、原门禁/回程与后续拒绝叠加 | 事实输入不预填语义结果或告诉被测Agent预期Finding；独立评估完整输出，不以退出码或断言数量替代 |
| V2 | D1-AC1 创建边界 | 原创建入口/门禁处理不合规与修订后完整稿，观察未通过前无首次provider写入；核普通、Issue-only、现成草稿、已有Task/阶段不同路由，等价路由复用 | 模拟provider只证明动作边界；实际GitHub对象仅在必要且明确目标时使用，不为测试制造无关工作项 |
| V3 | D1-AC2 分发 | 现有test_issue_content_distribution、test_review_sufficiency_distribution执行真实writer/reapply，覆盖受影响正文/引用、声明平台、用户内容与sidecar | 既有定向fixture已覆盖分发，不扩成多平台clean/existing/update全矩阵；不证明Agent判断 |
| V4 | D1-AC2 目标采用 | 原tools owner更新本checkout并readback，source/installed validation、dogfood drift及实际continuation，核Task/session及peer保持 | local_candidate不证明正式source lock、其他业务仓采用或release |
| V5 | 工程与交付完整性 | 实际变更相关package测试、eval discovery、JSON/bash/内存Python语法、Task context与diff检查；原知识整合后完整B..H独立Review | 采用仍适用证据，仅填实际缺口，不增加惯例层级或重复回退 |

先完成人工/原生语义和分发的独立价值观察，再据实际差额补工程检查。永久case覆盖真实回归，临时诊断回答具体未决事实即停止。达到当前AC覆盖后停止追加实验；首次失败与返修事实保留，设施故障不能充当产品缺陷或语义pass。

## 9. Canonical 引用、差额与未决项

沿PRD第7节真实current R153/R818/R819/R850、D153/D818/D819/D850、T153/T818/T819/T850及Architecture authority。此次只补本能力的R868/BEH868、D868/CON868和T868/SC868差额及必要关系，未迁移其他主题或重写旧观察。原RDT owner使用 `docs/requirements-design-test-contributions/868-issue-acceptance-boundary/` 的manifest、requirements/design/test/traceability承接任务提案和真实工程结果，在final_integration晋升。

当前无未决产品/范围问题，eval具体fixture装配和调用属于既有机制内实施细化；若需要新生产runtime、公共I/O或新增评测平台则超出本方案，先回原Author/Architecture，不自动实现。
