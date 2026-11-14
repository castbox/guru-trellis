# D1 Issue 审核评论与 Intake 分流实施与验证计划

## 1. 输入与引用

整体范围为 ../../prd.md 第5节完整来源、R1–R7、SC01–12、AC1–5；本批以 prd.md 的全部D1要求/场景为输入。design.md 第3节是唯一来源设计处置，第5节拥有实际profile/逐出口DTO，第6–7节拥有顺序与恢复/迁移；实施前读完整相关条件，不从接口名称自行补语义。

起点B与H0同为4f2adef1f7b099f78bb8429e8b8facd66dce3bfc；没有前序Delivery。固定开发来源origin/main，集成target=main；当前key为819-issue-review-intake/gen0/f108d161-d60d-4c89-91bf-d96004ef86a6。独立Architecture candidate_assessment为architecture_impact/target_native，决策ADR-ISSUE-REVIEW-INTAKE；真实final_plan与Approval尚需由原owner完成，文件存在不表示激活。

必要工程规则为 .trellis/spec/workflow/{workflow-contract,skill-package-contract,quality-guidelines,subtraction-first-compatibility,clear-technical-writing}.md 及 .trellis/guru-team/skills/packages/guru-author-task-plan/references/planning-body.md。Architecture authority/constitution/change-contract和RDT两个完整命中单元见design §9。Trellis官方首页、custom-workflow、custom-spec-template-marketplace已用于确认扩展面；实施不改上游源码或hook分叉。

ready的真实创建consumer按原Create Task SKILL和Interface加载schemas/public-delivery-task-creation-input-2.0.schema.json、共享contracts/task-lifecycle/task-creation-input-3.0.schema.json及MIGRATION-813。design §5.1–5.3单写来源三字段、独立集成/交付目标、原acquisition和同步/恢复条件；实施前实际加载当前选定版本，不用保留的旧1.0 schema替代。

## 2. 有依赖顺序的步骤与文件责任

本表是后续实施安排，本轮不执行。每批Task写入前执行原checkout boundary；原implementation owner保持同Task/key，不重建资源。

| 步骤 | 依赖、owner及真实文件 | 实际改动及完成观察 |
| --- | --- | --- |
| I819-01 | Activation后；原workflow与各package owner；trellis/workflows/guru-team/{workflow.md,references/routing.md}，trellis/skills/guru-team/packages下Sync/Readiness/Discovery/Clarify/Wording/Create Issue/Create Task各SKILL、references、interface、schemas、runtime、examples | 按design §5明确独立profile/output及consumer；Sync read/sync归一化真实base_source三字段，新ready只向当前Create Task投reviewed_base_source，集成/交付branch由原owner独立审定。保原source/acquisition及同步/恢复条件，不恢复已移除公共字段、不复制旧transition；原confirmation/draft/no_issue保真实用途。AI owns判断，runtime不实现分流推理。 |
| I819-02 | I01的输入/出口已明确；原Readiness与三个局部owners | 实现existing_issue_intake/issue_review_return及三个issue_readiness_supplement；Clarify额外事实、Wording需求变化及基线刷新返回均保持真实来源kind和精确对象。必要全链消费原Sync transition，不从三字段反拼。生产wrapper用真实producer结果返回并进入当前Creation；普通stale/mismatch回原owner。 |
| I819-03 | I01评论合同；原Clarify/Create Issue | 新增Clarify-owned references/issue-review-comment.md一份正文；Create2.0接AI已审review_comment_body，正式内容读回后评论POST/GET再created；recover定位原Issue/评论。Clarify引用同规则，复用source_actions的POST/PATCH/readback，只读不写。每个结果保真实部分完成事实。 |
| I819-04 | I01–03；原公共合同/分发owner | 更新实际受影响registry、production manifest、shared runtime消费者和examples；新ready示例接当前Create Task profile2.0/creation3.0，保来源/目标区分；现有正确#813例子保持其原适用性。新增trellis/presets/guru-team/MIGRATION-819.md，逐项旧新schema及consumer切换、固定旧操作恢复。核旧资产真实consumer；失去current用途的branch/entry同批退出，不增长期dual-reader。 |
| I819-05 | I01–04；原工程验证owner | 扩充下节定向长期测试并执行生产入口；实际Agent复核、评论内容和live动作分层取证。实验证据以其原边界采用，缺真实外部对象时保留AC缺口，不造新Issue或擅自发布。 |
| I819-06 | canonical完成；原guru-upgrade-tools及installer | 完整matching更新当前checkout工具/workflow/Skills，保Task/session；按原sidecar owner处理每个.new/.bak；同步本仓dogfood和声明平台，执行drift和定向reapply，核mode与用户内容。不得手工覆盖受管副本或借apply旧Task阻塞绕门禁。 |
| I819-07 | 完整实施及真实工程结果；原RDT和Architecture maintenance owners | 执行§6的delta_first及隔离完整Architecture拟写final_integration；重读live expected-current、整合仍有效条件并readback全部真实targets。贡献/ADR和知识after均进入后续同一内容候选。 |
| I819-08 | I01–07；原TaskCommit、implementation与独立Review owners | 原本地TaskCommit纳入完整after；固定B/H构造committed Candidate和begin_check；新的独立reviewer完成一次Architecture before/after及完整Review。后续修复形成后继本地提交和受影响独立补审。通过后才原Delivery Review/readiness→Publication；本表不预填通过。 |

