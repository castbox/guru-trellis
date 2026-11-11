# D1：qualifier 条件加载与调用设计

## 1. 设计目标、需求承接与内容基线

本批覆盖 [PRD](prd.md) D1-R1—R6、D1-AC1—AC4，对应整体 R1—R6、AC1—AC4。目标是让原 caller 先判断各 qualifier 是否适用，按条件加载、调用或采用结论，同时保留各阶段完整判断。

development baseline B 为 `e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e`，来源是本 Task Intake 选定并核验的 main/origin/main。Planning H0 同为该 SHA；H0 只是观察值。D1 内容范围采用固定 B 到实际实施 HEAD 及当前 dirty increment；不包含 Task/session/private result。PR target 独立固定为 main，不以未来 main 前进重选 B。

独立 Architecture 实际 candidate_assessment 已返回 `baseline_current / architecture_impact / target_native`，decision_refs 为 ADR-008、ADR-020，candidate freshness 为 `sha256:ae9479ec980357d83f0154c5163f066d841d11e8533c656180565e5e097ab29b`。本设计展开该候选，不代表 final_plan 或实施通过。阶段适用 authority 为 `docs/architecture/00-foundation/{baseline,design-constitution}.md`、`docs/architecture/06-governance/change-contract.md`，身份分别为 `guru-trellis-architecture`、`guru-trellis-design-constitution-v1`、`guru-trellis-architecture-change-contract-v1`。

## 2. 当前系统、边界与目标差额

D1 是首次切片，没有前序交付。当前十类 lifecycle 候选边界在 workflow 和 caller 中要求 normal/solution 调用；Author 另有既存 `author_candidate_set`。Check 已有空候选不调用，root 已有不变机制结论采用。root 的 Markdown 前置仍要求实际 normal/solution outcomes，公开输入本身只携带 refs/locators，不携这两个上游对象。

本轮差额是：三个 qualifier 各自提供可独立读取的适用条件；十一处实际候选边界先分别判断是否触发；root 接受本 caller 当前场景和 authority-placement 判断以及真正触发的上游结果。未触发不装配输入、不加载全文、不制造 classified/empty/skipped 输出。原阶段照常审查需求、实现、测试、严重度、充分性及路由。

不合并三个 owner，不改未受影响资格算法、目标枚举或生命周期。身份组合、Check/Review 合并、发布合并和归档时序属于其他范围。

## 3. 来源设计处置（唯一）

| 来源与原承诺 | 处置 | 本设计落点、理由与影响 | 上游处置 |
| --- | --- | --- | --- |
| ADR-008 Decision：normal 独占场景，solution 独占 authority placement；脚本只验事实 | retain | 第4、5节保留三 owner、语义闭环和原消费者 | 无偏离 |
| ADR-008：OS/kernel/process/descriptor 不得承担业务 authority；普通文件 I/O 可用 | retain | 第4节条件覆盖全部 authority 机制；触发不依赖 OS 关键词。正式 solution 仍判断合格性 | 无偏离 |
| 三 qualifier 当前完整合同及 workflow：非空候选边界固定 normal→solution，root 要求两者实际 outcome | change | 第4—7节改为独立适用条件；root 使用真实 caller 判断及适用结果。取消为满足下游而产生的无关调用 | 本 Task #793 正文授权；以 MIGRATION-793 与隔离 ADR 候选说明窄替代，经原 Architecture 晋升 |
| normal/solution 当前 Re-entry：target、caller、范围或文件身份变化普遍 fresh invoke | change | 第6节区分新调用事实绑定与语义适用性；阶段/caller 或无关字节变化不重审同结论，材料变化刷新受影响项 | #793 行为4；原 facts 校验继续，迁移说明新调用不复用旧 invocation envelope |
| ADR-020：真实新建/实质变化诊断、缓解、修复、保护进入 root；不变机制采用仍适用结论 | retain | 第4、6节先判适用性，保 root 目标感知方法和原非通过回程 | 无偏离；ordinary feature 原分类仍兼容真实已进入的调用 |
| 三原 Interfaces/schemas/consumers：固定 profile/caller、非空候选、最小 refs 输出和唯一消费者 | retain | 第5节不新增字段、exit、结果存储或 caller；仅同步实际改变的语义前置、说明及示例 | 成套 matching 安装；若实施发现真实 wire 差额，回原设计/Architecture，不静默改接口 |

## 4. 模块、职责与设计取舍

### 4.1 owner 拥有的加载前条件

分别新增三个原包内 `references/applicability.md`。每份只拥有本 qualifier 的触发、采用、刷新和加载动作条件，能直接读取；`SKILL.md`、完整 contract 和 caller 引用该文件，避免另抄一套条件。Interface 声明相应公开 reference。没有新 Skill、脚本 classifier 或统一问卷。

