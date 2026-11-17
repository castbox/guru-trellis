# #880 追踪与替代范围

前驱 Git `76198a53b4da989b66d2e5f135ff4d2b703ca3cf`；authority `guru-trellis-rdt/active`；Architecture `guru-trellis-architecture/active`。当前状态为 `integrated_pending_review`；原 RDT owner 已在真实工程结果后重读 proposal、current targets 与必要关系，整合、写回并 readback。

| 要求 | 设计 | 观察 | 整合目标 |
| --- | --- | --- | --- |
| R880-01/BEH880-RESPONSIBILITY | D880-01 | T880-01 | docs/{requirements,design,test}/current/issue-content.md |
| R880-02/BEH880-NECESSARY | D880-01/02 | T880-01/03 | 同上；跨阶段边界同步 behavior-validation-method |
| R880-03/BEH880-SEPARATION | D880-01/02 | T880-01/03 | 同上 |
| R880-04/BEH880-SCENARIOS | D880-01/03 | T880-01/02 | docs/{requirements,design,test}/current/issue-content.md |
| R880-05/BEH880-OWNERS | D880-03 | T880-01/02 | 同上 |
| R880-06/BEH880-DISTRIBUTION | D880-02/04 | T880-02/03/04/05 | 六个 current targets；canonical/dogfood/platform projections |
| R880-07/BEH880-VERIFY | D880-01/04 | T880-01..05 | 六个 current targets |

补足 R153/R818/R868/R735 的既有条件和关系，不删除其他有效来源、历史观察、公共接口或原安装合同。本轮 Architecture 为 no impact，不创建 contribution/ADR。整合后状态只能为 `integrated_pending_review`；TaskCommit 与同一次独立 committed Review 仍待执行。
