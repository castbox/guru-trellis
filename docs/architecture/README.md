# Architecture Baseline SSOT

版本：`current-main-0.6.5-guru.43`；状态：`active`；predecessor：`current-main-0.6.5-guru.42`；source baseline：#335 contribution `architecture-contribution-335-repository-private-release-orchestration-v1` + inherited `.42` authority；#305 已确认的 `EVO-001..007` 保持独立 target authority。精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD。

本目录是唯一 Architecture Baseline authority。分区不可互换：FOUNDATION 是横向约束，CURRENT 只放证据证明的实现，TARGET 是已接受方向，GAP 是显式差距，PLAN 是已记录但未自动授权的执行顺序，ADR 是历史决策，EVIDENCE 只支撑判断。

版本历史：`current-main-0.6.5-guru.43` 是唯一 active Architecture baseline；`.42`、`.41`、`.40`、`.39`、`.38`、`.37`、`.36` 与 `.35` 是 superseded Architecture identities。`.43` 增加 `castbox/guru-trellis` 仓库私有正式发布编排 authority，不改变 extension candidate `0.6.15-guru.39`、Trellis CLI `0.6.15` 或任何 tag/GitHub Release 状态。Requirements/Design/Test 与 Architecture 共同使用 `.43` current knowledge identity；该 identity 只表示稳定 authority，不记录 promotion 阶段或发布结果。

读取顺序：FOUNDATION -> CURRENT -> DOMAIN/INTEGRATION -> TARGET/GAP -> GOVERNANCE/PLAN -> ADR/EVIDENCE。普通 task 先调用 `guru-maintain-architecture-baseline:task_impact_sync`，需要共享 authority 变化时走 contribution + `promotion`；不完整或冲突走 `repair`。

| 分区 | Locator |
| --- | --- |
| FOUNDATION | [`00-foundation/baseline.md`](./00-foundation/baseline.md) / [`00-foundation/design-constitution.md`](./00-foundation/design-constitution.md) |
| CURRENT | [`01-current/system.md`](./01-current/system.md) |
| TARGET | [`02-target/target.md`](./02-target/target.md) |
| DOMAIN / INTEGRATION | [`03-domains/ownership.md`](./03-domains/ownership.md) / [`04-integrations/distribution.md`](./04-integrations/distribution.md) |
| GAP / GOVERNANCE / PLAN | [`05-gaps/current-to-target.md`](./05-gaps/current-to-target.md) / [`06-governance/rules.md`](./06-governance/rules.md) / [`06-governance/change-contract.md`](./06-governance/change-contract.md) / [`07-plans/roadmap.md`](./07-plans/roadmap.md) |
| ADR / EVIDENCE | [`adr/README.md`](./adr/README.md) / [`evidence/current-evidence.md`](./evidence/current-evidence.md) |
