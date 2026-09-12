# Architecture Baseline SSOT

版本：`current-main-0.6.5-guru.49`；状态：`active`；predecessor：`current-main-0.6.5-guru.48`；source baseline：reviewed #329 contribution `architecture-contribution-329-developer-free-trellis-v1` + inherited immutable `.48` authority；#305 已确认的 `EVO-001..007` 保持独立 target authority。精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD。

本目录是唯一 Architecture Baseline authority。分区不可互换：FOUNDATION 是横向约束，CURRENT 只放证据证明的实现，TARGET 是已接受方向，GAP 是显式差距，PLAN 是已记录但未自动授权的执行顺序，ADR 是历史决策，EVIDENCE 只支撑判断。

版本历史：`current-main-0.6.5-guru.49` 是唯一 active Architecture baseline；`.48`、`.47`、`.46`、`.45`、`.44`、`.43`、`.42`、`.41`、`.40`、`.39`、`.38`、`.37`、`.36` 与 `.35` 是 immutable superseded identities。`.49` 继承 `.48` 的 release mapping、#378/#240/#348/#332/#376 authority、`ADR-008` 与 23 Skills / 97 exits / 78 commands，并提升 #329 developer-free source 与 identity lifecycle。current framework source 为 `castbox/Trellis@a2003296b4c4ce46c50d72ead3b2ec9c317f69fc`、CLI `0.6.17`、package manager `pnpm@10.32.1`；extension 仍为 `0.6.16-guru.41`。released repository axis `v0.6.16-guru.1` 保持 immutable history，且不包含 #329 candidate。本 promotion 不证明 Publication、push、PR、merge、tag、Release 或 Issue closure；promotion-created diff 必须重新进入 fresh Phase 2、task commit 与独立完整 Branch Review。

读取顺序：FOUNDATION -> CURRENT -> DOMAIN/INTEGRATION -> TARGET/GAP -> GOVERNANCE/PLAN -> ADR/EVIDENCE。普通 task 先调用 `guru-maintain-architecture-baseline:task_impact_sync`，需要共享 authority 变化时走 contribution + `promotion`；不完整或冲突走 `repair`。

| 分区 | Locator |
| --- | --- |
| FOUNDATION | [`00-foundation/baseline.md`](./00-foundation/baseline.md) / [`00-foundation/design-constitution.md`](./00-foundation/design-constitution.md) |
| CURRENT | [`01-current/system.md`](./01-current/system.md) |
| TARGET | [`02-target/target.md`](./02-target/target.md) |
| DOMAIN / INTEGRATION | [`03-domains/ownership.md`](./03-domains/ownership.md) / [`04-integrations/distribution.md`](./04-integrations/distribution.md) |
| GAP / GOVERNANCE / PLAN | [`05-gaps/current-to-target.md`](./05-gaps/current-to-target.md) / [`06-governance/rules.md`](./06-governance/rules.md) / [`06-governance/change-contract.md`](./06-governance/change-contract.md) / [`07-plans/roadmap.md`](./07-plans/roadmap.md) |
| ADR / EVIDENCE | [`adr/README.md`](./adr/README.md) / [`evidence/current-evidence.md`](./evidence/current-evidence.md) |
