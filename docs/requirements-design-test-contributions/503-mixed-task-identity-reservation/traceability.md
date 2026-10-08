# #503 双向追踪

| Requirement | Design responsibility / contract | Test / scenario |
| --- | --- | --- |
| R503-01 | D503-CLASSIFY / D503-RESERVE | T503-CREATE / S503-CREATE |
| R503-02 | D503-CLASSIFY / D503-EXIT | T503-CREATE / T503-REJECT |
| R503-03 | D503-RESERVE | T503-RESERVE / T503-REJECT |
| R503-04 | D503-RESERVE / D503-DIAGNOSTIC | T503-REJECT |
| R503-05 | D503-CLASSIFY / D503-RESERVE | T503-PRESERVE / T503-RESERVE |
| R503-06 | D503-DISTRIBUTION | T503-INSTALLED |

来源：#503；predecessor：R495-08 / D495-MIXED（历史不改写）；candidate继承current .75，Architecture关联ARCH-CUR-049、ARCH-DOM-034、ARCH-INT-037及task architecture contribution。每个测试反向回到同表requirement/design；执行结果仅在test.md承接，不重复历史证据。
