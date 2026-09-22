# Architecture Baseline SSOT

版本：`current-main-0.6.17-guru.60`；状态：`active`；predecessor：`current-main-0.6.17-guru.59`；source baseline：reviewed [#454 C3 contribution](./contributions/454-task-lifecycle-state-model-c3.md) + inherited immutable `.59` authority；#305 的 `EVO-001..007` 仍是独立 target authority。精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD。

本目录是唯一 Architecture Baseline authority。分区不可互换：FOUNDATION 是横向约束，CURRENT 只放证据证明的实现，TARGET 是已接受方向，GAP 是显式差距，PLAN 是已记录但未自动授权的执行顺序，ADR 是历史决策，EVIDENCE 只支撑判断。

版本历史：`current-main-0.6.17-guru.60` 是唯一 active Architecture baseline；`.59` 及更早 identities 保持 immutable superseded history。`.60` 完整继承 `.59`，只吸收 #454 已审查的 C3 checkout substrate，决策与证据见 `ARCH-CUR-037`、`ARCH-DOM-022`、`ARCH-INT-025`、`ARCH-GAP-011`、`ADR-015`、`EVD-035`。active registry 保持 32 Skills / 142 package exits / 102 commands，并额外保留一个 planned ID；production business workflow 仍为 22 mandatory invokes / 98 exits。

Repository `v0.6.17-guru.1`、extension `0.6.17-guru.42`、CLI/core `0.6.17` 与固定 Fork source `castbox/Trellis@eb370008c7689d4e272ae626bd002190ecbb3296` 仍保持独立版本轴。`.60` promotion 不是 production graph activation 或软件发布；C4-C7、D443、D436 与 E434 仍未完成，#434 继续独占 Delivery/lifecycle graph 激活与旧 edge retirement。promotion-created diff 必须重新通过 Phase 2、task commit 与独立完整 Branch Review，才可进入 Publication；package suite `19/20`、preset suite `85/86` 与完整 Release matrix 均未被声明为通过。

读取顺序：FOUNDATION -> CURRENT -> DOMAIN/INTEGRATION -> TARGET/GAP -> GOVERNANCE/PLAN -> ADR/EVIDENCE。普通 task 先调用 `guru-maintain-architecture-baseline:task_impact_sync`，需要共享 authority 变化时走 contribution + `promotion`；不完整或冲突走 `repair`。

| 分区 | Locator |
| --- | --- |
| FOUNDATION | [`00-foundation/baseline.md`](./00-foundation/baseline.md) / [`00-foundation/design-constitution.md`](./00-foundation/design-constitution.md) |
| CURRENT | [`01-current/system.md`](./01-current/system.md) |
| TARGET | [`02-target/target.md`](./02-target/target.md) |
| DOMAIN / INTEGRATION | [`03-domains/ownership.md`](./03-domains/ownership.md) / [`04-integrations/distribution.md`](./04-integrations/distribution.md) |
| GAP / GOVERNANCE / PLAN | [`05-gaps/current-to-target.md`](./05-gaps/current-to-target.md) / [`06-governance/rules.md`](./06-governance/rules.md) / [`06-governance/change-contract.md`](./06-governance/change-contract.md) / [`07-plans/roadmap.md`](./07-plans/roadmap.md) |
| ADR / EVIDENCE | [`adr/README.md`](./adr/README.md) / [`evidence/current-evidence.md`](./evidence/current-evidence.md) |
