# Architecture Baseline SSOT

版本：`current-main-0.6.17-guru.52`；状态：`active`；predecessor：`current-main-0.6.5-guru.51`；source baseline：reviewed [#410 contribution](./contributions/410-release-v0617-guru1.md) + inherited immutable `.51` authority；#305 已确认的 `EVO-001..007` 保持独立 target authority。精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD。

本目录是唯一 Architecture Baseline authority。分区不可互换：FOUNDATION 是横向约束，CURRENT 只放证据证明的实现，TARGET 是已接受方向，GAP 是显式差距，PLAN 是已记录但未自动授权的执行顺序，ADR 是历史决策，EVIDENCE 只支撑判断。

版本历史：`current-main-0.6.17-guru.52` 是唯一 active Architecture baseline；`.51`、`.50`、`.49`、`.48`、`.47`、`.46`、`.45`、`.44`、`.43`、`.42`、`.41`、`.40`、`.39`、`.38`、`.37`、`.36` 与 `.35` 是 immutable superseded identities。`.52` 继承 `.51` 的完整 current authority，并提升 #410 的 release-facing 四轴映射：repository `v0.6.17-guru.1`、extension `0.6.17-guru.42`、CLI/core `0.6.17` 与固定 Fork source 不变。前序 released `v0.6.16-guru.1` 与 extension `0.6.16-guru.41` 保持 immutable history；本知识基线提升不是软件发布，promotion-created diff 必须重新通过 Phase 2、task commit 与独立完整 Branch Review，才可进入后续 Publication。

读取顺序：FOUNDATION -> CURRENT -> DOMAIN/INTEGRATION -> TARGET/GAP -> GOVERNANCE/PLAN -> ADR/EVIDENCE。普通 task 先调用 `guru-maintain-architecture-baseline:task_impact_sync`，需要共享 authority 变化时走 contribution + `promotion`；不完整或冲突走 `repair`。

| 分区 | Locator |
| --- | --- |
| FOUNDATION | [`00-foundation/baseline.md`](./00-foundation/baseline.md) / [`00-foundation/design-constitution.md`](./00-foundation/design-constitution.md) |
| CURRENT | [`01-current/system.md`](./01-current/system.md) |
| TARGET | [`02-target/target.md`](./02-target/target.md) |
| DOMAIN / INTEGRATION | [`03-domains/ownership.md`](./03-domains/ownership.md) / [`04-integrations/distribution.md`](./04-integrations/distribution.md) |
| GAP / GOVERNANCE / PLAN | [`05-gaps/current-to-target.md`](./05-gaps/current-to-target.md) / [`06-governance/rules.md`](./06-governance/rules.md) / [`06-governance/change-contract.md`](./06-governance/change-contract.md) / [`07-plans/roadmap.md`](./07-plans/roadmap.md) |
| ADR / EVIDENCE | [`adr/README.md`](./adr/README.md) / [`evidence/current-evidence.md`](./evidence/current-evidence.md) |
