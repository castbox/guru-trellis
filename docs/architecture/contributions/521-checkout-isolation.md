# #521 隔离执行 Architecture candidate

Identity：`architecture-contribution-521-checkout-isolation-v1`；状态：`implementation candidate`；change path：`target_native`。本文件承接当前候选的设计职责、before/after 和适用证据边界；不表示完整 Check、committed review、promotion、业务安装或发布已完成。

## Authority

Task：`.trellis/tasks/10-11-issue-521-checkout-isolation`；requirement authority：`issue:castbox/guru-trellis#521`（live updatedAt `2026-10-10T15:07:28Z`）；design object：该 Task 的 `design.md`。
Guru contract：`guru-maintain-architecture-baseline:2.0`。
Baseline：`docs/architecture/README.md` / `current-main-0.6.17-guru.83` / `active`；expected current 同为 `.83`。
Constitution：`docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / `version` / `current`。
Change contract：`docs/architecture/06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1`；concern set：`guru-trellis-architecture-change-concerns-v1`。
Applicable principle refs：`mature-practice-applicability`、`concept-semantic-completeness`、`cohesion-change-isolation`、`minimum-necessary-complexity`、`debt-one-way-convergence`。只引用 identity，不复制正文。
Domain refs：`ARCH-DOM-001/004/005/008/016/019/021/022/023/026/029`；integration refs：`ARCH-INT-019/024/025/026/029/032/033`；decision refs：`ADR-005/011/014/016/019`；descriptor 继承 `ADR-005/009` 和 `ARCH-GAP-006/008`，不重开其 closed 状态。

## 九项 concerns

| Concern | Applicability | 设计职责与边界 |
| --- | --- | --- |
| authority-binding | applicable | 使用上述唯一 current authorities；live Issue 是行为约束，design.md 是候选，不互相替代。 |
| constitution-binding | applicable | linked/non-base 位置用于解决真实共享 primary HEAD 影响；现有 owners、Git facts 和 typed exits 承担职责，不新增 registry、mapping、Task-free identity、wrapper 或授权存储。 |
| boundary-and-decision | applicable | selector 只判 mode；execute-task-free-change 判位置并执行有界编辑；workflow 消费 no_current_task；C6 creation preparation 拒绝新 Task primary acquisition；upstream entries 保持原 owner。 |
| owner-and-single-writer | applicable | Task/session/branch/resource 原 writers 保持；task-free 不调用 Task wrappers。候选写入本 Task checkout；shared current 仅由 Architecture/RDT 原 promotion owners 串行写。 |
| compatibility-and-exit | applicable | 新安装默认仅 linked/non-base 编辑；旧 current-checkout task-free 合同直接退出 current，无双模式 fallback。旧 primary Task 的既有恢复仍由原 owners 持有，不新增 legacy adapter。逐例迁移需真实安装/Task facts 和适用副作用计划，不能自动搬运或宣称完成。 |
| gap-and-deviation | applicable | 只收敛本次 primary 编辑/新 Task adoption 默认；不关闭或重开既有 GAP，不把无关历史债务扩为本 Task 义务。旧在途 primary 状态和尚无 native 证据是显式边界。 |
| parallel-scope | applicable | 允许本 Task candidate、相关 canonical contracts/runtime、定向 specs/README 和受管安装投影；禁止写 shared current、其他 Task、业务仓受管副本、upstream entries/hooks 或无关 worktree 内容。 |
| evidence-and-freshness | applicable | Planning 依据真实 design bytes、live Issue 和 affected consumers；后续客观 topology/schema/installation 与真实 Agent continuation 分别验证。候选、owner 或实际依赖变化重入，静态证据不替代 native proof。 |
| review-and-promotion | applicable | 本 contribution 和内嵌 ADR 仅 candidate；独立 committed full-diff review 后 expected-current-bound promotion；晋升 diff fresh Phase2/commit/Branch Review。Planning 不声称后续门禁已通过。 |

## Before、target 和唯一 owners

Before：selector 限定 current checkout；task-free execution 不以 default/non-default 阻塞。C6 prepare_creation_inputs 校验 generation-zero acquisition 和非 base/delivery branch，但允许 primary adoption；shared adopt_invocation_checkout 又由 recover_checkout_acquisition 复用。upstream continue 无绑定只返回 no_current_task 并结束自身步骤。

Target：execute-task-free-change 的既有 pre-write suitability 读取真实 topology、registration、common-dir、branch/HEAD、binding 和 dirty 差额，选择本仓 linked/non-base 位置；location_required self-reentry 消费实际位置选择，必要 Git 创建沿原副作用边界执行。selector 不因位置需求自动升级 Task。所有文件/命令指向隔离绝对路径。

正式新 Task 的 primary 拒绝放在 `runtime/task_lifecycle/composition.py:prepare_creation_inputs` 与 `guru-create-task` 的 create-only 合同。共享 `adopt_invocation_checkout`、`recover_checkout_acquisition`、checkout resolution 和旧 Task result recovery 不增加全局 primary 禁令或放宽 clean 校验；base Sync、Cleanup 保留 checkout 职责不变。该位置由已存在 C6 owner 持有，不另建 acquisition owner。

workflow 独占 Guru-owned no_current_task caller continuation：fresh 请求/位置/真实 binding 后返回原 selector/execution owner。upstream start/continue/extractor/hooks 不被 preset patch/delete。现有 native entry 是否实际把 no_current_task 交回 caller 尚未验证；若无法交回，受影响验收暂停，列明最小 upstream change、独立 owner 和未交付依赖，不伪报完整可用。

部分修改后扩张仍立即停止剩余 writes，自动/显式选择分别走原 reselect_mode/explicit_choice_required。原 Intake/C6 owner 读取完整差额后判断复用 clean linked worktree 或另一 clean linked target；承接脏候选需要精确来源/目标/差额及独立适用动作，不自动 stash、重复搬运、丢弃、回 primary 或制造空 Task。没有新增 migration ledger。

Current/target semantic owners相同：selector、task-free execution、workflow continuation、C6 creation、Bind、base Sync 和 terminal lifecycle 各自保留唯一职责。中立 Git facts 是事实材料，不成为语义 policy owner。删除隔离位置职责会重新允许 primary HEAD 影响；更直接的现有-owner实现已满足当前必要职责，无额外抽象依据。

## 退出、删除和证据

Current-only task-free migration owner 是现有 preset/install owner；全部 current canonical/installed/platform callers 同步后退出旧 current-checkout 文案和默认主分支编辑例子，旧版只作为 pinned 历史。不能用 source tests 宣称业务安装生效。
旧 primary Task recovery 是既有 supported behavior，不是新增兼容层；原生命周期 owner 逐例判断何时可迁移到 linked checkout。该 Task identity 在 linked checkout 的 binding/control state 和真实恢复行为已核对后，该对象不再依赖 primary execution；未完成迁移的对象保留原路径真实限制，不删除共享 recovery 能力、不覆盖 pointer，不宣称新默认已普遍生效。任何新增 adapter 或自动迁移将改变本路径，必须重入 Planning。
Deviations.closed：无实现关闭声明；retained：既有旧 primary Task 恢复/真实迁移、独立 Release/业务安装验证与因果无关历史债务；new：本设计不新增 authority/store/owner 或无退出双写，实际 implementation discovery 再判。

Design responsibilities：overview 为 Task design.md 的路径/回程/partial ownership；detailed 为 canonical selector/execution/workflow、C6 prepare_creation_inputs、shared acquisition/recovery/clean resolver 和安装投影。
Runtime locators：`trellis/skills/guru-team/runtime/task_lifecycle/{composition,checkout_acquisition,checkout_resolution}.py`；`trellis/skills/guru-team/packages/{guru-select-workflow-mode,guru-execute-task-free-change,guru-create-task}/`；`trellis/workflows/guru-team/workflow.md`。
Test owner：`docs/requirements-design-test-contributions/521-checkout-isolation/test.md`；该唯一文件拥有实际 native、定向 runtime 和代表性安装结果及首次失败/恢复，Architecture 不复制测试矩阵或预填通过。业务安装、完整矩阵、软件发布仍为独立未验证边界。

Project descriptor：`guru-trellis-architecture-convergence:repository:1`；check id/version：`guru-trellis-architecture-convergence` / `1`；entrypoint：`docs/architecture/06-governance/change-contract.md`；result contract：`guru-project-architecture-check-result-2.0`。
Applicable scope：stage invocation、authority binding、path exclusivity、required concern completeness、before/after regression、single-writer、parallel stale、contribution/ADR review、promotion freshness；rule refs `ARCH-GOV-006..009`，decision refs `ADR-005/009`，gap refs `ARCH-GAP-006/008`。
Freshness source：当前 design/contribution bytes 与 live authority；后续 Phase2 完整 candidate、Branch Review exact committed range。实际 Architecture owner_result 持有本轮 check result，不在候选预填 future pass。

## ADR-521-CANDIDATE：隔离默认和 creation-only acquisition 政策

状态：`proposed`；locator：`docs/architecture/contributions/521-checkout-isolation.md#adr-521-candidate`；`adr.required=true`。
Decision candidate：task-free 修改由原 execution owner 在 linked/non-base 位置执行，不创建 Task；正式新 Task creation 默认同一位置，C6 creation-only precondition 拒绝 primary acquisition；共享旧 Task recovery、base Sync 和 Cleanup 保留现有职责。Guru workflow 消费 upstream no_current_task，不接管上游入口。
依据：live #521 的共享 primary HEAD 影响和 no-Task 隔离需求；改变既有 primary-adoption/default checkout decision，需要具名决策候选承接，不能仅记为文案修复。
替代与边界：Task 强制升级、第二 acquisition Skill/store、shell alias/自动切回、共享 resolver 全局 primary 拒绝、upstream patch 均不能保留全部当前职责；不新增安全隔离或未来平台机制。
Promotion 时才由原 Architecture owner 决定长期 ADR identity/登记，不在本轮写 shared ADR/current。

