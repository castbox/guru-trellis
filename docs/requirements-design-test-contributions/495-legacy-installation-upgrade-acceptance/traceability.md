# #495 验收增量双向追踪

继承 `.72/active` [唯一原 trace](../../requirements/versions/current-main-0.6.17-guru.72/traceability.md)；本贡献只调整 R495-05 样本来源并补正式结果，未晋升 shared current。

| Requirement / behavior | Design responsibility | Test strategy / current evidence |
| --- | --- | --- |
| R495-01 / MIG-495-01 | D495-INVENTORY | T495-PREVIEW；固定来源及零写 preview |
| R495-02 / MIG-495-02 | D495-CORE, D495-GURU | T495-INSTALL, T495-DISTRIBUTION；source_locked/update/provider/保留 |
| R495-03 / MIG-495-03..04 | D495-CORE, D495-LIFECYCLE | T495-TASK, T495-RESUME；正式 planning/in_progress 样本 |
| R495-04 / MIG-495-05 | D495-LIFECYCLE | T495-RESUME；current owners/fresh Planning/dev-check |
| R495-05 / MIG-495-06 | D495-INVENTORY, D495-LIFECYCLE | T495-DELIVERY；真实 PR/merge + 旧 writer 构造快照 + 新 source_locked preserve |
| R495-06 / MIG-495-07 | D495-RECOVERY | T495-RECOVERY, T495-ROLLBACK；原样本恢复/真实写后回退/新工作保护 |
| R495-07 / MIG-495-08 | D495-DISTRIBUTION | T495-DISTRIBUTION；source/actual installed/update/reapply/drift |
| R495-08 / MIG-495-09 | D495-MIXED, D495-CORE, D495-LIFECYCLE | T495-MIXED, T495-DEFERRED；current creator、旧 direct 拒绝和保留 |

每个 test 的反向需求/职责由本表给出，无新增孤立 ID。Architecture：expected `.72`，增量 [acceptance contribution](../../architecture/contributions/495-legacy-installation-upgrade-acceptance.md)，继承 ARCH-CUR-049/ARCH-DOM-034/ARCH-INT-037/ADR-017；ARCH-GAP-012 只有独立 review/promotion 后才能按证据更新，当前不标 closed。历史 v1 contribution 与 `.72` 不覆写。
