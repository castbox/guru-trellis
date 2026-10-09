# #404 候选设计

## 候选结构与职责
以下描述是设计对象，不是合规/完成结论。
沿用 Architecture 2.0 的四个 profiles 与七个 declared exits。Architecture Skill 的 semantic responsibility 不变；当 task_impact_sync 的 Planning、implementation_discovery、Phase2、branch_review 需要新的评估时，由未参与候选编写/实现、未预载任务叙事的 subagent 执行该 Skill。主会话协调 dispatch、候选 freshness 与修订，不 author reviewer 的结论。shared CURRENT 与 serialized promotion 继续属于现有 owner。

### Step-local Architecture 入口
canonical owner 为 trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/SKILL.md 与 references/contract.md。短 Skill 只声明加载、profile 路由和 entry；详细 reviewer 方法归 contract 唯一来源。
评估 caller 提供 repository/task locator、stage、候选设计定位或 full diff 的 exact base/head、必要 authority/约束来源，不提供期望 pass、impact 判定、PRD/验收/实现总结。Planning 读取 design.md 的设计事实；其 scope/验收/自述结论不成为架构 authority。不制造第二份长期设计文件。
fresh generic worker 使用空任务历史；不得使用自动预注入 task narratives 的 trellis-check/implement/research role。当前 Codex SubagentStart matcher 仅匹配这三类，generic dispatch 可避开其叙事注入。其它平台使用官方提供的 fresh Task/Agent/subagent 能力，并核对实际 prelude；没有满足边界的能力时返回既有 blocked，不 patch 官方 hooks/agents。只用改角色名称不能证明输入隔离。
worker 先读取项目 constitution/baseline，再实际候选、共享行为改变、真实消费者/状态装配、同类能力及约束。此时形成独立结论，之后仅当独立判断须核对变更归因或约束来源时读取对应设计解释/contribution，核对归因和责任。新业务约束若只存在 task，caller 只给必要事实与来源；reviewer 不读整份完成叙事。第一轮如缺设计对象、必要 authority/约束/证据，走已有 incomplete/blocked，不能以先前 pass 代替。
reviewer 自己执行适用 project checks，按既有 semantic-result schema author 最小 result，自己调用既有 formal wrapper。wrapper 保持 schema/identity/freshness/linkage/consumer validation；独立性由实际执行与输入证明，不新增 reviewer_pass、agent_id 或 digest 作为替代。
正常主会话自填 owner_result 可能仍通过结构检查；该结果不满足 Markdown 调度合同，caller 必须回合规 fresh 评估，不把结构失败强行扩展成攻击防护。

### 职责与任务必要性方法
reviewer 从实际变化分析决策 owner、通用层是否承载业务语义、default 是否影响未修改 caller、状态读写/装配/依赖方向和同类能力真实差异；不能仅用声明 owner 一致或技术关键词判定。现有错误被本次扩展/固化时，独立说明 before/after 因果及必要局部收敛；无关历史偏离保持如实证据而不自动 current P0-P3。
Planning/实施协调/Check/Branch Review 的现有 semantic owners 在扩展写入、测试、severity、revision route 前分别判断问题成立、任务必要与机制适合。以当前目标/受影响合同的反事实约束判必要性，保留必要重构、调用方同步迁移和旧路径退出；拒绝复制逻辑、跨层 branch、第二 authority、无退出兼容。
资格 owner 的 normal-scenario 与 mechanism 判断保持独立，不把真实职责偏离要求为先发生功能失败；架构合同本身及可复现候选变化可构成 required-behavior defect。无关债务/红测只有限只读取证，经当前目标或受影响合同证明不可分割的前置/本次回归必须处理；未归因保留不确定性。默认/推荐/合法范围/硬不变量取现有 authority，诊断缺标签不升级为业务拒绝。原则与测试价值正文继续由既有 constitution/quality authority 独占。

### Stage 与 consumer
| 调用位置 | 候选 | 执行与接续 |
| --- | --- | --- |
| Planning | 真实 design facts + 受影响既有实现 | fresh Architecture wrapper 的 current 结果进入 guru-approve-task-plan |
| implementation_discovery | 资格通过后、扩展修改前的实际变化对象 | fresh reviewer；现有回程后才能恢复写入 |
| Phase2 | 完整 tracked/untracked worktree candidate | fresh reviewer 先专项；可再读取 PRD 执行 guru-check-task，两个结果分开 |
| Branch Review | exact committed base/head/full diff | 新的 fresh reviewer 独立重算；可以先专项再整体，不能继承 Phase2 pass |
| Delivery/Completion | 原阶段仍 current 的独立结论 + eligibility/live facts | Architecture owner 亲自完成 publication/acceptance_finish eligibility 与 formal wrapper，产生匹配 stage/source_profile/freshness 的结果；不因为 caller 改变重复同质评估 |
| promotion/finding-fix | 既有 owner 产生的新 diff | 原 Phase2/TaskCommit/full BranchReview 接续，无新增 state machine |

下游的薄接续保留2.0：原Architecture owner读取仍current的独立结论与已审contribution及live authority/candidate/committed review/promotion事实，作本stage eligibility判断并亲自调用既有formal wrapper。只复用仍适用的独立判断，不重做同质取证；该调用不把主会话变成新的架构评估者。缺committed review、authority/candidate变化或未promotion时，返回对应existing owner route；若须形成新的架构判断，先回对应stage fresh独立评估。主会话只消费真实匹配stage输出，不改写/relabel branch_review DTO为publication/acceptance_finish，不能以Phase2替代committed判断。

