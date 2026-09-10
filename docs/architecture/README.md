# Architecture Baseline SSOT

版本：`current-main-0.6.5-guru.47`；状态：`active`；predecessor：`current-main-0.6.5-guru.46`；source baseline：reviewed #378 contribution `architecture-contribution-378-pinned-fork-runtime-v1` + inherited `.46` authority；#305 已确认的 `EVO-001..007` 保持独立 target authority。精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD。

本目录是唯一 Architecture Baseline authority。分区不可互换：FOUNDATION 是横向约束，CURRENT 只放证据证明的实现，TARGET 是已接受方向，GAP 是显式差距，PLAN 是已记录但未自动授权的执行顺序，ADR 是历史决策，EVIDENCE 只支撑判断。

版本历史：`current-main-0.6.5-guru.47` 是唯一 active Architecture baseline；`.46`、`.45`、`.44`、`.43`、`.42`、`.41`、`.40`、`.39`、`.38`、`.37`、`.36` 与 `.35` 是 superseded identities。`.47` 保留 `.46` 的 #240/#348/#332/#376 authority、`ADR-008` 与 23 Skills / 97 exits / 78 commands，提升 #378 的固定 Fork 来源、会话隔离与验证边界。extension 仍为 `0.6.15-guru.40`；当前框架源码为 `castbox/Trellis@ad332e3fe5a19d7274cb03e7c2f3e2128f8de291`，CLI `0.6.16`。这不是 npm 或 Release 发布。继承的 #332 Release 目标与历史 stable 记录不因本 promotion 改写；完整历史矩阵、业务接续和远端发布仍不由本 evidence 证明。

读取顺序：FOUNDATION -> CURRENT -> DOMAIN/INTEGRATION -> TARGET/GAP -> GOVERNANCE/PLAN -> ADR/EVIDENCE。普通 task 先调用 `guru-maintain-architecture-baseline:task_impact_sync`，需要共享 authority 变化时走 contribution + `promotion`；不完整或冲突走 `repair`。

| 分区 | Locator |
| --- | --- |
| FOUNDATION | [`00-foundation/baseline.md`](./00-foundation/baseline.md) / [`00-foundation/design-constitution.md`](./00-foundation/design-constitution.md) |
| CURRENT | [`01-current/system.md`](./01-current/system.md) |
| TARGET | [`02-target/target.md`](./02-target/target.md) |
| DOMAIN / INTEGRATION | [`03-domains/ownership.md`](./03-domains/ownership.md) / [`04-integrations/distribution.md`](./04-integrations/distribution.md) |
| GAP / GOVERNANCE / PLAN | [`05-gaps/current-to-target.md`](./05-gaps/current-to-target.md) / [`06-governance/rules.md`](./06-governance/rules.md) / [`06-governance/change-contract.md`](./06-governance/change-contract.md) / [`07-plans/roadmap.md`](./07-plans/roadmap.md) |
| ADR / EVIDENCE | [`adr/README.md`](./adr/README.md) / [`evidence/current-evidence.md`](./evidence/current-evidence.md) |
