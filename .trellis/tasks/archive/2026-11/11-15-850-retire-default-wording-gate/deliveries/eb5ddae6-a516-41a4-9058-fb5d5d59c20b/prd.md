# D1：默认 Wording 退出与直接依赖迁移

## 1. 整体来源与术语

TaskId 为 `850-retire-default-wording-gate`，generation 0，DeliveryId 为 `eb5ddae6-a516-41a4-9058-fb5d5d59c20b`；公共 planning_root 为 `deliveries/eb5ddae6-a516-41a4-9058-fb5d5d59c20b`。scope_ref 使用整体 `prd.md` 的实际 accepted_scope，选择 R01–R04、AC01–AC05，精确 revision 由公共 Task 记录拥有。

| 来源 | 角色及本批用途 |
| --- | --- |
| [整体 PRD](../../prd.md) 第1–8节 | 已接受的完整整体来源、行为与验收；本批全量承接，必要正文在第5、6节展开 |
| [#850 完整正文](https://github.com/castbox/guru-trellis/issues/850) | Direct Source，约束行为、默认链退出、资产退役、API／在途／安装迁移 |
| [复审评论](https://github.com/castbox/guru-trellis/issues/850#issuecomment-6892152938) | 已接受范围与设计约束；方案细节由本 Planning 判断，不能弱化真实 Agent 验收 |
| canonical workflow/routing、design第4节列出的packages、preset installer | 当前实现事实与直接 consumer；不是目标要求或已通过结论 |

S1与S5分别指整体PRD来源表的Direct Source及仓库执行/验证约束。Wording、内容 owner、审核 owner 和 Task／Delivery 的含义沿整体 PRD 第1节。规划写作与语义审核方法仅由原 package 和共享写作规范拥有。

## 2. 整体与本批目标、非目标

本批独立交付目标是从所有实际受影响的正常入口解除独立 Wording 及专属证明前置，同时保留原语义责任、显式只读能力和合法恢复。D1 覆盖整体全部范围；不能只改路由或先保留悬挂 consumer 再宣称目标完成。

整体非目标完整适用：不实施 #848／#853、不新增 Issue、不展开 Evolution、不新增替代关卡或通用迁移框架、不扩张攻击／竞态／crash 验证，不执行完整多平台 Release 矩阵。独立同名 Skill 的去留以实际当前职责判断，不预设保留 scanner。

## 3. 本批起点、前序结果、依赖与剩余责任

首次 D1，没有前序 Delivery。固定开发起点为 Git `a72981db56d2070d8140b468cab3a97ae82effd3`，交付目标 main。整体 scope 已接受，但 D1 的 Planning、Architecture、Approval、实现与验收均须取得本阶段真实结果。

当前直接依赖包括：Readiness full-chain runtime 只接 wording_current；#819 的 supplement_wording／issue_review_return 与完整回程；Author 的 delivery_wording_reentry；final Architecture 的 Wording-current 表述；Clarify resume_target 和 clear-router；共享 transition/owner schemas、Create Issue 的 readiness消费；registry、workflow graph、安装 inventory 与分发/行为测试。受管 installer 已有 stale managed skill removal 和冲突保留机制，应复用其实际合同。

D1 承担 API、在途和受管安装退出闭合，不将这些必要工作留作未指派后继。Delivery 结果之后仍须 whole-Task Completion、Closure、Finish；合并待协调器处置。其它 Task、branch、session 与公共 API 合法消费者均保持原职责。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置与触发 | 行为与可观察结果 | 验收 |
| --- | --- | --- | --- |
| SC01 | 正常新请求、拟创建 Issue、完整 Intake 的当前来源已就绪 | 原 Clarify 到 Readiness 及其唯一 consumer；三类来源无独立 Wording 前置，Create 自己的门禁仍执行 | AC01、AC02、AC04 |
| SC02 | #819 existing-Issue Readiness 发现实际缺口，或需要 full-intake | 补审交实际原内容 owner，回同一 Issue/source/continuation 的 Readiness；完整回程不造 Wording pass | AC01、AC04 |
| SC03 | 当前 Delivery 初次 Planning、scope 或内容返工 | Author 形成实际规划，final Architecture 与 Approval 在当前内容执行；返工回实际受影响 owner，保留原身份和有效覆盖 | AC01、AC02、AC04 |
| SC04 | 用户显式请求有界只读措辞审核，可能没有 Task 绑定 | 按对象和原职责审核，输出具体发现及结论；无需绑定／选择，不写对象，不自动扩大为完整 Intake 或开工审核 | AC02、AC03 |
| SC05 | 原 owner 实际修订文字 | 语义未变变化只刷新直接依赖；需求、机制、Architecture、验收变化返回原受影响 owner；不全链重跑或把实质变化当润色 | AC03 |
| SC06 | 支持的调用待 Wording、已有适用内容结果，或处于 content_changed／缺口补审 | 按未完成义务接续；复用有效判断；真缺结果回 producer；不重建 Task／Delivery、不清空规划和合法选择 | AC04 |
| SC07 | 已有项目从匹配来源更新，或当前版本干净安装 | 原安装 owner 更新匹配合同并处理退役文件及冲突；当前可达入口无退役专属 consumer，分发一致 | AC05 |

本批验证 SC01 的 current_issue、proposed_draft、standalone_request，以及 SC02 的本地补审和 full-intake；不能以一种来源成功替代全部受影响返回。SC03 同时包含初次规划与同一 Delivery 的 scope／content返工。SC06 按真实未完成义务选择接续，保持固定旧 provider 的原操作恢复边界。

## 5. 完整行为、条件与约束

以下 R01–R04 按职责承接、行为要求、完整迁移、在途续接分别定义整体责任。正文保持 S1 的完整条件、否定、例外、顺序及责任。

### R01 语义职责承接

| 原七项规划判断 | 收敛后的实际责任 |
| --- | --- |
| 不弱化已确认需求 | Author 保留适用要求和义务强度，Approval 在 requirement authority／scope 内判断；Issue 内容由 Clarify／Readiness 承担 |
| 来源 Issue 语义保留 | Author 读完整规范性来源及关联条件，Approval 核对 provenance 和实际规划落点；建议与历史不被提升为义务 |
| 条件路径有明确触发及结果 | 原内容 owner 写清实际分支，原需求／规划审核判断完整条件、否定、例外和顺序 |
| 没有未定竞争实现路径 | Author 形成当前方案，Architecture／Approval 按原职责判断机制和责任；不由措辞审核选方案 |
| 确定性 gate 有客观可验证条件 | 原 gate owner 按现有 semantic／deterministic 边界定义条件，Author／Approval 核对；不把需要 AI 判断的充分性改成脚本 pass |
| 验收结果明确可观察 | Author 将行为与验证关联，Approval 判断 acceptance verifiability；可观察结果不代表一律要求机器理解自然语言 |
| 外部引用与历史不冒充当前合同 | 原写作／审核 owner 按来源角色、Issue 内容规范和共享清晰写作规范保留引用、literal、建议及历史身份 |

这份职责对照用于确认必要语义责任没有丢失，不要求把原七项布尔字段、逐词分类或另一套固定审核记录搬入接收 owner。

### R02 行为要求

- 默认 Intake／Planning 不再调用独立 Wording 关卡，也不要求其 pass、完整词面分类、scan receipt 或为该步骤恢复绑定／选择。保留必要语义检查，不把旧扫描和证明链整体搬入另一个 Skill，不为维持原关卡新增替代 gate、wrapper 或流程状态；实际 public API 迁移按下节给出新版本合同。
- 原审核发现条件不清、语义丢失、义务弱化或验收无法判断时，报告具体内容、影响和原修订 owner；这些问题仍可阻塞对应质量结论。不能只因出现“建议”“相关”“等”就要求改写、分类或阻塞。清楚合法的建议、默认值、引用、历史和 literal 不需要逐词免责记录。
- 仅服务拟退役关卡的词表、分类结果、scan／receipt／digest linkage 随依赖解除而退役。只有资产承担独立的当前语义／执行职责时才评估保留，并说明实际入口、结果和直接 consumer。仅有旧 scanner、checker、receipt 或过渡 linkage 相互消费，不是保留理由；对应依赖在本项内迁出后删除。不以未知未来用途预留可选扫描器。
- 显式只读措辞审核仍输出实际发现和结论，按对象使用既有内容审核职责及清晰写作规范；不因此启动完整 Intake、创建 Task、恢复 Task／Delivery 选择或修改被审对象。实际修订遵守原写入边界。不得把有界措辞请求自动扩大为整个需求／设计的开工审核。若没有独立的当前质量职责，退役同名 Skill 及仅服务它的入口和资产；真正需要保留的能力或有期限兼容须在规划中说明当前依据、最小范围及退出条件，不保留只做转发的长期 wrapper。
- 语义未变文字变化只刷新直接受影响的内容身份和判断；涉及需求、机制、Architecture 或验收变化时返回原受影响 owner。不能因普通文字修改重跑全部阶段，也不能把实质变化当作语义未变润色。

### R03 完整迁移范围

在原 owner 内迁移以下直接依赖，确认每个实际出口都有唯一 consumer：

- 默认 Intake 的 `clarity_current → wording_current → Readiness`：覆盖 Readiness 的 `current_issue`、`proposed_draft`、`standalone_request`，以及 Issue 创建的真实前序审核和最小审核评论；取消专属 Wording 前置，不跳过 Clarify／Readiness／Create 自己的语义门禁；
- Planning 的 Author→Wording→final Architecture→Approval：涵盖初次规划、同一 Delivery 的 scope／内容返工及 Wording pass／content_changed 到 Author 的回程，同时更新将 Architecture 输入称为 Wording-current 的前置。final Architecture 和 Approval 在当前实际规划上执行；删除 Wording 不代表重做或删除它们的必要判断；
- #819 existing-Issue intake 的 `supplement_wording`、`issue_review_return` 和 full-intake 回程；补审缺口交原内容 owner，完成后回原 Readiness，不补造旧 Wording pass；
- 公共 input／output／transition／schema、入口路由、installed inventory、实际受影响的runtime／测试，以及 canonical、dogfood、声明平台投影和当前文档。

Skill／typed exit／schema 是公共 API，按明确版本及迁移合同切换。已有安装通过匹配来源升级，退役或保留资产遵守原安装 owner；不靠新旧回执混用、手工覆盖受管文件或无期限双链维持兼容。保留调用方和原生命周期 owner 所需的身份、freshness、实际内容及合法阶段检查；只解除为独立 Wording 步骤存在的依赖。

### R04 在途续接与退役完成条件

新路径从原 caller 的当前对象和真实所需前序结果直接接续；不伪造 Wording pass，不只改 stage／exit 标签来满足旧 checker，也不让新路径接受缺少必要语义判断的旧结果。接收 owner 对旧内容身份的正常比较继续有效，取消的只是 Wording 专属 linkage。

对本项实际改变的受支持在途调用，按未完成义务处理：尚待 Wording 的调用进入新的原内容／审核路径；已有仍适用内容判断的调用复用其有效覆盖；原 content_changed／缺口补审回到实际内容 owner，修订后回原 consumer。真正缺失的来源或结果回原 producer；不重建 Task／Delivery，不清空规划、已完成结果或合法会话选择，也不把普通迁移变成首次激活或全链重跑。旧 provider 的未完成操作按明确的固定版本恢复边界处理，不混用新旧 envelope。

完成条件是：当前可达入口已不消费退役专属结果，受影响在途入口能续接，受管安装按原 owner 完成匹配更新及必要退役文件处理。删除无人消费的当前资产；历史归档和兼容验证材料保留历史身份，不要求重放全部旧任务。不新增通用迁移引擎、状态账本或无期限双读。

整体 PRD 第6节的完整执行约束及该节列明的工作边界继续适用。来源约定设计的唯一 retain/change/reject 处置由本 D1 design 第3节拥有；该文档在候选 Architecture 后编写，不在此预填方案通过。

## 6. 本批验收、验证方式与未决项

AC01–AC05 按下列顺序对应 S1 验收1–5。SC 表给出对应场景；第5节完整行为都须进入最终验收覆盖。

1. **AC01：默认路径确实缩短且可继续。** 从正常新请求、拟创建 Issue、已有 Issue 的补审和 Delivery Planning 入口，实际进入唯一后续 owner；没有 Wording 强制调用或专属回执要求，也没有替换成重复承担相同职责的新关卡。
2. **AC02：质量责任仍有效。** 以正常含有需求弱化、条件缺失、来源语义丢失或不明确验收的 Issue／规划为输入，通过受支持的真实 Agent 入口观察原内容审核仍能指出具体缺陷并返回原修订 owner；覆盖没有受控词命中却仍存在语义缺口的材料。正常清楚的建议、默认值、引用、历史与 literal 不被词面命中阻塞。不能以预填七个 true、词面扫描或仅断言未调用 Wording 代替这一语义证明。
3. **AC03：显式审核及修改回程正确。** 只读措辞请求无需 Task 绑定即可完成且不写入；语义未变修改只刷新直接依赖，实质变更回原受影响 owner。
4. **AC04：迁移闭合。** 定向核对并验证实际受影响的 producer／consumer／schema／inventory，覆盖默认完整链、#819 本地补审、原 Author 内容返工和本项实际影响的在途续接；必要语义前置仍有效，没有当前入口悬挂在退役结果上。不把清楚的范围内修订升级为新关卡；历史材料保留历史身份，不将旧结果改标签作为新通过。
5. **AC05：分发一致且证据诚实。** 同步 canonical／dogfood 与声明平台投影，执行适用 drift 和安装／升级定向验证；当实际改动需要证明干净安装时，最多执行一个代表性 clean throwaway，不把本 Issue 扩为完整多平台 Release 矩阵。源码、机械校验、真实 Agent 行为与安装证明分别报告，未完成项不得宣称通过；不设没有依据的耗时收益门槛。

验证按 S5 选择足以观察真实行为的最小可靠层级。具体入口、样本和命令由 Delivery Planning 展开；不能缩小上述结果责任。当前没有修复后验收通过结论，源码、机械校验、真实 Agent 与安装证据必须分开报告。

本批无待决定需求范围。实际consumer、公共API新版本及路由/返回、固定旧provider恢复和安装退役方案由design第4–7节展开，原Architecture/Approval按各自职责审核；实现者不能跳过这些责任。真实Agent、runtime与安装分别证明其覆盖，不能互相替代。

## 7. Canonical 引用与本轮差额

| authority／当前实现 | 本批差额与读取用途 |
| --- | --- |
| `docs/requirements/current/issue-content.md` R153/R818/R819；`docs/design/current/issue-content.md` D153/D818/D819；`docs/test/current/issue-content.md` T153/T818/T819 | 替换独立Wording及title/body scan的当前责任引用，保留来源、完整性、只读、评论和证据边界；历史观察保留 |
| `docs/{requirements,design,test}/current/local-fix-intake.md` R819/D819/T819 | 补审与完整链的直接 consumer、source和continuation返回须同步迁移；保留先行Readiness及其它scope/base/creation边界 |
| `docs/test/current/task-delivery-lifecycle.md` T531-02；`docs/architecture/01-current/system.md`、`03-domains/ownership.md`、`03-domains/issue-review-intake.md` | 移除当前Wording mandatory与专属回程，更新实际职责及必要关系；不重写历史Task证据或 unrelated lifecycle |
| `trellis/skills/guru-team/packages/*`、`consumers/workflow/stage0/`、registry、`trellis/workflows/guru-team/{workflow.md,references/routing.md}` | 这些位置拥有实际 public input/output/schema/route，不在RDT复制字段定义；本批同步受影响接口和唯一consumer |
| `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`、完整 preset、平台投影及当前安装 inventory | 保留原受管安装和用户修改保护；本批删除退役专属资产，匹配更新和定向验证 |
| `.trellis/guru-team/skills/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md`；Architecture README／constitution／change-contract | 共享定义由原RDT与Architecture owner隔离拟写、提交前整合/readback、提交后独立完整Review；Planning不直接改shared current |

当前文档没有宣称软件实现、真实Agent效果、安装采用或Release已通过。canonical current、未晋升贡献、目标和历史须按各原authority的实际状态分别读取。
