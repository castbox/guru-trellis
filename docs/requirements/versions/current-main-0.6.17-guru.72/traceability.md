# 迁移双向 trace

版本：`current-main-0.6.17-guru.72`；状态：`active`；predecessor：`current-main-0.6.17-guru.71`。完整继承[不可变前驱合同](../current-main-0.6.17-guru.71/traceability.md)；除下文明确修订的独立迁移边界外，既有 requirement/design/test、无人员模型、source disposition、owner、历史拒绝边界、NFR 与 trace 继续有效。前驱 source、计数和证据只表示历史快照。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.72` / `active`。知识版本不是软件发布。

| Requirement | Design owner | Test |
| --- | --- | --- |
| R495-01 / MIG-495-01 | D495-INVENTORY | T495-PREVIEW |
| R495-02 / MIG-495-02 | D495-CORE, D495-GURU | T495-INSTALL, T495-DISTRIBUTION, T495-ROLLBACK |
| R495-03 / MIG-495-03..04 | D495-CORE, D495-LIFECYCLE | T495-TASK, T495-RESUME |
| R495-04 / MIG-495-05 | D495-LIFECYCLE | T495-RESUME |
| R495-05 / MIG-495-06 | D495-INVENTORY, D495-LIFECYCLE | T495-DELIVERY |
| R495-06 / MIG-495-07 | D495-RECOVERY | T495-RECOVERY, T495-ROLLBACK |
| R495-07 / MIG-495-08 | D495-DISTRIBUTION | T495-DISTRIBUTION |
| R495-08 / MIG-495-09 | D495-MIXED, D495-CORE, D495-LIFECYCLE | T495-MIXED, T495-DEFERRED |

Design responsibility正文：[本版 design](../../../design/versions/current-main-0.6.17-guru.72/design-main.md)；Test正文：[本版 strategy](../../../test/versions/current-main-0.6.17-guru.72/test-strategy.md)，实际证据/剩余边界：[plan](../../../test/versions/current-main-0.6.17-guru.72/test-plan.md)。Architecture：ARCH-CUR-049 / ARCH-DOM-034 / ARCH-INT-037 / ARCH-GAP-012 / ADR-017 / EVD-048。每项R495拥有design和test；每个D495与T495由本表反向承接，无孤立验收。