允许改动仅本Task范围、上述原owners及真实受影响受管投影。共享知识只在I07由原owner写；不修改其他Task、#808或发布事项，不扩大到全仓旧测试清理或完整矩阵。后续merge前停交协调会话。

## 3. 验证入口、输入与预期观察

V819-01–07的独立行为断言见design §8。以下给实施者的可执行入口；先读当前测试支持参数再执行，不把旧命令假定成新公共API。

| 验证 | 入口及输入 | 预期观察、对应验收和限制 |
| --- | --- | --- |
| V819-01–02 | 原生产packages/*/scripts/invoke.sh及record/check；真实Sync read或sync stdout→本项新入口/局部producer→ready→原Create Task公开入口，在临时Git fixture内使用当前profile2.0/creation3.0。扩展test_intake_profile_integration.py，执行 python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p test_intake_profile_integration.py | 六类分叉、三局部/Clarify事实/刷新返回保来源三字段；固定对象来源ref与独立集成main分开，即使local main已前进也按精确commit取得Task，原primary内容保持；实际sync保来源branch身份及新建HEAD条件，成功恢复不因后来HEAD前进重复创建。必要全链用真实transition；不直接造supplemented或修被测producer输出。复用#813原内部覆盖，只补新桥接边，fixture不替代实际AI观察（AC2/AC4）。 |
| V819-03–04 | 原Create2.0和Clarify公开入口；在trellis/skills/guru-team/runtime/tests/test_issue_review_intake.py新增窄测试，复用原gh替身。执行 python3 -m unittest discover -s trellis/skills/guru-team/runtime/tests -p test_issue_review_intake.py，再执行同目录的test_intake*.py受影响回归 | 创建→正式readback→评论→readback→created；失败/未知结果恢复同对象；Clarify局部不冒称全审、只读无写。隔离替身不宣称live写入（AC1），不建立第二测试框架。 |
| V819-01–05的Agent部分 | I06完成matching采用后，通过原start/selector/Sync入口执行获选正常对象；实际读取Issue/评论，按充分性选择路线；分别观察局部返回、必要全链和阻塞恢复、讨论/草稿/仅创建终点、原no_issue | 以实际调用顺序和完整答复核是否只做必要步骤，不能只断言Markdown包含规则。测试对象和初始事实由真实受支持入口产生，不代造被测producer结果（AC2/AC3）；I07前完成这些实际观察。 |
| V819-03–05的外部部分 | 后续原Create/Clarify owner展示精确repo/Issue/评论及正文，范围满足后运行原repo-bound gh POST/PATCH和GET readback；unknown结果走原recover | live评论准确、对象一致、已成功对象不重复，创建并开工消费正式Issue和实际评论。当前未选定且未执行任何外部验收动作；此部分不能被mock替代，缺口会阻止对应AC完成，不阻止当前写可实施计划（AC1/AC3）。 |
| V819-06公共合同 | 复用trellis/skills/guru-team/runtime/tests/test_intake_projection.py、test_intake_semantic_authoring.py、test_discovery_exits.py和生产public graph/examples检查入口；以真实各profile结果运行reader | 每个producer→consumer projection能实际接收；所改schema/Interface/manifest/examples匹配；不只比较常量或增加“字段存在”自证。仅扩受影响部分（AC4）。 |
| V819-06分发 | python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p test_issue_content_distribution.py；再运行test_public_skill_examples.py、test_public_example_installation.py的适用定向入口；bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh | 共用评论规范和受影响Skill真实安装/reapply可用，mode、sidecar、声明平台投影、Task/session与用户内容保持。由原tools owner做正式更新，测试不替其授权或恢复判断（AC4）。 |
| V819-07 | 原trellis-check/committed独立Review/Delivery Review及Task Completion入口，分别消费真实工程、committed before/after和交付结果 | 全部要求及配对知识完整；按真实质量结果决定继续。未执行不能写pass；本轮无Activation/工程/交付证据（AC5）。 |

长期回归保不同动作/结果边界，不按排列组合扩样本。实际Agent与外部观察属于本项真实验收，不建评测系统或固定计时指标。已有完整链/source-selection/qualification测试继续采用；新Readiness无前序、局部producer返回、评论终点是必须补的实际缺口。静态声明检查只证明分发/引用，不能证明语义。

完成低成本接口检查后再做较高成本行为/安装观察。追加诊断必须指向尚未解决的问题及预期可观察结果；不要求历史版本必红或重复回退。未覆盖完整多平台Throwaway、官方upgrade/update全矩阵、Release Gate和生产效果；本项只做与差额匹配的package/installed/reapply/平台/sidecar/mode证据。

## 4. 停止条件与适用回退点

- Task/key/generation/checkout不符，或实际phase不是原步骤合法状态：回原Identity/Ensure/Bind/Selection，不手改状态或创建第二Task。
- Direct Source/范围/来源角色出现真实变化：原Clarify处理；只影响当前技术方案则回原Author/Architecture并刷新最早受影响gate。无关main前进或时间经过不重启整个规划。
- 新机制、必要字段或新外部consumer超出design：先审实际必要性；需要兼容例外时按原subtraction-first展示真实consumer及退出，不默加fallback。
- 外部写入对象/payload不明确或未在当前动作范围：停在原副作用预览；未知结果先恢复已有对象，不能为测试重复创建/评论。只读验收不触发mutation。
- wrapper、实际Agent或分发验证失败：保留真实失败和边界，修最早受影响owner；设施反复失败时重评复现方式，选择设施修复、等价直接观察或明确证据缺口，不改断言制造通过。
- shared expected-current或sidecar冲突：原maintenance/installer owner判断实际差额，保留并行改动；Planning不覆盖共享current。普通本地未提交修复可按精确本Task文件撤回，不能revert别人改动。
- 无业务数据库或运行部署数据迁移，不设计数据库回滚。知识部分写入由原唯一intent恢复；外部Issue/comment成功事实不能因本地回退抹除。
- 必要行为和受影响回归已有足够证据且无新差额时停止追加测试，进入原质量链；未解决的外部验收或真实分支缺口不能预填AC通过。后续每次merge前停交协调会话。

## 5. Delivery Policy（唯一）

policy=full。D1共同交付整体R1–R7的评论生产/消费、已有Issue先行Readiness、三个补审返回、讨论/草稿/创建终点、no_issue保留、公共迁移/恢复/分发，以及AC1–4所需真实验证。整体AC5仍由原交付与Task收尾链完成；它已在本批scope_ref内，不被规划通过或D1合并替代。

没有延期到后继Delivery的实现能力或额外版本绑定。当前只到可审阅规划；后续须实际Activation、I01–08、真实外部/Agent证据、原完整Review/readiness/交付及Task Completion/Closure/Finish。未完成外部验收不是临时删减要求，也不是让源码和mock通过直接算full完成。没有新增临时环境限制或冻结整个Task的安排。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。implementation先在本Task隔离拟写中形成完整目标，原maintenance owners在提交前final_integration整合/readback；TaskCommit后一次独立committed Review审核真实after。当前规划不得直接写共享current或声明reviewed_promoted。

| 真正命中定义 | 本批差额与完整单元 | 原writer、直接consumer与时点 |
| --- | --- | --- |
| docs/requirements/current/local-fix-intake.md：R692-02 / BEH692-REUSE；docs/design/current/local-fix-intake.md：D692-01 / CON692-OWNERS；docs/test/current/local-fix-intake.md：T692-01 / SC692-ROUTE/REUSE | 保留事实适用性/普通诊断；窄替代已有Issue固定全链条件，完整写新先行/局部返回/必要全链/阻塞及真实验证边界。保持原stable aliases，不另留第二current正文。 | 原guru-maintain-requirements-design-test-ssot；直接consumer是后续Intake owners及当前独立Review；实施完成后的原final_integration。 |
| docs/{requirements,design,test}/current/issue-content.md | 保留#818完整内容方法；补最小评论单一正文来源、准确覆盖及Readiness消费关系；配对Test只写实际观察，旧未知/失败保原截止。 | 同上原RDT owner；不修改旧Task/PR/原始证据，不向README登记普通独立主题。 |
| docs/architecture/contributions/819-issue-review-intake/contribution.md及issue-review-intake.md | 原Author真实task-owned架构贡献/ADR候选，design §4–7是完整设计定位；实施期形成拟03-domains/issue-review-intake.md及adr/issue-review-intake.md完整after，九concerns与before保持。 | Author只写隔离候选；Planning直接consumer是原独立final_plan；共享晋升只属guru-maintain-architecture-baseline，之后原committed独立Review。 |
| workflow、七包references/SKILL、两README、MIGRATION-819及真实受影响launcher/overlay | 修改本身是可执行合同与使用说明，随各原owner实现同步；不得与RDT/Architecture current形成互相矛盾的两套流程。 | 原workflow/package writer；安装投影由原tools owner，真实消费者是安装Agent和public runtime。 |

普通主题不改Architecture根/system/ownership/ADR index或RDT共享导航；只有其自身发现/身份关系真的变化才交原owner处理。保留固定B的晋升前authority和真实proposed来源；shared writer写前reread仍有效条件及target，不用新CURRENT为自身证明。当前未形成实施/安装/外部结果，所以配对Test与架构候选明确pending；后续原owner记录实际截止即可，不为追写自己的最终SHA/Review结论增加文档提交。

