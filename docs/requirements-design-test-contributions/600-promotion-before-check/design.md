# #600 设计责任增量

流程正文由 canonical workflow 编排，step-local 行为由原 Skill package 独占。本文件只定位责任与追踪，不复制各 owner 的完整合同。

| Design / Contract | 唯一责任与落点 | Requirement | Test |
| --- | --- | --- | --- |
| D600-01 / CON600-01 | 原 Architecture 的独立 before/after 评估、分支晋升及 final applicability；原 Check/Commit/committed Review 继续消费实际完整候选 | R600-01/02/04/06 | T600-01/02/04/06 |
| D600-02 / CON600-02 | Architecture 显式后继 nonplanning4.0/Delivery2.0 候选与晋升前 authority 绑定；原 owner 判断变化和恢复；runtime 仅验证事实 | R600-02/03/05 | T600-02/03/05 |
| D600-03 / CON600-03 | 原 Branch Review 的 promotion-reference alignment profile，消费原完整结果及全部差额，产生最终正式 passed；Git continuity 仍为真实整合 | R600-05 | T600-05 |
| D600-04 / CON600-04 | MIGRATION-600 与完整 preset/workflow 投影；三类在途状态、旧入口退出、无循环状态补写；实际结果只由唯一 Test 拥有 | R600-06/07/08 | T600-06/07/08 |

长期入口为 [Architecture package](../../../trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/SKILL.md)、[Branch Review package](../../../trellis/skills/guru-team/packages/guru-review-branch/SKILL.md) 和 [MIGRATION-600](../../../trellis/presets/guru-team/MIGRATION-600.md)。Architecture 贡献为 [600-promotion-before-check](../../architecture/contributions/600-promotion-before-check.md)。

采用 target_native；ADR-005 的旧顺序由本次后继决定替代，ADR-019/028/029 的独立性、适用性与工程事实边界保持。没有新 GAP、semantic owner、public Task/Delivery state 或兼容双 reader。当前文件存在不代表实现、晋升、软件发布或业务采用完成。
