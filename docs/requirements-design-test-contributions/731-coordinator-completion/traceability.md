# 协调责任关系

本贡献是完整拟写，不是共享current或实现通过。三个稳定单元分别拥有完整需求、设计与测试，当前适用来源为Issue #731。

| 需求/行为 | 设计职责/合同 | 测试策略/场景 |
| --- | --- | --- |
| R731-01 / BEH731-GOAL | D731-01/02 / CON731-OWNER/LOOP | T731-01/02/05 |
| R731-02 / BEH731-UNBLOCK | D731-02 / CON731-LOOP | T731-01/02 |
| R731-03 / BEH731-RECOVERY | D731-03 / CON731-RECOVER | T731-02/04/05 |
| R731-04 / BEH731-WAIT | D731-04 / CON731-WAIT | T731-03/05 |
| R731-05 / BEH731-BLOCK | D731-03/04 | T731-01/02/03/04 |
| R731-06 / BEH731-EVIDENCE | D731-01/05 / CON731-VERIFY | T731-06/07及全部行为场景 |

每个目标完整单元的identity、来源和必要跨层关系由自身承载。原RDT owner在candidate Check后重读真实目标并final_integration，随后implementation重绑全部实际after进入最终质量链。无共享根/current README或全局索引登记，无Architecture决策变化。历史记录保持原观察；不复制授权过程。
