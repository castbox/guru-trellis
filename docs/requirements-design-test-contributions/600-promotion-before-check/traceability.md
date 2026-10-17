# #600 双向追踪

| Requirement / Behavior | Design / Contract | Test / acceptance |
| --- | --- | --- |
| R600-01 / BEH600-01 | D600-01 / CON600-01 | T600-01 / AC1 |
| R600-02 / BEH600-02 | D600-01/02 / CON600-01/02 | T600-02 / AC2 |
| R600-03 / BEH600-03 | D600-02 / CON600-02 | T600-03 / AC3 |
| R600-04 / BEH600-04 | D600-01 / CON600-01 | T600-04 / AC4 |
| R600-05 / BEH600-05 | D600-02/03 / CON600-02/03 | T600-05 / AC5 |
| R600-06 / BEH600-06 | D600-01/04 / CON600-01/04 | T600-06 / AC6 |
| R600-07 / BEH600-07 | D600-04 / CON600-04 | T600-07 / AC7 |
| R600-08 / BEH600-08 | D600-04 / CON600-04 | T600-08 / AC8 |

本增量已由原 RDT owner 晋升为 `.104/active`；这只表示知识承接。各 owner 的行为合同留在原 package；实际证据与未验证边界只写 [test.md](./test.md)。新规则按 #600 在最终 Check 前由原 owners 晋升，不复制旧 post-Review 晋升循环。
