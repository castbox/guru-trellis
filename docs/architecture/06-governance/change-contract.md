# Architecture Change Contract

Identity：`guru-trellis-architecture-change-contract-v1`；状态：`current`；required concern set：`guru-trellis-architecture-change-concerns-v1`。本文件是本仓库 task-local Architecture change contract 与 project-check protocol 的项目 authority；Guru Team public package只定义可复用 shape 和 routes。

## Required concerns

| Concern | Required current meaning |
| --- | --- |
| `authority-binding` | Planning 绑定 `guru-maintain-architecture-baseline:planning:3.0` 与明确的 `candidate_assessment` 或 `final_plan`；非 Planning impact/promotion 绑定 `guru-maintain-architecture-baseline:5.0`（Delivery3.0）；bootstrap/repair 保留原2.0合同；同时绑定明确阶段适用的 baseline 与本 change-contract identity |
| `constitution-binding` | 绑定 current constitution locator、status、version/content identity 与实际命中的原则 refs |
| `boundary-and-decision` | 记录 requirement/behavior authority、current/target boundary、decision/GAP refs 与唯一 change path |
| `owner-and-single-writer` | 明确 current/target semantic owner、task writer 与 shared-current promotion single-writer |
| `compatibility-and-exit` | legacy/adapter 适用性、owner、可验证退出与旧实现删除条件；`target_native` 不保留 dual-read |
| `gap-and-deviation` | 区分计划关闭、保留、新增和恶化的 GAP/偏移，并为每项保留 owner 与 closure condition |
| `parallel-scope` | 列出允许的 task-isolated scope 与禁止竞争的 shared current/GAP/owner 范围 |
| `evidence-and-freshness` | 绑定 design responsibility、before/after、test/runtime/external evidence 与当前 invocation freshness |
| `review-and-promotion` | 绑定 contribution、必要 ADR、完整候选与晋升前 authority、全部拟写内容、expected-current 与 promotion state；Branch Review 阶段另绑定精确 committed range |

每项必须显式判定 `applicable|not_applicable` 并给出理由；architecture impact 不得以空值代替判断。范围、风险、authority、持久化、SDK、外部、owner 或架构边界扩大时，旧结果 stale 并重新进入 Architecture owner。

## Stage-applicable authority（ADR-028）

每次读取 live authority 后，原语义 owner 判断本阶段实际适用的基线、规则与候选；无关整体 CURRENT、安装版本或共享 ref 前进不自动使在途结论 stale。真实 scope、规划假设、实现、依赖或明确立即适用规则改变时仍回对应原 owner，旧快照不能遮蔽这些变化。内容候选与 integration target 分离；不以 latest-target ancestry 代替完整内容审查或当前 PR 资格。

shared-current promotion 自身绑定写前 live expected-current；错配只由原 promotion owner 按实际差额处理。原独立Phase2及完整候选Check先审实现/隔离拟写，候选出口合法回implementing后由原owners最终整合；implementation重新candidate/begin_check，最终Check、TaskCommit与独立完整committed BranchReview覆盖真实after。九 concern、descriptor identity、check id/version 与 result contract 保持。ADR-005 中普遍 CURRENT-advance stale 与 committed-review-first 的片段分别由 ADR-028、ADR-030 窄替代，不创建第二 authority 或新增检查协议。

## Constitution applicability consumption

对完整当前 change 的新增能力读取唯一 current constitution 的 `minimum-necessary-complexity` 适用结论及 evidence；覆盖公共合同与抽象，不局限 task-local 持久化。Applicable concern 绑定真实必要性、具体冲突或证据缺口；不创建空白逐原则 verdict、逐能力 DTO 或评分表。

