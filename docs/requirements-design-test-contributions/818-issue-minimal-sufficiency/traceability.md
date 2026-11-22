# #818 Issue 内容的追踪与迁移范围

本贡献的 [requirements.md](requirements.md)、[design.md](design.md)、[test.md](test.md)保留本次完整拟写、来源及工程观察，不成为第二共享 current，也不复制 canonical 内容方法。基线为 Git `fd0ee32618433a92ae934e29afb5b72e7136b4f7`；整体范围及 D1 仍由原 Task 接受的规划承担。strategy=`delta_first`，整合状态=`integrated_pending_review`。

## 完整目标与原来源

| 层 | 原完整来源 | 拟整合目标 |
| --- | --- | --- |
| Requirement | [#153](../153-issue-content-ssot/requirements.md)，经 `.109/requirement-main.md` 承接；#818 R1–R4 | [完整 current](../../requirements/current/issue-content.md) |
| Design | [#153](../153-issue-content-ssot/design.md)，经 `.109/design-main.md` 承接；#818 D1 design第4/9节 | [完整 current](../../design/current/issue-content.md) |
| Test | [#153 历史](../153-issue-content-ssot/test.md)，经 `.109/test-strategy.md` 承接；#818 V1–V4当前观察 | [完整 current](../../test/current/issue-content.md) |

整合前，三层 stable/current 入口的限定发现及 R153/BEH153/D153/CON153/T153、Issue内容/issue-content 概念检索未找到已迁移的同能力完整 current。已读共同 `review-sufficiency` 三单元；其共同审核职责与本次 Issue-specific 方法互为必要关系，不能并成第二内容定义。

## 双向关系

| Requirement / Behavior | Design / Contract | Test / 当前验收 |
| --- | --- | --- |
| R153-01 / BEH153-01 | D153-01 / CON153-01 | T153-01；T818-01 |
| R153-02 / BEH153-02 | D153-01/02 / CON153-01/02 | T153-02/03；T818-01/02 |
| R153-03 / BEH153-03 | D153-01/03 / CON153-01/03 | T153-02/03/04；T818-01/03 |
| R153-04 / BEH153-04 | D153-02 / CON153-02 | T153-02/03；T818-02 |
| R153-05 / BEH153-05 | D153-02/03 / CON153-02/03；D818-03 / CON818-03 | T153-02/03/04/05；T818-01..04 |
| R818-01 / BEH818-01 | D153-01/02 / CON153-01/02；D818-01 / CON818-01 | T818-01/02；AC1 |
| R818-02 / BEH818-02 | D153-01/02 / CON153-01/02；D818-01 / CON818-01 | T818-01/02；AC1 |
| R818-03 / BEH818-03 | D153-01/02 / CON153-01/02；D818-01/02 / CON818-01/02 | T818-01/02/03；AC1/2 |
| R818-04 / BEH818-04 | D153-01/02/03 / CON153-01/02/03；D818-01/02/03 / CON818-01/02/03 | T818-01..04；AC1/2 |

## 精确替代与当前状态

实际整合只替代 `.109` 三入口所连接的 R153-01..05 / BEH153-01..05、D153-01..03 / CON153-01..03、T153-01..05 的 Issue 内容责任及关系的当前组装方式。存活身份和 aliases 在各自完整目标内继续检索；#818 新方法差额使用 R818/BEH818、D818/CON818、T818/SC818 身份。canonical `issue-content.md` 继续独占完整方法，不在 RDT、共同规范或入口复制。

`.109` 对 `.108` 的其他能力/继承、旧 Task 的阶段适用读取、原 #153 贡献及原始 Test 事实保持。旧 Git/版本仍表示历史含义；新单元不宣称迁移整个语料。根/current README、共享索引、全局版本及 Architecture 正文均无本轮必要差额，不写这些文件。

原 Architecture final_plan 已返回 `baseline_current / no_architecture_impact / no_change`，继承 `docs/architecture/README.md / guru-trellis-architecture / active`。原 tools 安装/readback、同源 reapply、V3/V4 验证以及新行为正常返修均已完成，实际首轮失败、漏检及后继结果由本贡献 Test 保留其观察截止点。

原 RDT owner 在 `codex/818-issue-minimal-sufficiency`、HEAD=`fd0ee32618433a92ae934e29afb5b72e7136b4f7` 的真实工作区执行 final_integration：重读三层 authority、Architecture 公开身份、原 #153 来源、共同 review-sufficiency 关系及完整提案，确认三个目标原先不存在且没有同能力 current/介入变更，再整合本次完整单元并逐项 readback。引用及原身份检索检查通过。实际目标为 `RDT-REQ-ISSUE-CONTENT`、`RDT-DES-ISSUE-CONTENT`、`RDT-TST-ISSUE-CONTENT`；它们是本轮真实单元身份，不是新全局版本或未来 commit。

本次只建立文档实际整合事实，状态为 `integrated_pending_review`。后续 TaskCommit 与一次独立完整 committed Review 尚未发生；没有 Check/Review pass 或 Task Completion。current 三正文直接提供完整能力定义及观察，普通读者无需拼接本贡献；旧贡献及固定 Git 继续保留历史含义。
