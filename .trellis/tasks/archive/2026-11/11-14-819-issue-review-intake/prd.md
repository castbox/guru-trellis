# #819 Issue 审核评论与开工分流整体需求

## 1. 来源与术语

| 来源 | locator / 章节 | 角色与用途 |
| --- | --- | --- |
| SRC819 | https://github.com/castbox/guru-trellis/issues/819；完整正文，updatedAt=2026-11-12T13:06:35Z，无评论 | 唯一 Direct Source。第5节完整承接其当前正文；不把旧草稿 receipts 当正式 Issue 结果。 |
| BASE819 | trellis/workflows/guru-team/workflow.md；原 Create/Clarify/Discovery/Wording/Readiness packages | 当前行为与原 owner 事实，固定 Git 4f2adef1f7b099f78bb8429e8b8facd66dce3bfc。 |
| HIST692 | .trellis/tasks/archive/2026-10/10-31-692-intake-reuse-diagnostics/prd.md；docs/{requirements,design,test}/current/local-fix-intake.md | 原事实复用与诊断边界；不重复交付其已完成部分。 |
| CONTENT818 | docs/{requirements,design,test}/current/issue-content.md | 最小充分内容与原审核职责；不重复交付内容规范。 |
| RUN819 | 本 Task 当前验证与交付范围；本节及第7节 | 完整代码交付、必要定向工程检查及原质量/收尾门禁；不再追加 live 或实际 Agent 验收。未观察部分保持未验证。 |

Readiness 是原 guru-review-change-request；Discovery、Clarify、Wording 是原调查、澄清与措辞审核。评论是供 AI 复核的依据，不是放行凭证。Task 承担整体 accepted scope；Delivery 是其中的交付切片。

## 2. 背景与问题

当前 workflow 要求 Sync 后完整 Discovery→Clarify→Wording→Readiness；Create Issue 成功后也回完整 Intake。原 Skill 依赖本轮前序，不能通过仍适用历史覆盖合法省去未受影响步骤。#692 改善事实复用，但没有交付审核评论与入口分流。#818 只改善内容方法。当前 #819 仍 OPEN。

## 3. 目标与非目标

整体目标是共同交付评论生产、当前适用性消费和必要补审返回。范围为第5节完整行为、公共合同迁移、恢复、受管投影及第7节验收。保留 Task 后续完整门禁和整体 Completion/Closure/Finish。

不新增复核 Skill、第二审核步骤、资格/label/有效期体系、hash 链、长期账本或评测系统。不批量补标旧 Issue，不增加固定案例数、计时指标或完整发布矩阵。不关联发布版本，不进入 #822 或其他事项。只处理受支持正常协作、普通 stale/mismatch 和原恢复，不扩张到恶意伪造、并发压力、TOCTOU、锁或非常规 crash 加固。

本次承担完整功能的代码交付、必要定向工程检查和原独立 Review、Delivery、Completion、Closure、Finish。既有观察按其真实层级采用，不再追加 live 或实际 Agent 验收，不为补证创建新的 Issue/Task。未观察部分保持未验证，不作为通过证据，也不转成后继验收任务。Git/GitHub 各副作用边界仍由原 owner 执行。

## 4. 真实调用方、场景与流程

