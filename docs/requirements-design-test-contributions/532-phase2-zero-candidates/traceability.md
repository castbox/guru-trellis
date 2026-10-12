# #532 双向 trace

| Requirement / behavior | Design responsibility / contract | Test |
| --- | --- | --- |
| R532-01 / BEH532-EMPTY | D532-01/02 / CON532-CHECK-SET/VALIDATOR | T532-01/02 |
| R532-02 / BEH532-QUALIFY | D532-01/02 / CON532-CHECK-SET/VALIDATOR | T532-03/04 |
| R532-03 / BEH532-GATES | D532-01/02/03 / CON532-CHECK-SET/VALIDATOR/CONSUMERS | T532-04/05/06 |
| R532-04 / BEH532-PROFILES | D532-02/03 / CON532-VALIDATOR/CONSUMERS | T532-06 |
| R532-05 / BEH532-DISTRIBUTE | D532-04 / CON532-DISTRIBUTE | T532-07/08 |

[Requirement](requirement.md)、[Design](design.md)、[Test](test.md)分别拥有本层内容。共享 current 的晋升由原 RDT owner 承接，本 contribution 不复制 canonical step-local 流程，不含 Gate artifact、用户授权或审查历史。
