# #710 Phase 2 正常 authoring 与结果职责：整体需求

## 1. 来源与术语

| 来源 | 角色、章节与用途 |
| --- | --- |
| [castbox/guru-trellis #710](https://github.com/castbox/guru-trellis/issues/710) | 唯一 Direct Source，exact_source。本轮完整读取 title/body；OPEN，updatedAt=2026-10-31T11:52:12Z，无评论。目标、行为要求1–5、全部验收、交接及非目标均为要求；原 owner、职责、顺序及兼容承诺为设计约束。 |
| [Check 合同](../../../trellis/skills/guru-team/packages/guru-check-task/references/contract.md) | 现行约束及待修复对象：完整九维审查、profiles、出口、Docs/Architecture 与 freshness。 |
| [workflow](../../workflow.md) / [质量指南](../../spec/workflow/quality-guidelines.md) | 原 owner 顺序、候选→最终整合→重绑→最终 Check、验证价值及普通任务验证边界。 |
| [#417](https://github.com/castbox/guru-trellis/issues/417) / [#638](https://github.com/castbox/guru-trellis/issues/638) | 已有能力与历史约束；保留当前 AI 亲自审查及候选/最终阶段，不继承历史 pass。 |
| Trellis [workflow 定制](https://docs.trytrellis.app/advanced/custom-workflow.md) / [spec marketplace](https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md) | 本轮已正常读取官方文档；Markdown 定义流程，原受管机制分发，不修改上游或全局安装。 |

**authoring** 是当前 Check AI 审查后填写的最小语义输入。**完整结果** 由原 recorder 根据语义输入、调用定位和 live facts 生成。候选 token 与 Phase 2 私有 token 分属现有直接 consumer，不能互换。“首次正确”指当前阶段第一份输入、参数及结果承接正确；存在真实 finding 时不要求返回 passed。

## 2. 背景与问题

#710 记录业务 #994 的历史故障：Agent 将候选算法摘要填入完整6.0结果的 reviewed_content_sha256，record成功而checker返回stale_identity。删除手填五个结果字段后，既有 recorder 可生成正确客观事实。这证明最小语义输入能力存在，不证明首次正常流程可执行，也不说明 Task/Delivery 路由错误。

本轮 main 起点2fc49bda6552d1a8bf95dff243ab2de9a9ea8e30仍有缺口：合同引用 Recorder Authoring 却没有正文；完整结果示例被称为 authoring 示例；两类 recorder 输入的正常用途未分清。候选测试预填私有 content_identity，合同测试用关键词存在断言，均不能证明正常 Agent 首次选对输入。checker合并诊断增加定位成本，但更早报错不能替代根因修复。

## 3. 目标与非目标

让 AI 从正常安装 Skill 入口读取正式说明，完成真实九维判断，填写语义字段并承接合法公共输入，沿原 record→check→invoke 返回符合真实结论的唯一出口。完整范围包括说明/示例、完整结果兼容、实际调用承接、辅助诊断、定向命令与首次native证据、canonical/dogfood/安装分发。本 Task 对全部验收负责，候选、fixture pass、单个Delivery或合并不能替代整体完成。

不承担#713跨步骤完整生命周期链、#711导航隔离、#712新增legacy恢复家族；它们不是本项前置。不改业务#994代码、Mobile、会话或任务状态。不改变全局phase，不新增semantic owner、审批链、全流程token、通用恢复框架、授权记录或长期台账。不改Trellis上游、全局npm或node_modules。不扩攻击/伪造、并发压力、TOCTOU、锁、fault injection、crash consistency范围。不执行Release、部署或完整发布矩阵，不迁移历史Task。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置与触发 | 行为和可观察结果 |
| --- | --- | --- |
| S710-01 候选首次Check | 当前Check AI；合法Task/Planning/候选、原Architecture/RDT证据和确定性测试环境齐备，候选token正常存在 | 自行读正式Skill并首次正确authoring、调用及承接，返回candidate_checked；无输入装配纠偏重试。 |
| S710-02 最终首次Check | 原owners完成最终集成，implementation重绑实际候选并取得匹配阶段证据 | 从合法最终profile首次正确调用，返回passed。两阶段合法转换不算失败重试。 |
| S710-03 实际finding | 当前AI真实观察到实现缺陷或规划变化 | 按实际结论返回implementation_required或planning_stale，合法返回原owner；不能为首次passed隐去问题。 |
| S710-04 完整结果消费/恢复 | checker、invocation及调查确认的完整6.0输入consumer持有原recorder结果 | 合法消费与恢复；业务变化拒绝旧结果，不自动更新旧结果身份。 |
| S710-05 普通装配错误 | 受影响原入口遇到可机器判定的不匹配 | 保留错误合同，定位字段及原处理owner；无法定位根因时只报告已确定范围。 |
| S710-06 安装采用 | 原preset/工具owner，匹配canonical与实际安装 | 同步受影响平台，定向reapply/drift/sidecar/mode；分开报告安装、命令及native证据。 |

## 5. 行为要求

### R710-01 唯一正常authoring合同（S01–03）

原guru-check-task独占实际Recorder Authoring正文和最小输入示例，列明封闭语义字段、调用定位参数、recorder派生结果字段及唯一直接consumer。正常示例不要求AI填写、计算或复制私有摘要、候选摘要、HEAD或结果身份占位值；Task定位由公共入口和参数提供。AI保持完整九维、finding、验证适用性、Docs/Architecture消费与出口判断，脚本不能生成semantic pass。

优先复用既有输入和recorder；只有实际结构化边界无法表达时才补定义，不预设新schema/命令/版本。不用大量optional字段的结果对象冒充输入，不新增无人消费DTO、wrapper或长期artifact。

### R710-02 完整实际命令链（S01–03）

正式说明给出真实安装路径、每条命令的argv、输入载体、读取位置及回执：AI审查并author→原recorder生成完整结果→原checker验证刚生成结果→原invocation消费同一完整结果并输出唯一出口。checker回执不能替代owner result；仅把profile要求的验证回执按原字段传递。Agent不重组结果、不导入私有Python计算身份、不从结果示例复制摘要。真实producer的Task/Delivery/Planning身份和合法上游token原样承接，不删除、重算或禁止传递。

覆盖delivery_candidate_check及适用的delivery_initial_check、delivery_finding_fix_rerun、delivery_planning_reentry、delivery_resolved_reconciliation，保留各自语义、前置和出口。

### R710-03 完整结果与兼容（S04）

最小示例是唯一正常authoring路径，完整结果示例只解释输出或合法消费。盘点recorder完整6.0输入的真实调用者、恢复与兼容用途，区别于checker/invoke合法消费已生成结果。有直接consumer时写明用途、前置和区别；无consumer时按显式兼容/迁移合同退役，不为假设用途保留双入口。不静默删除公共命令、输入能力、schema或出口。不得重算覆盖旧完整结果的摘要、HEAD或绑定来延续过期判断。两类token保持原职责，不统一算法或更换Task/Delivery身份掩盖输入问题。

### R710-04 诊断与真实stale（S04–05）

受影响入口保留原错误合同，在机器可判定范围指出字段和原owner；否则报告确定的不匹配范围。不能仅凭摘要不同断言算法混用、内容变化或编码损坏。真实业务变化仍阻断，结果/生命周期metadata保持既有排除规则，不制造摘要循环；路径覆盖、Architecture和Check门禁保留。

### R710-05 定向真实命令验证（S01–05）

authoring测试从正式语义输入进入真实recorder/checker/invoke，host不预填完整结果私有摘要。checker/schema/兼容消费单元测试可构造其真实入口的完整结果，但只证明各自入口。保留合法完整结果消费/恢复、真实业务变化拒绝和metadata continuity验证。合同测试须发现正文缺失、引用失效及示例与入口不一致；机械断言不替代AI判断说明可执行性。其余profiles、finding/规划/blocked路由沿真实入口定向验证，不扩无关业务矩阵。

### R710-06 首次native证据（S01–03）

真实native Agent从正常安装Skill入口开始；提供合法public profile、当前Task/Planning/候选、实际阶段证据和确定性环境，候选token正常存在。必需语义前置由原owner实际完成。host不预填本阶段owner result、私有摘要或内部authoring选择，不注入结论或预期出口，不给报错后纠偏Prompt。预期出口仅由模型输入外验收程序比较。

从合法候选Check开始，经原owners最终集成、重绑到最终Check，分别保存profile、候选、前置事实、首次输入、实际命令、承接和出口。装配错误或纠偏使该案例不满足首次正确，保留原失败并区分修订后的新案例，不把重试改名首次。缺mandatory前置或native能力时如实未验证，不补假pass。复用现有finding场景验证合法非通过出口。本项无需从Task创建运行完整链，完整链由#713负责。

### R710-07 分发及后继交接（S06）

通过canonical package、原preset/工具owner及声明平台同步dogfood和实际安装，验证定向reapply/drift、必要sidecar和mode。普通任务最多使用确有必要的一个代表性clean throwaway，不承担完整多平台Release Gate。

交付时在原规划或验证位置给出可获取固定候选提交、匹配安装来源、适用profiles、实际命令及首次native证据定位供#713 fresh核验。#713亲自执行其完整链当前Check，不将本项旧出口当作新任务结果；跨项变化只重验受影响依赖。交接不新增公共DTO、长期台账或确认步骤。

## 6. 约束与依赖

TaskId=710-phase2-recorder-authoring，generation=0；唯一当前专用checkout，branch=codex/710-phase2-recorder-authoring，目标main。规划起点不冻结未来实现HEAD，当前无前序Delivery。复用已有正确recorder，只在真实装配差额需要时改runtime，不为文件类型或数量制造改动。

沿原owners接受整体scope、创建Delivery、独立Architecture、Wording、Approval和实施前接受。规划不替代门禁。公共不兼容调整先形成明确迁移合同，不将本项扩大为其它Issue或历史迁移。native执行与正常安装能力在执行时核验；缺口是未验证边界，不能删除R710-06。官方三份必读文档本轮已正常读取。无业务数据库、部署或业务数据迁移。

## 7. 可观察验收与验证方式

以下全部待实施，Intake和规划结果不证明验收完成。

| AC | 要求 | 入口、输入及预期结果 |
| --- | --- | --- |
| AC710-01 | R01 | 正式安装Skill有实际Recorder Authoring正文和可用示例，无手填客观身份，完整结果用途清楚。 |
| AC710-02 | R02 | 同一真实authoring→record→check→invoke正确承接，客观事实只由原owner生成，不将回执替代结果。 |
| AC710-03 | R02/R06 | 无finding native案例首次候选Check取得candidate_checked；原owners集成重绑后首次最终Check取得passed，首次输入/命令/承接可查且无装配纠偏。 |
| AC710-04 | R05/R06 | 当前实际finding场景返回implementation_required或planning_stale，并合法回原owner。 |
| AC710-05 | R02/R05 | 其余适用profiles定向真实入口测试保持成功、finding、规划和blocked语义及事实生成职责。 |
| AC710-06 | R03/R04 | 业务内容变化拒绝旧结果；metadata排除保持；不自动刷新旧结果伪造新审查。 |
| AC710-07 | R03 | 完整6.0输入consumer清单、保留/退役依据和显式兼容合同明确；完整结果消费与恢复合法，无静默公共API破坏。 |
| AC710-08 | R05/R06 | authoring命令测试不预填私有摘要；完整结果单测只证明各自入口；native输入无预期结论；原失败与新案例分开保留。 |
| AC710-09 | R07 | canonical/dogfood/实际安装/受影响平台一致，定向reapply/drift/sidecar/mode通过；未跑完整发布矩阵如实列明，#713交接定位可获取。 |

## 8. 实际未决项

没有阻塞的产品或范围问题。完整6.0输入consumer处置、真实installed命令承接及native fixture/执行能力由Delivery Author调查并形成唯一方案；真实authority冲突回原owner。本root PRD不决定方案、不批准规划、不启动实施。