原 caller 读取当前 authority、真实工作和这些短条件，判断是否需要专属 owner；此处不提前给出 qualified/rejected、因果充分性或机制合格 verdict。满足触发条件且没有仍适用结论时，显式加载原 stable Skill 完整合同并调用。不能通过故意不提出真实候选来规避判断。

| owner | 触发条件 | 可省略的工作与保留边界 |
| --- | --- | --- |
| normal | 存在新建或实质改变的真实场景准入候选：原 owner 要将某种行为新增为 scope/acceptance/test/finding/implementation/blocker 的义务，且其 authority、支持的诚实入口、复现或当前 Task 必要性仍需专属准入判断；包括实际观察到的职责合同缺陷及争议范围 | 已清楚接受的普通工作、常规核验或已采用且适用的场景不构造形式候选。候选涉及明确排除、合法 stale/mismatch、secret/权限例外时仍按本条件及原完整合同处理，不能以安全标签直接省略判断 |
| solution | 拟采用或实质改变的机制实际承担业务决定、证明、拒绝或执行资格的 authority，例如 identity、state ownership、并发、cancel/recovery、inspection/monitoring、publication 或 evidence；或发现真实 authority placement 冲突 | 普通纯计算、文本/导航修订及普通状态 I/O 若不承载这些 authority，不因“会影响正确性”自动触发。检查实际职责，不按文件名、OS 词或技术类别判定 |
| root | 新建或实质改变的真实诊断、缓解、根因修复或保护机制；普通 feature 中含这些实际行为也触发 | 纯普通 feature 无事故/保护机制时不加载、不填 incident 问卷。真实故障与保护不能改名绕过；未知根因不阻止有界诊断和适用缓解 |

三条件独立。normal 非通过限制其候选的推进；solution 不合格回原机制修订；root 只接收当前可进入因果判断的实际机制。顺序依赖成立时先处理前项结果，但不为凑齐顺序调用本来不适用的 owner。边界是否适用不确定且事实足以形成真实候选时，进入相应原 owner；缺具体 authority/对象则由原 owner 处理实际缺口，不默认通过。

### 4.2 实际 caller 落点

下表每行保留现有 profile、caller 和原 return owner。在原阶段提升候选义务前，读取三个条件并分别决定 skip/adopt/invoke/refresh；这些词只描述会话行为，不新增字段或 typed exit。

| profile / 原 owner | 判定落点与实际省略、保留对象 |
| --- | --- |
| `task_free_pre_write` / `guru-execute-task-free-change` | suitability/写入前；普通局部文本或纯函数变更不自动全调，真实范围争议/authority/修复保护各自进入对应 owner |
| `task_free_evolution` / 同上 | 写后新发现的变化提升为进一步修改或风险路由前；已适用结论采用，真实 scope/机制变化只刷新命中项 |
| `requirements_scope_set` / `guru-clarify-requirements` | 新 scope 提案/范围问题/处置前；明确需求整理不造候选，真实准入问题仍 normal，方案含 authority/保护时独立触发 |
| `change_request_candidate_set` / `guru-review-change-request` | readiness finding、测试义务或 blocker 前；常规就绪性核对不自动全调，实际候选按各自条件进入 |
| `author_candidate_set` / `guru-author-task-plan` | 候选交独立 Architecture 前；普通接受功能不填 incident 问卷，真实机制准入和材料变化不省略 |
| `planning_scenario_set` / `guru-approve-task-plan` | acceptance、negative test、finding/revision 前；采用仍适用准入结论，独立判断规划完整性和当前证据 |
| `implementation_discovery` / `guru-phase2-implementation-coordinator` | 规划外真实发现转 edit/test 前；未产生准入候选不造调用，新增机制或范围扩大仍走原 Architecture/Clarify |
| `base_impact_candidate_set` / `guru-reconcile-task-base` | base impact finding、验证义务/route 前；无关 base 前进不重做未变结论，实际影响刷新命中项 |
| `phase2_candidate_set` / `guru-check-task` | finding/severity/planning-stale/实施 route 前；空候选原逻辑保留，非空也独立按条件判断，不缩减九维 Check |
| `branch_review_candidate_set` / `guru-review-branch` | P0-P3、scope/阻塞 route 前；完整 range 与当前 consumers 独立审查保持，阶段切换不重调相同结论 |
| `publication_candidate_set` / `guru-review-task-delivery` | readiness finding/task-work/blocker 前；当前切片真实候选按条件进入，原 PR/Issue/live readiness 不由 qualifier 代替 |

