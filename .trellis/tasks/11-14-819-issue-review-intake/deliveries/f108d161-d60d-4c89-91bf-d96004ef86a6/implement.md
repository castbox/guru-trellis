# D1 Issue 审核评论与 Intake 分流实施与验证计划

## 1. 输入与引用

整体范围为 ../../prd.md 第5节完整来源、R1–R7、SC01–12、AC1–5；本批以 prd.md 的全部D1要求/场景为输入。design.md 第3节是唯一来源设计处置，第5节拥有实际profile/逐出口DTO，第6–7节拥有顺序与恢复/迁移；实施前读完整相关条件，不从接口名称自行补语义。

起点B与H0同为4f2adef1f7b099f78bb8429e8b8facd66dce3bfc；没有前序Delivery。固定开发来源origin/main，集成target=main；当前key为819-issue-review-intake/gen0/f108d161-d60d-4c89-91bf-d96004ef86a6。当前独立 Architecture candidate_assessment 已按新验证范围返回 architecture_impact/target_native，决策 ADR-ISSUE-REVIEW-INTAKE 保持；机制、公共合同和知识定义没有新差额。当前 final_plan 与 Approval 仍由原 owner 完成，文件存在不表示激活。

必要工程规则为 .trellis/spec/workflow/{workflow-contract,skill-package-contract,quality-guidelines,subtraction-first-compatibility,clear-technical-writing}.md 及 .trellis/guru-team/skills/packages/guru-author-task-plan/references/planning-body.md。Architecture authority/constitution/change-contract和RDT两个完整命中单元见design §9。Trellis官方首页、custom-workflow、custom-spec-template-marketplace已用于确认扩展面；实施不改上游源码或hook分叉。

ready的真实创建consumer按原Create Task SKILL和Interface加载schemas/public-delivery-task-creation-input-2.0.schema.json、共享contracts/task-lifecycle/task-creation-input-3.0.schema.json及MIGRATION-813。design §5.1–5.3单写来源三字段、独立集成/交付目标、原acquisition和同步/恢复条件；实施前实际加载当前选定版本，不用保留的旧1.0 schema替代。

## 2. 有依赖顺序的步骤与文件责任

本表保留完整功能实施职责和依赖。已有工作按原实际结果及当前适用性采用；本次只更新验证责任，不重新实施未改变的代码或整合未改变的知识。每批 Task 写入前执行原 checkout boundary；保持同 Task/key，不重建资源。

| 步骤 | 依赖、owner及真实文件 | 实际改动及完成观察 |
| --- | --- | --- |
| I819-01 | Activation后；原workflow与各package owner；trellis/workflows/guru-team/{workflow.md,references/routing.md}，trellis/skills/guru-team/packages下Sync/Readiness/Discovery/Clarify/Wording/Create Issue/Create Task各SKILL、references、interface、schemas、runtime、examples | 按design §5明确独立profile/output及consumer；Sync read/sync归一化真实base_source三字段，新ready只向当前Create Task投reviewed_base_source，集成/交付branch由原owner独立审定。保原source/acquisition及同步/恢复条件，不恢复已移除公共字段、不复制旧transition；原confirmation/draft/no_issue保真实用途。AI owns判断，runtime不实现分流推理。 |
| I819-02 | I01的输入/出口已明确；原Readiness与三个局部owners | 实现existing_issue_intake/issue_review_return及三个issue_readiness_supplement；Clarify额外事实、Wording需求变化及基线刷新返回均保持真实来源kind和精确对象。必要全链消费原Sync transition，不从三字段反拼。生产wrapper用真实producer结果返回并进入当前Creation；普通stale/mismatch回原owner。 |
| I819-03 | I01评论合同；原Clarify/Create Issue | 新增Clarify-owned references/issue-review-comment.md一份正文；Create2.0接AI已审review_comment_body，正式内容读回后评论POST/GET再created；recover定位原Issue/评论。Clarify引用同规则，复用source_actions的POST/PATCH/readback，只读不写。每个结果保真实部分完成事实。 |
| I819-04 | I01–03；原公共合同/分发owner | 更新实际受影响registry、production manifest、shared runtime消费者和examples；新ready示例接当前Create Task profile2.0/creation3.0，保来源/目标区分；现有正确#813例子保持其原适用性。新增trellis/presets/guru-team/MIGRATION-819.md，逐项旧新schema及consumer切换、固定旧操作恢复。核旧资产真实consumer；失去current用途的branch/entry同批退出，不增长期dual-reader。 |
| I819-05 | I01–04；原工程验证owner | 采用下节现有生产入口、分层观察和工程结果；实际修复执行必要定向检查。未观察层级如实保留，不再新增 live/Agent 验收，不造新 Issue/Task 或后继验收义务。 |
| I819-06 | canonical完成；原guru-upgrade-tools及installer | 完整matching更新当前checkout工具/workflow/Skills，保Task/session；按原sidecar owner处理每个.new/.bak；同步本仓dogfood和声明平台，执行drift和定向reapply，核mode与用户内容。不得手工覆盖受管副本或借apply旧Task阻塞绕门禁。 |
| I819-07 | 完整实施及真实工程结果；原RDT和Architecture maintenance owners | 执行§6的delta_first及隔离完整Architecture拟写final_integration；重读live expected-current、整合仍有效条件并readback全部真实targets。贡献/ADR和知识after均进入后续同一内容候选。 |
| I819-08 | I01–07；原TaskCommit、implementation与独立Review owners | 原本地TaskCommit纳入完整after；固定B/H构造committed Candidate和begin_check；新的独立reviewer完成一次Architecture before/after及完整Review。后续修复形成后继本地提交和受影响独立补审。通过后才原Delivery Review/readiness→Publication；本表不预填通过。 |