Review：`pending` / `independent=false` / `committed_range=null`，仅描述尚未发生的 committed review。
Promotion：`required` / `promoted_identity=""` / `expected_current_identity=current-main-0.6.17-guru.83`。live current 推进则 sync_required，不覆盖 shared authority。

## 当前 Planning 增量：无 Issue 标准 Intake 的 mode 兼容

实际 consumer `guru-review-change-request` 的 `public-standalone-request-input.schema.json` 当前仅接受 `mode=standalone`，而生产 Intake transition 保留 `mode=workflow`；profile 描述无 Issue 请求来源，mode 描述执行方式，两者不应混为同一资格。当前设计只把该既有 profile 的 mode 扩为 `workflow|standalone`，保持 schema identity、target/source 匹配、完整 producer transition 与 mode equality、原 ready router 和 C6 clean acquisition。不新增字段、状态、writer、store、wrapper 或 Task 创建副作用。

这是现有接管 consumer 的局部输入兼容修正，归原 Review owner；current-only schema/合同通过原 preset 同步后退出仅 standalone 的限制。旧 standalone caller 保持有效，普通 mode mismatch 仍拒绝。改变 producer mode、改用 Issue、绕过 Review 或放宽 acquisition clean 前置均不能保留当前合同。该修正不改变 ADR-521 的 isolation decision、shared GAP 生命周期或 promotion owner。

