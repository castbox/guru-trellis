# #553 双向追踪

状态：candidate；preimage RDT .93/active，继承Architecture .89/active；delta_first。唯一实际结果与未验证边界位于[Test](./test.md)。

| Requirement / behavior | Design/contract | Test | Source AC |
| --- | --- | --- | --- |
| R553-01 / BEH553-PREPLAN | D553-01/02/05 | T553-01/05 | 1/2 |
| R553-02 / BEH553-EVIDENCE | D553-05 | T553-01/05 | 2 |
| R553-03 / BEH553-IDENTITY | D553-01/04/05 | T553-02/05 | 3 |
| R553-04 / BEH553-PENDING | D553-03/04 | T553-02/03 | 4 |
| R553-05 / BEH553-FRESH | D553-01/02/04 | T553-03 | 5 |
| R553-06 / BEH553-RECOVERY | D553-04/05 | T553-02/04 | 6 |
| R553-07 / BEH553-DISTRIBUTION | D553-06 | T553-05/06 | 7 |
