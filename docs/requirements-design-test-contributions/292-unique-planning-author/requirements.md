# #292 需求增量

来源：[live #292](https://github.com/castbox/guru-trellis/issues/292) 的 `2026-10-10-r27`；需求 identity 与验收映射见 [task PRD](../../../.trellis/tasks/10-11-292-unique-planning-author/prd.md)。本贡献为 RDT `.87` 的隔离候选，继承 Architecture `.84/active`，尚未晋升。下表登记新增行为 identity；不复制来源设计处置矩阵或 step-local 合同。

| Requirement | Behavior identity / 增量 |
| --- | --- |
| R292-01 | BEH292-WRITER：唯一 Planning Author，独立 Wording/Approval。 |
| R292-02 | BEH292-SOURCE：fresh 来源与规范性/建议角色。 |
| R292-03 | BEH292-DISPOSITION：design 唯一逐项设计处置。 |
| R292-04 | BEH292-PROFILES：八个闭合 Author 输入。 |
| R292-05 | BEH292-CHAIN：两个 Architecture 调用串联现有门禁。 |
| R292-06 | BEH292-PURPOSE：candidate/final 的唯一回程。 |
| R292-07 | BEH292-RECOVERY：正常 docs 状态与同任务恢复。 |
| R292-08 | BEH292-BRAINSTORM：方法加载服从 Guru owner。 |
| R292-09 | BEH292-PREWRITE：首次 substantive solution 写入前评估。 |
| R292-10 | BEH292-POLICY：唯一 Delivery Policy 与四 Docs 策略。 |
| R292-11 | BEH292-DELIVERY：两个修订原因与既有 Completion 分流。 |
| R292-12 | BEH292-DEPENDENCY：原 qualification 与因果语义，最早依赖重入。 |
| R292-13 | BEH292-EXECUTION：原 active replan/resume_execution 身份承接。 |
| R292-14 | BEH292-DISTRIBUTION：current-only migration 与受管投影。 |
| R292-15 | BEH292-HANDOFF：最小 public DTO 与 AI/script 边界。 |

[traceability](traceability.md) 承接双向 identity，[test](test.md) 独占实际结果与限制。软件发布、完整矩阵及外部业务安装不属于本增量。
