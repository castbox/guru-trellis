# Architecture Baseline SSOT

版本：`current-main-0.6.17-guru.69`；状态：`active`；predecessor：`current-main-0.6.17-guru.68`；source baseline：reviewed [#467 release preparation contribution](./contributions/467-release-v0617-guru2.md) + inherited immutable `.68` authority；#305 的 `EVO-001..007` 仍是独立 target authority。精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD。

本目录是唯一 Architecture Baseline authority。分区不可互换：FOUNDATION 是横向约束，CURRENT 只放证据证明的实现，TARGET 是已接受方向，GAP 是显式差距，PLAN 是已记录但未自动授权的执行顺序，ADR 是历史决策，EVIDENCE 只支撑判断。

版本历史：`current-main-0.6.17-guru.69` 是唯一 active Architecture baseline；`.68` 及更早 identities 保持 immutable superseded history。`.69` 完整继承 #434/#454 current graph，并在既有 TaskId preflight owner 内消除无关旧状态造成的新任务创建失败；见 `ARCH-CUR-046`、`ARCH-DOM-031`、`ARCH-INT-034`、`EVD-045`。active registry 为 34 Skills / 155 package exits / 104 commands，零 planned；production business workflow 为 33 mandatory invokes / 153 exits。

`.62` 的 C4 provenance 还明确绑定同一变更范围内的 Finalizer 首次 publication recovery guard：无 predecessor transaction 时只接受 absent、exact reviewed HEAD 或 strict historical ancestor remote，并把 exact `pre_push_remote_head` 写入 replacement transaction，再在任何远端 mutation 前复核同一 remote identity。该 guard 复用既有 Finalizer authority（`REQ-048` / `DES-046` / `TST-032`），不新增 lifecycle owner、public DTO 或生产 activation；执行级回归位于 `guru-finalize-task/tests/test_provenance.py`。

同一 authority 还允许 identity-matched unbound transaction 在 selected base 未变化时承接 fresh-reviewed finding-fix descendant：predecessor review-to-Publication 必须相等或为合法 provenance tail，base 已在 predecessor lineage，current Branch Review/Publication/live HEAD 相等且严格后继，并且没有 Open PR。历史 terminal PR 不作为 current candidate；remote 仅可等于 transaction-owned pre-push 或 Publication endpoint。该最小充分路径不增加 branch/session/path authority 或新的 recovery API。

历史 `.68` authority 将 repository `v0.6.17-guru.1`、extension `0.6.17-guru.42`、CLI/core `0.6.17` 与固定 Fork source `castbox/Trellis@8336e78b8fafe2a4bc4ea3d01815a61cf4f08983` 作为独立版本轴；它记录 RDT 从 `.67` 串行提升至 `.68`，不证明软件发布。该段仅为 predecessor provenance；当前版本目标及未验证边界以下段 `.69` 为准。

当前目标为 repository `v0.6.17-guru.2`、extension `0.6.17-guru.43`，CLI/core 与固定 Fork source 不变。`.69` knowledge promotion 仍不是软件发布；preparation PR 合并和 Finish 后必须重新冻结 exact main candidate，验证前一版本既有安装升级时退役受管 Skill 等内容已删除，再经 tag-pinned smoke 和 GitHub Release 才能声称公开发布。完整多平台矩阵与业务仓生产安装仍未验证。

读取顺序：FOUNDATION -> CURRENT -> DOMAIN/INTEGRATION -> TARGET/GAP -> GOVERNANCE/PLAN -> ADR/EVIDENCE。普通 task 先调用 `guru-maintain-architecture-baseline:task_impact_sync`，需要共享 authority 变化时走 contribution + `promotion`；不完整或冲突走 `repair`。

| 分区 | Locator |
| --- | --- |
| FOUNDATION | [`00-foundation/baseline.md`](./00-foundation/baseline.md) / [`00-foundation/design-constitution.md`](./00-foundation/design-constitution.md) |
| CURRENT | [`01-current/system.md`](./01-current/system.md) |
| TARGET | [`02-target/target.md`](./02-target/target.md) |
| DOMAIN / INTEGRATION | [`03-domains/ownership.md`](./03-domains/ownership.md) / [`04-integrations/distribution.md`](./04-integrations/distribution.md) |
| GAP / GOVERNANCE / PLAN | [`05-gaps/current-to-target.md`](./05-gaps/current-to-target.md) / [`06-governance/rules.md`](./06-governance/rules.md) / [`06-governance/change-contract.md`](./06-governance/change-contract.md) / [`07-plans/roadmap.md`](./07-plans/roadmap.md) |
| ADR / EVIDENCE | [`adr/README.md`](./adr/README.md) / [`evidence/current-evidence.md`](./evidence/current-evidence.md) |
