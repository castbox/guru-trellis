# Architecture Baseline SSOT

版本：`current-main-0.6.17-guru.96`；状态：`active`；predecessor：`current-main-0.6.17-guru.95`；source baseline：[已晋升 #589 D7 贡献](./contributions/589-git-object-performance.md) + immutable `.95` authority（Git 历史）。constitution、原 owners、ADR/GAP lifecycle 与软件四轴保持。

当前增量 ARCH-CUR-069 / ARCH-DOM-052 / ARCH-INT-055 承接已独立完整审查的 #589 D7。manual recovery/history 的不可变内容摘要由上游公开 owner 承担；Guru 保留对象准备、逐输入独立检查与恢复职责，旧 snapshot 实现退出。[唯一 Test](../requirements-design-test-contributions/589-git-object-performance/test.md)拥有实际结果及正式采用的未验证边界。此次晋升新增差额尚须 fresh Phase2、TaskCommit 与独立完整 Branch Review；不表示 Delivery、整体完成、正式工具采用、软件发布或业务部署。

历史 `.95`：以下保留 #599 晋升时的 authority 与增量记录。

版本：`current-main-0.6.17-guru.95`；状态：`active`；predecessor：`current-main-0.6.17-guru.94`；source baseline：[已晋升 #599 贡献](./contributions/599-clear-technical-writing.md) + immutable `.94` authority（Git 历史）。constitution、原 owners、GAP lifecycle 与软件四轴保持。

当前增量 ARCH-CUR-068 / ARCH-DOM-051 / ARCH-INT-054 承接首次独立完整审查的 #599。清晰写作正文由 canonical managed-spec 单写，现有 Agent 与审核 owner 在原职责内读取和执行；不新增语言审核阶段或公共 I/O。[唯一 Test](../requirements-design-test-contributions/599-clear-technical-writing/test.md)拥有源码、投影、实际 Codex 行为和未验证边界。晋升新差额仍须 fresh Phase2、TaskCommit 与不同 reviewer 的完整 BranchReview；知识晋升不表示 Delivery、Completion、软件发布或业务采用。

历史 `.94`：当时版本为 `current-main-0.6.17-guru.94`；predecessor 为 `.93`；source baseline 为[已晋升 #578 贡献](./contributions/578-cross-owner-validation-facts.md)与 immutable `.93` authority。以下保留该轮增量记录。

历史 `.94` 增量 ARCH-CUR-067 / ARCH-DOM-050 / ARCH-INT-053 与 ADR-029 承接首次独立完整审查的 #578。原 owner 独立当前判断与工程事实采用分离；当前绑定、private 退休与完整安装边界保持。[唯一 Test](../requirements-design-test-contributions/578-cross-owner-validation-facts/test.md)单写真实验证和边界。晋升新差额仍须 fresh Phase2/TaskCommit/不同 reviewer 完整 BranchReview，不表示 Delivery/Completion、软件发布或业务采用。

历史 `.93`：当时版本：`current-main-0.6.17-guru.93`；状态：`active`；predecessor：`current-main-0.6.17-guru.92`；source baseline：[已晋升 #569 贡献](./contributions/569-fixed-cutoff-history-query.md) + immutable `.92` authority（Git 历史）。constitution、ADR-026/028、GAP lifecycle、原 owners 与软件四轴保持。

当前增量 ARCH-CUR-066 / ARCH-DOM-049 / ARCH-INT-052 承接已独立完整审查的 #569。原 history owner 自动准备固定截点所需历史，原 AI consumer 判断适用性；没有新 owner、缓存或 ADR。[唯一 Test](../requirements-design-test-contributions/569-fixed-cutoff-history-query/test.md)拥有实际结果与未验证边界；本次晋升新差额仍须 fresh Phase2、TaskCommit 与不同 reviewer 的独立完整 BranchReview。

历史 `.92`：版本：`current-main-0.6.17-guru.92`；状态：`active`；predecessor：`current-main-0.6.17-guru.91`；source baseline：[已晋升 #567 贡献](./contributions/567-fixed-development-baseline.md) + immutable `.91` authority（Git 历史）。既有 constitution、GAP lifecycle、软件四轴与业务采用责任保持。

当前增量 ARCH-CUR-065 / ARCH-DOM-048 / ARCH-INT-051 与 [ADR-028](./adr/028-fixed-content-baseline.md) 承接已独立完整审查的 #567。ADR-028 只替代已定位的旧默认追赶、祖先资格及无关整体版本前进即 stale 的冲突片段；原语义 owners、真实内容/事务一致性与 shared-current 写前 expected-current 保持。[唯一 Test](../requirements-design-test-contributions/567-fixed-development-baseline/test.md)拥有实际结果、首次失败/修复和未验证边界；本次晋升新差额仍须 fresh Phase2、TaskCommit 与不同 reviewer 的独立完整 BranchReview。

历史 `.91`：版本：`current-main-0.6.17-guru.91`；状态：`active`；predecessor：`current-main-0.6.17-guru.90`；source baseline：[已晋升 #566 贡献](./contributions/566-single-checkout-upgrade.md) + immutable `.90` authority（Git 历史）。既有 constitution、GAP lifecycle、软件四轴与业务采用责任保持。

历史 `.91` 增量 ARCH-CUR-064 / ARCH-DOM-047 / ARCH-INT-050 与 ADR-027 承接已独立审查的 #566；[唯一 Test](../requirements-design-test-contributions/566-single-checkout-upgrade/test.md)拥有实际证明与未验证边界。promotion 新差额必须重新进入 Phase2、TaskCommit 与独立完整 BranchReview。

历史 `.90`：版本：`current-main-0.6.17-guru.90`；状态：`active`；predecessor：`current-main-0.6.17-guru.89`；source baseline：[已晋升 #557 贡献](./contributions/557-manual-merged-delivery-recovery.md) + immutable `.89` authority（Git 历史）。既有 constitution、GAP lifecycle、软件四轴与业务采用责任保持。

历史 `.90` 增量 ARCH-CUR-063 / ARCH-DOM-046 / ARCH-INT-049 与 ADR-026 承接已独立审查的 #557；[唯一 Test](../requirements-design-test-contributions/557-manual-merged-delivery-recovery/test.md)拥有 source、matching installed、真实 GitHub 链和旧安装/业务/Release 边界。promotion 新差额必须重新进入 Phase 2、Task Commit 与独立完整 Branch Review。

历史 `.89`：当时版本：`current-main-0.6.17-guru.89`；状态：`active`；predecessor：`current-main-0.6.17-guru.88`；source baseline：[已晋升 #548 贡献](./contributions/548-creation-recovery.md) + immutable `.88` authority（Git 历史）。既有 owners、constitution、ADR 与 GAP lifecycle、软件四轴保持。

本目录是唯一 Architecture Baseline authority。分区不可互换：FOUNDATION 是横向约束，CURRENT 只放证据证明的实现，TARGET 是已接受方向，GAP 是显式差距，PLAN 是已记录但未自动授权的执行顺序，ADR 是历史决策，EVIDENCE 只支撑判断。

历史 `.89` 记录：当时 `current-main-0.6.17-guru.89` 是唯一 active；`.88` 及更早是 immutable superseded history（Git 历史）。当前增量 ARCH-CUR-062 / ARCH-DOM-045 / ARCH-INT-048 承接已独立审查 #548；[唯一 Test](../requirements-design-test-contributions/548-creation-recovery/test.md)拥有验证和未验证边界。晋升新 diff 须 fresh Phase2、TaskCommit、不同 reviewer 完整 BranchReview，不证明 Delivery、Task Completion 或软件发布。

历史 `.88`：版本：`current-main-0.6.17-guru.88`；状态：`active`；predecessor：`current-main-0.6.17-guru.87`；source baseline：[#547 Closure disposition contribution](./contributions/547-retain-source-open.md) + immutable `.87` authority（Git 历史）。#305 EVO-001..007、现有 owners、GAP lifecycle、constitution 与软件四轴保持。

历史 `.88` 记录：版本历史：`current-main-0.6.17-guru.88` 是唯一 active；`.87` 及更早为 immutable superseded history（Git 历史）。当前增量 ARCH-CUR-061 / ARCH-DOM-044 / ARCH-INT-047 与 [ADR-025](./adr/025-retain-source-open-disposition.md) 承接已独立审查的 #547 contribution。Completion、Closure、Finish 与 Cleanup 原 owners 保持；[唯一 Test](../requirements-design-test-contributions/547-retain-source-open/test.md)拥有验证及未验证边界。晋升新 diff 仍须 fresh Phase2/TaskCommit/不同 reviewer 完整 BranchReview，不证明 Delivery、Task Completion、软件发布或原 CMS 恢复。

历史 `.87`：当时增量 ARCH-CUR-060 / ARCH-DOM-043 / ARCH-INT-046 与 ADR-024 承接已独立审查的 #531 contribution。公共 Task/Delivery authority 归上游；Guru 保留语义门禁与私有发布事务，所有 Delivery 含 D1 独立 Planning。旧安装成套迁移前保留原完整版本。历史 `.86` 的 #530 原TaskCommit clean接续决定与已审查事实继续继承。

历史 `.85`：当时增量为 ARCH-CUR-058 / ARCH-DOM-041 / ARCH-INT-044 与 ADR-022/023；继承全部有效决定、owners 与 GAP lifecycle，包括 closed ARCH-GAP-012。当时 registry 为37 packages/169 exits/110 commands，business workflow为35 mandatory invokes/163 exits。历史 `.84` 的 #521 增量为 ARCH-CUR-057 / ARCH-DOM-040 / ARCH-INT-043 / EVD-060 与 ADR-021，其 registry36/164/109、business34/158 只绑定该轮。晋升新 diff 必须 fresh Phase2/TaskCommit/独立完整 Branch Review；软件四轴和 Release 状态不变。

`.62` 的 C4 provenance 还明确绑定同一变更范围内的 Finalizer 首次 publication recovery guard：无 predecessor transaction 时只接受 absent、exact reviewed HEAD 或 strict historical ancestor remote，并把 exact `pre_push_remote_head` 写入 replacement transaction，再在任何远端 mutation 前复核同一 remote identity。该 guard 复用既有 Finalizer authority（`REQ-048` / `DES-046` / `TST-032`），不新增 lifecycle owner、public DTO 或生产 activation；执行级回归位于 `guru-finalize-task/tests/test_provenance.py`。

同一 authority 还允许 identity-matched unbound transaction 在 selected base 未变化时承接 fresh-reviewed finding-fix descendant：predecessor review-to-Publication 必须相等或为合法 provenance tail，base 已在 predecessor lineage，current Branch Review/Publication/live HEAD 相等且严格后继，并且没有 Open PR。历史 terminal PR 不作为 current candidate；remote 仅可等于 transaction-owned pre-push 或 Publication endpoint。该最小充分路径不增加 branch/session/path authority 或新的 recovery API。

历史 `.68` authority 将 repository `v0.6.17-guru.1`、extension `0.6.17-guru.42`、CLI/core `0.6.17` 与固定 Fork source `castbox/Trellis@8336e78b8fafe2a4bc4ea3d01815a61cf4f08983` 作为独立版本轴；它记录 RDT 从 `.67` 串行提升至 `.68`，不证明软件发布。该段仅为 predecessor provenance；当前版本目标及未验证边界以下段 `.70` 为准。

`.69` 的 extension `0.6.17-guru.43` 与当时固定的 `0.6.17` Fork 属于 predecessor provenance。历史 `.70` 可安装候选为 extension `0.7.0-guru.1`、CLI/core `0.7.0-castbox.1`、固定 Fork `castbox/Trellis@64fe9a15a68df1add3a2a7fd182f3d84e6eba4ac`。repository `v0.6.17-guru.2` 仍是独立未发布目标。一个代表性新装已验证；旧 `0.6.17` 安装无法由该 Fork 的 update 命令升级，前驱升级、完整多平台 Release matrix、远端 marketplace 与业务仓生产安装均未验证。`.70` knowledge promotion 不代表软件发布。

`.71` 历史固定 Fork 为 `castbox/Trellis@9c36002a324c16a09a85b6aa5a380b74aabf801f`，CI `37179218822`，CLI/core `0.7.0-castbox.1`，extension `0.7.0-guru.1`。既有 C6/writer/recovery/source/Closure owner 不变，无 ADR/GAP/兼容双读增量。代表性 Codex local-workflow sample clean/current-update/reapply 与 projection parity 已验证；remote/native-host/full matrix、predecessor refusal/no-write、tag/Release 由 #489 独立完成。knowledge promotion 不表示发布，promotion-created diff 须 fresh Phase 2/commit/独立完整 Branch Review。

历史 `.73` 固定 Fork `castbox/Trellis@8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1` / CI `37473087582`，CLI/core `0.7.0-castbox.2`，Guru `0.7.0-guru.2` 为未发布候选。完整代表性验收由 [唯一增量结果](../requirements-design-test-contributions/495-legacy-installation-upgrade-acceptance/test.md) 承接；固定远端 Guru `6a563f5f` 的 public/source_locked/provider、真实 PR195 deferred/merge 诊断与 accepted 旧正式 writer 在途快照已有证据，首次失败及 same-owner 恢复仍单列。该知识晋升不证明新文档 HEAD 重跑、真实业务原始在途、真实业务安装、软件发布或完整矩阵；晋升 diff 必须 fresh Phase2/commit/不同 reviewer 完整 Branch Review 后才进入 Delivery/merge/Completion。

历史 `.75` 固定 Fork `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c` / main CI `37647767799`，CLI/core `0.7.0-castbox.3`、Guru `0.7.0-guru.3` 未发布候选；本地分组历史由 EVD-050保留；EVD-051承接精确远端ecd同源验收，accepted MIG-495-01..12已齐备、ARCH-GAP-012 closed。#495仍open，merge/Completion/Closure/Finish未执行；晋升后重新 Phase2/commit/完整 Branch Review。

历史 `.76` 固定 Fork `5c760463680ffc10a3f26957b330c57a4b0c3ff8` / main CI `37735554354`；CLI/core `0.7.0-castbox.3` 与 Guru `0.7.0-guru.3` 版本轴不变。#503 按 consumer 拆分身份占用与 selected lifecycle，migration 完整分类及 ADR-017/018 owner/退出保持；无新 ADR/GAP/store/writer。RDT 同步 `.76`；EVD-052 仅证明 source/代表性 clean-installed 候选，晋升 diff 须 fresh Phase2/commit/完整 Branch Review。Backend 恢复与软件 Release/部署未验证。

历史 `.77` 按 expected `.76` 晋升已独立审查的 #466 contribution；只强化唯一 constitution 的 `minimum-necessary-complexity` 与现有 semantic 消费。五原则 identity/short name、ADR/GAP、owner、公共 I/O 与软件四轴不变。RDT 同步 `.77`；ARCH-CUR-050 / EVD-053 承接已审查增量及唯一 Test locator。晋升 diff 尚须 fresh Phase2/TaskCommit/不同 reviewer 完整 Branch Review；知识晋升不表示 Delivery、Release、业务安装或部署完成。

历史 `.78` 按 expected `.77` 晋升 #404 已独立审查的 `implementation-v2` contribution 与 ADR-019；Architecture Skill 继续拥有方法，fresh generic subagent 执行新评估，原 owner 承接下游 eligibility 和 promotion。Architecture 2.0 I/O、四 profiles、七 exits、constitution 与 GAP lifecycle 不变；RDT `.78` 同步当前 Architecture 继承。ARCH-CUR-051 / EVD-054 只承接已审查增量和唯一 Test locator。此次晋升 diff 仍须 fresh Phase2、TaskCommit、不同 reviewer 完整 Branch Review；不表示 Delivery、Completion、软件发布或业务部署完成。

历史 `.79` 按 expected `.78` 晋升 #382 已独立审查的根因候选资格 contribution 与 ADR-020；[唯一 Test](../requirements-design-test-contributions/382-root-cause-qualification/test.md)拥有实际结果与未验证边界。新增 owner 只拥有候选准入，不接管阶段完成或 #383 共同语义。晋升差异的后续 gates 尚待执行。

历史 `.80` 按 expected `.79` 晋升 #383 已独立审查的共同因果语义 contribution；七个现有 owner 读取单一受管 spec，本阶段 evidence/route 和 whole-task Completion 职责保持。实际结果与边界由[唯一 Test](../requirements-design-test-contributions/383-causal-completion-semantics/test.md)拥有；此次晋升 diff 仍须 fresh Phase2/TaskCommit/独立完整 Branch Review，不表示 Delivery、Completion 或软件发布。

历史 `.81` 按 expected `.80` 晋升 #468 已独立审查贡献；Planning approved 保持唯一 consumer，原 execution owner 增加活动 resume 与 identity-only completed-result recovery，Check 只调用其 retirement 端口。Direct Source/必要用途/重开与原完成 owners 保持。实际结果和限制由[唯一 Test](../requirements-design-test-contributions/468-direct-source-replanning-compatibility/test.md)拥有；晋升 diff 仍须 fresh Phase2/TaskCommit/独立完整 Branch Review。软件版本轴、历史证据、ADR/GAP 生命周期保持。

读取顺序：FOUNDATION -> CURRENT -> DOMAIN/INTEGRATION -> TARGET/GAP -> GOVERNANCE/PLAN -> ADR/EVIDENCE。普通 task 先调用 `guru-maintain-architecture-baseline:task_impact_sync`，需要共享 authority 变化时走 contribution + `promotion`；不完整或冲突走 `repair`。

| 分区 | Locator |
| --- | --- |
| FOUNDATION | [`00-foundation/baseline.md`](./00-foundation/baseline.md) / [`00-foundation/design-constitution.md`](./00-foundation/design-constitution.md) |
| CURRENT | [`01-current/system.md`](./01-current/system.md) |
| TARGET | [`02-target/target.md`](./02-target/target.md) |
| DOMAIN / INTEGRATION | [`03-domains/ownership.md`](./03-domains/ownership.md) / [`04-integrations/distribution.md`](./04-integrations/distribution.md) |
| GAP / GOVERNANCE / PLAN | [`05-gaps/current-to-target.md`](./05-gaps/current-to-target.md) / [`06-governance/rules.md`](./06-governance/rules.md) / [`06-governance/change-contract.md`](./06-governance/change-contract.md) / [`07-plans/roadmap.md`](./07-plans/roadmap.md) |
| ADR / EVIDENCE | [`adr/README.md`](./adr/README.md) / [`evidence/current-evidence.md`](./evidence/current-evidence.md) |

历史 `.82` 按 expected `.81` 晋升 #453 已独立审查贡献；shared dispatcher 只拥有 CLI stdout transport，原 Skill 保留 semantic/deterministic 判断、正式 exit/consumer 与 owner/checkpoint/digest。current commands/callers 完整直接迁移；[唯一 Test](../requirements-design-test-contributions/453-formal-skill-exit-boundary/test.md)拥有客观与真实 native 行为证据及边界。历史证据保持原对象；知识晋升不代表软件发布或生产升级。

历史 `.83` 按 expected `.82` 晋升 #250 已独立审查贡献；Clarify 独占 Intake 意图、来源角色与真实选择，Discovery 返回原 caller 的证据，Wording/readiness 薄 relay，当前 Planning 拥有最终设计处置。六 profiles、四 context returns 与明确 current-only API migration 保持原 lifecycle/Closure owners，无新 store、ADR 或 GAP 变化；[唯一 Test](../requirements-design-test-contributions/250-phase0-intake-owner/test.md)拥有实际验证、首次失败/恢复与未验证边界。晋升新 diff 尚须 fresh Phase2/TaskCommit/独立完整 Branch Review；不表示 Delivery、Completion、软件发布或生产部署。

历史 `.84` 按 expected `.83` 晋升 #521 已独立审查贡献与 [ADR-021](./adr/021-checkout-isolation.md)。原 task-free execution owner 独占 linked/non-base 位置与有界写入，Guru workflow caller 独占无 Task continuation，C6 只拒绝新 Task primary adoption；现有 Task recovery、Bind、Sync、Cleanup 各自保留职责。无 Issue Review profile 直接接受真实 workflow mode，三方 mode equality 不变。旧 current-checkout task-free 退出 current，无 Task-free 身份、mapping、授权状态或第二 acquisition owner。实际验证由[唯一 Test](../requirements-design-test-contributions/521-checkout-isolation/test.md)拥有；旧 primary Task 逐例迁移、业务 #120 安装、完整 Release matrix 和软件发布仍分别未验证。晋升新 diff 尚须 fresh Phase2/TaskCommit/独立完整 Branch Review，不表示 Delivery、Completion 或生产升级。

当前 `.85` 的 Planning writer 是 `guru-author-task-plan`。Clarify 单写 scope/来源判断，Architecture 单写候选与最终评估，Wording 单写受控措辞审查，Approval 独占规划批准；Planning 3.0 的两目的通过原 current router 分别回 Author 与 Approval。活动 scope_ready 先完成 scope 判断再交 Author 写作；Delivery/Completion 修订回同一 writer。当前事实见 `ARCH-CUR-058`、`ARCH-DOM-041`、`ARCH-INT-044` 与 [ADR-022](./adr/022-unique-planning-author.md)、[ADR-023](./adr/023-scope-ready-before-planning.md)。软件版本轴、constitution 和 GAP lifecycle 继承 `.84`；[唯一 Test](../requirements-design-test-contributions/292-unique-planning-author/test.md)拥有验证与未覆盖边界。知识晋升新差异仍须 fresh Phase2、Task Commit 与独立完整 committed Branch Review，不代表软件发布或业务部署。