当前 Requirement 必要而 mechanism 多余时，由当前阶段 qualification owner 经既有 `mechanism_revision_required` consumer 返回设计/实现 remove/replace，保留 accepted scope。Requirement-authority 本身冲突由 Architecture `architecture_conflict` -> `guru-architecture-baseline-planning-router` 返回 Planning，需修订 source scope 时进入既有澄清并取得新 current 后重审。缺适用证据使用 `contract_incomplete`，真实选择/依赖使用已有澄清/blocked。Phase 2 的真实 scope/authority 变化由 `planning_stale` 承接；Branch Review 的当前 finding 和真实 scope choice 分别由 `implementation_required`、`scope_confirmation_required` 承接。Project-check 在现有九 concern 和 before/after 中判断这一消费，不新增 descriptor、exit 或脚本语义判定。

## Change paths and lifecycle

- `target_native`：新能力直接进入 target boundary，不新增 legacy authority 或 compatibility layer。
- `legacy_boundary_convergence`：仅在旧边界仍有真实依赖时保留局部 compatibility，并明确 remaining debt、owner、退出和删除条件。
- `dedicated_refactor_slice`：在行为/API/规则不变前提下，以单一主写的小切片收敛旧实现，要求可验证、可观测、可回滚和明确删除条件。
- `no_architecture_impact`：只记录 current baseline/constitution、task/stage 与可审核理由，不创建 contribution、ADR 或 project-check burden。

阶段顺序为Planning candidate_assessment→Author solution→Wording→final_plan→Approval/Activation→implementation/完整隔离拟写→implementation candidate/begin_check→独立Architecture phase2及原Check候选检查→原Check合法rework回implementation→candidate_checked唯一router→原owners final_integration/readback→implementation重新candidate/begin_check→最终Architecture/Check→TaskCommit→独立完整committed Review→readiness/Ready/Acceptance。稳定正常候选无需在晋升前先做 committed Review；finding 修复、多 Delivery、真实候选改变或合法窄绑定刷新仍按原生命周期回最早受影响 owner。未 promotion 的 `reviewed_candidate` 不得进入最终 readiness/Ready Publication 或 Finish；早期 Draft 反馈按 ADR-033 的独立入口承接。

## Current project-check descriptor

- descriptor identity：`guru-trellis-architecture-convergence:repository:1`。
- check id/version：`guru-trellis-architecture-convergence` / `1`。
- entrypoint：`docs/architecture/06-governance/change-contract.md`；这是 AI 语义检查协议，不是替代判断的脚本。
- applicable scope：stage invocation、authority binding、path exclusivity、required concern completeness、before/after regression、single-writer、parallel stale、contribution/ADR review 与 promotion freshness。
- rule refs：`ARCH-GOV-006..009`；decision refs：`ADR-005`、`ADR-009`；gap refs：`ARCH-GAP-006`、`ARCH-GAP-008`。
- result contract：`guru-project-architecture-check-result-2.0`；freshness source 是当前 task candidate 或 exact committed range。

稳定失败路由为：缺适用 contract/constitution/check facts -> `contract_incomplete`；与 current authority 冲突 -> `architecture_conflict`；新增或恶化偏移、owner 扩张、无退出双写或 closed GAP 重现 -> `fitness_regression`；明确阶段适用的 baseline、constitution、contribution/candidate stale，或本次 promotion 写前 expected-current 错配 -> `sync_required`；无关整体版本/ref 推进不构成此路由。AI 根据 applicability 与 task 真实依赖决定 `blocking`，runtime 只验证 descriptor/result 一一绑定、locator、freshness 与 route consistency。

## Current Planning boundary

`guru-author-task-plan` 独占整体 scope PRD 与每 Delivery PRD/design/implement 的规划语义写作及已有 revision 回程，Clarify 的来源/scope 判断、Architecture 独立评估、Wording 受控 rewrite 与 Approval 批准分别归其原 owner。`candidate_assessment` 评估真实候选但不要求尚未产生的 contribution，不输出 promotion_state；其 current consumer 是 Author solution_planning。`final_plan` 评估 Wording-current design 与真实 contribution/必要 ADR，保留 reviewed_candidate 或合法 reviewed_promoted 约束，current consumer 只为相邻 Approval。前置结果不能替代最终结果；两目的仍属于同一 Architecture owner/stage，project descriptor/result 保持2.0。

