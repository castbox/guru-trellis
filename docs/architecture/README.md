# Architecture Baseline SSOT

版本：`current-main-0.6.5-guru.45`；状态：`active`；predecessor：`current-main-0.6.5-guru.44`；source baseline：reviewed #332 contribution `architecture-contribution-332-release-wrapper-entry-correction-v1` + inherited `.44` authority；#305 已确认的 `EVO-001..007` 保持独立 target authority。精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD。

本目录是唯一 Architecture Baseline authority。分区不可互换：FOUNDATION 是横向约束，CURRENT 只放证据证明的实现，TARGET 是已接受方向，GAP 是显式差距，PLAN 是已记录但未自动授权的执行顺序，ADR 是历史决策，EVIDENCE 只支撑判断。

版本历史：`current-main-0.6.5-guru.45` 是唯一 active Architecture baseline；`.44`、`.43`、`.42`、`.41`、`.40`、`.39`、`.38`、`.37`、`.36` 与 `.35` 是 superseded Architecture identities。`.45` 保留 `.44` 的 extension `0.6.15-guru.40`、Release target `v0.6.15-guru.6`、Trellis CLI `0.6.15`、#240/#348 authority 与 `ADR-008`，并把四阶段 public entry 收敛回原 wrapper/command、把 Interface 提升为 wrapper selection 唯一 authority、把 graph 收敛为 23 Skills / 97 exits / 77 commands。目标 `.6` 的 tag、GitHub Release、latest-stable 晋升与 tag-pinned smoke 在 post-merge exact candidate 发布前保持 `unverified`；本 knowledge identity 不记录动态发布结果。

读取顺序：FOUNDATION -> CURRENT -> DOMAIN/INTEGRATION -> TARGET/GAP -> GOVERNANCE/PLAN -> ADR/EVIDENCE。普通 task 先调用 `guru-maintain-architecture-baseline:task_impact_sync`，需要共享 authority 变化时走 contribution + `promotion`；不完整或冲突走 `repair`。

| 分区 | Locator |
| --- | --- |
| FOUNDATION | [`00-foundation/baseline.md`](./00-foundation/baseline.md) / [`00-foundation/design-constitution.md`](./00-foundation/design-constitution.md) |
| CURRENT | [`01-current/system.md`](./01-current/system.md) |
| TARGET | [`02-target/target.md`](./02-target/target.md) |
| DOMAIN / INTEGRATION | [`03-domains/ownership.md`](./03-domains/ownership.md) / [`04-integrations/distribution.md`](./04-integrations/distribution.md) |
| GAP / GOVERNANCE / PLAN | [`05-gaps/current-to-target.md`](./05-gaps/current-to-target.md) / [`06-governance/rules.md`](./06-governance/rules.md) / [`06-governance/change-contract.md`](./06-governance/change-contract.md) / [`07-plans/roadmap.md`](./07-plans/roadmap.md) |
| ADR / EVIDENCE | [`adr/README.md`](./adr/README.md) / [`evidence/current-evidence.md`](./evidence/current-evidence.md) |
