# #710：原 Check 职责与完整定义差额

状态：proposed。固定 before 为 Git `2fc49bda6552d1a8bf95dff243ab2de9a9ea8e30`。完整拟写见 [Design 目标正文](proposed/docs/design/current/knowledge-maintenance.md)，保留所有前驱条件和身份。本批选定方案由 [D1 design](../../../.trellis/tasks/10-31-710-phase2-recorder-authoring/deliveries/63d55014-9fec-48da-a106-2a7403305977/design.md) 第3节唯一来源处置及第4–8节拥有。

D710/CON710 将职责落在原 Check AI、recorder、checker、invocation、原 eval transport 和原安装 owner。采用既有语义 recorder，只退出没有独立必要 consumer 的完整结果输入；完整结果的合法 checker/invoke/maintenance 消费与 stale 不变。公开身份和两类 token 按其现行 producer/consumer 承接，不建立第二身份算法、摘要 authority、包装层或长期账本。

输入退出的 Architecture 判断、ADR 和完整架构拟写由原 Architecture owner 持有，RDT 只继承 `docs/architecture/README.md` / `guru-trellis-architecture` / active，before 同固定 Git。原 Task 的 [Architecture 设计](../../../.trellis/tasks/10-31-710-phase2-recorder-authoring/architecture/phase2-authoring.md) 和 [输入退出 ADR 候选](../../../.trellis/tasks/10-31-710-phase2-recorder-authoring/architecture/adr-phase2-recorder-input.md) 是其来源，不被本目录升级为已完成晋升。

本批完整提案先进入独立 Architecture 和候选 Check。candidate_checked 后，原 RDT owner 固定真实 target branch/commit，重读适用 before、完整 proposed 和 live target，保留仍有效条件及真实并行增量，实际写入并 readback。implementation 再以同一 B 构造含全部实际写入的新 candidate/begin_check，最终 Check、精确 TaskCommit 和完整 committed Review 各由原 owner 完成。此时序不因本批增加 authoring 说明而改变。

这里不新增共享根版本或导航关系；三个完整单元的现有定位保持。源代码、命令、真实 Agent、安装采用和后续正式结果分别取证，结果仅在 [Test](test.md) 记录当前观察边界。RDT 不替代 Check/Architecture 或本 Task 的最终门禁。
