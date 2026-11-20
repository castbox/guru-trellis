# #887 Issue 入口架构贡献

状态 proposed。Task 887-issue-entry-streamline/gen0，Delivery d04ab09f-4768-4279-b224-aba82f373843。固定 before 为 61da60132bd0f6b64ab8626ac3158093481cd21e。来源为 [#887](https://github.com/castbox/guru-trellis/issues/887)。直接消费者为原 Architecture final_plan。完整拟后设计见本 Delivery design 第 4–7 节。

本批采用 target_native。将只建单和独立审核的进入条件按目的分开，选择现有 Create Issue、Clarify、Readiness。语义由原 owner 完成。脚本只处理当前快照、准确数据投影及原事务。保持已有 full-chain 与正式开工的实际调用职责。兼容范围依据 ADR-ISSUE-REVIEW-INTAKE、ADR-005 和 ADR-009。

| 项目关切 | 归属及判断依据 |
| --- | --- |
| authority-binding、constitution-binding | 现行 Architecture Baseline、constitution 和 change contract。沿原 Planning 3.0 两目的、后续 Delivery 4.0。 |
| boundary-and-decision、owner-and-single-writer | D1 design 第 4–6 节。Workflow 调用原 owners，执行器负责客观输入和原 GitHub 事务。 |
| compatibility-and-exit、gap-and-deviation | D1 design 第 7 节。按明确目的选择新入口，已进入原链的调用保原 wire 和恢复。依赖现有合同，无新的封闭 GAP 或持续状态。 |
| parallel-scope、evidence-and-freshness | 隔离工作树、本 Task 与现有职责正文。已审内容、查重时间和操作身份各有用途。复审覆盖留在当前上下文。 |
| review-and-promotion | 原 Architecture owner 在工程验证后集成并读回。独立 committed Review 对实际 before/after 评估。 |

拟集成 `docs/architecture/03-domains/issue-review-intake.md` 的当前职责。隔离决定见 [ADR-887-ISSUE-ENTRY-STREAMLINE](887-issue-entry-streamline-adr.md)。实施后沿原 owner 集成决定及可验证关系。配对 RDT 由原 owner 维护。现阶段提供规划依据，实施、实际采用、集成及独立代码审核另以结果为据。
