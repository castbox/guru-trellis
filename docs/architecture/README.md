# Architecture Baseline SSOT

版本：`current-main-0.6.17-guru.76`；状态：`active`；predecessor：`current-main-0.6.17-guru.75`；source baseline：[已审查身份职责贡献](./contributions/503-mixed-task-identity-reservation.md) + immutable `.75` authority（Git 历史）。#305 的 EVO-001..007 仍为独立 target；精确 revision 由包含本 authority 的 Git identity 绑定。

本目录是唯一 Architecture Baseline authority。分区不可互换：FOUNDATION 是横向约束，CURRENT 只放证据证明的实现，TARGET 是已接受方向，GAP 是显式差距，PLAN 是已记录但未自动授权的执行顺序，ADR 是历史决策，EVIDENCE 只支撑判断。

版本历史：`current-main-0.6.17-guru.76` 是唯一 active；`.75` 及更早为 immutable superseded history。沿 ADR-017 与 ADR-018 一次性迁移，current-only/唯一 owners 不变。Current：ARCH-CUR-049、ARCH-DOM-034、ARCH-INT-037、closed ARCH-GAP-012、EVD-052；EVD-049 是历史固定来源验收。registry35/159/106，business33/153 不变。

`.62` 的 C4 provenance 还明确绑定同一变更范围内的 Finalizer 首次 publication recovery guard：无 predecessor transaction 时只接受 absent、exact reviewed HEAD 或 strict historical ancestor remote，并把 exact `pre_push_remote_head` 写入 replacement transaction，再在任何远端 mutation 前复核同一 remote identity。该 guard 复用既有 Finalizer authority（`REQ-048` / `DES-046` / `TST-032`），不新增 lifecycle owner、public DTO 或生产 activation；执行级回归位于 `guru-finalize-task/tests/test_provenance.py`。

同一 authority 还允许 identity-matched unbound transaction 在 selected base 未变化时承接 fresh-reviewed finding-fix descendant：predecessor review-to-Publication 必须相等或为合法 provenance tail，base 已在 predecessor lineage，current Branch Review/Publication/live HEAD 相等且严格后继，并且没有 Open PR。历史 terminal PR 不作为 current candidate；remote 仅可等于 transaction-owned pre-push 或 Publication endpoint。该最小充分路径不增加 branch/session/path authority 或新的 recovery API。

历史 `.68` authority 将 repository `v0.6.17-guru.1`、extension `0.6.17-guru.42`、CLI/core `0.6.17` 与固定 Fork source `castbox/Trellis@8336e78b8fafe2a4bc4ea3d01815a61cf4f08983` 作为独立版本轴；它记录 RDT 从 `.67` 串行提升至 `.68`，不证明软件发布。该段仅为 predecessor provenance；当前版本目标及未验证边界以下段 `.70` 为准。

`.69` 的 extension `0.6.17-guru.43` 与当时固定的 `0.6.17` Fork 属于 predecessor provenance。历史 `.70` 可安装候选为 extension `0.7.0-guru.1`、CLI/core `0.7.0-castbox.1`、固定 Fork `castbox/Trellis@64fe9a15a68df1add3a2a7fd182f3d84e6eba4ac`。repository `v0.6.17-guru.2` 仍是独立未发布目标。一个代表性新装已验证；旧 `0.6.17` 安装无法由该 Fork 的 update 命令升级，前驱升级、完整多平台 Release matrix、远端 marketplace 与业务仓生产安装均未验证。`.70` knowledge promotion 不代表软件发布。

`.71` 历史固定 Fork 为 `castbox/Trellis@9c36002a324c16a09a85b6aa5a380b74aabf801f`，CI `37179218822`，CLI/core `0.7.0-castbox.1`，extension `0.7.0-guru.1`。既有 C6/writer/recovery/source/Closure owner 不变，无 ADR/GAP/兼容双读增量。代表性 Codex local-workflow sample clean/current-update/reapply 与 projection parity 已验证；remote/native-host/full matrix、predecessor refusal/no-write、tag/Release 由 #489 独立完成。knowledge promotion 不表示发布，promotion-created diff 须 fresh Phase 2/commit/独立完整 Branch Review。

历史 `.73` 固定 Fork `castbox/Trellis@8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1` / CI `37473087582`，CLI/core `0.7.0-castbox.2`，Guru `0.7.0-guru.2` 为未发布候选。完整代表性验收由 [唯一增量结果](../requirements-design-test-contributions/495-legacy-installation-upgrade-acceptance/test.md) 承接；固定远端 Guru `6a563f5f` 的 public/source_locked/provider、真实 PR195 deferred/merge 诊断与 accepted 旧正式 writer 在途快照已有证据，首次失败及 same-owner 恢复仍单列。该知识晋升不证明新文档 HEAD 重跑、真实业务原始在途、真实业务安装、软件发布或完整矩阵；晋升 diff 必须 fresh Phase2/commit/不同 reviewer 完整 Branch Review 后才进入 Delivery/merge/Completion。

历史 `.75` 固定 Fork `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c` / main CI `37647767799`，CLI/core `0.7.0-castbox.3`、Guru `0.7.0-guru.3` 未发布候选；本地分组历史由 EVD-050保留；EVD-051承接精确远端ecd同源验收，accepted MIG-495-01..12已齐备、ARCH-GAP-012 closed。#495仍open，merge/Completion/Closure/Finish未执行；晋升后重新 Phase2/commit/完整 Branch Review。

当前 `.76` 固定 Fork `5c760463680ffc10a3f26957b330c57a4b0c3ff8` / main CI `37735554354`；CLI/core `0.7.0-castbox.3` 与 Guru `0.7.0-guru.3` 版本轴不变。#503 按 consumer 拆分身份占用与 selected lifecycle，migration 完整分类及 ADR-017/018 owner/退出保持；无新 ADR/GAP/store/writer。RDT 同步 `.76`；EVD-052 仅证明 source/代表性 clean-installed 候选，晋升 diff 须 fresh Phase2/commit/完整 Branch Review。Backend 恢复与软件 Release/部署未验证。

读取顺序：FOUNDATION -> CURRENT -> DOMAIN/INTEGRATION -> TARGET/GAP -> GOVERNANCE/PLAN -> ADR/EVIDENCE。普通 task 先调用 `guru-maintain-architecture-baseline:task_impact_sync`，需要共享 authority 变化时走 contribution + `promotion`；不完整或冲突走 `repair`。

| 分区 | Locator |
| --- | --- |
| FOUNDATION | [`00-foundation/baseline.md`](./00-foundation/baseline.md) / [`00-foundation/design-constitution.md`](./00-foundation/design-constitution.md) |
| CURRENT | [`01-current/system.md`](./01-current/system.md) |
| TARGET | [`02-target/target.md`](./02-target/target.md) |
| DOMAIN / INTEGRATION | [`03-domains/ownership.md`](./03-domains/ownership.md) / [`04-integrations/distribution.md`](./04-integrations/distribution.md) |
| GAP / GOVERNANCE / PLAN | [`05-gaps/current-to-target.md`](./05-gaps/current-to-target.md) / [`06-governance/rules.md`](./06-governance/rules.md) / [`06-governance/change-contract.md`](./06-governance/change-contract.md) / [`07-plans/roadmap.md`](./07-plans/roadmap.md) |
| ADR / EVIDENCE | [`adr/README.md`](./adr/README.md) / [`evidence/current-evidence.md`](./evidence/current-evidence.md) |
