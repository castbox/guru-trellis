# Architecture Change Contract

Identity：`guru-trellis-architecture-change-contract-v1`；状态：`current`；required concern set：`guru-trellis-architecture-change-concerns-v1`。本文件是本仓库 task-local Architecture change contract 与 project-check protocol 的项目 authority；Guru Team public package只定义可复用 shape 和 routes。

## Required concerns

| Concern | Required current meaning |
| --- | --- |
| `authority-binding` | Planning 绑定 `guru-maintain-architecture-baseline:planning:3.0` 与明确的 `candidate_assessment` 或 `final_plan`；非 Planning impact/promotion 绑定 `guru-maintain-architecture-baseline:4.0`（Delivery2.0）；bootstrap/repair 保留原2.0合同；同时绑定明确阶段适用的 baseline 与本 change-contract identity |
| `constitution-binding` | 绑定 current constitution locator、status、version/content identity 与实际命中的原则 refs |
| `boundary-and-decision` | 记录 requirement/behavior authority、current/target boundary、decision/GAP refs 与唯一 change path |
| `owner-and-single-writer` | 明确 current/target semantic owner、task writer 与 shared-current promotion single-writer |
| `compatibility-and-exit` | legacy/adapter 适用性、owner、可验证退出与旧实现删除条件；`target_native` 不保留 dual-read |
| `gap-and-deviation` | 区分计划关闭、保留、新增和恶化的 GAP/偏移，并为每项保留 owner 与 closure condition |
| `parallel-scope` | 列出允许的 task-isolated scope 与禁止竞争的 shared current/GAP/owner 范围 |
| `evidence-and-freshness` | 绑定 design responsibility、before/after、test/runtime/external evidence 与当前 invocation freshness |
| `review-and-promotion` | 绑定 contribution、必要 ADR、independent committed range、expected current 与 promotion state |

每项必须显式判定 `applicable|not_applicable` 并给出理由；architecture impact 不得以空值代替判断。范围、风险、authority、持久化、SDK、外部、owner 或架构边界扩大时，旧结果 stale 并重新进入 Architecture owner。

## Stage-applicable authority（ADR-028）

每次读取 live authority 后，原语义 owner 判断本阶段实际适用的基线、规则与候选；无关整体 CURRENT、安装版本或共享 ref 前进不自动使在途结论 stale。真实 scope、规划假设、实现、依赖或明确立即适用规则改变时仍回对应原 owner，旧快照不能遮蔽这些变化。内容候选与 integration target 分离；不以 latest-target ancestry 代替完整内容审查或当前 PR 资格。

shared-current promotion 自身仍绑定写前 expected-current；错配只由原 promotion owner 按实际差额处理。已经发生的 promotion 新 diff 仍重新经过 Phase2/TaskCommit/独立完整 BranchReview。九 concern、descriptor identity、check id/version 与 result contract 保持；ADR-005 中的普遍 CURRENT-advance stale 片段按 ADR-028 的窄 successor 解释，不创建第二 authority 或新增检查协议。

## Constitution applicability consumption

对完整当前 change 的新增能力读取唯一 current constitution 的 `minimum-necessary-complexity` 适用结论及 evidence；覆盖公共合同与抽象，不局限 task-local 持久化。Applicable concern 绑定真实必要性、具体冲突或证据缺口；不创建空白逐原则 verdict、逐能力 DTO 或评分表。

当前 Requirement 必要而 mechanism 多余时，由当前阶段 qualification owner 经既有 `mechanism_revision_required` consumer 返回设计/实现 remove/replace，保留 accepted scope。Requirement-authority 本身冲突由 Architecture `architecture_conflict` -> `guru-architecture-baseline-planning-router` 返回 Planning，需修订 source scope 时进入既有澄清并取得新 current 后重审。缺适用证据使用 `contract_incomplete`，真实选择/依赖使用已有澄清/blocked。Phase 2 的真实 scope/authority 变化由 `planning_stale` 承接；Branch Review 的当前 finding 和真实 scope choice 分别由 `implementation_required`、`scope_confirmation_required` 承接。Project-check 在现有九 concern 和 before/after 中判断这一消费，不新增 descriptor、exit 或脚本语义判定。

## Change paths and lifecycle

- `target_native`：新能力直接进入 target boundary，不新增 legacy authority 或 compatibility layer。
- `legacy_boundary_convergence`：仅在旧边界仍有真实依赖时保留局部 compatibility，并明确 remaining debt、owner、退出和删除条件。
- `dedicated_refactor_slice`：在行为/API/规则不变前提下，以单一主写的小切片收敛旧实现，要求可验证、可观测、可回滚和明确删除条件。
- `no_architecture_impact`：只记录 current baseline/constitution、task/stage 与可审核理由，不创建 contribution、ADR 或 project-check burden。

阶段顺序固定为 Planning candidate_assessment impact/path -> Author solution writing -> Wording -> final_plan actual contribution/current eligibility -> Approval -> qualified implementation discovery re-entry -> Phase 2 before/after + project checks -> task contribution/necessary ADR -> independent committed full-diff Branch Review -> expected-current-bound serialized promotion -> fresh Phase 2/commit/Branch Review -> Publication/Acceptance current consumption。未 promotion 的 `reviewed_candidate` 不得进入 Publication/Finish。

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

Clarify active scope_ready1.0 在完成 scope 判断后，经原 clear-router 的薄 consumer1.0 projection 交同一 Author，先判断后写作；不写 planning hash、生命周期或授权状态。Wording change refs、Approval revision actions 与 Delivery/Completion 的适用修订原因均经显式 projection 回唯一 writer。旧 planning2.0 无 purpose 入口不作 runtime fallback，中断旧调用 fresh 重入；合法非 Planning2.0 和历史 validation assets 保持原边界。canonical workflow/preset matching migration 是唯一安装切换路径。

#531以ADR-024迁移上述Planning责任：Task整体scope-only由Author写作后Clarify审查；Delivery candidate/final两目的独立Architecture、Wording、Approval与Activation保持原owner，同DeliveryKey/planning_root回程。Task-only Completion/Finish仍使用task_impact_sync，不将Delivery与Task结果换标签。

## #600 晋升顺序与输入后继

[ADR-030](../adr/030-promotion-before-final-check.md)作为 ADR-005 的晋升时机后继。非 Planning4.0/Delivery2.0 current input 显式绑定 before_authority 与完整 candidate；promotion 移除尚未发生的 committed_range 前置。Planning purpose3.0、bootstrap/repair、九 concerns、descriptor/check/result identities 与原 owners保持。新 CURRENT 必须作为受审差额与晋升前 authority 比较；最终 Check及committed独立判断覆盖实际写入。窄引用对齐、恢复和在途切换由 [MIGRATION-600](../../../trellis/presets/guru-team/MIGRATION-600.md)定位原合同。