允许改动仅本Task范围、上述原owners及真实受影响受管投影。共享知识只在I07由原owner写；不修改其他Task、#808或发布事项，不扩大到全仓旧测试清理或完整矩阵。后续merge前停交协调会话。

## 3. 验证入口、输入与预期观察

当前验证范围继承整体 PRD 第7节、本批 PRD 第6节和 design §8。采用已取得的分层观察与仍适用工程事实，只为实际修复、缺失或不确定的具体工程结论运行定向检查，不追加 live 或实际 Agent 验收。

| 验证 | 入口、输入及当前责任 | 预期观察及证明边界 |
| --- | --- | --- |
| V819-01–02 | 既有真实 Sync/Readiness/局部/Creation 生产 wrappers；修复后运行 `python3 -B trellis/skills/guru-team/runtime/tests/test_issue_review_intake.py IssueReviewIntakeTests.test_real_sync_preserves_synced_source_kind IssueReviewIntakeTests.test_dedicated_sync_refresh_preserves_fixed_source_and_issue -v` | 未改写的真实 Sync stdout 先满足 Interface 声明的 direct consumer，再薄投影和回同 Issue Readiness；来源种类/selected_ref/commit、独立集成目标及 acquisition 保持。其他已覆盖分支采用原报告，fixture 不等于 live/Agent。 |
| V819-03–04 | 采用现有 `test_issue_review_intake.py`、受影响 Intake/Discovery/Create 回归、评论与 source_actions 实现，以及 Test 报告中的已取得 live 结果 | 评论动作顺序、准确覆盖、只读无写和同对象恢复继续成立；未实际观察 live PATCH/unknown/补发的路径保持未验证，不另造对象。原失败及其后续修复事实不被改写。 |
| V819-05 | 完整原实现、已有 Agent 分流/讨论/no_issue 观察及当前 Creation 桥接 | 各终点、正式 Issue 汇合、仅必要补审和原 Task 门禁由代码与已取得层级分别支持。创建后 live 正向 Task 写前、完整 start/selector 和其他平台 Agent 未验证，不再追加验收或创建后继任务。 |
| V819-06 | 采用原 public graph/examples、分发/reapply、matching tools、installed/native/drift、mode/sidecar 和 Task/session/用户保留结果 | 实际安装差额才由原 tools owner 更新；本次仅改规划正文，不重复不变安装。canonical/installed 一致不证明 Agent 行为、正式 source-lock 或其他业务采用。 |
| V819-07 | 原知识整合/readback、当前 TaskCommit、独立 committed Review、Delivery Review及Task收尾 | 原 owner 亲自判断当前 accepted scope、完整固定 B..H、必要定向检查和证据边界；代码修复、Review、合并与 Task Completion各为独立结论，不预填后续通过。 |

原 Test 报告唯一定位既有观察和历史失败；原始 stdout 不可取得的早期工程仅按报告层采用，不补造执行记录或重跑旧全集。新修复事实以原执行者实际命令及结果判断。定向检查的条件、动作和结果来自 accepted 行为，不镜像实现常量，不修 producer 输出或手填被测 producer 结果。

完整多平台 Throwaway、官方 upgrade/update/Release 矩阵、formal Fork source-lock、其他业务仓采用和生产效果均未建立，本 Task 不新增这些验证义务。证据足以支持当前层级且没有新差额时结束检查；所有未观察事实继续明示未验证。

## 4. 停止条件与适用回退点

