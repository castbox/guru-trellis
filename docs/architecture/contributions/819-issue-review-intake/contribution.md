# #819 Issue 审核与 Intake 架构隔离贡献

状态：proposed（保留Planning隔离来源；实际工程与采用结果由配对Test单写）。Task=819-issue-review-intake/gen0，Delivery=f108d161-d60d-4c89-91bf-d96004ef86a6；固定before=4f2adef1f7b099f78bb8429e8b8facd66dce3bfc。唯一来源为[Issue #819](https://github.com/castbox/guru-trellis/issues/819)和本Task根PRD的accepted scope。本文是原Author真实task-owned贡献，直接consumer为原独立Architecture final_plan；不代表共享current、实施、验收或晋升通过。

## 当前authority、边界与完整拟后定义

baseline为docs/architecture/README.md（guru-trellis-architecture / active）；constitution为00-foundation/design-constitution.md（guru-trellis-design-constitution-v1 / current）；change contract为06-governance/change-contract.md（guru-trellis-architecture-change-contract-v1 / current）。Planning采用guru-maintain-architecture-baseline:planning:3.0、concern set guru-trellis-architecture-change-concerns-v1。R/B authority为docs/requirements/README.md与docs/design/README.md的guru-trellis-rdt/active，完整命中local-fix-intake和issue-content。

change_path=target_native；必要decision=ADR-ISSUE-REVIEW-INTAKE。完整设计唯一定位为
.trellis/tasks/11-14-819-issue-review-intake/deliveries/f108d161-d60d-4c89-91bf-d96004ef86a6/design.md 第4–7节。本文不复制公共接口完整规格。

拟后定义：已有Issue在原Sync后先到原Readiness新入口。AI读取完整live对象、讨论/评论、必要前置和相关代码，直接ready或只补最早缺口；三个原局部owner通过各自profile完成并回同Issue/base/continuation的Readiness。来源角色歧义仍由Clarify处理；脚本只校验对象/固定来源/返回关系和真实producer结果，不把评论、hash或receipt当覆盖authority。无Issue/draft/no_issue仍用真实完整链，不改变Task后续门禁。

来源接续遵从原Create Task当前Interface选择的profile2.0/共享creation3.0和MIGRATION-813。新入口、局部及刷新保base_source的真实kind/selected_ref/commit，仅投影reviewed_base_source；Task集成branch和未来delivery target仍由原Create Task分别审定。原来源对象/acquisition等值、同步来源分支身份、新建时local HEAD条件及成功结果恢复语义保持，详细规格与字段例子只读Delivery design §5.1–5.3。旧1.0 schema不进入本项consumer判断；不新增长期兼容层或Task状态。

Create完整草稿审核后创建、正式内容读回、评论、评论读回才created；Clarify在实际复审且本次写范围明确时发布/更新准确评论，只读不写。共用Clarify-owned评论正文规则，不新增固定模板或历史评论准入条件。Create复用单次attempt只定位其已成功Issue/comment，Clarify复用source_actions/readback和原动作恢复；没有独立长期ledger或评论状态authority。

## Owners、共享单写与拟targets

current/target semantic owners均为原Sync、Discovery、Clarify、Wording、Readiness、Create Issue和Create Task。改变的是它们已有职责的profile/consumer和评论完成终点，不将判断交给executor。Author独占Task/Delivery规划；原RDT只写三层authority；原Architecture单写共享架构；tools owner单写受管投影。

| 拟共享target | 真实内容责任与当前边界 |
| --- | --- |
| docs/architecture/03-domains/issue-review-intake.md | 完整原/目标流程、七owner、对象/来源/返回与评论恢复、direct consumer及迁移关系；实施期按真实after形成完整proposed，不能只发布增量说明。 |
| docs/architecture/adr/issue-review-intake.md | 同目录issue-review-intake.md的决定，实施期按真实差额完善；Planning不向共享ADR index登记。 |

不改共享root/system/ownership/列表。必要关系直接定位上述完整unit及原local-fix-intake/issue-content；原RDT owner窄替代固定全链命中条件并保事实reuse/内容方法，不遗留冲突current。其他Task、共享GAP和owner定义不在允许写范围。

## 九 concerns

| Concern | applicability、理由和落点 |
| --- | --- |
| authority-binding | applicable：Planning3.0同Task/key/purpose，当前baseline及change-contract已明确；后续非Planning按原6.0/Delivery4.0，不套旧2.0asset。 |
| constitution-binding | applicable：五原则完整读取。官方Markdown扩展面、逐出口完整语义、原owner隔离、最小调用期handoff和target_native直接迁移分别满足本项真实约束；独立评估仍属原Architecture。 |
| boundary-and-decision | applicable：R1–R7和SC01–12要求共同评论与分流；新profile改变前序及consumer而不增Task模型；ADR说明旧末尾限制及替代。 |
| owner-and-single-writer | applicable：上述current/target owners不变；Author写隔离候选，原maintenance owners共享单写，脚本不判覆盖/路线。 |
| compatibility-and-exit | applicable：新schema/Interface/consumer按MIGRATION-819同步切换，旧资产仅保pinned验证；current无dual-reader，完整链保其draft/no_issue/资格确认真实不同用途。 |
| gap-and-deviation | applicable：修本项已接受的入口/评论能力缺口；不创建、恶化或重开ARCH-GAP-006/008，不扩owner/第二authority。关闭本项需真实验收与交付，Planning不能宣称缺口已闭合。 |
| parallel-scope | applicable：仅本Task规划及819隔离贡献可写；禁止竞争其他Task和共享current/GAP/owners。共享final_integration写前核live expected-current，冲突回原owner。 |
| evidence-and-freshness | applicable：candidate是实际已形成机制，final_plan绑定Wording-current design实际bytes及贡献/ADR；before固定B，after及工程/外部证据当前未产生，后续按真实边界补足。 |
| review-and-promotion | applicable：本贡献/ADR由独立final_plan审核；实施后完整proposed与真实工程结果交原final_integration/readback，TaskCommit后一次独立完整Review才能建立reviewed_promoted。 |

project descriptor= guru-trellis-architecture-convergence:repository:1；check id/version= guru-trellis-architecture-convergence/1；result contract= guru-project-architecture-check-result-2.0；原ARCH-GOV-006..009、ADR-005/009及closed GAP006/008约束保持。本文不生成或代填project-check pass。

## 前后状态、成本、替代与迁移

before：原Readiness必须在本轮完整链末尾，局部完成自动走后续owner，Create没有评论终点。拟after：真实当前充分性判断先行，按缺口往返原owners；评论是可读依据且有原动作恢复。

必要成本为现有七包、workflow/graph/Interface及matching投影迁移，Readiness真实live复核，Create多一次评论发布/读回。取消新入口仍不能满足按缺口开工；另建复核Skill重复同一职责；强制全receipt重跑继续制造无效工作；长期coverage ledger引入共享写、维护和不必要生命周期。选择原owner profiles与最小对象/返回identity，避免这些成本。评论attempt定位仅覆盖当前executor，不用于历史覆盖资格。

旧current消费者同批适配；旧新完整provider不混装。已执行旧创建动作由pinned原owner恢复Issue事实，再在新实际评论动作范围内补必要结论，不重复Issue、不把旧pass换标签。旧未发生动作在matching新入口重新判断；历史schema/example保原字节可追溯，runtime不增加fallback。无未知未来consumer或长期兼容例外。

## 证据、直接consumer与晋升边界

Planning候选写作时已经完成完整来源和机制调查、根scope接受、D1需求、独立candidate_assessment及隔离拟写；当时Wording/final_plan/Approval、Activation和工程/采用尚未完成。当前完整实施、配置quality、同checkout原tools及直接ready观察已完成，实际结果及剩余Agent/live GitHub/交付边界由配对Test单写。本段截止于Architecture共享写前，不把Planning或工程结论写成独立committed Review。

V819-01–07的输入/动作/独立观察见design §8及implement §3。Planning直接consumer是原final_plan，不要求尚未产生的工程after。实施期原owner读取本贡献和完整拟targets、保晋升前authority，核expected-current后整合/readback，返回integrated_pending_review；随后TaskCommit纳入真实after，新的独立committed reviewer判断Architecture before/after与完整质量。当前promotion pending，不直接改共享current，不为追写最终SHA再加文档提交。

