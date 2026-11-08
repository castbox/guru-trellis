# Current-schema Task copies：设计责任差额

状态：proposed。适用完整前驱为 Git `2ab135ed2d3908966785bb23ad42ada0790f0c81:docs/design/current/native-compatibility.md`。继承 Architecture `guru-trellis-architecture`、ADR-024/017 及原公共/私有分工；真实 Architecture 拟写由 [原贡献](../../architecture/contributions/752-current-task-worktree-copies.md) 定位，本文不复制其判断或写共享 baseline。

完整拟生效责任由 [proposed Design](./proposed/docs/design/current/native-compatibility.md) D752-01..05 单写。Fork public parser/group/executor 校验 current authority 和 mixed defer2 peers；Guru 透传全部 inventory、原 binding 和 core_plan，维持 selected workspace 的 projected-only private migration。原 raw preservation、frozen source、begin/resume/rollback 和实际 installed validation 不变，不增加第二 copy 模型、ledger 或 binding writer。

当前 successor 为 Fork `b4f1665143bd4ecf3a290d426ad62293fc13ea42` / CLI-Core `0.7.0-castbox.6`；精确 source lock与正常同源build仍由原 owner验证。旧冻结计划保持原package pair和anchors，不换包续跑或发布同版本npm替换。选择、成本及重新评估条件在完整 Design 中保留；未验证安装不得由 source/CI替代。

[traceability](./traceability.md) 定位完整前驱、目标正文和原迁移合同。候选 Check 后才由原 RDT owner 在 final_integration 重读真实目标、整合并读回；最终质量覆盖实际 after。本文不声称 promotion 或交付已完成。
