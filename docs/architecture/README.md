# Architecture Baseline SSOT

版本：`current-main-0.6.5-guru.51`；状态：`active`；predecessor：`current-main-0.6.5-guru.50`；source baseline：reviewed [#408 contribution](./contributions/408-nightly-session-binding-manual-fallback.md) + inherited immutable `.50` authority；#305 已确认的 `EVO-001..007` 保持独立 target authority。精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD。

本目录是唯一 Architecture Baseline authority。分区不可互换：FOUNDATION 是横向约束，CURRENT 只放证据证明的实现，TARGET 是已接受方向，GAP 是显式差距，PLAN 是已记录但未自动授权的执行顺序，ADR 是历史决策，EVIDENCE 只支撑判断。

版本历史：`current-main-0.6.5-guru.51` 是唯一 active Architecture baseline；`.50`、`.49`、`.48`、`.47`、`.46`、`.45`、`.44`、`.43`、`.42`、`.41`、`.40`、`.39`、`.38`、`.37`、`.36` 与 `.35` 是 immutable superseded identities。`.51` 继承 `.50` 的 developer/ledger 退役、旧 lifecycle、23 Skills / 97 exits / 78 commands 与 accepted `ADR-009`，提升 #408 的 Nightly 来源、正常 authoring/会话接续与独立手动操作边界。current framework source 为 `castbox/Trellis@db4ca1dfbb5abaf9be62b2a01b70dda3f80df0f0`、CI `34838784963`、CLI/core `0.6.17`、package manager `pnpm@10.32.1`；extension 仍为 `0.6.16-guru.41`。released repository axis `v0.6.16-guru.1` 保持 immutable history，不包含 #408 candidate。知识基线提升不是软件发布；promotion-created diff 必须重新通过 Phase 2、task commit 与独立完整 Branch Review，才可进入后续 Publication。

读取顺序：FOUNDATION -> CURRENT -> DOMAIN/INTEGRATION -> TARGET/GAP -> GOVERNANCE/PLAN -> ADR/EVIDENCE。普通 task 先调用 `guru-maintain-architecture-baseline:task_impact_sync`，需要共享 authority 变化时走 contribution + `promotion`；不完整或冲突走 `repair`。

| 分区 | Locator |
| --- | --- |
| FOUNDATION | [`00-foundation/baseline.md`](./00-foundation/baseline.md) / [`00-foundation/design-constitution.md`](./00-foundation/design-constitution.md) |
| CURRENT | [`01-current/system.md`](./01-current/system.md) |
| TARGET | [`02-target/target.md`](./02-target/target.md) |
| DOMAIN / INTEGRATION | [`03-domains/ownership.md`](./03-domains/ownership.md) / [`04-integrations/distribution.md`](./04-integrations/distribution.md) |
| GAP / GOVERNANCE / PLAN | [`05-gaps/current-to-target.md`](./05-gaps/current-to-target.md) / [`06-governance/rules.md`](./06-governance/rules.md) / [`06-governance/change-contract.md`](./06-governance/change-contract.md) / [`07-plans/roadmap.md`](./07-plans/roadmap.md) |
| ADR / EVIDENCE | [`adr/README.md`](./adr/README.md) / [`evidence/current-evidence.md`](./evidence/current-evidence.md) |
