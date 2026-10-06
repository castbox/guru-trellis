# Architecture Baseline SSOT

版本：`current-main-0.6.17-guru.72`；状态：`active`；predecessor：`current-main-0.6.17-guru.71`；source baseline：reviewed [#495 migration candidate contribution](./contributions/495-legacy-installation-upgrade.md) + inherited immutable `.71` authority；#305 的 `EVO-001..007` 仍是独立 target authority。精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD。

本目录是唯一 Architecture Baseline authority。分区不可互换：FOUNDATION 是横向约束，CURRENT 只放证据证明的实现，TARGET 是已接受方向，GAP 是显式差距，PLAN 是已记录但未自动授权的执行顺序，ADR 是历史决策，EVIDENCE 只支撑判断。

版本历史：`current-main-0.6.17-guru.72` 是唯一 active Architecture baseline；`.71` 及更早 identities保持immutable superseded history。本版继承无人员/current-only、source/TaskId/session/branch/checkout及Delivery/Completion ownership，并按ADR-017增加独立一次性迁移。见ARCH-CUR-049、ARCH-DOM-034、ARCH-INT-037、ARCH-GAP-012与EVD-048。registry为35 Skills /159 package exits /106 commands、零planned；migration standalone-only，business graph仍为33 invokes/153 exits。迁移最终验收保持open，当前知识不证明remote来源/MIG06完成。

`.62` 的 C4 provenance 还明确绑定同一变更范围内的 Finalizer 首次 publication recovery guard：无 predecessor transaction 时只接受 absent、exact reviewed HEAD 或 strict historical ancestor remote，并把 exact `pre_push_remote_head` 写入 replacement transaction，再在任何远端 mutation 前复核同一 remote identity。该 guard 复用既有 Finalizer authority（`REQ-048` / `DES-046` / `TST-032`），不新增 lifecycle owner、public DTO 或生产 activation；执行级回归位于 `guru-finalize-task/tests/test_provenance.py`。

同一 authority 还允许 identity-matched unbound transaction 在 selected base 未变化时承接 fresh-reviewed finding-fix descendant：predecessor review-to-Publication 必须相等或为合法 provenance tail，base 已在 predecessor lineage，current Branch Review/Publication/live HEAD 相等且严格后继，并且没有 Open PR。历史 terminal PR 不作为 current candidate；remote 仅可等于 transaction-owned pre-push 或 Publication endpoint。该最小充分路径不增加 branch/session/path authority 或新的 recovery API。

历史 `.68` authority 将 repository `v0.6.17-guru.1`、extension `0.6.17-guru.42`、CLI/core `0.6.17` 与固定 Fork source `castbox/Trellis@8336e78b8fafe2a4bc4ea3d01815a61cf4f08983` 作为独立版本轴；它记录 RDT 从 `.67` 串行提升至 `.68`，不证明软件发布。该段仅为 predecessor provenance；当前版本目标及未验证边界以下段 `.70` 为准。

`.69` 的 extension `0.6.17-guru.43` 与当时固定的 `0.6.17` Fork 属于 predecessor provenance。历史 `.70` 可安装候选为 extension `0.7.0-guru.1`、CLI/core `0.7.0-castbox.1`、固定 Fork `castbox/Trellis@64fe9a15a68df1add3a2a7fd182f3d84e6eba4ac`。repository `v0.6.17-guru.2` 仍是独立未发布目标。一个代表性新装已验证；旧 `0.6.17` 安装无法由该 Fork 的 update 命令升级，前驱升级、完整多平台 Release matrix、远端 marketplace 与业务仓生产安装均未验证。`.70` knowledge promotion 不代表软件发布。

`.71` 历史固定 Fork 为 `castbox/Trellis@9c36002a324c16a09a85b6aa5a380b74aabf801f`，CI `37179218822`，CLI/core `0.7.0-castbox.1`，extension `0.7.0-guru.1`。既有 C6/writer/recovery/source/Closure owner 不变，无 ADR/GAP/兼容双读增量。代表性 Codex local-workflow sample clean/current-update/reapply 与 projection parity 已验证；remote/native-host/full matrix、predecessor refusal/no-write、tag/Release 由 #489 独立完成。knowledge promotion 不表示发布，promotion-created diff 须 fresh Phase 2/commit/独立完整 Branch Review。

`.72` 当前固定 Fork为 `castbox/Trellis@8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1`，main CI `37473087582`，CLI/core `0.7.0-castbox.2`，extension `0.7.0-guru.2`未发布候选。本地source/installed/迁移/owner接续/partial recovery/写后rollback/current update与reapply已定向验证，same-remote-HEAD source_locked/provider和完整MIG-495-06仍未验收；缺失时不得merge/Completion。知识晋升不发布软件、不升级真实业务仓，也不关闭迁移GAP；promotion-created diff必须fresh Phase2/commit/不同reviewer完整Branch Review。

读取顺序：FOUNDATION -> CURRENT -> DOMAIN/INTEGRATION -> TARGET/GAP -> GOVERNANCE/PLAN -> ADR/EVIDENCE。普通 task 先调用 `guru-maintain-architecture-baseline:task_impact_sync`，需要共享 authority 变化时走 contribution + `promotion`；不完整或冲突走 `repair`。

| 分区 | Locator |
| --- | --- |
| FOUNDATION | [`00-foundation/baseline.md`](./00-foundation/baseline.md) / [`00-foundation/design-constitution.md`](./00-foundation/design-constitution.md) |
| CURRENT | [`01-current/system.md`](./01-current/system.md) |
| TARGET | [`02-target/target.md`](./02-target/target.md) |
| DOMAIN / INTEGRATION | [`03-domains/ownership.md`](./03-domains/ownership.md) / [`04-integrations/distribution.md`](./04-integrations/distribution.md) |
| GAP / GOVERNANCE / PLAN | [`05-gaps/current-to-target.md`](./05-gaps/current-to-target.md) / [`06-governance/rules.md`](./06-governance/rules.md) / [`06-governance/change-contract.md`](./06-governance/change-contract.md) / [`07-plans/roadmap.md`](./07-plans/roadmap.md) |
| ADR / EVIDENCE | [`adr/README.md`](./adr/README.md) / [`evidence/current-evidence.md`](./evidence/current-evidence.md) |
