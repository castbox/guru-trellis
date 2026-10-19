# #636 双向追踪和替代边界

适用来源为 Issue #636 当前完整行为1..7、候选边界与AC01..10，以及本Task已接受的唯一D1方案。当前基线 RDT `.112` / Git `b470580d4f79f61c66d72db97861fe1564b5e746`，Architecture `.103`。本目录三正文分别是受影响生命周期单元的完整proposed resulting definition；未受影响单元不复制。

| Requirement / behavior | Design responsibility | Test / AC |
| --- | --- | --- |
| R636-01 / BEH636-01 | D636-01/02 | T636-01；AC01/02 |
| R636-02 / BEH636-02 | D636-03 | T636-04；AC05/07 |
| R636-03 / BEH636-03 | D636-01/02 | T636-01/02；AC02/03 |
| R636-04 / BEH636-04 | D636-02/05 | T636-02/03/05；AC04/06/09 |
| R636-05 / BEH636-05 | D636-03 | T636-04；AC07 |
| R636-06 / BEH636-06 | D636-02/05 | T636-03/05/07；AC06/08/09 |
| R636-07 / BEH636-07 | D636-04 | T636-06/07；AC10 |

早期提交的输入/出口与Publication的Draft终点是新语义，不静默改变最终committed或Ready输出含义。正式full_review保留Check predecessor；原Task/Delivery API不加phase或Draft PublicationFact。来源中最终Publication重新判断关闭语义按当前Refs-only/Closure分工保留，不恢复旧关闭关键字。只窄替代当前“所有提交/远端反馈统一在完整Check/readiness后”的时机；D531身份/阶段、ADR-028固定内容、ADR-030晋升顺序及整体收尾保持。

MIGRATION-636由原代码/安装owner单写成套profile/schema/事务与consumer切换，本文只定位其职责。旧Task/Delivery、历史事实、固定版本和未受影响原支持不删除；不新增current兼容双读。本隔离贡献经原 RDT 评估与 promotion 后，由 RDT .113 的完整 current 生命周期单元承接；本目录保留来源与测试执行事实，普通读者无需组装本贡献。实际代码、安装/远端、软件 Release 和 Task Completion 各自判断。唯一执行结果见test.md的#636当前执行事实与未验证边界。
