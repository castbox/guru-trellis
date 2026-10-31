# D1：Phase 2 正常 authoring、兼容及首次执行验收

## 1. 整体来源与术语

公共 accepted_scope 指向 [整体PRD](../../prd.md) 的实际sha256 revision；本D1 scope_ref选择AC710-01至AC710-09全部锚点。TaskId=710-phase2-recorder-authoring，generation=0，DeliveryId=63d55014-9fec-48da-a106-2a7403305977；planning_root为本目录。

Direct Source为[Issue #710](https://github.com/castbox/guru-trellis/issues/710)，本轮完整读取目标、行为要求1–5、验收、交接及非目标，未选择评论。整体PRD第1节定义authoring、完整结果、两类token及首次正确；本批使用同一含义。来源行为要求中的原owner、职责、调用顺序、兼容和native输入边界是规范性设计约束，具体处置只写design第3节。

## 2. 整体与本批目标、非目标

当前正常说明让Agent在最小语义输入与完整结果之间自行选择，并可能手填错误摘要。本批完整交付该职责修复和其行为证明：原AI继续九维审查，只填语义内容；原recorder生成客观事实；原checker/invoke消费同一完整结果。交付必须同时包括完整结果兼容、诊断、真实命令、首次候选/最终native、finding路由和安装投影。

覆盖整体R710-01至R710-07及九条AC，不将native或分发留给后续Delivery。排除项继承整体第3节：#713完整生命周期链、#711/#712、业务#994现场、历史迁移、上游/全局包、攻击/并发/锁/crash加固及完整Release矩阵均不进入本批。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首个Delivery，无前序交付。开发基线B明确选2fc49bda6552d1a8bf95dff243ab2de9a9ea8e30，当前HEAD观察H0相同；PR目标main另行判断，不使用移动origin/main替代B，不冻结未来HEAD。

现有最小语义recorder已经生成五个结果身份字段；完整6.0分支采用传入结果。test_candidate_check从完整示例及内部content_identity开始；现有native适配器会执行record/check/invoke，但当前cases和host准备是否覆盖合法候选到最终阶段须调查。已有fixture不算本批native证据。

上游需求已明确，无#711/#712前置。当前安装Guru 0.7.0-guru.7 / Trellis 0.7.0-castbox.6；本批需匹配修改后的安装，沿原工具owner更新，保留当前Task/session。native能力或mandatory语义前置缺失只阻塞相应验收，不能补假pass或删验收。D1完成后不留未分配实现项；Task Completion仍独立核全部AC和未验证边界。#713后续亲自执行其完整链，消费本批固定提交与证据定位。

## 4. 本批调用方、场景与流程

| ID | caller、前置与触发 | 行为和观察 |
| --- | --- | --- |
| D1-S01 | 正常安装Check AI；合法候选profile、Task/Planning/candidate、Architecture/RDT及测试环境已齐备 | 自行读取正式Skill，第一份authoring与命令正确；原record/check/invoke返回candidate_checked。候选token存在但不填私有结果字段。 |
| D1-S02 | 原owners完成最终整合、implementation重绑并取得当前阶段证据 | 合法最终profile第一份authoring与命令正确，返回passed；阶段转换不算失败重试。 |
| D1-S03 | 真实finding、规划变化或证据缺失 | 按事实返回implementation_required、planning_stale或blocked；真实finding保留并合法返回原owner。 |
| D1-S04 | 已生成完整结果的消费与恢复 | checker/invoke继续消费，业务变化拒绝旧结果，metadata不制造循环；recorder完整输入依真实consumer作显式兼容处置。 |
| D1-S05 | 普通参数、字段、摘要或路径覆盖不匹配 | 原错误合同保持，诊断只报告机器可确定的字段/范围及原恢复owner；不猜算法或根因。 |
| D1-S06 | canonical能力交付给dogfood、声明平台及实际安装 | 原受管owner同步后定向检查reapply/drift、sidecar和mode，分开报告native/命令/投影证据。 |

## 5. 完整行为、条件与约束

- D1-R01承接整体R01：实际Recorder Authoring正文给出封闭语义字段、调用定位参数、派生字段和直接consumer；最小示例是唯一正常authoring路径，无私有摘要、HEAD及结果身份占位。原AI九维/Docs/Architecture/出口判断保留；不制造无人消费schema/DTO/wrapper/artifact。
- D1-R02承接R02：说明真实安装路径、各argv和输入载体、读取位置及输出；按AI审查→record完整结果→check→invoke承接，同一完整结果不重组。checker回执不替代owner result；profile要求的回执原样传递。合法producer的Task/Delivery/Planning身份及上游token不得删除、重算或禁止。
- D1-R03承接R03：盘点完整6.0输入当前consumer、恢复和兼容；区别于checker/invoke消费完整结果。有consumer写明用途和前置，无consumer沿显式兼容/迁移退役，不静默破坏API，不让Agent自行选两种authoring。两类token职责保留，不重算旧结果延续过期语义判断。
- D1-R04承接R04：具体字段诊断保留原错误合同，只陈述机器事实；真实业务变化、路径覆盖及Architecture/Check仍阻断，metadata保持原排除规则。诊断不是根因修复的行为证据。
- D1-R05承接R05：五类适用profiles经正式语义authoring进入真实命令，不由host预填私有摘要。完整结果单元测试仍可验证其真实入口，但不能被称为authoring/native证据。合同测试发现缺正文、坏引用或示例入口不一致；不靠关键词证明可执行性。
- D1-R06承接R06：真实native从正常安装Skill执行合法候选→原owners整合/重绑→最终Check，必需语义前置实际完成。host不预填本阶段结果/摘要/内部选择/预期出口；不事后纠偏。模型外验收程序比较预期。案例记录profile、候选、前置、首次输入、命令、承接及出口；原失败保留，新案例边界明确；不能把重试改名首次。复用真实finding场景，缺native能力或前置如实未验证。
- D1-R07承接R07：定向分发与模式、sidecar检查，不跑完整发布矩阵；确有必要最多一个代表clean样本。给#713可获取固定提交、匹配安装、profiles、命令和首次native定位；不新建公共handoff DTO或长期台账。

适用profiles为delivery_candidate_check、delivery_initial_check、delivery_finding_fix_rerun、delivery_planning_reentry、delivery_resolved_reconciliation。全部保留原前置、语义、出口及唯一consumer。现有能力优先复用，仅实际装配差额授权runtime变化；不能通过自动刷新旧完整结果掩盖stale。

## 6. 本批验收、验证方式与未决项

| AC | 要求/场景 | 输入、入口、预期观察 |
| --- | --- | --- |
| AC710-01 | D1-R01/S01 | 实际安装Skill正文与最小示例可直接执行，无手填客观身份，完整结果用途清楚。 |
| AC710-02 | D1-R02/S01–02 | 同一实际record/check/invoke链正确承接recorder结果及要求的回执，不重组结果。 |
| AC710-03 | D1-R06/S01–02 | 合法无finding native案例首次候选得到candidate_checked、原owners整合重绑后首次最终得到passed；可核首次输入和实际命令，无装配纠偏。 |
| AC710-04 | D1-R05/06、S03 | 真实finding返回implementation_required或planning_stale并合法回原owner。 |
| AC710-05 | D1-R02/05、S03 | 其余适用profiles定向真实入口保持成功、finding、规划、blocked及客观事实职责。 |
| AC710-06 | D1-R03/04、S04 | 普通业务内容变化拒绝旧结果；metadata连续性保持；不自动刷新旧语义判断。 |
| AC710-07 | D1-R03/S04 | 完整6.0输入consumer清单及保留/退役兼容合同明确；合法完整结果消费恢复保留。 |
| AC710-08 | D1-R05/06、S01–03 | authoring测试无host预填私有摘要；native输入无预期结论；完整结果单元测试只声明各自入口；失败和新案例分开。 |
| AC710-09 | D1-R07/S06 | canonical/dogfood/installed/平台投影、定向reapply/drift/sidecar/mode验证及后继固定定位完整；发布矩阵边界明确。 |

本批requirements阶段无未决产品问题。consumer精确盘点、命令承接配方和native环境准备属于下一方案细化，必须在plan_ready前给出唯一可实施方案；不能靠旧fixture或#713完成本批验收。全部AC当前待实施。

## 7. Canonical引用与本轮差额

| authority | 具体用途与本批差额 |
| --- | --- |
| trellis/skills/guru-team/packages/guru-check-task/references/contract.md，Execution Order、Semantic payload | 正常authoring正文、命令、示例及完整结果用途在原owner收敛。 |
| .trellis/spec/workflow/skill-package-contract.md，Public Skill I/O And Private State | 不扩大public DTO或私有状态；任何不兼容演进有显式迁移。 |
| .trellis/spec/workflow/quality-guidelines.md，Test And Validation Value、Validation Scope Ownership | 分别证明命令、native及安装，不扩完整矩阵。 |
| docs/architecture/README.md及00-foundation/design-constitution.md、06-governance/change-contract.md | 独立Architecture candidate_assessment/final_plan读取原authority；本PRD不预判影响或创建贡献。 |
| docs/design/current/knowledge-maintenance.md及docs/test/current/knowledge-maintenance.md | 保留候选→最终集成→重绑→最终Check的现行完整知识合同，不另建owner或阶段。 |

必要引用在其原owner实际读取；link存在不证明读过。本阶段只写本D1需求，不写共享current、导航或contribution。
