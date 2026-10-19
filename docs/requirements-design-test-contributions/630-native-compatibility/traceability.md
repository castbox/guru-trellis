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

## 当前验收修订关系

修订 `630-script-validation-2026-10-20` 后，当前 R630-06 / BEH630-06 → D630-06 → T630-01..07；T630-08 为已撤销的历史会话验收，不再进入本 Task 必需验证集合。上表及本目录原 requirements/design 保留 D1 晋升时的来源关系，旧含义定位于 [cf07d082 固定版本](https://github.com/castbox/guru-trellis/blob/cf07d082c046b8e5e3c5050a603f22285821b215/docs/requirements-design-test-contributions/630-native-compatibility/traceability.md)。当前完整定义以 docs/requirements/current/native-compatibility.md、docs/design/current/native-compatibility.md 和 docs/test/current/native-compatibility.md 为准；实际结果仍由唯一 Test 单写。
