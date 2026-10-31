# #693 双向追踪与继承边界

before 为 Git `e514770dfa03711a4606046232593b9bf782695a`，RDT authority 为 `guru-trellis-rdt`；Architecture 为 `docs/architecture/README.md / guru-trellis-architecture / active`。proposed 镜像最终路径，内部链接按最终目标解释。

| 整体要求 / D1 验收 | requirement / behavior | design / contract | test |
| --- | --- | --- | --- |
| R693-03/04/07；D1-AC02 | R693-01 / BEH693-CONTINUITY | D693-01 / CON693-METHOD | T693-02 |
| R693-05/06；D1-AC03 | R693-02 / BEH693-EVIDENCE | D693-01 / CON693-METHOD | T693-02 |
| R693-01/02；D1-AC01 | R693-03 / BEH693-HISTORY | D693-02 / CON693-HISTORY | T693-01 |
| R693-07/08；D1-AC04，整体 AC693-05 | R693-04 / BEH693-ADOPTION | D693-03 / CON693-ADOPTION | T693-03 |

没有既有 identity 被替代或删除。原 R648 的完整来源/未改消费者/共同错误预期、R-MECH 的机制必要性及原知识晋升条件完整保留。本项不继承其他 Task 的专项 native eval、A/B、固定次数或完整矩阵安排；#693 的定向验证和原质量链由 T693 具体定义。后端采用由整体 Task 保留，不因 D1 合并或 RDT 晋升消失。