Clarify当前Task/Delivery scope profiles先判断范围，返回无task_key的pre-Author scope_ready2.0；原clear-router交Author task_scope_requirements写实际根PRD，scope_requirements_ready及原selection再交Clarify task_scope_requirements_acceptance。只有acceptance核真实AuthorityRef并accept_scope，输出含task_key的post-acceptance scope_ready；其consumer才按义务进入原stage合法rework/stop、显式Creation或Completion。三种scope_action均保留该顺序，不能把pre结果当发布或post结果重复写根PRD。无current Delivery不造空切片。

Wording change refs、Approval revision actions与Delivery/Completion修订经显式projection回唯一writer。旧#292 private4/scope_ready1、active_task_scope_change Author及Task-status activation/resume只属固定旧完整安装，不作current fallback。旧planning2.0无purpose入口也不回退；非Planning5.0/Delivery3.0与bootstrap/repair保持。完整matching切换见MIGRATION-657，公共created wire、原初始Creation validator、原producer恢复及唯一continuation保持；既有Task按当前identity/binding/checkout和实际stage gates续接，Delivery created consumer重读公共phase并核实际未完成义务后进入适用owner。只有真实initial requirements且符合入口才initial Author；已有planning回适用Author/Wording/Architecture/Approval，当前approved进入Activation，缺失/过期输出回原producer。该窄决定由ADR-035拥有，不新建descriptor、状态authority或授权存储。

#531以ADR-024迁移上述Planning责任：Task整体scope-only由Author写作后Clarify审查；Delivery candidate/final两目的独立Architecture、Wording、Approval与Activation保持原owner，同DeliveryKey/planning_root回程。Task-only Completion/Finish仍使用task_impact_sync，不将Delivery与Task结果换标签。

## 当前候选、晋升与恢复输入

非 Planning `5.0` / Delivery `3.0` input 显式绑定 `before_authority` 与完整 `candidate`。前者定位固定 Git authority 的 baseline、constitution 和 change-contract，后者绑定当前 head/content identity。Branch Review 的 before Git revision 等于精确 committed range 的 base。新 CURRENT 必须作为受审差额比较，不能以其自身证明符合旧约束。Planning purpose `3.0`、bootstrap/repair、九 concerns、descriptor/check/result identities 与原 owners 保持。

promotion发生在final_integration，绑定贡献、原独立Architecture及完整候选Check和完整proposed targets，不要求尚未发生的 committed_range。原 owner 写前重读 live expected-current 及各 target 原文；一致时只写已审内容。写后读取全部实际 targets 并判断语义、依赖与验证义务是否保持，再交implementation重新candidate/begin_check，最终Architecture/Check只消费新的content_ref。发生额外变更、内容缺失或适用性变化时回原 assessment/check，不借用旧结论。

部分晋升写入由原 owner 按同一个唯一 intent 区分 completed、pending、conflict；只补未冲突的 pending 内容。冲突或 intent 不明确时停止。完成后输出丢失，只从仍匹配的实际文件和原 intent 恢复同一结果，不创建新 successor 或长期账本。不可重新推导的恢复内容仅在有直接 consumer 时进入 owner-private 短期运行状态，消费后删除；授权信息不写入任何状态。

本合同直接给出当前顺序；[ADR-KNOWLEDGE-FINAL-INTEGRATION](../adr/knowledge-final-integration.md)拥有当前时机决定，[MIGRATION-638](../../../trellis/presets/guru-team/MIGRATION-638.md)定位接口切换及在途恢复。旧 `.100` 内容与 ADR-005 历史保持可追溯，不是当前执行前置。

## 当前知识和通用源的项目读取关系

