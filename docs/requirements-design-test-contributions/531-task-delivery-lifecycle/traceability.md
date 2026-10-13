# #531 Traceability

状态：draft，isolated contribution；shared current 尚未晋升。

| Requirement / behavior | Design responsibility | Test / scenario |
| --- | --- | --- |
| R531-01 / BEH531-OWNERS | D531-01/08 | T531-01/02 |
| R531-02 / BEH531-PLAN | D531-02 | T531-02/08：D1/D2、#149活动replan |
| R531-03 / BEH531-REWORK | D531-03 | T531-03：方案/整体修订、部分/全部撤回 |
| R531-04 / BEH531-CANDIDATE | D531-04 | T531-04：#444 clean、dirty HEAD变化 |
| R531-05 / BEH531-FACT | D531-05 | T531-05：Publish/Merge/history与输出丢失 |
| R531-06 / BEH531-COMPLETION | D531-06 | T531-06：整体遗漏、无Delivery证据/收尾、Reactivate |
| R531-07 / BEH531-MIGRATION | D531-07/08 | T531-01/07：版本、installed/native/reapply、D2切换 |
| R531-08 / BEH531-DEPENDENCY | D531-03 | T531-08：#155局部provider边界 |

Requirements拥有目标，Design拥有职责，Test拥有实际结果与缺口。
本增量不改写历史 #468/#292/#530 或 shared current；promotion按原RDT/Architecture owner。

本轮基线承接 RDT .89 / Architecture .86。R531-04 沿已交付 #530 的原 Check、
TaskCommit、Reconcile 和首次完整 Review consumer 迁移；R531-02 沿已交付 #292
的原 Author/Wording/Architecture/Approval 迁移。R531-07 的 worktree-copy 与 unique
active binding 归 T531-07，真实 #149/#444/#155 接续归 T531-08；历史与当前候选
结果由唯一 test.md 分段记录，不能从上游完成或本地绿色推定 joint/原业务恢复。
