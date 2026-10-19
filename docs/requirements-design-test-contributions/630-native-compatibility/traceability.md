# #630 双向追踪与替代边界

| Requirement / behavior | Design responsibility | Test strategy |
| --- | --- | --- |
| R630-01 / BEH630-01 | D630-01 | T630-01 |
| R630-02 / BEH630-02 | D630-01/02/03 | T630-01/02/04 |
| R630-03 / BEH630-03 | D630-02/05 | T630-02/03/06 |
| R630-04 / BEH630-04 | D630-04 | T630-05/07 |
| R630-05 / BEH630-05 | D630-04/05 | T630-05/06/07 |
| R630-06 / BEH630-06 | D630-06 | T630-01..08 |

需求、设计与测试正文分别由本目录requirements.md、design.md、test.md拥有，均来自Issue #630当前完整来源及同Task批准设计。新native-compatibility完整单元只承接#630明确跨系统边界，已有Task/Delivery、Completion和knowledge单元及未迁移legacy不变。不重编号旧identity，不把历史贡献改成新含义。

原installer/upstream-ownership关于unknown raw差异一律conflict的规则，仅由D630-04/本Task ADR窄替代声明文本的精确CRLF→LF恢复分支。恢复后raw hash、真实编辑.new、原.bak、binary/lock及ownership仍保持。正式Architecture晋升、原RDT promotion和完整候选后续Check/Review各自判断，不能互相代替。
