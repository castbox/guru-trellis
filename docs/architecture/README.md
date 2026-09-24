# Architecture Baseline SSOT

版本：`current-main-0.6.17-guru.62`；状态：`active`；predecessor：`current-main-0.6.17-guru.61`；source baseline：reviewed [#454 C4 branch association contribution](./contributions/454-task-lifecycle-state-model-c4.md) + inherited immutable `.61` authority；#305 的 `EVO-001..007` 仍是独立 target authority。精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD。

本目录是唯一 Architecture Baseline authority。分区不可互换：FOUNDATION 是横向约束，CURRENT 只放证据证明的实现，TARGET 是已接受方向，GAP 是显式差距，PLAN 是已记录但未自动授权的执行顺序，ADR 是历史决策，EVIDENCE 只支撑判断。

版本历史：`current-main-0.6.17-guru.62` 是唯一 active Architecture baseline；`.61` 及更早 identities 保持 immutable superseded history。`.62` 完整继承 `.61`，吸收 #454 已审查的 C4 branch association、establishment、rebind substrate 与同范围 bounded Finalizer provenance recovery guard，决策与证据见 `ARCH-CUR-039`、`ARCH-DOM-024`、`ARCH-INT-027`、`ARCH-GAP-011`、`ADR-015`、`EVD-037`。active registry 保持 32 Skills / 142 package exits / 102 commands，并额外保留三个 planned IDs；production business workflow 仍为 22 mandatory invokes / 98 exits。

`.62` 的 C4 provenance 还明确绑定同一变更范围内的 Finalizer 首次 publication recovery guard：无 predecessor transaction 时只接受 absent、exact reviewed HEAD 或 strict historical ancestor remote，并把 exact `pre_push_remote_head` 写入 replacement transaction，再在任何远端 mutation 前复核同一 remote identity。该 guard 复用既有 Finalizer authority（`REQ-048` / `DES-046` / `TST-032`），不新增 lifecycle owner、public DTO 或生产 activation；执行级回归位于 `guru-finalize-task/tests/test_provenance.py`。

同一 authority 还允许 identity-matched unbound transaction 在 selected base 未变化时承接 fresh-reviewed finding-fix descendant：predecessor review-to-Publication 必须相等或为合法 provenance tail，base 已在 predecessor lineage，current Branch Review/Publication/live HEAD 相等且严格后继，并且没有 Open PR。历史 terminal PR 不作为 current candidate；remote 仅可等于 transaction-owned pre-push 或 Publication endpoint。该最小充分路径不增加 branch/session/path authority 或新的 recovery API。

Repository `v0.6.17-guru.1`、extension `0.6.17-guru.42`、CLI/core `0.6.17` 与固定 Fork source `castbox/Trellis@eb370008c7689d4e272ae626bd002190ecbb3296` 仍保持独立版本轴。`.62` promotion 不是 production graph activation 或软件发布；C5-C7、D443、D436 与 E434 仍未完成。promotion-created diff 必须重新通过 Phase 2、task commit 与独立完整 Branch Review；focused lifecycle `93/93` 只证明提升前 C4 candidate，preset `85/86` 与完整 Release matrix 均未被声明为通过。

读取顺序：FOUNDATION -> CURRENT -> DOMAIN/INTEGRATION -> TARGET/GAP -> GOVERNANCE/PLAN -> ADR/EVIDENCE。普通 task 先调用 `guru-maintain-architecture-baseline:task_impact_sync`，需要共享 authority 变化时走 contribution + `promotion`；不完整或冲突走 `repair`。

| 分区 | Locator |
| --- | --- |
| FOUNDATION | [`00-foundation/baseline.md`](./00-foundation/baseline.md) / [`00-foundation/design-constitution.md`](./00-foundation/design-constitution.md) |
| CURRENT | [`01-current/system.md`](./01-current/system.md) |
| TARGET | [`02-target/target.md`](./02-target/target.md) |
| DOMAIN / INTEGRATION | [`03-domains/ownership.md`](./03-domains/ownership.md) / [`04-integrations/distribution.md`](./04-integrations/distribution.md) |
| GAP / GOVERNANCE / PLAN | [`05-gaps/current-to-target.md`](./05-gaps/current-to-target.md) / [`06-governance/rules.md`](./06-governance/rules.md) / [`06-governance/change-contract.md`](./06-governance/change-contract.md) / [`07-plans/roadmap.md`](./07-plans/roadmap.md) |
| ADR / EVIDENCE | [`adr/README.md`](./adr/README.md) / [`evidence/current-evidence.md`](./evidence/current-evidence.md) |
