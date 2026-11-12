# #813 固定来源贯通追踪

| 原稳定需求/行为 | 设计/合同 | 验证/场景 |
| --- | --- | --- |
| R718-07 / BEH718-BASELINE | D718-04 / CON718-BASE | T718-04 / S718-READ；T718-08 / S718-AGENT |
| R718-08 / BEH718-OPERATION | D718-04/05 | T718-05 / S718-REJECT |
| R718-09 / BEH718-DRAFT | D718-04/05 | T718-04/08 |
| R718-10 / BEH718-CONSUMER | D718-05 / CON718-CONSUMER | T718-04/05/08 |
| R718-11 / BEH718-MIGRATION | D718-04/07 | T718-05/07 |

三个原 runtime-location 完整单元就地细化，保留所有稳定身份和原 R760/D760/T760、R769/D769/T769 关系，不另建 Issue-specific current、共享索引或全局版本。原 B 下完整单元为 expected-current，完整 proposed 为拟写目标；真实 final_integration 检查适用条件和历史、写入并逐一读回，再交原 TaskCommit。
