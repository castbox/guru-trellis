# #154 规划正文设计增量

本贡献定位当前设计责任。正文规则唯一归 `trellis/skills/guru-team/packages/guru-author-task-plan/references/planning-body.md` 和同 package 的四个 templates。资产已写入 canonical，并通过原 tools-only owner 同步本 worktree；实际安装和 Agent 行为结果仍只由唯一 Test 承接。

| Design / Contract | 责任与落点 | Requirement | Test |
| --- | --- | --- | --- |
| D154-01 / CON154-01 | 原 Author package 维护共享正文合同、四类薄模板和 detailed/brief 完整去敏过程示例；task_scope_requirements、requirements、solution/revision 按适用阶段显式加载 | R154-01/02/03/04 | T154-01/02/03 |
| D154-02 / CON154-02 | 原 Clarify/Wording/Approval、Guru 实施 dispatch、Check/Delivery Review/Completion 读取同源合同和必要引用，普通遗漏回最早 owner；Architecture 保持独立首轮读取，不预载 PRD/验收 | R154-02/03/04/05 | T154-02/03/04 |
| D154-03 / CON154-03 | 复用递归 package/preset 和声明平台投影；完整 matching 采用/reapply 保留用户内容与 sidecar，seed/generator/hook/官方 agents 不变 | R154-06 | T154-01/05 |

继续使用公共 accepted_scope、scope_ref/planning_root 和原 freshness；模板只写正文，不增加公共 I/O、阶段、writer、长期缓存或授权记录。来源设计处置只在选定 Delivery design；本长期贡献只引用责任，不复制该矩阵。Policy 与 Docs Plan 仍只在 implement。

Architecture 责任见 [本轮隔离贡献](../../architecture/contributions/154-planning-body-contract.md)，采用原 ADR-022/024 与现有 target-native 边界。shared-current 晋升按原 owners 的 expected-current 合同进行，最终 Check/commit/独立完整 Branch Review 覆盖实际写入。
