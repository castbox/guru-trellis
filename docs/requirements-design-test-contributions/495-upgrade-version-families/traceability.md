# R495 / D495 / T495 增量 Trace

状态：draft_candidate；原 `.73` trace 继承不改写。

| behavior | design responsibility | scenario |
| --- | --- | --- |
| MIG-495-01/10 | INVENTORY / FAMILY | S-MIG-495-FAMILY / REMOTE |
| MIG-495-02/08 | CORE / GURU | PRESERVE / REAPPLY / FAMILY / REMOTE |
| MIG-495-03/04/11 | CORE / LIFECYCLE | TASK / MIXED / LINKED |
| MIG-495-05/11 | LIFECYCLE | PLAN / DEV |
| MIG-495-06 | LIFECYCLE / INVENTORY | DELIVERY |
| MIG-495-07/12 | RECOVERY | PARTIAL / ROLLBACK / NEW-WORK |

Design ID 均使用 `D-MIG-495-` 前缀，scenario 均使用 `S-MIG-495-` 前缀。本表引用身份，行为由 requirements 与其 authority 拥有，机制由 design 拥有，实际执行结果只由 test 拥有。
