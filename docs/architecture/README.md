# Architecture Baseline SSOT

版本：`current-main-0.6.17-guru.56`；状态：`active`；predecessor：`current-main-0.6.17-guru.55`；source baseline：reviewed [#436 contribution](./contributions/436-post-delivery-completion-finish.md) + inherited immutable `.55` authority；#305 的 `EVO-001..007` 仍是独立 target authority。精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD。

本目录是唯一 Architecture Baseline authority。分区不可互换：FOUNDATION 是横向约束，CURRENT 只放证据证明的实现，TARGET 是已接受方向，GAP 是显式差距，PLAN 是已记录但未自动授权的执行顺序，ADR 是历史决策，EVIDENCE 只支撑判断。

版本历史：`current-main-0.6.17-guru.56` 是唯一 active Architecture baseline；`.55` 及更早 identities 保持 immutable superseded history。`.56` 完整继承 `.55` 并吸收 #436 Post-Delivery Completion and Finish capability，决策见 [ADR-013](./adr/013-post-delivery-completion-finish.md)，证据见 `EVD-031`。active registry 为 31 Skills / 136 package exits / 101 commands；production business workflow 仍为 22 mandatory invokes / 98 exits。

Repository `v0.6.17-guru.1`、extension `0.6.17-guru.42`、CLI/core `0.6.17` 与固定 Fork source 均继承 `.55`。本提升不是 production graph activation 或软件发布；#434 独占 Delivery graph 激活与旧 edge retirement，#436 提供 Completion、Closure、Finish、Cleanup 与 Reactivate，但不激活其 production edges。promotion-created diff 必须重新通过 Phase 2、task commit 与独立完整 Branch Review，才可进入 Publication；完整 Release matrix 仍为 `unverified`。

读取顺序：FOUNDATION -> CURRENT -> DOMAIN/INTEGRATION -> TARGET/GAP -> GOVERNANCE/PLAN -> ADR/EVIDENCE。普通 task 先调用 `guru-maintain-architecture-baseline:task_impact_sync`，需要共享 authority 变化时走 contribution + `promotion`；不完整或冲突走 `repair`。

| 分区 | Locator |
| --- | --- |
| FOUNDATION | [`00-foundation/baseline.md`](./00-foundation/baseline.md) / [`00-foundation/design-constitution.md`](./00-foundation/design-constitution.md) |
| CURRENT | [`01-current/system.md`](./01-current/system.md) |
| TARGET | [`02-target/target.md`](./02-target/target.md) |
| DOMAIN / INTEGRATION | [`03-domains/ownership.md`](./03-domains/ownership.md) / [`04-integrations/distribution.md`](./04-integrations/distribution.md) |
| GAP / GOVERNANCE / PLAN | [`05-gaps/current-to-target.md`](./05-gaps/current-to-target.md) / [`06-governance/rules.md`](./06-governance/rules.md) / [`06-governance/change-contract.md`](./06-governance/change-contract.md) / [`07-plans/roadmap.md`](./07-plans/roadmap.md) |
| ADR / EVIDENCE | [`adr/README.md`](./adr/README.md) / [`evidence/current-evidence.md`](./evidence/current-evidence.md) |
