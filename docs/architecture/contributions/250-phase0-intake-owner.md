# #250 Phase 0 Intake task-owned Architecture candidate

Identity：`architecture-contribution-250-phase0-intake-owner-v2`；状态：`task-owned phase2 reviewed candidate`；change path：`target_native`。本文件承接当前实现候选的 Architecture 判断，不表示完整 Phase 2、committed review、promotion、Delivery 或完成。

## Authority 与边界

Task locator：`.trellis/tasks/10-11-250-phase0-intake-owner`；requirement authority：`https://github.com/castbox/guru-trellis/issues/250` 当前 `2026-10-10-r19` 正文中的 owner、profile、context return、source 与 entry 约束。Behavior/design object：该 task 的 `design.md`，以及 current canonical workflow/Skill contracts。
Guru contract：`guru-maintain-architecture-baseline:2.0`。
Baseline / expected current：`docs/architecture/README.md` / `current-main-0.6.17-guru.82` / `active`。
Constitution：`docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / `content` / `current`。
Project change contract：`docs/architecture/06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1`；concern set：`guru-trellis-architecture-change-concerns-v1`。
Applicable principle refs：`mature-practice-applicability`、`concept-semantic-completeness`、`cohesion-change-isolation`、`minimum-necessary-complexity`、`debt-one-way-convergence`；仅引用 identity，不复制原则正文或建立评分。
Domain/integration refs：`ARCH-DOM-001/003/004/005/006/016/029/037/038`、`ARCH-INT-001/002/005/007/019/041`；decision refs：`ADR-001/004/005/009/011/016/019`；项目检查继承 `ARCH-GAP-006/008`，不改变其 closed 状态。

## 九项 required concern applicability

| Concern | Applicability | 当前设计事实与限制 |
| --- | --- | --- |
| authority-binding | applicable | 明确绑定 current baseline、Guru 2.0 与项目 change contract；#250 的真实新约束与 design object 分离，不由旧 task/摘要决定 authority。 |
| constitution-binding | applicable | 新 profiles 是当前六种具名入口所需；return identity 服务当前四类 context consumer；source locator/choice 服务当前 Planning。无 unused 字段、未来 Author gate 或审计 capsule。 |
| boundary-and-decision | applicable | Clarify 单写 Intake 意图、来源分类与真实选择；Discovery 单写检索充分性；Wording/readiness 保留各自判断，Planning 单写最终技术处置。初始 Sync→Discovery→Clarify 不变。 |
| owner-and-single-writer | applicable | 不新增 lifecycle/source/task/session owner。脚本只验证/投影事实；本 task 写隔离候选，Architecture/RDT 原 owner 分别串行 promotion shared current。 |
| compatibility-and-exit | applicable | 公共 profiles/schema 直接演进，有显式 successor 编号及同步 consumer migration；完整 preset/current callers 同轮更新。无 dual reader、alias、fallback 或旧 invocation 自动成功转换。 |
| gap-and-deviation | applicable | 当前候选在同一 owner graph 内替换固定 pre_task/initial_change_request 回程；未观察新增或恶化职责偏移，不新建或重开 ARCH-GAP-006/008，不扩张无因果关系历史债务。 |
| parallel-scope | applicable | 允许本 task 的候选、相关 canonical packages/workflow/受管投影和定向文档；禁止竞争 shared current/GAP/constitution、其它 task、上游 trellis-* 与业务生产写入。 |
| evidence-and-freshness | applicable | Phase 2 独立评估完整 tracked/untracked 候选与 unchanged consumers、HEAD before 和正常 wrapper 行为；本阶段适用 Architecture check 已执行，native 与完整任务验收边界由唯一 Test 如实承接。每阶段绑定自己的候选，scope/owner/source/boundary 扩大即重入。 |
| review-and-promotion | applicable | 本贡献已形成 Phase 2 Architecture reviewed candidate，仍待独立 committed full-diff review；随后按 expected .82 串行 promotion。晋升 diff 再经 fresh Check/commit/完整 Branch Review。 |

## Before / target 与直接 consumer

Before：current Clarify `needs_context` wrapper 固定输出 `handoff_profile=pre_task`，只投影 base/continuation；Discovery `context_ready` wrapper 固定输出 `handoff_profile=initial_change_request`。active/standalone return identity 无法由该 public loop 保留。当前 clear transition 不携带明确选定 source sections；readiness reroute 也固定 initial profile。

Target：Clarify 以 standard_intake/reviewed_plan_intake 替换旧 initial profile，保留 active、standalone 与两种 qualifier confirmation。四个 context-capable profile 在 load-bearing evidence 不足时进入 Discovery 的 discriminated context_request；output 仅携带原 return profile、target/continuation、active TaskId/generation 或 standalone consumer 以及必要客观 context 身份。Discovery 不读 Clarify private state，fresh return projection 只组装目标 owner 的合法 input。

两个 qualifier confirmation 继续消费各自原 qualifier 的最小输入和精确 original owner；authority/context repair 回原 qualifier re-entry，不经过另一 qualifier 或重解释其结论。Planning/Approval、Architecture、Reconcile、Check、Branch Review、Delivery Review、Completion 与 task-free 的现有 scope ingress 保留各自唯一 consumer。

source selection 只包含 load-bearing locator/section 和不可重新推导的当前语义选择，经过声明的薄 relay 交给当前 Planning；不携带全文、retain/change/reject、review history 或授权。Wording/readiness 不解释这项选择，不产生新的 source authority。Create Task 的 created identity 与 official task.json 不增加来源模型；丢失相邻 selection 时回原 Clarify/context owner，不猜测或建立 cache。#292 未交付时当前 Planning 仍是实际 consumer。

更直接的替代为保留初始顺序并只修复 profile/return/source projection；这已承担全部当前必要职责。Clarify-first 同时改变 Sync 和 duplicate snapshot 前置，无当前额外必要性；通用 capsule、shared cache 或未来 Author adapter 不进入本候选。

## Owner、compatibility 与删除条件

Current/target semantic owners 相同：Sync 负责 base，Discovery 负责 context evidence，Clarify 负责 Intake 语义，Wording 负责 wording，readiness 负责 readiness，Planning 负责设计，原 mutation/lifecycle owners 负责其操作。Guru-owned workflow/entry 约束 brainstorm 的本轮 owner/stage/return；上游 questioning method 保持可发现且不被 preset patch/delete。

Single writer：task checkout 的候选实现 owner 写本 task-isolated changes；官方 task/session、branch binding 和 resource ledger 的既有 writers 保持；shared current 仍由原 Architecture/RDT promotion owners 写入。无新 store、session slot、ledger、路径映射或 durable Intake artifact。

Legacy compatibility exception：无。原 schema/profile 仅可作为明确 pinned-old history 留存；全部受控 current producer/consumer/interface/registry/installed/platform projections 迁移完成后，旧 current selector、固定回程及无 consumer examples 退出。旧在途调用通过既有 source refresh/re-entry 获取 current 输入，不转换成新成功 DTO。完整 preset 同步不足或 mixed install 沿现有 validator 阻塞；实际迁移结果待后续证据，不在 Planning 宣称通过。

无关 Related Work 变化不作废完整链；只有实际依赖发生变化的 owner evidence 重入。active replanning 继续使用 #468 的 resume_execution，TaskId/generation/source/session/checkout 不重建。

## Project-check protocol 与 evidence

Descriptor：`guru-trellis-architecture-convergence:repository:1`；check id/version：`guru-trellis-architecture-convergence` / `1`。
Entrypoint：`docs/architecture/06-governance/change-contract.md`，是 AI 语义协议；result contract：`guru-project-architecture-check-result-2.0`。
Applicable scope：stage invocation、authority binding、path exclusivity、required concern completeness、before/after regression、single-writer、parallel stale、contribution/ADR review、promotion freshness。
Rule refs：`ARCH-GOV-006..009`；decision refs：`ADR-005`、`ADR-009`；gap refs：`ARCH-GAP-006`、`ARCH-GAP-008`。
Freshness source：当前 design bytes、本贡献与 current authority；Phase 2 改用完整实际 candidate，Branch Review 改用 exact committed range。实际 owner result 承载该轮 descriptor-bound result；本贡献不预填 future check pass。

Design responsibility overview：task `design.md` 的 profile/return graph、API migration、source→Planning seam、scope ingress 与 state/distribution。Detailed：canonical Clarify/Discovery contract/interface/schema/runtime，current Sync/Wording/readiness/Create Task consumers，以及 Guru-owned entry/continuation。
Runtime evidence locators：`trellis/skills/guru-team/packages/guru-clarify-requirements/runtime/invoke.py`、`guru-discover-change-context/runtime/invoke.py`、`guru-review-change-request/runtime/invoke.py`；`trellis/workflows/guru-team/workflow.md`；current target installed counterparts。
Test evidence owner：`docs/requirements-design-test-contributions/250-phase0-intake-owner/test.md` 是唯一实际 Test locator，拥有当前实际执行结果、首次失败/恢复及未验证边界。Architecture owner 亲自执行适用检查并区分正式 wrapper 的客观传输与真实 Agent 行为；静态绿色不能替代后者。
Existing projection `.trellis/spec/architecture/baseline-usage.md` 的 .79 摘要不是 current .82 authority；本 task 的 Docs SSOT Plan 已指明受影响定向同步，shared promotion 仍由原 owner 承接。此处不批量修订历史摘要。
Official extension evidence：已直接读取 `https://docs.trytrellis.app/index.md`、`https://docs.trytrellis.app/advanced/custom-workflow.md` 与 `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`。官方 workflow 合同允许通过 Markdown phase/routing/breadcrumb 改变运行行为而不改 Python/hooks；spec marketplace 只承载可复用工程规则，不承载 task、private runtime 或平台 prompt。本候选采用这些现有扩展面，保持 upstream-owned entry/method 与 Guru-owned runtime/Skill 边界。
External runtime/install status：仅按唯一 Test 的实际对象和层级承接；本轮独立执行 source/installed validators、dogfood drift 与 installed profile integration，证明当前受管投影和正常 wrapper 回程。后续证据补齐当前来源到 Planning、普通 prompt/方法复用、partial、实际压缩恢复及无变化 active resume 的具名观察；结果、首次失败与恢复均只由唯一 Test 承接，不在本贡献复制执行叙事。该证据增量未改变实现、DTO、workflow、owner 或 architecture boundary，原独立判断仍适用；完整多平台 Upgrade/Release matrix、其它 host/model、真实 external GitHub mutation、业务生产安装/部署与软件发布仍未验证。

