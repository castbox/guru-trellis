# #896 架构贡献候选

当前状态为候选。架构基线为 `guru-trellis-architecture`。设计宪章为 `guru-trellis-design-constitution-v1`。项目 change contract 为 `guru-trellis-architecture-change-contract-v1`。变更路径为 `target_native`。

当前 ADR-026 要求以已有 Publication 归属手动合并的交付。#896 补充 Publication 缺失时的关系证据。原 Merge 评审原 Task/Delivery、PR Git 历史与目标合并事实。它仍通过公共 Delivery API 写入。原 Completion 读取 PR head Candidate 和 merge commit，并检查范围和实际验证。原 Closure 与 Finish 各自承接结果。

| 项目关切 | 候选处置 |
| --- | --- |
| authority-binding | 以 #896 行为要求和验收、整个 Task scope、D1 scope 及既有 ADR-024/026 为准。 |
| constitution-binding | 复用原语义 owner、公共关系和 writer。Git/GitHub 提供客观事实。 |
| boundary-and-decision | 更新 ADR-026，保留原 Publication 恢复，并增加独立的 Git 归属入口。PR head 与实际合入树各有明确角色。 |
| owner-and-single-writer | Merge 独占交付事实的归属和记录。Completion 独占验收判断。Closure 与 Finish 继续收尾。 |
| compatibility-and-exit | 通过完整匹配 preset 更新。原 #557 公开 profile 与历史读接口保持。新入口使用新版本聚合 schema。 |
| gap-and-deviation | 收敛已合入但缺 Publication 的恢复缺口。现有架构规则及 GAP 生命周期维持现行承诺。 |
| parallel-scope | 仅本 Delivery、关联权威和隔离验证资源。 |
| evidence-and-freshness | 用真实 Git 调用、状态回读和已关闭 Issue 的隔离路径核对边界。把 PR head CI 与实际合并内容分别审阅。 |
| review-and-promotion | 在实施和工程验证后由原 owner 整合、读回实际目标。固定提交后的独立审查核对前后状态。 |

预期架构目标为 `docs/architecture/adr/026-manual-merged-delivery-recovery.md`。拟写决定见本 Task 的 ADR 候选。原 Architecture owner 对照实际实现和证据整合。当前候选不建立晋升状态。
