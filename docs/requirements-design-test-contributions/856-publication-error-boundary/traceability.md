# #856 追踪与整合边界

原完整来源为 Git `4f3d9069e0720ec94e39d1079154d2f7a7058935` 的 docs/{requirements,design,test}/current/task-delivery-lifecycle.md。原 owner 为 guru-maintain-requirements-design-test-ssot，authority identity guru-trellis-rdt，状态 active。proposed 中的完整三层单元保 RDT-REQ/DES/TST-LIFECYCLE，末尾增加原错误与恢复能力的具体定义，不创建第二 current，不改共享入口或全局版本。

| accepted scope | 要求 | 原设计责任 | 验证 |
| --- | --- | --- | --- |
| AC856-01/02 | R856-01 | D856-01 | T856-01/02 |
| AC856-03 | R856-01/02/04 | D856-01/02 | T856-02/03 |
| AC856-04 | R856-02 | D856-02/03 | T856-03 |
| AC856-05 | R856-03 | D856-01/02 | T856-04 |
| AC856-06 | R856-04 | D856-03 | T856-05 |

R713-03/D713-03/T713-03 的错误语义、R531-05/D531-05/T531-05 的事实及同事务恢复、原 Refs-only/Closure 与全部未替代条件保持。JSON-input R695/D695/T695 的共享读取合同不变。本次是增加具体 Publish 边界，无删除、拆分或新公共协议。Planning Architecture 已判断 no_architecture_impact，未新增 Architecture 内容。

原 owner 在工程验证后、TaskCommit前重读实际 current、完整拟写与必要关系，再整合/readback。原 owner 已在 main 集成目标、当前专用分支 HEAD 4f3d9069e0720ec94e39d1079154d2f7a7058935 的未提交工作树完成整合/readback；状态为 integrated_pending_review，仍待完整 committed before/after 独立 Review，不能由本文产生实现、安装或发布通过。
