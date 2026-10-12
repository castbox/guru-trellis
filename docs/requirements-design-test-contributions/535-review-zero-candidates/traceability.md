# #535 双向 trace

| Requirement / behavior | Design responsibility / contract | Test |
| --- | --- | --- |
| R535-01 / BEH535-EMPTY | D535-01/02 / CON535-ACTUAL-SET/VALIDATOR | T535-01/02/03 |
| R535-02 / BEH535-QUALIFY | D535-01/03 / CON535-ACTUAL-SET/CONSUMERS | T535-01/02/04 |
| R535-03 / BEH535-GATES | D535-02/03 / CON535-VALIDATOR/CONSUMERS | T535-01/02/03/04 |
| R535-04 / BEH535-PROFILES | D535-02/03 / CON535-VALIDATOR/CONSUMERS | T535-01/02 |
| R535-05 / BEH535-DISTRIBUTE | D535-04 / CON535-PROJECTIONS | T535-05/06/07 |

[Requirements](requirements.md)、[Design](design.md)、[Test](test.md)分别拥有本层正文。共享 current由原RDT owner晋升；本目录不复制完整 Skill流程，不含 gate artifact、用户授权或审查历史。
