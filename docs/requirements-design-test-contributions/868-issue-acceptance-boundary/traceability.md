# #868 追踪与替代范围

前驱Git b85ea7bdf80db97ba8aceb1298dd61ed5f1ebeec；authority guru-trellis-rdt/active；Architecture guru-trellis-architecture/active。原RDT owner已在codex/868-issue-acceptance-boundary整合并读回上述六个完整current目标，状态integrated_pending_review；TaskCommit及独立committed Review尚待执行。

| 要求 | 设计 | 观察 | 整合目标 |
| --- | --- | --- | --- |
| R868-01/BEH868-BOUNDARY | D868-01 | T868-01 | docs/{requirements,design,test}/current/issue-content.md |
| R868-02/BEH868-PREWRITE | D868-01/02 | T868-01/02/04 | 同上 |
| R868-03/BEH868-CONTINUING | D868-02 | T868-02/04 | 同上 |
| R868-04/BEH868-EVIDENCE | D868-03 | T868-02/03/04 | docs/{requirements,design,test}/current/behavior-validation-method.md；Issue单元保关系 |

补足R153/R818/R819/R850与R735边界和持续去重责任，不删其他有效条件、来源、历史观察或原接口。共同审核仅补现有验证引用，不新建authority；不登记共享导航或全局版本。本次工程ready后已重读固定前驱、真实目标及完整提案，保留全部既有条件，整合完整定义并readback；TaskCommit后独立committed Review判断before/after。最终交付读取原公共结果与Git/PR，不由本贡献复制完成账本。