- Task/key/generation/checkout不符，或实际phase不是原步骤合法状态：回原Identity/Ensure/Bind/Selection，不手改状态或创建第二Task。
- Direct Source/范围/来源角色出现真实变化：原Clarify处理；只影响当前技术方案则回原Author/Architecture并刷新最早受影响gate。无关main前进或时间经过不重启整个规划。
- 新机制、必要字段或新外部consumer超出design：先审实际必要性；需要兼容例外时按原subtraction-first展示真实consumer及退出，不默加fallback。
- 外部写入对象/payload不明确或未在当前动作范围：停在原副作用预览；未知结果先恢复已有对象，不能为测试重复创建/评论。只读验收不触发mutation。
- 已有观察或必要定向工程检查发现当前失败：保留真实失败和边界，修最早受影响 owner；设施反复失败时判断具体工程结论所需的复现方式或证据缺口，不改断言制造通过，不将这一规则扩成新增 live/Agent 验收。
- shared expected-current或sidecar冲突：原maintenance/installer owner判断实际差额，保留并行改动；Planning不覆盖共享current。普通本地未提交修复可按精确本Task文件撤回，不能revert别人改动。
- 无业务数据库或运行部署数据迁移，不设计数据库回滚。知识部分写入由原唯一intent恢复；外部Issue/comment成功事实不能因本地回退抹除。
- 当前代码/定向验证责任已有足够证据且无新差额时停止追加检查，进入原质量链；未观察的外部或 Agent 场景不预填通过，也不再构成追加验收义务。后续每次 merge 前停交协调会话。

## 5. Delivery Policy（唯一）

policy=full。D1 共同交付整体 R1–R7 的全部评论生产/消费、已有 Issue 先行 Readiness、三个补审返回、讨论/草稿/创建终点、no_issue 保留及公共迁移/恢复/分发。功能没有延期到后继 Delivery，整体 AC5 仍由原交付与 Task 收尾完成；D1 合并不能自行代替 Task Completion。

当前 AC1–4 的验证责任以整体 PRD 第7节为准：采用已取得的实际观察、仍适用工程报告和必要定向修复检查，不再要求新增 live 或实际 Agent 验收。创建后 live 正向 Task 写前、PATCH/unknown、完整 start/selector和其他平台实际 Agent 未验证；这些事实不改称通过，也不作为后继验收工作。未改变的代码和安装不因规划修订重新执行。

当前规划仍经原 Wording、Architecture final_plan、Approval、展示和 Activation，之后完成必要文档提交、完整独立 Review及Delivery/Task收尾。各 Git/GitHub 副作用由原 owner 展示精确动作并执行其边界。没有新增业务功能、版本绑定、临时能力限制或整个 Task 冻结。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。implementation先在本Task隔离拟写中形成完整目标，原maintenance owners在提交前final_integration整合/readback；TaskCommit后一次独立committed Review审核真实after。当前规划不得直接写共享current或声明reviewed_promoted。

| 真正命中定义 | 本批差额与完整单元 | 原writer、直接consumer与时点 |
| --- | --- | --- |
| docs/requirements/current/local-fix-intake.md：R692-02 / BEH692-REUSE；docs/design/current/local-fix-intake.md：D692-01 / CON692-OWNERS；docs/test/current/local-fix-intake.md：T692-01 / SC692-ROUTE/REUSE | 保留事实适用性/普通诊断；窄替代已有Issue固定全链条件，完整写新先行/局部返回/必要全链/阻塞及真实验证边界。保持原stable aliases，不另留第二current正文。 | 原guru-maintain-requirements-design-test-ssot；直接consumer是后续Intake owners及当前独立Review；实施完成后的原final_integration。 |
| docs/{requirements,design,test}/current/issue-content.md | 保留#818完整内容方法；补最小评论单一正文来源、准确覆盖及Readiness消费关系；配对Test只写实际观察，旧未知/失败保原截止。 | 同上原RDT owner；不修改旧Task/PR/原始证据，不向README登记普通独立主题。 |
| docs/architecture/contributions/819-issue-review-intake/contribution.md及issue-review-intake.md | 原Author真实task-owned架构贡献/ADR候选，design §4–7是完整设计定位；实施期形成拟03-domains/issue-review-intake.md及adr/issue-review-intake.md完整after，九concerns与before保持。 | Author只写隔离候选；Planning直接consumer是原独立final_plan；共享晋升只属guru-maintain-architecture-baseline，之后原committed独立Review。 |
| workflow、七包references/SKILL、两README、MIGRATION-819及真实受影响launcher/overlay | 修改本身是可执行合同与使用说明，随各原owner实现同步；不得与RDT/Architecture current形成互相矛盾的两套流程。 | 原workflow/package writer；安装投影由原tools owner，真实消费者是安装Agent和public runtime。 |

普通主题不改Architecture根/system/ownership/ADR index或RDT共享导航；只有其自身发现/身份关系真的变化才交原owner处理。保留固定B的晋升前authority和真实proposed来源；shared writer写前reread仍有效条件及target，不用新CURRENT为自身证明。当前未形成实施/安装/外部结果，所以配对Test与架构候选明确pending；后续原owner记录实际截止即可，不为追写自己的最终SHA/Review结论增加文档提交。


本次验证范围修订不改变共享功能、设计、可复用测试策略或 Architecture 决策，无新增知识定义差额。原整合内容继续进入当前独立 committed Review；不为追写其最终结果或重复观察增加共享知识写入。