| ID | 调用方、前置与触发 | 行为与可观察结果 |
| --- | --- | --- |
| SC01 | 原 Create，草稿获审且正式内容读回一致 | 发布最小真实审核结论，未知结果恢复同一 Issue/评论。 |
| SC02 | 原 Clarify，主动复审且本次写入范围明确 | 发布/更新实际覆盖；局部不冒称完整通过，只读不写。 |
| SC03 | 已有 Issue 经 Sync；覆盖仍充分且前置满足 | 原 Readiness 直接 ready，经原 router 进入 Task 创建。 |
| SC04 | Readiness 仅缺事实 | Discovery 补足后回同一 Readiness；无影响时直接 ready。 |
| SC05 | 需求、范围或交付单元缺口 | Clarify 补足并返回；确需事实沿原往返，只有受影响措辞再审。 |
| SC06 | 仅措辞缺口 | Wording 返回同一 Readiness；等义修改不重启调查/澄清。 |
| SC07 | 覆盖不足或变化不可界定 | 必要完整链后再由 Readiness 判断。无评论本身不阻塞。 |
| SC08 | 必要前置/选择/证据阻塞 | 原 blocked/等待说明恢复条件，不重复全链掩盖阻塞。 |
| SC09 | 多缺口或选定基线真实失效 | 按事实→需求→措辞逐项回判；仅真实基线失效回 Sync。 |
| SC10 | 无 Issue 的问题/需求讨论 | 原标准完整调查/澄清，按实际创建与开工意图继续。 |
| SC11 | 仅讨论/草稿/创建，或创建并开工 | 分别停止；开工以正式身份、实际评论回 Sync→Readiness。 |
| SC12 | 合法 standalone_request/no_issue | 保留完整审核和原创建，不造空壳 Issue 或评论。 |

## 5. 行为要求

R1 对应下文“行为一”的共享评论与两个生产入口；R2 对应已有 Issue 的入口与直接 ready；R3 对应事实/需求/措辞补审及多缺口依赖；R4 对应完整链、阻塞及真实刷新；R5 对应讨论/创建/开工及终点；R6 对应 no_issue 与 Task 后续门禁；R7 对应公开合同、恢复与受管分发。以下保留 SRC819 的完整原文，功能行为、正常路径和兼容承诺继续有效；本 Task 当前验证义务由第7节界定，原文的验收表述不再单独要求新增 live 或实际 Agent 观察。章节上移一级以置于本节，不改写原文。

### 背景：已经审过的 Issue，开工时仍要重走完整审核链

通常先通过 guru-create-issue 创建 Issue。创建前，草稿已经经过上下文调查、需求澄清、措辞审核和开工就绪审核；创建后，用户还可能主动调用 guru-clarify-requirements 复审、修订 Issue。到正式开工时，Issue 可能已经内容明确、范围稳定，且已充分审核。

但这些审核结论没有通过统一、可读的 Issue 评论承接。后续会话或执行 Agent 即使能找到一些历史结论，当前 Intake 仍要求先执行本轮完整 Discovery、Clarify、Wording，再到末尾的 Readiness 判断是否可以开工。创建后的新 Issue 也返回 Sync 和完整 Intake。

因此，现流程不能根据“这个 Issue 已经审过，而且当前仍然适用”直接减少步骤。它会重复调查、澄清和审核，增加耗时与交互，也可能在重复审核中重新打开已决定的问题。#692 已改进事实复用和重复工作方法，但仍保留上述完整链；本项解决剩余的入口与路由问题。

### 目标：审核时留下最小结论，开工时复核并分流

本项需要两类行为配合完成：

| 职责 | 负责的 Skill | 需要做什么 |
| --- | --- | --- |
| 提供审核结论 | guru-create-issue、guru-clarify-requirements | 在实际审核、创建或获准修订完成后，将本次审核的对象、覆盖范围、结论及未决项写入最小审核评论，供以后开工复核 |
| 消费结论并决定路线 | guru-review-change-request，由 workflow 在 Sync 后显式调用 | 读取当前 Issue 和审核评论，检查原审核是否充分、是否仍适用，决定直接进入 Task 创建，还是只补缺失的审核 |

只添加评论不能减少现有步骤；只移动 Readiness 而没有可读结论，也无法稳定复用已完成的审核。两部分及其 workflow 路由在本项中共同交付。

### 行为一：提供最小审核评论

#### 谁在什么时候提供

- guru-create-issue：保留创建前的完整草稿审核。创建并回读确认正式标题、正文与获审内容一致后，在该 Issue 发布本次实际完成的审核结论。
- guru-clarify-requirements：用户主动复审 Issue，并允许发布结论或修订时，发布或更新本次实际覆盖的审核结论。只审核需求或局部措辞时如实写明范围，不能写成完整开工审核通过。纯只读审核仍只返回结论，不自动写评论。

