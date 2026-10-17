# Design SSOT

唯一 current RDT authority 为 `current-main-0.6.17-guru.106/active`；[本版入口](./versions/current-main-0.6.17-guru.106/design-main.md) 完整继承 `.105` 并承接 [#577 唯一增量](../requirements-design-test-contributions/577-manual-archive-resume/traceability.md)。实际结果与边界由 [唯一 Test](../requirements-design-test-contributions/577-manual-archive-resume/test.md) 维护。Architecture 原 owner 单独晋升；知识晋升不表示业务完成或软件发布。

历史 `.105` authority：

唯一 current RDT authority 为 `current-main-0.6.17-guru.105/active`；[本版入口](./versions/current-main-0.6.17-guru.105/design-main.md)继承 main 的 immutable `.104`（#589）并承接 [#600 唯一增量](../requirements-design-test-contributions/600-promotion-before-check/traceability.md)。双方来源与追踪保留。本 Task 的 Architecture 比较起点仍为 `.95`；当前组合由 Architecture 原 owner 单独核验。[唯一 Test](../requirements-design-test-contributions/600-promotion-before-check/test.md)记录实际验证与边界。

历史 `.104` authority：

唯一 current RDT authority 为 `current-main-0.6.17-guru.104/active`；[本版入口](./versions/current-main-0.6.17-guru.104/design-main.md)完整继承 immutable `.103`，承接 [#589 唯一增量](../requirements-design-test-contributions/589-git-object-performance/traceability.md)。Architecture 继承 `.95/active`；公开摘要 owner、独立校验和资源生命周期保持原职责。[唯一 Test](../requirements-design-test-contributions/589-git-object-performance/test.md)区分读取/hash消除、耗时与内存观测、历史失败及未完成的正式采用。晋升差额仍须 fresh Phase2、TaskCommit 与独立完整 Branch Review；知识晋升不表示 Delivery、整体完成、软件发布或业务采用。

历史 `.103` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.103/active`；[本版入口](./versions/current-main-0.6.17-guru.103/design-main.md)继承 immutable `.102` 并承接 [#599 唯一增量](../requirements-design-test-contributions/599-clear-technical-writing/traceability.md)。Architecture 继承 `.95/active`；规则正文保持单一来源，[唯一 Test](../requirements-design-test-contributions/599-clear-technical-writing/test.md)记录实际结果与未验证边界。晋升差额须 fresh Phase2、TaskCommit 和不同 fresh reviewer 完整 Branch Review。

历史 `.102` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.102/active`；[本版入口](./versions/current-main-0.6.17-guru.102/design-main.md)完整继承 immutable `.101` 的有效合同并承接 [#575 准备贡献](../requirements-design-test-contributions/575-release-preparation/traceability.md)的 S2/S3/S4/S5 增量，继续继承 Architecture `.94/active`。原 owners、#575 S1 及 #578 工程事实适用性保持；[唯一 Test](../requirements-design-test-contributions/575-release-preparation/test.md)单写实际结果、首次失败与未验证边界。晋升差额须 fresh Phase2、TaskCommit 与不同评估者完整 Branch Review；知识晋升不表示整个准备任务完成、软件发布或业务采用。

历史 `.101` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.101/active`；[本版入口](./versions/current-main-0.6.17-guru.101/design-main.md)完整继承 immutable `.100` 的有效合同并承接 [#578 唯一增量](../requirements-design-test-contributions/578-cross-owner-validation-facts/traceability.md)，继承 Architecture `.94/active` 与 ADR-029。当前完整独立判断、跨 owner 工程事实适用性与当前绑定分离；原 owners、private retirement 和软件四轴保持。[唯一 Test](../requirements-design-test-contributions/578-cross-owner-validation-facts/test.md)单写实际结果和未验证边界；晋升新差额须 fresh gates，不表示软件发布或业务采用。

历史 `.100` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.100/active`；[本版入口](./versions/current-main-0.6.17-guru.100/design-main.md)完整继承 immutable `.99` 的有效合同并承接 [#575 S1 唯一增量](../requirements-design-test-contributions/575-source-adoption/traceability.md)，继续继承 Architecture `.93/active`。本版只拥有正式来源采用与公开映射；M/S2、最终投影和软件发布仍由原 owners 负责。[唯一 Test](../requirements-design-test-contributions/575-source-adoption/test.md)保留真实验证及未验证边界。晋升新差额须 fresh gates，不表示整个准备任务完成。

历史 `.99` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.99/active`；[本版入口](./versions/current-main-0.6.17-guru.99/design-main.md)继承 immutable `.98` 的有效合同并承接 [#569 唯一增量](../requirements-design-test-contributions/569-fixed-cutoff-history-query/traceability.md)，继承 Architecture `.93/active`、ADR-026/028。行为、机制与实际结果由专属文档单写；[唯一 Test](../requirements-design-test-contributions/569-fixed-cutoff-history-query/test.md)保留 fixture、外部/业务/Release 边界。本次晋升新差额须 fresh gates，不代表软件交付或整体完成。

历史 `.98` authority：当时 RDT authority 为 `current-main-0.6.17-guru.98/active`；[本版入口](./versions/current-main-0.6.17-guru.98/design-main.md)继承 immutable `.97` 的其余有效合同，并由 [#567 唯一增量](../requirements-design-test-contributions/567-fixed-development-baseline/traceability.md)替代冲突的默认追赶/祖先/整体 stale 片段，继承 Architecture `.92/active` 与 ADR-028。行为、机制和实际结果分别由专属文档单写；[唯一 Test](../requirements-design-test-contributions/567-fixed-development-baseline/test.md)保留首次失败/修复、历史红测及外部/业务/Release边界。本次晋升新差额须 fresh gates，不代表软件交付或整体完成。

历史 `.97` authority：当时 RDT authority 为 `current-main-0.6.17-guru.97/active`；[本版入口](./versions/current-main-0.6.17-guru.97/design-main.md)完整继承 immutable `.96`，承接 [#566 唯一增量](../requirements-design-test-contributions/566-single-checkout-upgrade/traceability.md)，继承 Architecture `.91/active`。行为与实际结果由专属文档单写；[唯一 Test](../requirements-design-test-contributions/566-single-checkout-upgrade/test.md)保持正式来源、业务采用和 Release 的未验证边界。晋升新差额须 fresh gates，不代表软件交付或业务完成。

历史 `.96` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.96/active`；[本版入口](./versions/current-main-0.6.17-guru.96/design-main.md)完整继承 immutable `.95`，承接 [#557 唯一增量](../requirements-design-test-contributions/557-manual-merged-delivery-recovery/traceability.md)，继承 Architecture `.90/active`。需求、设计和实际结果分别由专属文档单写；[唯一 Test](../requirements-design-test-contributions/557-manual-merged-delivery-recovery/test.md)保持 source、matching installed、真实 GitHub 与旧安装/业务/Release 边界。晋升新差额须 fresh gates，不代表软件交付或业务采用。

历史 `.95` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.95/active`；[本版入口](./versions/current-main-0.6.17-guru.95/design-main.md)完整继承 immutable `.94`，承接 [#556 唯一增量](../requirements-design-test-contributions/556-managed-python-update/traceability.md)，继承 Architecture `.89/active`。需求、设计和实际验证分别由增量专属文档单写；[唯一 Test](../requirements-design-test-contributions/556-managed-python-update/test.md)保留真实安装、fixture、旧 dogfood 和未验证矩阵边界。晋升新差额重新进入原 gates，不代表软件发布或业务升级。

历史 `.94` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.94/active`；[本版入口](./versions/current-main-0.6.17-guru.94/design-main.md)完整继承 immutable `.93`，承接 [#553 唯一增量](../requirements-design-test-contributions/553-preimplementation-reconciliation/traceability.md)，继承 Architecture `.89/active`。行为正文与实际结果由专属文档单写，[唯一 Test](../requirements-design-test-contributions/553-preimplementation-reconciliation/test.md)保留已验证层与旧 dogfood/业务/Release 边界；晋升新差额重新进入原 gates。

历史 `.93` authority：唯一 current RDT authority 为 `current-main-0.6.17-guru.93/active`；[本版入口](./versions/current-main-0.6.17-guru.93/design-main.md)完整继承 immutable `.92`，承接 [#548 唯一增量](../requirements-design-test-contributions/548-creation-recovery/traceability.md)并继承 Architecture `.89/active`。实际结果与未验证边界由[唯一 Test](../requirements-design-test-contributions/548-creation-recovery/test.md)拥有，晋升新差额重走原 gates。

历史 `.92` authority：唯一current RDT authority为`current-main-0.6.17-guru.92/active`；[本版入口](./versions/current-main-0.6.17-guru.92/design-main.md)完整继承immutable `.91` 的 #547 增量。本版仅同步 Architecture `.88/active` 的[已晋升贡献](../architecture/contributions/547-retain-source-open.md)；[唯一Test](../requirements-design-test-contributions/547-retain-source-open/test.md)继续拥有验证边界。晋升差额仍须 fresh Phase2/TaskCommit/独立完整 Review。

历史 `.91` authority：唯一current RDT authority为`current-main-0.6.17-guru.91/active`；[本版入口](./versions/current-main-0.6.17-guru.91/design-main.md)完整继承immutable `.90`，承接[#547唯一增量](../requirements-design-test-contributions/547-retain-source-open/traceability.md)。Architecture继承`.87/active`；[唯一Test](../requirements-design-test-contributions/547-retain-source-open/test.md)记录验证边界。fresh后续gates不由文档晋升替代。

历史 `.90` authority：当时 RDT authority为`current-main-0.6.17-guru.90/active`；[本版入口](./versions/current-main-0.6.17-guru.90/design-main.md)完整继承immutable `.89`，承接[#531唯一增量](../requirements-design-test-contributions/531-task-delivery-lifecycle/traceability.md)。Architecture继承`.87/active`；历史段落保持其原身份。promotion新diff须fresh gates，不证明软件发布或原业务恢复。

历史 `.89` RDT authority 当时是 `current-main-0.6.17-guru.89` / `active`；[本版入口](./versions/current-main-0.6.17-guru.89/design-main.md)完整继承 immutable `.88`，承接 [#530 增量 trace](../requirements-design-test-contributions/530-clean-committed-reentry/traceability.md)。Architecture 继承 `.86/active`。[唯一Test](../requirements-design-test-contributions/530-clean-committed-reentry/test.md)拥有实际验证及未验证边界；晋升差异须 fresh Phase2、TaskCommit 与不同 reviewer 完整 BranchReview，知识晋升不代表软件发布。

历史 `.70` Design authority：[`versions/current-main-0.6.17-guru.70/design-main.md`](./versions/current-main-0.6.17-guru.70/design-main.md)。版本状态与 source binding 见同目录 `manifest.yaml`；#481 后的 registry（34 packages / 155 exits / 104 commands，零 planned）见 [`capability-inventory.md`](./versions/current-main-0.6.17-guru.70/capability-inventory.md)，引用链见 `traceability.md`，决策见 `decisions.md`。production workflow 为 33 mandatory invokes / 153 exits。Architecture 为 `.70` / `active`；`.69` 及更早版本保持 immutable。

`.62` Design source binding 同时承接 C4 范围内的 Finalizer provenance recovery guard：初始 reprepare 在无 predecessor transaction 时按真实 Git ancestry 接受 strict historical ancestor，并由 application-level replacement transaction 保存 exact `pre_push_remote_head`；后续 pre-mutation preflight 必须复用该 remote identity。该段只闭合 `REQ-048` / `TST-032` 的设计映射，不把 C4 变成 Finalizer、C5-C7 或 production activation。

`FIN454-C4-P1-004` 仍由 `DES-046` 处理：selected base 无变化时，以 predecessor tail/base lineage/current review equality 与无 Open PR证明 fresh-reviewed descendant；remote 只认 transaction-owned pre-push/Publication endpoints，terminal PR history 不参与 current classification。它不新增 schema、public DTO、selector 或 branch/session/path 绑定。

Design 只解释实现 ownership 与 contract，不覆盖 Requirements 或 Architecture。普通 task 通过 RDT `task_impact_sync` / contribution / `promotion` 更新 current。

| 状态 | 版本 | Locator |
| --- | --- | --- |
| `active` | `current-main-0.6.17-guru.106` | [本版入口](./versions/current-main-0.6.17-guru.106/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.105` | [不可变前驱](./versions/current-main-0.6.17-guru.105/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.101` | [本版入口](./versions/current-main-0.6.17-guru.101/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.100` | [本版入口](./versions/current-main-0.6.17-guru.100/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.99` | [本版入口](./versions/current-main-0.6.17-guru.99/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.98` | [本版入口](./versions/current-main-0.6.17-guru.98/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.97` | [本版入口](./versions/current-main-0.6.17-guru.97/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.96` | [本版入口](./versions/current-main-0.6.17-guru.96/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.95` | [本版入口](./versions/current-main-0.6.17-guru.95/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.94` | [本版入口](./versions/current-main-0.6.17-guru.94/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.93` | [本版入口](./versions/current-main-0.6.17-guru.93/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.92` | [本版入口](./versions/current-main-0.6.17-guru.92/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.91` | [本版入口](./versions/current-main-0.6.17-guru.91/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.90` | [本版入口](./versions/current-main-0.6.17-guru.90/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.89` | [本版入口](./versions/current-main-0.6.17-guru.89/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.88` | [不可变前驱](./versions/current-main-0.6.17-guru.88/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.87` | [不可变前驱](./versions/current-main-0.6.17-guru.87/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.86` | [新 current](./versions/current-main-0.6.17-guru.86/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.85` | [新 current](./versions/current-main-0.6.17-guru.85/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.84` | [新 current](./versions/current-main-0.6.17-guru.84/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.83` | [新 current](./versions/current-main-0.6.17-guru.83/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.82` | [新 current](./versions/current-main-0.6.17-guru.82/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.81` | [design-main.md](./versions/current-main-0.6.17-guru.81/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.80` | [design-main.md](./versions/current-main-0.6.17-guru.80/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.79` | [design-main.md](./versions/current-main-0.6.17-guru.79/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.78` | [design-main.md](./versions/current-main-0.6.17-guru.78/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.77` | [design-main.md](./versions/current-main-0.6.17-guru.77/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.76` | [design-main.md](./versions/current-main-0.6.17-guru.76/design-main.md) | reviewed #503 identity responsibility; immutable .75 inheritance; post-promotion gates required |
| `superseded` | `current-main-0.6.17-guru.75` | [design-main.md](./versions/current-main-0.6.17-guru.75/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.74` | [design-main.md](./versions/current-main-0.6.17-guru.74/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.73` | [design-main.md](./versions/current-main-0.6.17-guru.73/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.72` | [design-main.md](./versions/current-main-0.6.17-guru.72/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.71` | [`design-main.md`](./versions/current-main-0.6.17-guru.71/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.70` | [`design-main.md`](./versions/current-main-0.6.17-guru.70/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.69` | [`design-main.md`](./versions/current-main-0.6.17-guru.69/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.68` | [`design-main.md`](./versions/current-main-0.6.17-guru.68/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.67` | [`design-main.md`](./versions/current-main-0.6.17-guru.67/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.66` | [`design-main.md`](./versions/current-main-0.6.17-guru.66/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.65` | [`design-main.md`](./versions/current-main-0.6.17-guru.65/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.64` | [`design-main.md`](./versions/current-main-0.6.17-guru.64/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.63` | [`design-main.md`](./versions/current-main-0.6.17-guru.63/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.62` | [`design-main.md`](./versions/current-main-0.6.17-guru.62/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.61` | [`design-main.md`](./versions/current-main-0.6.17-guru.61/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.60` | [`design-main.md`](./versions/current-main-0.6.17-guru.60/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.59` | [`design-main.md`](./versions/current-main-0.6.17-guru.59/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.58` | [`design-main.md`](./versions/current-main-0.6.17-guru.58/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.57` | [`design-main.md`](./versions/current-main-0.6.17-guru.57/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.56` | [`design-main.md`](./versions/current-main-0.6.17-guru.56/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.55` | [`design-main.md`](./versions/current-main-0.6.17-guru.55/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.54` | [`design-main.md`](./versions/current-main-0.6.17-guru.54/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.53` | [`design-main.md`](./versions/current-main-0.6.17-guru.53/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.52` | [`design-main.md`](./versions/current-main-0.6.17-guru.52/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.51` | [`design-main.md`](./versions/current-main-0.6.5-guru.51/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.50` | [`design-main.md`](./versions/current-main-0.6.5-guru.50/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.49` | [`design-main.md`](./versions/current-main-0.6.5-guru.49/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.48` | [`design-main.md`](./versions/current-main-0.6.5-guru.48/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.47` | [`design-main.md`](./versions/current-main-0.6.5-guru.47/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.46` | [`design-main.md`](./versions/current-main-0.6.5-guru.46/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.45` | [`design-main.md`](./versions/current-main-0.6.5-guru.45/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.44` | [`design-main.md`](./versions/current-main-0.6.5-guru.44/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.43` | [`design-main.md`](./versions/current-main-0.6.5-guru.43/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.42` | [`design-main.md`](./versions/current-main-0.6.5-guru.42/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.41` | [`design-main.md`](./versions/current-main-0.6.5-guru.41/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.40` | [`design-main.md`](./versions/current-main-0.6.5-guru.40/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.39` | [`design-main.md`](./versions/current-main-0.6.5-guru.39/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.38` | [`design-main.md`](./versions/current-main-0.6.5-guru.38/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.37` | [`design-main.md`](./versions/current-main-0.6.5-guru.37/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.36` | [`design-main.md`](./versions/current-main-0.6.5-guru.36/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.35` | [`design-main.md`](./versions/current-main-0.6.5-guru.35/design-main.md) |
| `released-history` | `v0.6.5-guru.9` | [`README.md`](./versions/v0.6.5-guru.9/README.md) |

Released history 只固定 release identity；未从 tag 恢复的设计内容保持 `unverified`，不能用 current 设计倒填。

`.58` 作为 immutable predecessor 完整继承 `.57` 并吸收 reviewed #452 contribution；该 snapshot 的 Architecture identity 为 `.58/active`。平台 authority 只有 pinned upstream 22-platform inventory 与目标仓库 exact `selected_platforms` 两层；重复 `--platform` 选择 exact subset，公开 CLI 不提供全集安装选项，无 flag 默认及 `guru-trellis` dogfood 均为 Claude、Codex、Cursor，OpenCode 是 upstream inventory 普通成员。#434 独占 production graph activation；promotion-created combined diff 必须重新通过 fresh Phase 2、Task Commit、完整 Branch Review，且该 snapshot 不声明 implementation、tests 或完整 Release matrix 已通过。
