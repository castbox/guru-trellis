# #495 双向追踪

Current inheritance：`.71/active`；task-owned candidate，未晋升。

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

反向 consumer：每个 test row 的 requirement/design 均由本表唯一列明，不产生孤立验收。Architecture contribution：`docs/architecture/contributions/495-legacy-installation-upgrade.md`，路径 `legacy_boundary_convergence`。RDT 与 Architecture 的 shared promotion 仅由各自 owner 在独立 committed full-diff review 后执行；promotion-created diff重新 Phase2/commit/review。