共享评论规则保持一个正文源，两个入口引用同一规则。评论只说明：审核了哪个对象和哪些内容、得到什么结论、还有哪些影响开工的未决项或前置条件。代码基线只有在影响判断时才说明。

评论是供 AI 阅读和复核的依据，不是自动放行凭证。已有清楚且充分的历史评论也可使用，不要求固定模板、label、审核者身份资格、有效期、hash 链或长期审核账本。评论写入仍遵守精确外部操作范围；结果不确定时恢复同一已成功对象，不重复创建 Issue 或重复发布评论。

### 行为二：在 Sync 后复核，并推进 Intake 分叉

#### 现有流程

已有 Issue 开工及草稿创建都先经过：

模式选择 → Sync → Discovery → Clarify → Wording → Readiness → 按目标进入 Issue 创建或 Task 创建。

其中，Discovery 负责上下文调查，Clarify 负责需求澄清，Wording 负责措辞审核，Readiness 即 guru-review-change-request，负责判断能否作为独立交付单位开工。当前 Readiness 位于末尾，且依赖本轮前序结果；Issue 创建成功后又回到 Sync 和完整 Intake。

#### 调整后的已有 Issue 开工流程

入口为：模式选择 → Sync → guru-review-change-request 的已有 Issue 当前适用性复核。下文简称 Readiness；Discovery、Clarify、Wording 分别指原上下文调查、需求澄清、措辞审核 Skill。

Readiness 读取完整 live Issue、有效讨论、审核评论、必要前置交付和影响原判断的代码变化。它先判断现有审核覆盖和当前缺口，再选择下面一条路线；评论存在本身不构成通过。

| Readiness 判断 | 下一步如何执行 | 如何继续或结束 |
| --- | --- | --- |
| 审核充分、仍适用，且开工前置已满足 | 返回 ready，经原 router 调用 guru-create-task | 在 Task 创建原有检查和所需副作用确认满足后创建 Task，进入原规划流程；不再调用 Discovery、Clarify、Wording |
| 仅缺上下文事实，尚不能判断原结论是否适用 | 调用 guru-discover-change-context，查清指明的事实缺口 | Discovery 完成后返回本次 Readiness；若需求和措辞未受影响，直接判断 ready，不自动串行调用 Clarify、Wording |
| 存在需求、范围或独立交付单位问题 | 调用 guru-clarify-requirements，处理指明的问题；它确需额外事实时沿原上下文往返取得 | 澄清完成后返回本次 Readiness，检查变更后的覆盖。若正文变化使措辞审核失效，再进入 Wording；未受影响的上下文和措辞结论继续复用 |
| 仅有措辞问题，需求和上下文已有充分依据 | 调用 guru-review-contract-wording，完成指明范围的审核或获准修订 | 完成后返回本次 Readiness；等义修订不重启 Discovery、Clarify。若发现真实需求变化，返回需求澄清分支 |
| 无充分审核依据，或变化影响无法界定，无法安全复用原覆盖 | 执行必要的完整链：Discovery → Clarify → Wording → Readiness | 最后的 Readiness 根据真实本轮结果判断 ready 或未决；没有评论只是依据不足的可能原因，不是独立阻塞条件 |
| 已确认存在尚未满足的必要前置、未解决的真实选择，或当前无法取得必要证据 | 按原 blocked/等待合同说明具体阻塞和恢复条件 | 不创建 Task，不以重复执行审核掩盖阻塞。条件满足后回到受影响步骤或本次 Readiness，复用仍适用的结果 |

同时存在多个局部缺口时，按上下文 → 需求 → 措辞的依赖顺序先处理最早必要项，每次补足后由 Readiness 判断剩余缺口；只执行仍有必要的后续项。例如，调查发现原行为未变，则调查后即可 ready；调查发现需求已变，则补 Clarify，并在需要时补 Wording，再判断 ready。不得把“局部补审”实现成只要进入一个原 Skill 就自动重走全部后续步骤。