此增量同时适用 boundary-and-decision、owner-and-single-writer、compatibility-and-exit、evidence-and-freshness 和 review-and-promotion concerns；上述九项 applicability 保持。详细设计 locator 增加 `trellis/skills/guru-team/packages/guru-review-change-request/{references/contract.md,schemas/public-standalone-request-input.schema.json}` 及其 production transition consumer。Planning 只确认机制与职责相容；package/producer-chain、installed parity 与原 native same-input 接续实际结果由后续阶段分别验证，未执行不记为通过。

## Phase 2 当前候选 before/after

当前完整 tracked/untracked 候选在原 C6 preparation 加入 primary topology 拒绝，并同步 create-only 合同；共享 acquisition/resolution 和旧 created-result recovery 不增加该拒绝。selector 保持原 mode DTO，execution owner 通过原 location_required 承担 linked/non-base 位置与精确 Git 动作，workflow 单一 continuation block 承担 upstream no_current_task caller 接续。原 Review 的无 Issue profile 增加 workflow 输入接受，producer transition、mode equality、source/target 与原 Task gates 不变。安装副本由原 preset 投影，无新增 store、writer、公共字段、wrapper 或授权状态。

这改变默认位置决策，仍使用 target_native 与上述 proposed ADR；不是 no-impact 文案修正。九 concern 的适用性、原 single-writer、当前 necessity、旧模式删除出口与 expected .83 promotion 保持。Architecture project check 评估上述实际 before/after 和职责图；客观命令仅提供事实，不代替判断。当前实现没有把无 Task 或位置缺失转换为强制创建，也未把 create-only 拒绝扩大至旧 Task recovery。

真实标准接管、绑定及 caller 的测试充分性继续由唯一 Test 与本阶段 Check owner 判断；首次失败和恢复只绑定各自实际候选。Architecture current candidate 不能把未执行的 Task/承接、副作用、业务安装或 Release 当作完成，亦不能将 serializer/静态合同当 native proof。完整 committed review 与 shared promotion 尚未发生；当前候选字节变化后重新 freshness 评估。

## 已执行的 committed review 与知识晋升

Identity：`architecture-contribution-521-checkout-isolation-v1`；当前状态：`reviewed_promoted`；expected_current_identity=`current-main-0.6.17-guru.83`；promoted_identity=`current-main-0.6.17-guru.84`。独立审查范围为 `origin/main@44a8b9c1f8495e2f811f892f248a1f2693a8bc80...5bcee456787cfb70bb6f26956a90af696083e73d`。实际 committed Architecture public output 为 `baseline_current / architecture_impact / reviewed_candidate`，完整 Branch Review public output 为 `passed`；原 recorder/checker/public invoke 均完成，task/commit 匹配。后续 publication eligibility 因尚未 promotion 实际返回 `sync_required / promotion_required`。

原 Architecture owner fresh 复核 expected `.83` 后串行晋升 `.84`，将上述 ADR-521-CANDIDATE 登记为 [ADR-021](../adr/021-checkout-isolation.md)。constitution、GAP 生命周期、原 Task/Bind/Sync/recovery/terminal owners、公共 exits 和软件四轴保持；唯一 Test 继续拥有实际结果与首次失败，不改写原证据对象。上文 implementation/Planning/Phase2 candidate 与 pending 字段保留为 preimage，当前状态以本 successor 节为准。晋升产生的新 diff 尚须 fresh Phase2/TaskCommit/独立完整 Branch Review；不声明其已完成，也不表示 Delivery、Completion、Release、业务 #120 安装或旧 primary Task 迁移已完成。
