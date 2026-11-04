# 跨 Issue 协调的验证策略

Identity：RDT-TST-ISSUE-ORCHESTRATION；别名：T731、主动解阻多轮验证。原语义 owner：guru-maintain-requirements-design-test-ssot。目标：docs/test/current/issue-orchestration.md。Version：issue-orchestration-1；Status：current。原 RDT owner 在 final_integration 晋升本完整定义。来源：Issue #731；关系 RDT-REQ-ISSUE-ORCHESTRATION → RDT-DES-ISSUE-ORCHESTRATION。本文件定义验证方法，实际结果由原Task/Delivery及Git事实提供，不预填通过。

| 验证/场景 | 需求 → 设计 | 入口、输入与必须观察的行为 |
| --- | --- | --- |
| T731-01 / SC731-GOAL | R731-01/02 → D731-01/02 | 真实Agent显式DAG入口、独立/依赖节点和终点前的无建议障碍；调查/商讨/核证、具体原owner动作、结果再判断直至场景终点，独立工作推进而依赖不被削弱 |
| T731-02 / SC731-SERIAL | R731-01/02/03 → D731-02/03 | Sequence两个节点，旧事务已知终止、普通输入/路径/前置错误及不足完成声明；保留旧失败/同身份，合法后续执行且原gate完成后才下一项，至chain_completed |
| T731-03 / SC731-WAIT | R731-04/05 → D731-04 | 已处理不变等待、实际外部变化、结束/超时/无人承接/复查失效；真实复查且条件变化后重新安排，不靠文字去重空转 |
| T731-04 / SC731-BLOCK | R731-03/05 → D731-03/04 | 必需外部条件或producer无支持路径，明确停止边界；先核当前入口/原owner修正及范围内方向，准确最小请求，安全inactive/无pending且实际心跳停止，至真实blocked |
| T731-05 / SC731-OBSERVE | R731-01/04 → D731-02/04 | 顺利运行、不变真实等待、真实完成；轻量观察，无无意义通知、重复审核或无限重试；未知发送/创建/merge结果先恢复原操作不重复 |
| T731-06 / SC731-BASELINE | R731-06 → D731-05 | 相同或严格等价输入的修改前/候选真实Agent运行；确证缺陷保留首失当和修复后对照，未复现则说明实际覆盖/历史缺口，不制造失败 |
| T731-07 / SC731-PROJECT | R731-06 → D731-01/05 | source/package、原安装owner实际同步与同候选reapply、drift、mode/sidecar；保持显式调用、Codex-only和public I/O，私有tests不泄入public |

多轮trace必须显示发现障碍→调查/商讨/审核→实际处置→接收结果→再判断。提出推荐、发一次指令、命中exit或文件存在都不足。输入只给目标、事实与边界，host-only预期不能进入模型；工具不能代选路线、代发下一指令或构造gate通过。需要理解自然语言的子会话由真实Agent承担，不能让fixture对消息关键词机械推进。

采用历史现场先刷新原入口、provider、版本、终点、停止约束及首失当处置，提供可移植去敏说明；不可访问时标明缺项并用当前正常入口补调查。不得接管原业务会话或复制秘密/授权过程。

分别报告源码/包、实际投影和真实行为。未运行或缺必要分支记未验证；隔离provider不证明真实app、生产效果、全部客户端或完整多平台Release/Upgrade。定向回归按当前入口和实际受影响consumer选择，测试数和静态parity不替充分性判断。