局部步骤完成后必须有合法的返回入口，将实际结果交回同一 Issue 的 Readiness，而不是落入当前默认完整链。为此调整原 Skill 的适用 profile、必要输入、typed exit consumer 和薄投影。补审调用的前置可以由仍适用的审核覆盖和本轮事实满足，不强迫为取得 receipts 先执行本轮完整前序链，也不伪造前序通过结果。具体公共合同通过本项兼容或迁移方案落地。

若选定基线真实失效，先由原 Sync 刷新，再回已有 Issue 的 Readiness 入口判断受影响覆盖；单纯缺少上下文事实不自动刷新 Sync。换会话、换 Agent、时间经过或无关 HEAD 变化本身不使结论失效。

上述分支由原 guru-review-change-request 的入口 profile 和 workflow 显式编排，不新增复核 Skill 或第二个审核步骤。复核及补审自动接续不要求额外人工批准；真实需求选择、Issue/评论写入和 Task/资源创建仍遵守原交互及副作用边界。

#### 未指定 Issue：从讨论进入，再按需创建并开工

必须保留用户没有提供 Issue 编号、先描述问题或讨论需求的入口。没有 Issue 不要求用户先手工创建，也不把讨论对象当作“已审核 Issue”套用上述快速路径。

1. 由原模式选择判断是否进入标准 Intake；本项不改变 task-free 的适用条件。选择标准 Intake 后，按 Sync → Discovery → Clarify 开展必要调查与讨论，形成明确需求。资源创建仍保持未授权状态。
2. 若本次需要并已请求或获准创建 Issue，形成完整草稿，继续 Wording → Readiness。草稿 ready 后进入 guru-create-issue，创建、回读正式内容并发布最小审核评论。没有充分草稿审核不能提前创建，也不要求用户重复回答已明确的问题。
3. 用户只要求讨论或准备草稿时，在相应结果处结束，不自动发布 Issue；只要求创建 Issue 时，在创建、评论及读回完成后结束，不自动创建 Task。
4. 若用户还要求正式开工，创建后的正式 Issue 进入 Sync → 已有 Issue Readiness。该复核核对正式身份、实际内容与刚发布的审核结论；仍适用时直接进入 Task 创建，不重做刚完成的完整审核链。这里消费实际评论和正式 Issue，不把草稿旧 receipts 改写成正式 Issue 的通过结果。
5. 若按原合同采用不关联 Issue 的正式 Task 路线，保留 standalone_request/no_issue 的完整审核及原 Task 创建路径，不强制创建空壳 Issue，也不要求不存在的审核评论。本项不扩大该路线的适用范围。

因此，“给定已有 Issue 开工”和“讨论 → 创建 Issue → 开工”在正式 Issue 的 Sync → Readiness 处汇合；讨论及草稿阶段仍使用原完整调查与审核方法。

Task 创建继续执行原身份、checkout、分支和副作用检查；Task 后续规划及交付门禁保留。评论不代替这些判断。

### 交付范围与兼容

同步修改原 workflow 路由、Readiness 入口与局部补审返回、Create/Clarify 评论行为，以及实际受影响的公开输入、typed exits、校验、示例和恢复说明。给出明确的公共 I/O 兼容或迁移合同，使新入口合法消费评论和当前事实，不再要求先取得本轮完整前序 receipts，也不伪造那些步骤的结果。

AI 判断审核覆盖、变化影响和开工路线；脚本只读取、执行与校验客观事实。受影响 canonical、dogfood 和声明平台投影由原安装 owner 同步。本项不新增资格体系、证明账本或评测系统，不批量补标旧 Issue，不把尚未实现的评论机制宣称为已有能力。

### 验收

- 从实际创建及获准复审入口，观察最小审核评论的发布或更新及 live 读回：评论准确说明本次覆盖、结论和未决条件；已成功对象能按原恢复路径继续，不重复创建。
- 从已有 Issue 开工入口实际验证分流、各局部步骤的返回和阻塞恢复：仍适用时直接开工，有缺口时只补必要步骤，依据不足时走必要完整链。覆盖未指定 Issue 的讨论 → 按需创建 → 开工，以及讨论/仅创建到此结束的边界；原 no_issue 路线保留。Task 创建及后续门禁未被评论替代。
- 受影响公开合同、workflow 路由、兼容说明及安装投影一致，完成与本项差额匹配的定向验证。无需完整发布矩阵、计时指标或固定案例数量。

