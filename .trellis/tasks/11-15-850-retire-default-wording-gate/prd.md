# #850 取消默认独立 Wording 关卡：整体需求

## 1. 来源与术语

| 标识 | 完整来源及章节 | 角色 | 用途 |
| --- | --- | --- | --- |
| S1 | [Direct Source：#850](https://github.com/castbox/guru-trellis/issues/850)，完整正文 | 行为、范围、约束与验收要求；G06 为历史调查证据 | 下文按 Task 模板保留完整要求，历史证据不冒充候选验收 |
| S2 | [复审评论](https://github.com/castbox/guru-trellis/issues/850#issuecomment-6892152938)，复审结论与实施边界 | 已接受的范围及设计约束 | 七项职责、三类 Readiness、#819、Author 返工和在途迁移均保留；consumer、退役及真实验证方案由 Planning 确定 |
| S3 | `trellis/workflows/guru-team/workflow.md` 的 Intake／Planning；`trellis/skills/guru-team/packages/guru-review-change-request/references/issue-intake.md`；`trellis/skills/guru-team/packages/guru-author-task-plan/references/authoring.md` | 当前实现事实 | 固定基线 a72981db56d2070d8140b468cab3a97ae82effd3 仍有独立 Wording 依赖，不把源码调查当成修复完成 |
| S4 | `.trellis/guru-team/skills/packages/guru-author-task-plan/references/planning-body.md`；`.trellis/guru-team/skills/packages/guru-clarify-requirements/references/issue-content.md`；`.trellis/spec/workflow/clear-technical-writing.md` | 当前内容与写作约束 | 来源、语义及清晰度由原内容与审核 owner 承接 |
| S5 | `AGENTS.md`；`.trellis/spec/workflow/quality-guidelines.md` 的 Test And Validation Value 与 Validation Scope Ownership | 仓库执行与验证约束 | AI/脚本分层、正常场景、受管分发和最小可靠验证 |

S1、S2 已完整读取。Wording 指现有独立 `guru-review-contract-wording` 步骤及其专属证明依赖。原内容 owner 指原写作／修订者；原审核 owner 保持其 Issue、Planning、Architecture 或实现职责。Task 拥有整体范围，Delivery 只拥有选定切片。

### S1 的可复核来源

- [Wording 七项判断与固定闭环](https://github.com/castbox/guru-trellis/blob/0fb7dc9aac817a684c2f95bebb6570061a5ef868/trellis/skills/guru-team/packages/guru-review-contract-wording/references/contract.md)；[合并诊断的 scope 实现](https://github.com/castbox/guru-trellis/blob/0fb7dc9aac817a684c2f95bebb6570061a5ef868/trellis/skills/guru-team/packages/guru-review-contract-wording/runtime/common.py)。
- [Author 规划正文与来源处理](https://github.com/castbox/guru-trellis/blob/0fb7dc9aac817a684c2f95bebb6570061a5ef868/trellis/skills/guru-team/packages/guru-author-task-plan/references/planning-body.md)；[Approval 原审核维度](https://github.com/castbox/guru-trellis/blob/0fb7dc9aac817a684c2f95bebb6570061a5ef868/trellis/skills/guru-team/packages/guru-approve-task-plan/references/contract.md)。
- [Issue 内容规范](https://github.com/castbox/guru-trellis/blob/0fb7dc9aac817a684c2f95bebb6570061a5ef868/trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md)；[已有 Issue 本地补审](https://github.com/castbox/guru-trellis/blob/0fb7dc9aac817a684c2f95bebb6570061a5ef868/trellis/skills/guru-team/packages/guru-review-change-request/references/issue-intake.md)；[共享清晰写作规范](https://github.com/castbox/guru-trellis/blob/0fb7dc9aac817a684c2f95bebb6570061a5ef868/trellis/presets/guru-team/spec/workflow/clear-technical-writing.md)。

场景限于诚实协作的正常入口、普通遗漏、过期／不匹配及实际兼容问题，不扩展攻击模型、竞态压力、锁、崩溃一致性或无关 failure matrix。

## 2. 背景与问题

### 当前问题与目标差额

常规 Intake／Planning 中，`guru-review-contract-wording` 仍是独立强制关卡。当前需求澄清、正文写作、规划审核和共享清晰写作规范已经承担其必要语义质量职责，但流程仍额外要求逐词命中分类、扫描回执、record/check/invoke，以及接收会话的 Task／Delivery 绑定与选择。这使审核职责重复，并增加输入构造、读取、恢复与返工成本。

本 Issue 取消默认流程中的独立强制 Wording 关卡及其专属证明依赖，由既有内容 owner 和原审核 owner 处理真实歧义。显式“审核措辞”的能力继续支持，按实际对象和请求范围完成；保留独立同名 Skill 不是前提。

### G06 历史证据及其边界

诊断样本运行在旧版 `0.7.0-guru.8@8c158381b5bdb61fd961cbb89e23c2d1f659c9aa`。初次诊断核对基线为 `main@ac1c823857ad6695c106daeedd25aafce4c50934`；本轮复审基线为 `main@0fb7dc9aac817a684c2f95bebb6570061a5ef868`，其间变更仅涉及 Issue 编排监督，本项 Wording、正文和审核合同未变。不能用新版本规则追溯认定旧执行违规，也不能因发生过升级就认定旧问题已解决。

| 样本 | 已确认事实及归属 |
| --- | --- |
| Hume | 已有完整 Task／Delivery 定位，仍按当时正式 phase2 入口恢复接收会话绑定和选择；不是已经证实的派工漏传 locator |
| Ohm | 恢复正式 Check 的执行身份后，candidate 等前置仍未满足；不能将正常停止当作校验器缺陷。当前 #794 已退出这套旧阶段链，但没有取消 Wording 关卡 |
| Mendel | 已查到 `implementing`，随后却调用 planning Activation 的 scope revision；原校验正确拒绝。属于执行侧误路由，未证实并发阶段漂移 |
| Hooke | 显式 planning 文档 scan 返回泛化 stage rework 错误；实际后续恢复的是 Task 绑定和 Delivery 选择，然后同一对象 scan 成功。错误回执不能证明阶段发生变化 |

当前 Wording `runtime/common.py::scope` 将非 current、key、phase、generation 和 scope authority 不匹配合并为 `stale_identity / delivery_key / stage rework`。旧安装的关键文件已与旧 canonical 对照；该 scope 函数在当前仍相同。两版本各四种状态的隔离实验确认：缺绑定、缺选择和真实阶段错误得到同一提示，健康 planning 对照成功。此实验只证明诊断分支，不是完整原生会话恢复重放或候选修复验收。恢复窗口含必要阅读与其他工作，不作为净浪费或节省量。

### 已确认根因

1. **历史质量目标与实现机制没有随职责演进而收敛。** #83 处理歧义、需求弱化和验收不明确；#93 强制词表命中、逐条分类和未分类阻塞；#114 于 2026-07-17 将其抽为独立 Skill，并保留七项规划语义判断；#679 又补入接收会话恢复链。这些曾是明确需求，并非近期实现者擅自扩张。历史上有依据，不代表当前仍需原机制。
2. **独立关卡的语义职责与现有 owner 重叠。** 当前 Author 的来源与正文自检、Architecture 的方案／职责判断、Approval 的完整规划审核，以及 Clarify-owned Issue 内容规范和 Readiness 完整审核，已覆盖必要语义责任。共享清晰写作规范也要求原写作／审核 owner 保留含义、义务强度、完整条件和术语。尚未发现独立 Wording 关卡不可替代的质量判断。
3. **为关卡服务的证据和路由成为持续执行前置。** scanner／classification／receipt 和 `wording_current` 被下游 linkage 消费，接收方又须满足正式会话选择条件；机器字段有 consumer 不等于存在独立质量职责。泛化报错进一步增加错误恢复方向的可能性。仅修提示或提高 caller 熟练度，不能消除结构性重复。

当前仍有这些源码和合同依赖；本 Issue 提出显式迁移，不将“其它 owner 已有语义能力”写成迁移已经完成。

## 3. 目标与非目标

整体目标是移除默认独立 Wording 关卡及专属证明依赖，让原内容和审核 owner 保留真实语义责任，并完成实际公共接口、在途调用、资产退役及受管安装迁移。

本 Task 覆盖第5节完整行为及第7节全部验收。任何切片合并都不替代 whole-Task Completion、Closure 或 Finish。

不实施 #848／#853，不创建其它 Issue，不展开整个 Evolution，不新增统一返工 owner、替代 gate、长期 wrapper、通用迁移引擎、状态账本或无期限双链。其它范围边界与相关工作由第6节定义。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置与触发 | 行为与可观察结果 | 验收 |
| --- | --- | --- | --- |
| SC01 | 正常新请求、拟创建 Issue、完整 Intake 的当前来源已就绪 | 原 Clarify 到 Readiness 及其唯一 consumer；三类来源无独立 Wording 前置，Create 自己的门禁仍执行 | AC01、AC02、AC04 |
| SC02 | #819 existing-Issue Readiness 发现实际缺口，或需要 full-intake | 补审交实际原内容 owner，回同一 Issue/source/continuation 的 Readiness；完整回程不造 Wording pass | AC01、AC04 |
| SC03 | 当前 Delivery 初次 Planning、scope 或内容返工 | Author 形成实际规划，final Architecture 与 Approval 在当前内容执行；返工回实际受影响 owner，保留原身份和有效覆盖 | AC01、AC02、AC04 |
| SC04 | 用户显式请求有界只读措辞审核，可能没有 Task 绑定 | 按对象和原职责审核，输出具体发现及结论；无需绑定／选择，不写对象，不自动扩大为完整 Intake 或开工审核 | AC02、AC03 |
| SC05 | 原 owner 实际修订文字 | 等义变化只刷新直接依赖；需求、机制、Architecture、验收变化返回原受影响 owner；不全链重跑或把实质变化当润色 | AC03 |
| SC06 | 支持的调用待 Wording、已有适用内容结果，或处于 content_changed／缺口补审 | 按未完成义务接续；复用有效判断；真缺结果回 producer；不重建 Task／Delivery、不清空规划和合法选择 | AC04 |
| SC07 | 已有项目从匹配来源更新，或当前版本干净安装 | 原安装 owner 更新匹配合同并处理退役文件及冲突；当前可达入口无退役专属 consumer，分发一致 | AC05 |

## 5. 行为要求

以下 R01–R04 按职责承接、行为要求、完整迁移、在途续接分别定义整体责任。正文保持 S1 的完整条件、否定、例外、顺序及责任。

### R01 语义职责承接

| 原七项规划判断 | 收敛后的实际责任 |
| --- | --- |
| 不弱化已确认需求 | Author 保留适用要求和义务强度，Approval 在 requirement authority／scope 内判断；Issue 内容由 Clarify／Readiness 承担 |
| 来源 Issue 语义保留 | Author 读完整规范性来源及关联条件，Approval 核对 provenance 和实际规划落点；建议与历史不被提升为义务 |
| 条件路径有明确触发及结果 | 原内容 owner 写清实际分支，原需求／规划审核判断完整条件、否定、例外和顺序 |
| 没有未定竞争实现路径 | Author 形成当前方案，Architecture／Approval 按原职责判断机制和责任；不由措辞审核选方案 |
| 确定性 gate 有客观可验证条件 | 原 gate owner 按现有 semantic／deterministic 边界定义条件，Author／Approval 核对；不把需要 AI 判断的充分性改成脚本 pass |
| 验收结果明确可观察 | Author 将行为与验证关联，Approval 判断 acceptance verifiability；可观察结果不等于一律要求机器理解自然语言 |
| 外部引用与历史不冒充当前合同 | 原写作／审核 owner 按来源角色、Issue 内容规范和共享清晰写作规范保留引用、literal、建议及历史身份 |

这份职责对照用于确认必要语义责任没有丢失，不要求把原七项布尔字段、逐词分类或另一套固定审核记录搬入接收 owner。

### R02 行为要求

- 默认 Intake／Planning 不再调用独立 Wording 关卡，也不要求其 pass、完整词面分类、scan receipt 或为该步骤恢复绑定／选择。保留必要语义检查，不把旧扫描和证明链整体搬入另一个 Skill，不为维持原关卡新增替代 gate、wrapper 或流程状态；实际 public API 迁移按下节给出新版本合同。
- 原审核发现条件不清、语义丢失、义务弱化或验收无法判断时，报告具体内容、影响和原修订 owner；这些问题仍可阻塞对应质量结论。不能只因出现“建议”“相关”“等”就要求改写、分类或阻塞。清楚合法的建议、默认值、引用、历史和 literal 不需要逐词免责记录。
- 仅服务拟退役关卡的词表、分类结果、scan／receipt／digest linkage 随依赖解除而退役。只有资产承担独立的当前语义／执行职责时才评估保留，并说明实际入口、结果和直接 consumer。仅有旧 scanner、checker、receipt 或过渡 linkage 相互消费，不是保留理由；对应依赖在本项内迁出后删除。不以未知未来用途预留可选扫描器。
- 显式只读措辞审核仍输出实际发现和结论，按对象使用既有内容审核职责及清晰写作规范；不因此启动完整 Intake、创建 Task、恢复 Task／Delivery 选择或修改被审对象。实际修订遵守原写入边界。不得把有界措辞请求自动扩大为整个需求／设计的开工审核。若没有独立的当前质量职责，退役同名 Skill 及仅服务它的入口和资产；真正需要保留的能力或有期限兼容须在规划中说明当前依据、最小范围及退出条件，不保留只做转发的长期 wrapper。
- 等义文字变化只刷新直接受影响的内容身份和判断；涉及需求、机制、Architecture 或验收变化时返回原受影响 owner。不能因普通文字修改重跑全部阶段，也不能把实质变化当作等义润色。

### R03 完整迁移范围

在原 owner 内迁移以下直接依赖，确认每个实际出口都有唯一 consumer：

- 默认 Intake 的 `clarity_current → wording_current → Readiness`：覆盖 Readiness 的 `current_issue`、`proposed_draft`、`standalone_request`，以及 Issue 创建的真实前序审核和最小审核评论；取消专属 Wording 前置，不跳过 Clarify／Readiness／Create 自己的语义门禁；
- Planning 的 Author→Wording→final Architecture→Approval：涵盖初次规划、同一 Delivery 的 scope／内容返工及 Wording pass／content_changed 到 Author 的回程，同时更新将 Architecture 输入称为 Wording-current 的前置。final Architecture 和 Approval 在当前实际规划上执行；删除 Wording 不等于重做或删除它们的必要判断；
- #819 existing-Issue intake 的 `supplement_wording`、`issue_review_return` 和 full-intake 回程；补审缺口交原内容 owner，完成后回原 Readiness，不补造旧 Wording pass；
- 公共 input／output／transition／schema、入口路由、installed inventory、相关 runtime／测试，以及 canonical、dogfood、声明平台投影和当前文档。

Skill／typed exit／schema 是公共 API，按明确版本及迁移合同切换。已有安装通过匹配来源升级，退役或保留资产遵守原安装 owner；不靠新旧回执混用、手工覆盖受管文件或无期限双链维持兼容。保留调用方和原生命周期 owner 所需的身份、freshness、实际内容及合法阶段检查；只解除为独立 Wording 步骤存在的依赖。

### R04 在途续接与退役完成条件

新路径从原 caller 的当前对象和真实所需前序结果直接接续；不伪造 Wording pass，不只改 stage／exit 标签来满足旧 checker，也不让新路径接受缺少必要语义判断的旧结果。接收 owner 对旧内容身份的正常比较继续有效，取消的只是 Wording 专属 linkage。

对本项实际改变的受支持在途调用，按未完成义务处理：尚待 Wording 的调用进入新的原内容／审核路径；已有仍适用内容判断的调用复用其有效覆盖；原 content_changed／缺口补审回到实际内容 owner，修订后回原 consumer。真正缺失的来源或结果回原 producer；不重建 Task／Delivery，不清空规划、已完成结果或合法会话选择，也不把普通迁移变成首次激活或全链重跑。旧 provider 的未完成操作按明确的固定版本恢复边界处理，不混用新旧 envelope。

完成条件是：当前可达入口已不消费退役专属结果，受影响在途入口能续接，受管安装按原 owner 完成匹配更新及必要退役文件处理。删除无人消费的当前资产；历史归档和兼容验证材料保留历史身份，不要求重放全部旧任务。不新增通用迁移引擎、状态账本或无期限双读。

## 6. 约束与依赖

- 本 Issue 聚焦 G06 中旧 Wording 独立关卡的必要性及迁移。Mendel 的执行误路由继续按原 live phase／stage-owner 合同处理；不新增统一返工 owner。Hume／Ohm 的历史恢复不被追溯认定为违规，其他生命周期操作的必要身份检查不删除。
- 原误导诊断仍是真实缺陷。仅在实际保留的入口或明确过渡场景仍需要它时随该入口处理；不把单独强化拟退役机制作为本 Issue 的先决交付。
- 保留 #83 的真实质量目标，替代 #93/#114 中独立强制词面 gate 的对应机制。#154、#818 的现有正文与审核方法继续使用；#819 本地补审必须纳入迁移。
- #736 的通用减负、#747 的正常旅程与验证方法、#822 的 Task 内增量接续可复用其已交付且适用的能力；它们不覆盖本项独立关卡退出，不作为整项必须完成的前置。
- Evolution 的 `REQ-UC-EVO-037` 已在目标设计中排除正常 Planning 的 mandatory Wording gate，但尚未实施。本 Issue 不展开整个 Evolution，也不以其存在冒充当前已修复。
- 当前已完成历史与源码调查、语义职责对照和原诊断隔离实验。全部外部 consumer 清单、独立 Skill 的最终退役／兼容安排及真实 Agent 效果需在实施规划中确定；它们不构成保留默认强制关卡的理由。

### 本 Task 执行边界

- Markdown 与 AI 拥有 scope、充分性、finding、route、pass/block 判断；脚本只执行、记录最小必要结果和验证客观事实。
- 使用本专用 worktree 与 `codex/850-retire-default-wording-gate`。固定开发起点为 a72981db56d2070d8140b468cab3a97ae82effd3，Task integration／PR 与整体完成目标均为 main。真实基线集成问题沿原 Reconcile owner 处理；behind 或共享 fetch 本身不触发追赶。
- #848 的已交付读取与导航能力可使用；#853 不构成整项硬前驱，不同步其分支。不写共享 journal 或无关 Task metadata，保留他人工作与证据。
- 保留原 Check、独立完整 Review、readiness、受管同步、whole-Task Completion、Closure／Finish。合并前等待协调器处置。Git／GitHub 副作用按原边界分别确认，不持久化授权。

## 7. 可观察验收与验证方式

AC01–AC05 按下列顺序对应 S1 验收1–5。SC 表给出对应场景；第5节完整行为都须进入最终验收覆盖。

1. **AC01：默认路径确实缩短且可继续。** 从正常新请求、拟创建 Issue、已有 Issue 的补审和 Delivery Planning 入口，实际进入唯一后续 owner；没有 Wording 强制调用或专属回执要求，也没有替换成同等重复的新关卡。
2. **AC02：质量责任仍有效。** 以正常含有需求弱化、条件缺失、来源语义丢失或不明确验收的 Issue／规划为输入，通过受支持的真实 Agent 入口观察原内容审核仍能指出具体缺陷并返回原修订 owner；覆盖没有受控词命中却仍存在语义缺口的材料。正常清楚的建议、默认值、引用、历史与 literal 不被词面命中阻塞。不能以预填七个 true、词面扫描或仅断言未调用 Wording 代替这一语义证明。
3. **AC03：显式审核及修改回程正确。** 只读措辞请求无需 Task 绑定即可完成且不写入；等义修改只刷新直接依赖，实质变更回原受影响 owner。
4. **AC04：迁移闭合。** 定向核对并验证实际受影响的 producer／consumer／schema／inventory，覆盖默认完整链、#819 本地补审、原 Author 内容返工和本项实际影响的在途续接；必要语义前置仍有效，没有当前入口悬挂在退役结果上。不把清楚的范围内修订升级为新关卡；历史材料保留历史身份，不将旧结果改标签作为新通过。
5. **AC05：分发一致且证据诚实。** 同步 canonical／dogfood 与声明平台投影，执行适用 drift 和安装／升级定向验证；当实际改动需要证明干净安装时，最多执行一个代表性 clean throwaway，不把本 Issue 扩为完整多平台 Release 矩阵。源码、机械校验、真实 Agent 行为与安装证明分别报告，未完成项不得宣称通过；不设没有依据的耗时收益门槛。

验证按 S5 选择足以观察真实行为的最小可靠层级。具体入口、样本和命令由 Delivery Planning 展开；不能缩小上述结果责任。当前没有修复后验收通过结论，源码、机械校验、真实 Agent 与安装证据必须分开报告。

## 8. 实际未决项

当前整体需求范围没有待决定选择。全部实际 consumer 清单、公共 API 版本、独立 Skill 最终退役／有期限兼容、旧 provider 固定恢复边界，以及真实 Agent 与安装验证方案，由原 Author／Architecture／Approval 在 Planning 确定。它们不能作为保留默认强制关卡的理由。

本文件只定义整体需求，不替代 Delivery 方案及各阶段结论。整体 scope 接受以原 Clarify 实际 accept_scope 结果为准；后续各门禁以各原 owner 的实际结果为准。