workflow 只显式 mandatory invoke stable Skill 与消费 exits，不复制 reviewer 内部方法。#292 Planning author/Approval 责任不重分配。平台 entry 只加载与调度，方法不分叉。
current/missing/stale/conflict/regression/promotion 路由沿 live Interface；不得全部变成 Planning，也不将 blocked 映射为 passed。Worker 未运行、未完成、missing/mismatch 或平台不能隔离时，以现有 blocked/re-entry 处理；mapped 修订自动接续，无新的例行确认。

## 直接演进与兼容
直接替换当前主会话自评/预载叙事方法，受控消费者和 eval 同步修改；删除失去唯一支持用途的旧预填 no-impact/required narrative authoring staging。保留真实 post-owner wrapper 单元证据，但明确不作为独立 semantic 行为证明。
本设计不改 Architecture 2.0 DTO/schema、stable skill/profile/exit/consumer identity，不增加长期旧路径、fallback、dual-read 或 schema alias。Markdown 方法加强通过完整 preset 单元更新，同步安装副本；旧安装须官方 reapply/upgrade 消费 current package，不能混用新方法和旧 adapter。若实施发现确需公开 I/O 破坏变化，停止受影响修改，经现有 qualification/Planning 明确 migration；本计划不预授权该扩张。
备选：新增 Architecture Review Skill/ledger、script 推断合规、仅平台 prompt patch 都会引入平行 owner/authority 或漏掉其它 entry，因此不选。保持原主会话自评不能提供独立取证。

## 行为评测设计
复用 existing eval runner、native adapters、formal wrappers、semantic grading 接点；fixture 只携带去敏实际 source/design/diff/consumer/长期 authority 与需要的最小约束，不提供 reviewer 结论或 expected exit 叙事给 worker。expected outcomes 属于 grader 侧。没有真实候选的用例只支持 incomplete/blocked，不能 staging 一份 pass 当行为 proof。
受影响处包括 architecture planning semantic-authoring staging，以及 Phase2 authoring 中由同一 Agent 自填 Architecture 的原路径。将其演进为真实 fresh reviewer-first 执行：优先当前平台原生 generic subagent；native CLI eval 使用受支持的 fresh worker 启动边界，实测确认不注入任务叙事。脚本只能确定性建 fixture、启动既有 native provider/transport、记录客观 dispatch/read/invoke/stdout 与消费顺序；不 author judgment、不选 pass、不制造新调度状态机。
native 可观测项为 fresh dispatch 无历史、实际 read 顺序与完整候选/真实消费者覆盖、独立结论之后才读解释、reviewer 自己调用 wrapper、整体 owner/下一 consumer 接续。行为 grader 按 A404-01..10 语义判断“多做/少做/hack/误拒绝”及因果归属；静态 checks 只确认结构/投影/路由链接，不代替上述 proof。
native eval adapter/trace helper若需机械扩展，只为新执行边界所需事件与薄确定性链接，临时 eval evidence 随既有 runner 生命周期管理；不新增公共 reviewer 审计字段/长期 transcript。真实 native 无法执行则记录 accepted scope evidence pending/block，不能由 mock 代替。选定平台的真实执行与其它平台投影一致证据分别报告。

## Docs SSOT Plan
策略：delta_first。
Requirements/Design/Test current locator 为各层 README，knowledge current 为 current-main-0.6.17-guru.77。Phase2 用 docs/requirements-design-test-contributions/404-independent-architecture-review/ 承接 requirement、design、test、traceability 增量；Test 是结果唯一 authority，其余只引用。通过 guru-maintain-requirements-design-test-ssot 的 task_impact_sync/promotion 在最终 Phase2 check 前合并 durable authority，不直接竞争 shared current。
本候选改变评估执行与下游consumption合同，Planning先形成task-owned docs/architecture/contributions/404-independent-architecture-review.md，承接九concern、唯一target_native候选path、owner/兼容/parallel/deviation/before-after/project-check/evidence/expected-current。同时形成同目录404-independent-architecture-review-adr.md候选决策，记录执行者隔离与matching-stage eligibility改变，状态draft，非current authority。独立Architecture owner仍自主判impact/path、ADR必要性和route；它通过前不能把contribution写作已审/promotion。Planning committed review为pending/false/null，promotion为required/空identity；实现/native证据未验证。review后原ownerexpected-current promotion，promotion-created diff 返回 fresh Phase2/commit/full review。
同步 README.md、trellis/workflows/guru-team/README.md、trellis/presets/guru-team/README.md 的实际用户行为说明，导航指向唯一合同；不复制 method/constitution/质量正文。既有版本/任务/ADR/历史证据保持 immutable，不顺带清理其它历史陈述。docs_ssot_subtraction 明确退役主会话 authoring 作为独立 proof 的说明，保留仍有 wrapper consumer 的事实检查。

## 预期修改边界与验证
canonical Architecture contract；按实际 consumer 缺口修改 guru-approve-task-plan、两资格 owner、guru-check-task、guru-review-branch、Delivery/Completion 的 step-local消费；canonical workflow 的 mandatory stage/dispatch 与实施协调接点；承担 Architecture/Phase2 authoring 的 native eval adapter/staging/helper、真实行为 corpus 与 regression tests；三 README；task/RDT/Architecture 必要增量。
通过官方 apply.sh 同步 installed、Shared、Codex、Claude、Cursor dogfood managed projections，canonical workflow 同步 .trellis/workflow.md。其它声明平台以 descriptor 驱动相同 package 投影，不复制方法到平台 entry，不改官方 trellis-*。
最小验证集：受影响 package/runtime 和 eval helper 测试，source/installed graph/schema/unique-consumer，真实 native 行为，apply/reapply/drift/ownership/sidecar/manifest-selected projection，git diff --check。clean installation 仅在修改 installer/projection且确需新装证明时一个代表性 throwaway；完整平台 Upgrade/Release matrix 由专门任务承担。本次不修改部署/业务运行配置/DB/K8s/容器/生产。