## Phase 2 before/after Architecture 判断

本轮先读 current constitution、Baseline 分区和 change contract，再评估完整候选、实际消费者及相似 qualification/continuation 能力，独立形成判断后才读取 task design 和本贡献。HEAD before 的固定初始回程由显式六 profile 与四类 return identity 替换；当前 Sync→Discovery→Clarify 顺序、Wording/readiness 判断和现有 mutation/terminal owners 保持。

新增 `source_selection` 的唯一语义生产者是 Clarify，Wording/readiness 只投影，当前 Planning 在 live TaskId/binding/checkout 解析后消费并 fresh reread 来源；最终技术处置留在 design.md。Interface 1.8 只声明读取 producer `handoff_profile` 的 schema selector，不新增语义 router、表达式引擎、private-state reader 或持久化来源模型。两 qualifier confirmation 继续各回原 owner；普通 generation/source mismatch 停止并重入，不转换旧调用为新成功。

项目九 concern 均适用且当前 candidate 满足其 Architecture 边界；路径保持 `target_native`。新增属性与独立 schema 由当前受支持入口/直接 consumer 触发，无未知未来扩展依据；更薄实现仍需承担相同 caller identity/source selection 职责。未证明新或恶化 owner 扩张、第二 authority、无退出双写或 closed GAP 重现。ADR 仍不必需；shared current 未被本候选修改。后续 Test 证据及本贡献边界说明变化由原 Architecture owner 按依赖范围 fresh 重读、重绑定；该结论仅允许本阶段接续 Check，不替代完整 Check、committed review 或 promotion。

## Deviation / ADR / review / promotion

Deviations.closed：无实现关闭声明；retained：descriptor 继承的 closed GAP 状态、独立 Release/业务验证边界及因果无关历史债务；new：当前设计没有已证明新增 owner/双写/authority 偏离。实现 discovery 或后续 review 发现实质变化时重入原 owner。
ADR：`required=false`，locator 为空。当前设计遵循已有 semantic/执行分层、单图 continuation、最小 public projection 与 current-only migration 决策，不新增 owner/single-writer、原则例外、GAP lifecycle 或 legacy compatibility exit。API successor 不等同于新的 architecture decision；实际实现改变这些边界时必须重新判定。
Review：`pending` / `independent=false` / `committed_range=null`；这只描述尚未发生的 committed review，不替代各阶段实际评估。
Promotion：`required` / `promoted_identity=""` / `expected_current_identity=current-main-0.6.17-guru.82`。live current 已推进时走 `sync_required`，不覆盖。无 future reviewed/promoted 状态或完成声明。