修改各原 `SKILL.md`、命中的 `references/contract.md`，Author 修改 `references/authoring.md`；实施协调器落点在 workflow 第2.1节。workflow 保留每个 stable Skill 的 mandatory marker 和全量 exit consumer，只将 mandatory 正文约束为“条件触发时显式加载并调用”。平台 launcher 继续路由原 owner，不复制专属条件。

## 5. 接口与数据

三个 qualifier 输入保持现有 closed profile、target、非空 unique candidate_refs 和 live locators；新调用使用当前 Git/规划身份，不能重放旧 envelope。未触发没有输入/输出对象。不同 qualifier 可以接收同一原始集合中各自适用的真实子集，原阶段继续负责其余工作，不用空集合换取 pass。

root 入口使用 caller 已完成的当前场景/authority-placement 判断；normal/solution 触发时必须消费其真实结果，未触发时不要求捏造结果。该前置是 Markdown 语义职责，现有 root 公共 input 不新增上游 result 字段，runtime 不分类是否触发，也不从文件或 token 推导语义 pass。

| 原输出 | 直接 consumer 与行为 |
| --- | --- |
| normal/solution `classified` | 原 classified router 回 fixed caller；qualified 仅是准入，rejected 不提升为新义务、finding 或 blocker |
| normal/solution `scope_confirmation_required` | 分别交原 Clarify `normal_scenario_scope_confirmation` / `solution_mechanism_scope_confirmation`；真实选择后原 owner 刷新受影响判断 |
| normal/solution `mechanism_revision_required` | 原 mechanism router 回 fixed caller 删除/替换，不能转作普通 scope question |
| root `classified` | 原 root classified router 传最小 dispositions；诊断/缓解/保护/修复含义保持，不是阶段完成 |
| root `mechanism_revision_required` / `diagnosis_required` | 各原 router 回 fixed caller 修订或有界取证；暂停不成立的修复，保合法诊断与独立缓解 |
| 三者 `blocked` | 原唯一 stop，报告具体缺口；unknown/multiple/unmapped 保原 fail closed |

`implementation_discovery` 仍由 coordinator 判断、`guru-resume-implementation` 接续。Delivery Review 保自身 planning/implementation/scope/blocked 消费。不新增 consumer、状态、DTO、持久 qualification 账本或授权记录。runtime wrapper/schema/projection 只在真实确定性差额存在时修改；本设计预期 wire 无变化。

## 6. 状态、顺序、正常与失败流程

1. 原阶段 owner 读取 live authority、工作对象和变化，先读取各原包的短适用条件。
2. 对当前对象存在仍适用结论时，采用会话中的最小结论或原阶段本已需要的 owner gate；仍独立审查本阶段工作。不复制 qualifier stdout 到持久新文件。
3. 未触发的 qualifier 直接不加载、不调用；原阶段自行完成其职责，没有通过断言或 skipped exit。
4. 触发的 qualifier 完整加载，使用真实适用非空候选、当前 facts 和原 profile 执行正向语义判断、AI Gate、必要真实选择及原 recorder/validator；消费实际唯一出口。
5. 相关非通过出口先由原 owner 处理。只有满足其真实后续条件的候选继续，不以 runtime 成功代替 semantic pass。
6. authority、机制、适用条件、支持入口/consumer、因果证据或所依赖行为实质变化时，刷新依赖它的判断。阶段/caller/HEAD、无关文件变化本身不重复相同资格。新的正式 invocation 仍绑定当前事实；采用结论与重放旧 invocation 是两回事。
7. 丢失必要结论时由原 producer 恢复或重新判断，不能从测试绿、阶段状态、示例或摘要补造 pass。未变化的其他判断与合法工作可继续。

因此，典型普通纯函数增量可跳过三个形式调用；已有明确范围的真实无 authority placement 改变的故障诊断仍进入 root，normal/solution 可各自不触发；新 publication 资格机制可触发 solution 与 root，normal 仅在另有真实准入问题时触发。

## 7. 恢复、兼容、迁移与集成

新增 `trellis/presets/guru-team/MIGRATION-793.md`，说明调用语义窄替代、所有原 stable id/profile/input/output/消费者保持、在途采用与丢失结论恢复。没有持久格式/数据迁移。旧完整安装在成套采用前继续原合同；不得只复制新条件或只删 workflow mandatory 而混用旧 caller/root 前置。已有合法旧调用与 outcome 可按当前材料适用性采用，不因升级强制全重跑；新调用保 current facts 校验。

canonical 是 `trellis/skills/guru-team/packages/`、`trellis/workflows/guru-team/workflow.md`、preset/spec 源。dogfood `.trellis/guru-team/skills/`、`.trellis/workflow.md`、`.agents/skills/` 及声明平台投影由原 `guru-upgrade-tools` 从完整 matching source 同步，保 Task/session；不手工覆盖安装副本。读取实际 inventory、处理 `.new/.bak`，运行 dogfood drift。Codex shared projection、Claude Code 及其他真实受影响受管路径以 installer 声明为准，不自行新增平台合同。

