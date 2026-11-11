# #792 关系与晋升边界

| 要求/行为 | 职责 | 测试 |
| --- | --- | --- |
| R792-01 / BEH792-AUTHORITY | D792-01 | T792-01/02 |
| R792-02 / BEH792-QUERY | D792-01/02 | T792-01/02/06 |
| R792-03 / BEH792-LOAD | D792-03 | T792-03/06 |
| R792-04 / BEH792-LEGACY | D792-03 | T792-04/06 |
| R792-05 / BEH792-ADOPTION | D792-02/04 | T792-01/02/05/06 |

固定前驱为Git05a16a5989669ca216d8ba34b9b419776410f04d中三层current/task-delivery-lifecycle.md完整单元，保留稳定RDT-REQ/DES/TST-LIFECYCLE身份及原关系；本次只增加R/D/T792。proposed正文中的相对引用按其拟晋升current目标位置解释，未改authority从固定源/真实目标读取，不复制整库。

原RDT owner在candidate Check后final_integration读取本贡献、实际current目标及必要关系，保留双方有效条件，写入并读回；不递增全局identity或登记共享导航。真正当前版本由Git与locator定位，candidate_ready不等晋升完成。Architecture由其原owner独立维护。