按本阶段实际问题选择完整知识单元与必要关系，不以历史增量回放替代当前定义。RDT 和 Architecture 各由原维护方拥有正文与晋升，导航只定位。Architecture 的 FOUNDATION/CURRENT/TARGET/GAP/PLAN/ADR/EVIDENCE 仍分工；本文件不把 accepted target、推断或验证缺口提升为实现事实。

[技术基线选择](../00-foundation/stack-selection.md)定位本项目选定的公共技术栈源、准确版本、项目约束和差异。Architecture owner 在本项目范围维护投影，源维护方在公共源范围维护完整定义。源或引用缺失、范围冲突、迁移未完成时，明确受影响结论并进入原 repair/澄清，保留原 authority。源版本推进不自动替换已选版本或要求旧 Task 重写。当前组织候选的迁移与普通读取退出由 [MIGRATION-331](../../../trellis/presets/guru-team/MIGRATION-331.md)定位，最终状态由原 owner 晋升和真实 Test/EVIDENCE 决定。

## 早期 Draft 与最终 Publication 的区分（ADR-033）

#636 原 TaskCommit/Publication 在 implementing 的已激活切片中提供有界提交和同PR Draft反馈。该入口不消费最终Check/readiness，也不写公共gate或PublicationFact。Draft后固定B/H内容分析与风险验证并行；新未审HEAD push前由原Publication确保Draft。早期分析不自动映射正式full_review；最终Check predecessor、原完整质量链和Refs-only/Closure保持。

上述反馈可先于最终Phase2晋升链，不属于ARCH-GOV-008禁止未晋升贡献进入的最终readiness/Ready发布。独立Phase2仍评估完整实现与全部拟晋升内容，再原owner晋升/判断实际写入、最终Check、commit及独立完整committed Review；当前最终整合时机按上文执行，Draft本身仍不是最终结果。正式非Planning Architecture stage=publication仍用于最终Delivery readiness，不以Draft存在制造该stage通过。

## 候选适用性与独立职责（ADR-034）

Architecture 原 owner 保留首次独立读取顺序及当前 project-check 判断。后继读取合法原覆盖、Hr..Hi 全部真实差额、冲突双方/组合语义及受影响未改 consumers，分别确定保留、失效和补充；原覆盖不足补审，影响无法界定完整评估。同合规独立 reviewer 可以接续并依次完成 Architecture 与 Branch Review，各 matching stage 的判断和 formal result 仍实际发生。新架构事实回原评估；HEAD、阶段或身份变化本身不要求重建。

工程事实按定义/版本、输入/依赖、环境/工具链/参数/期望采用或补命中项，计划 ref 不证明执行，同树不证明环境。原公开结果/调用对象、精确 Git/正文与原命令为合法依据；初次 implementation_required 无 passed full_review，refs 只定位缺陷。缺来源补真实工作，不跨读或重建退休 private，不加账本、覆盖 DTO 或 digest 链。当前 Check/full_review 及 predecessor 绑定、finding ancestry、当前 payload/Issue/live 判断保留。

唯一执行定义由 [workflow-contract](../../../trellis/presets/guru-team/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage)单写；本合同只拥有项目职责和 concern/project-check 承接，不新增 descriptor/check/result identity。ADR-034 窄替代无因 fresh reviewer/相同完整重审；ADR-028/030/033 及九 concerns、single-writer、最终质量覆盖保持。matching安装沿MIGRATION-638，旧安装固定或原 owner 成套切换，同 key 原阶段恢复，不由新语义豁免当前旧安装的门禁。

## 稳定知识身份与真实目标

Architecture authority identity为guru-trellis-architecture，RDT为guru-trellis-rdt。完整单元保留既有identity，精确来源用完整Git revision与repo-relative locator；普通promotion允许同authority identity，不强制总README target、global successor或逐Issue摘要。导航只在定位/身份/状态改变时更新，真实public API/schema版本独立保留。bootstrap仍保留distinct successor合同。目标branch/commit、bytes与恢复intent只在原owner调用或有直接consumer的短期private状态；无全仓hash清单、第二current或授权记录。