### 关联与来源

#818 负责 Issue 内容的最小充分与验收收敛，本项负责审核结论的承接、消费和 Intake 分流，两项独立，不设硬前置；实施顺序由当前编排安排，不绑定特定发布 Issue 或版本。

当前实现依据：trellis/workflows/guru-team/workflow.md，以及 trellis/skills/guru-team/packages 下的 guru-create-issue、guru-clarify-requirements、guru-review-change-request 和 guru-discover-change-context 原合同。

<!-- guru-create-issue:5efc8652185f9c81b260521da28a76f815e324a7c139d5072e8e4429f8ed7816 -->

## 6. 约束与依赖

TaskId=819-issue-review-intake，generation=0。固定开发来源 origin/main@4f2adef1f7b099f78bb8429e8b8facd66dce3bfc；integration 和 delivery target=main。保持该身份及原操作恢复，写入前校验实际 checkout boundary。

Markdown/AI 拥有覆盖、充分性与路线；脚本只执行和校验客观事实。当前原 owner 是唯一正向实现位置。公共 I/O 直接成套演进并给出迁移，不因稳定名称制造长期 dual-read、wrapper 或新状态 authority。具体字段与受影响资产在 Delivery design 展开。

Requirements/Design/Test authority 由 docs/{requirements,design,test}/README.md 的 guru-trellis-rdt/active 定位；本项命中 local-fix-intake、issue-content 完整单元。Architecture authority 为 docs/architecture/README.md；独立原 owner 决定影响与贡献。#818 与本项独立，串行执行不新增硬前置。无业务数据库、支付、服务 API 或部署系统变更要求。

## 7. 可观察验收与验证方式

| ID | 要求/场景 | 入口、输入与预期结果 |
| --- | --- | --- |
| AC1 | R1/R7；SC01–02 | 审查完整评论生产、只读及同对象恢复实现，采用现有原入口、定向 executor 回归和已取得 live 观察；区分真实写入、fixture 与未观察恢复。无需新增 live 发布、PATCH 或未知响应验收。 |
| AC2 | R2–4；SC03–09 | 审查完整路由、三类补审返回、多缺口顺序、必要完整链及阻塞恢复；采用已有实际 Agent 观察与生产 wrapper/consumer 定向检查，不伪造前序或把 fixture 升级为 live 全链。无需追加 Agent 分流验收。 |
| AC3 | R5–6；SC10–12 | 审查讨论→创建→开工及各终点、no_issue 的完整实现和原 Task 门禁；采用已有原入口观察与当前 Creation 桥接检查。创建后 live ready→Task 写前正向、完整 start/selector 和其他平台 Agent 仍未验证；不再要求新增对象补验收。 |
| AC4 | R7；全部 | 原公开 wrapper/consumer/graph 和定向 package/runtime；原安装 owner 同步及 reapply，核 installed/声明平台、drift、mode、sidecar、用户内容与 Task/session 保留。 |
| AC5 | 全部 | 原独立 committed Review、Delivery readiness/交付、整体 Completion、Closure、Finish 覆盖完整范围；合并不自行证明 Task 完成。 |

既有实际 Agent、确定性检查、安装与 GitHub 外部回读按原层级分别提供证据；其原报告、失败和观察截止保持。必要修复仍须定向工程检查及独立 Review。本表不把未观察场景写成通过；这些边界不再构成本 Task 的追加验收或后继任务义务。不要求完整发布矩阵、计时或固定样本数。

## 8. 实际未决项

没有阻塞整体需求的产品选择。功能、公共合同及兼容实现责任保持，所需质量与收尾由原 owners 完成。当前不再追加外部或实际 Agent 验收；未验证范围按第7节及现有 Test 观察截止保留，不能宣称其已验证。后续发布和 Closure 分别判断实际交付及来源处置。
