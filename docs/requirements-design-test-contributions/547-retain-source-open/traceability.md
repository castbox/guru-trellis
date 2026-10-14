# #547 双向 Traceability

状态：reviewed_promoted；current RDT `.91/active`，完整继承前驱 `.90`；Architecture `.87/active`；delta_first。原 RDT owner reconciliation 后，只有此表连接增量，不复制长篇规范或 gate历史。

| Requirement / behavior | Design responsibility | Test / scenario | source AC |
| --- | --- | --- | --- |
| R547-01 / BEH547-SCOPE | D547-01 | T547-02/05 | AC1/5 |
| R547-02 / BEH547-DISPOSITION | D547-02 | T547-01/04 | AC2/4 |
| R547-03 / BEH547-RESULT | D547-02/04 | T547-01/02/03 | AC2/4 |
| R547-04 / BEH547-ARCHIVE | D547-03 | T547-02 | AC3 |
| R547-05 / BEH547-COMPLETION | D547-01 | T547-02/05 | AC5 |
| R547-06 / BEH547-PROJECTION | D547-02/03 | T547-03/04/05 | AC4/5 |
| R547-07 / BEH547-RECOVERY | D547-02/03 | T547-01/02/05 | AC6 |
| R547-08 / BEH547-ADOPTION | D547-04/05 | T547-06 | AC7 |

Requirements拥有增量目标，Design拥有职责，Test拥有验证层与未验证边界。R531-06/07和#436 predecessor不删除；本增量替换exact_source必须关闭及Finish仅要求CLOSED的错误条件，不重写历史能力或原业务责任。