Architecture [贡献](architecture-contribution.md)与[ADR 候选](adr-conditional-qualification.md)保持隔离。实施准备真实完整拟写，candidate Architecture/Check 后由原 Architecture/RDT final_integration 分别晋升；实际 after 重新 candidate/begin_check，最终 Check、commit、完整 committed Review 和 readiness 保持。当前 PR 到 main，发布后在 merge 前停。shared promotion 不等于 Task 完成或目标业务安装已采用。

## 8. 验证设计

按 `quality-guidelines.md#test-and-validation-value`，先审真实调用分支和已有覆盖，补实际缺口。选择足够观察层级，不以短条件文本存在、字符串匹配、case 数量或模型退出0证明语义行为。

| ID / 验收 | 入口与输入 | 预期观察及证据边界 |
| --- | --- | --- |
| V1 / AC1、AC2 | 原 package/graph validators，三 qualifier 既有 contract/runtime tests；实际改变 caller 的相关测试 | 原 stable profiles、非空输入、facts/stale、真实 wrapper 和所有非通过 projection 继续有效；只补改变的前置/consumer 缺口。确定性证据不能证明 caller 语义触发 |
| V2 / AC1 | 从完整 matching provider 的真实 task-free 或 Author 入口运行普通纯函数/正文维护正常工作；host 只给事实，不给 verdict | 实际工具事件显示先读短条件、未读未触发 qualifier 全文、未调用 wrapper，原 owner 仍完成自己的判断/公开结果。完整入口的实际必需前提不得被 fixture 替代 |
| V3 / AC1、AC2 | 实际原 caller 接收已清楚 scope、无 authority placement 改动的真实诊断机制，以及另一个确需专属准入的机制候选 | 前者 root 正常进入且不要求两次无关 upstream 输出；后者真实调用对应原 owner，实际非通过返回其原 consumer。采用已有可核验非通过测试，必要的 caller 消费以实际 trace 观察 |
| V4 / AC3 | 同一 caller 后续阶段采用不变结论，再提供实质 authority/机制/条件/因果证据变化；必要结论丢失走原恢复 | 实际采用且仍审当前工作；材料变化只刷新相关 owner；丢失不补造 pass。已有 root reuse 测试方法可用，但旧固定三连 prompt 不能作为新入口正确证据 |
| V5 / AC4 | 原 tools 更新后 source/installed package 验证、受管投影比对、必要 drift；匹配迁移语义审查 | 实际 dogfood/platform 文件符合 canonical；Task/key/root/session 保持，旧合法恢复可续。此证据不等于 clean install、全部平台实际 Agent 行为或完整 Release/upgrade 矩阵 |

V2—V4 使用现有 native fixture/run 方法作定向扩展或一次性有界观察，保 raw trace 在仓库外，原 owner 独立读取真实结果；长期保留能检测触发/回程缺陷的有效用例，不创建通用评测框架。普通 feature 与 root-only 入口是当前固定调用缺陷的独立风险，reuse/refresh 是另一行为；不做十一 profile 乘三个 owner 的乘积矩阵。发现真实未覆盖 consumer 时只补命中观察。

实施可先改清楚的 Markdown，再运行定向验证。既有 public runtime 非通过覆盖优先采用；凡声称本轮通过的命令须实际执行。达到上述必要行为、原非通过承接与分发证据后停止追加实验；设施未到产品分支不记产品失败或通过，回原 owner 重评入口并保留缺口。

## 9. Canonical 引用、本轮差额与实际未决项

requirement authority 为整体 PRD、Issue #793；当前 root R/D/T 完整单元为 `docs/requirements-design-test-contributions/382-root-cause-qualification/{requirements,design,test}.md`。本批维护新 `793-conditional-qualifiers` R/D/T 完整单元，原 RDT owner 处理其对旧前置的窄替代及真实必要引用，不改历史测试观察。

Architecture 命中 ADR-008、ADR-020、`ARCH-CUR-019/052`、`ARCH-DOM-011/035` 的适用内容；实施时原 owner 重读完整目标并准备隔离完整 proposed 定义。没有要求根 README、全局索引或 unrelated system 主题登记本 Issue；仅真实被改变的单元/引用由原 owner 同步。具体九 concerns、替代与责任见真实贡献。

当前无必要产品选择。尚待 Wording、独立 final_plan、Approval 及实际计划接受/Activation；未完成这些门禁不进入实施。实施行为、分发及远端发布仍未验证，不声称费用降低。
