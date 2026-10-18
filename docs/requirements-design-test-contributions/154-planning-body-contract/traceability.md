# #154 双向追踪

| Requirement / Behavior | Design / Contract | Test / acceptance |
| --- | --- | --- |
| R154-01 / BEH154-01 | D154-01 / CON154-01 | T154-01/02 / AC1/AC2 |
| R154-02 / BEH154-02 | D154-01/02 / CON154-01/02 | T154-02/03 / AC3/AC4/AC5 |
| R154-03 / BEH154-03 | D154-01/02 / CON154-01/02 | T154-03/04 / AC6/AC7 |
| R154-04 / BEH154-04 | D154-01/02 / CON154-01/02 | T154-02/03 / AC9 |
| R154-05 / BEH154-05 | D154-02 / CON154-02 | T154-02/03/04 / AC1/AC7/AC8 |
| R154-06 / BEH154-06 | D154-03 / CON154-03 | T154-01/05 / AC10 |

canonical Author package 拥有正文规则，原 consumers 拥有阶段判断；[test.md](./test.md) 唯一记录本轮实际验证、失败/修复与未验证边界。本贡献已由原 RDT owner 晋升至 `current-main-0.6.17-guru.108`，状态与 manifest 及三个 current 导航一致。知识晋升与来源追踪表均不代替实现或行为证明。
