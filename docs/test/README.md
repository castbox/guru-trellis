# Test Strategy / Test Plan SSOT

唯一 current RDT authority 为 `current-main-0.6.17-guru.108/active`；[本版入口](./versions/current-main-0.6.17-guru.108/test-strategy.md) 完整继承 `.107` 并承接 [#154唯一增量](../requirements-design-test-contributions/154-planning-body-contract/traceability.md)。本Task适用 Architecture `.98/active`；[唯一Test](../requirements-design-test-contributions/154-planning-body-contract/test.md) 持有实际结果与未验证边界。晋升不表示真实行为验收、软件发布或业务完成。

历史 `.107` authority：

唯一 current RDT authority 为 `current-main-0.6.17-guru.107/active`；[本版入口](./versions/current-main-0.6.17-guru.107/test-strategy.md) 完整继承 `.106` 并承接 [#575 正式来源采用增量](../requirements-design-test-contributions/575-release-source-adoption/traceability.md)。Architecture 继承 `.98/active`；实际结果与边界只由 [唯一 Test](../requirements-design-test-contributions/575-release-source-adoption/test.md) 维护。晋升差额仍须 fresh Check、Task Commit 和独立完整 Branch Review；不表示软件发布或业务完成。

历史 `.106` authority：

唯一 current RDT authority 为 `current-main-0.6.17-guru.106/active`；[本版入口](./versions/current-main-0.6.17-guru.106/test-strategy.md) 完整继承 `.105` 并承接 [#577 唯一增量](../requirements-design-test-contributions/577-manual-archive-resume/traceability.md)。实际结果与边界由 [唯一 Test](../requirements-design-test-contributions/577-manual-archive-resume/test.md) 维护。Architecture 原 owner 单独晋升；知识晋升不表示业务完成或软件发布。

历史 `.105` authority：

唯一 current RDT authority 为 `current-main-0.6.17-guru.105/active`；[本版入口](./versions/current-main-0.6.17-guru.105/test-strategy.md)继承 main 的 immutable `.104`（#589）并承接 [#600 唯一增量](../requirements-design-test-contributions/600-promotion-before-check/traceability.md)。双方来源与追踪保留。本 Task 的 Architecture 比较起点仍为 `.95`；当前组合由 Architecture 原 owner 单独核验。[唯一 Test](../requirements-design-test-contributions/600-promotion-before-check/test.md)记录实际验证与边界。

历史 `.104` authority：

唯一 current RDT authority 为 `current-main-0.6.17-guru.104/active`；[本版入口](./versions/current-main-0.6.17-guru.104/test-strategy.md)完整继承 immutable `.103`，承接 [#589 唯一增量](../requirements-design-test-contributions/589-git-object-performance/traceability.md)。Architecture 继承 `.95/active`；公开摘要 owner、独立校验和资源生命周期保持原职责。[唯一 Test](../requirements-design-test-contributions/589-git-object-performance/test.md)区分读取/hash消除、耗时与内存观测、历史失败及未完成的正式采用。晋升差额仍须 fresh Phase2、TaskCommit 与独立完整 Branch Review；知识晋升不表示 Delivery、整体完成、软件发布或业务采用。

历史 `.103` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.103/active`；[本版入口](./versions/current-main-0.6.17-guru.103/test-strategy.md)继承 immutable `.102` 并承接 [#599 唯一增量](../requirements-design-test-contributions/599-clear-technical-writing/traceability.md)。Architecture 继承 `.95/active`；规则正文保持单一来源，[唯一 Test](../requirements-design-test-contributions/599-clear-technical-writing/test.md)记录实际结果与未验证边界。晋升差额须 fresh Phase2、TaskCommit 和不同 fresh reviewer 完整 Branch Review。

历史 `.102` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.102/active`；[本版入口](./versions/current-main-0.6.17-guru.102/test-strategy.md)完整继承 immutable `.101` 的有效合同并承接 [#575 准备贡献](../requirements-design-test-contributions/575-release-preparation/traceability.md)的 S2/S3/S4/S5 增量，继续继承 Architecture `.94/active`。原 owners、#575 S1 及 #578 工程事实适用性保持；[唯一 Test](../requirements-design-test-contributions/575-release-preparation/test.md)单写实际结果、首次失败与未验证边界。晋升差额须 fresh Phase2、TaskCommit 与不同评估者完整 Branch Review；知识晋升不表示整个准备任务完成、软件发布或业务采用。

历史 `.101` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.101/active`；[本版入口](./versions/current-main-0.6.17-guru.101/test-strategy.md)完整继承 immutable `.100` 的有效合同并承接 [#578 唯一增量](../requirements-design-test-contributions/578-cross-owner-validation-facts/traceability.md)，继承 Architecture `.94/active` 与 ADR-029。当前完整独立判断、跨 owner 工程事实适用性与当前绑定分离；原 owners、private retirement 和软件四轴保持。[唯一 Test](../requirements-design-test-contributions/578-cross-owner-validation-facts/test.md)单写实际结果和未验证边界；晋升新差额须 fresh gates，不表示软件发布或业务采用。

历史 `.100` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.100/active`；[本版入口](./versions/current-main-0.6.17-guru.100/test-strategy.md)完整继承 immutable `.99` 的有效合同并承接 [#575 S1 唯一增量](../requirements-design-test-contributions/575-source-adoption/traceability.md)，继续继承 Architecture `.93/active`。本版只拥有正式来源采用与公开映射；M/S2、最终投影和软件发布仍由原 owners 负责。[唯一 Test](../requirements-design-test-contributions/575-source-adoption/test.md)保留真实验证及未验证边界。晋升新差额须 fresh gates，不表示整个准备任务完成。

历史 `.99` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.99/active`；[本版入口](./versions/current-main-0.6.17-guru.99/test-strategy.md)继承 immutable `.98` 的有效合同并承接 [#569 唯一增量](../requirements-design-test-contributions/569-fixed-cutoff-history-query/traceability.md)，继承 Architecture `.93/active`、ADR-026/028。行为、机制与实际结果由专属文档单写；[唯一 Test](../requirements-design-test-contributions/569-fixed-cutoff-history-query/test.md)保留 fixture、外部/业务/Release 边界。本次晋升新差额须 fresh gates，不代表软件交付或整体完成。

历史 `.98` authority：当时 RDT authority 为 `current-main-0.6.17-guru.98/active`；[本版入口](./versions/current-main-0.6.17-guru.98/test-strategy.md)继承 immutable `.97` 的其余有效合同，并由 [#567 唯一增量](../requirements-design-test-contributions/567-fixed-development-baseline/traceability.md)替代冲突的默认追赶/祖先/整体 stale 片段，继承 Architecture `.92/active` 与 ADR-028。行为、机制和实际结果分别由专属文档单写；[唯一 Test](../requirements-design-test-contributions/567-fixed-development-baseline/test.md)保留首次失败/修复、历史红测及外部/业务/Release边界。本次晋升新差额须 fresh gates，不代表软件交付或整体完成。

历史 `.97` authority：当时 RDT authority 为 `current-main-0.6.17-guru.97/active`；[本版入口](./versions/current-main-0.6.17-guru.97/test-strategy.md)完整继承 immutable `.96`，承接 [#566 唯一增量](../requirements-design-test-contributions/566-single-checkout-upgrade/traceability.md)，继承 Architecture `.91/active`。行为与实际结果由专属文档单写；[唯一 Test](../requirements-design-test-contributions/566-single-checkout-upgrade/test.md)保持正式来源、业务采用和 Release 的未验证边界。晋升新差额须 fresh gates，不代表软件交付或业务完成。

历史 `.96` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.96/active`；[本版入口](./versions/current-main-0.6.17-guru.96/test-strategy.md)完整继承 immutable `.95`，承接 [#557 唯一增量](../requirements-design-test-contributions/557-manual-merged-delivery-recovery/traceability.md)，继承 Architecture `.90/active`。需求、设计和实际结果分别由专属文档单写；[唯一 Test](../requirements-design-test-contributions/557-manual-merged-delivery-recovery/test.md)保持 source、matching installed、真实 GitHub 与旧安装/业务/Release 边界。晋升新差额须 fresh gates，不代表软件交付或业务采用。

历史 `.95` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.95/active`；[本版入口](./versions/current-main-0.6.17-guru.95/test-strategy.md)完整继承 immutable `.94`，承接 [#556 唯一增量](../requirements-design-test-contributions/556-managed-python-update/traceability.md)，继承 Architecture `.89/active`。需求、设计和实际验证分别由增量专属文档单写；[唯一 Test](../requirements-design-test-contributions/556-managed-python-update/test.md)保留真实安装、fixture、旧 dogfood 和未验证矩阵边界。晋升新差额重新进入原 gates，不代表软件发布或业务升级。

历史 `.94` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.94/active`；[本版入口](./versions/current-main-0.6.17-guru.94/test-strategy.md)完整继承 immutable `.93`，承接 [#553 唯一增量](../requirements-design-test-contributions/553-preimplementation-reconciliation/traceability.md)，继承 Architecture `.89/active`。行为正文与实际结果由专属文档单写，[唯一 Test](../requirements-design-test-contributions/553-preimplementation-reconciliation/test.md)保留已验证层与旧 dogfood/业务/Release 边界；晋升新差额重新进入原 gates。

历史 `.93` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.93/active`；[本版入口](./versions/current-main-0.6.17-guru.93/test-strategy.md)完整继承 immutable `.92`，承接 [#548 唯一增量](../requirements-design-test-contributions/548-creation-recovery/traceability.md)并继承 Architecture `.89/active`。实际结果与未验证边界由[唯一 Test](../requirements-design-test-contributions/548-creation-recovery/test.md)拥有，晋升新差额重走原 gates。

历史 `.92` authority：唯一current RDT authority为`current-main-0.6.17-guru.92/active`；[本版入口](./versions/current-main-0.6.17-guru.92/test-strategy.md)完整继承immutable `.91` 的 #547 增量。本版仅同步 Architecture `.88/active` 的[已晋升贡献](../architecture/contributions/547-retain-source-open.md)；[唯一Test](../requirements-design-test-contributions/547-retain-source-open/test.md)继续拥有验证边界。晋升差额仍须 fresh Phase2/TaskCommit/独立完整 Review。

历史 `.91` authority：唯一current RDT authority为`current-main-0.6.17-guru.91/active`；[本版入口](./versions/current-main-0.6.17-guru.91/test-strategy.md)完整继承immutable `.90`，承接[#547唯一增量](../requirements-design-test-contributions/547-retain-source-open/traceability.md)。Architecture继承`.87/active`；[唯一Test](../requirements-design-test-contributions/547-retain-source-open/test.md)记录验证边界。fresh后续gates不由文档晋升替代。

历史 `.90` authority：当时 RDT authority为`current-main-0.6.17-guru.90/active`；[本版入口](./versions/current-main-0.6.17-guru.90/test-strategy.md)完整继承immutable `.89`，承接[#531唯一增量](../requirements-design-test-contributions/531-task-delivery-lifecycle/traceability.md)。Architecture继承`.87/active`；历史段落保持其原身份。promotion新diff须fresh gates，不证明软件发布或原业务恢复。

历史 `.89` RDT authority 当时是 `current-main-0.6.17-guru.89` / `active`；[本版入口](./versions/current-main-0.6.17-guru.89/test-strategy.md)完整继承 immutable `.88`，承接 [#530 增量 trace](../requirements-design-test-contributions/530-clean-committed-reentry/traceability.md)。Architecture 继承 `.86/active`。[唯一Test](../requirements-design-test-contributions/530-clean-committed-reentry/test.md)拥有实际验证及未验证边界；晋升差异须 fresh Phase2、TaskCommit 与不同 reviewer 完整 BranchReview，知识晋升不代表软件发布。

历史 `.70` authority：[`versions/current-main-0.6.17-guru.70/test-strategy.md`](./versions/current-main-0.6.17-guru.70/test-strategy.md) 与 [`test-plan.md`](./versions/current-main-0.6.17-guru.70/test-plan.md)。`traceability.md` 连接 Requirements、Design、Architecture `.70/active` 和 evidence；`.69` 及更早版本保持 immutable。

历史 `.70` 状态：`superseded`。当时 `.70` 完整继承 immutable `.69` 并承接 #481 task-personnel retirement；`T481-01..07` 是本次增量的 current acceptance authority，`T467-01..06`、`T454-G7-01..10` 与 `T434-01..39` 是继承能力。提升前证据不能代替 promotion-created diff 的 fresh Phase 2、Task Commit 与完整 Branch Review。旧版本安装升级、完整多平台 Release Gate 与业务仓生产验证仍 `unverified`。

历史 `FIN454-C4-P1-004` 在相同 `TST-032/SCN-044` 下增加 same-base old-review/provenance-tail/two-finding-fix topology、terminal PR exclusion、Open PR rejection、两个 transaction endpoint、intermediate remote rejection 与 replacement transaction binding；当时 provenance `23/23`、recovery `48/48`、Finalizer package `113/113` 通过，raw preset apply 被三项 pre-E434 sidecar 阻塞。该前驱快照不代表当前 `.71`；`.67` 的 preset reapply、dogfood drift 与 installer/graph `118/118` 是独立历史证据，仍不替代本次 promotion-created diff 的正式门禁。

| 状态 | 版本 | Locator |
| --- | --- | --- |
| `active` | `current-main-0.6.17-guru.108` | [本版入口](./versions/current-main-0.6.17-guru.108/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.107` | [本版入口](./versions/current-main-0.6.17-guru.107/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.106` | [本版入口](./versions/current-main-0.6.17-guru.106/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.105` | [不可变前驱](./versions/current-main-0.6.17-guru.105/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.101` | [本版入口](./versions/current-main-0.6.17-guru.101/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.100` | [本版入口](./versions/current-main-0.6.17-guru.100/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.99` | [本版入口](./versions/current-main-0.6.17-guru.99/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.98` | [本版入口](./versions/current-main-0.6.17-guru.98/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.97` | [本版入口](./versions/current-main-0.6.17-guru.97/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.96` | [本版入口](./versions/current-main-0.6.17-guru.96/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.95` | [本版入口](./versions/current-main-0.6.17-guru.95/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.94` | [本版入口](./versions/current-main-0.6.17-guru.94/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.93` | [本版入口](./versions/current-main-0.6.17-guru.93/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.92` | [本版入口](./versions/current-main-0.6.17-guru.92/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.91` | [本版入口](./versions/current-main-0.6.17-guru.91/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.90` | [本版入口](./versions/current-main-0.6.17-guru.90/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.89` | [本版入口](./versions/current-main-0.6.17-guru.89/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.88` | [不可变前驱](./versions/current-main-0.6.17-guru.88/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.87` | [不可变前驱](./versions/current-main-0.6.17-guru.87/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.86` | [新 current](./versions/current-main-0.6.17-guru.86/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.85` | [新 current](./versions/current-main-0.6.17-guru.85/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.84` | [新 current](./versions/current-main-0.6.17-guru.84/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.83` | [新 current](./versions/current-main-0.6.17-guru.83/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.82` | [新 current](./versions/current-main-0.6.17-guru.82/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.81` | [test-strategy.md](./versions/current-main-0.6.17-guru.81/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.80` | [test-strategy.md](./versions/current-main-0.6.17-guru.80/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.79` | [test-strategy.md](./versions/current-main-0.6.17-guru.79/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.78` | [test-strategy.md](./versions/current-main-0.6.17-guru.78/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.77` | [test-strategy.md](./versions/current-main-0.6.17-guru.77/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.76` | [test-strategy.md](./versions/current-main-0.6.17-guru.76/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.75` | [test-strategy.md](./versions/current-main-0.6.17-guru.75/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.74` | [test-strategy.md](./versions/current-main-0.6.17-guru.74/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.73` | [test-strategy.md](./versions/current-main-0.6.17-guru.73/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.72` | [test-strategy.md](./versions/current-main-0.6.17-guru.72/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.71` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.71/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.70` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.70/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.69` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.69/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.68` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.68/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.67` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.67/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.66` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.66/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.65` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.65/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.64` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.64/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.63` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.63/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.62` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.62/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.61` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.61/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.60` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.60/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.59` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.59/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.58` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.58/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.57` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.57/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.56` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.56/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.55` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.55/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.54` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.54/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.53` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.53/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.52` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.52/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.51` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.51/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.50` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.50/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.49` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.49/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.48` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.48/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.47` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.47/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.46` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.46/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.45` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.45/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.44` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.44/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.43` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.43/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.42` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.42/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.41` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.41/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.40` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.40/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.39` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.39/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.38` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.38/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.37` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.37/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.36` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.36/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.35` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.35/test-strategy.md) |
| `released-history` | `v0.6.5-guru.9` | [`README.md`](./versions/v0.6.5-guru.9/README.md) |

历史 `.68/active` 快照完整继承 immutable `.67` 并承接 #454 generation 7；其 Architecture 当时为 `.68/active`，现已由 `.70` 取代。当前 `.70` 的 promotion-created diff 仍须 fresh Phase 2、Task Commit 与完整 Branch Review；专门 Release matrix 和业务仓生产验证仍未验证。
