# 独立迁移设计决策

版本：`current-main-0.6.17-guru.72`；状态：`active`；predecessor：`current-main-0.6.17-guru.71`。完整继承[不可变前驱合同](../current-main-0.6.17-guru.71/decisions.md)；除下文明确修订的独立迁移边界外，既有 requirement/design/test、无人员模型、source disposition、owner、历史拒绝边界、NFR 与 trace 继续有效。前驱 source、计数和证据只表示历史快照。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.72` / `active`。知识版本不是软件发布。

`legacy_boundary_convergence`：Fork 只写 core/task schema，Guru 只写自身资产并复用 current marketplace/preset 与既有 identity/branch/checkout/session owners。独立 migration 承载旧 parser；current known-legacy reader只保留身份占用，不产生生命周期候选。deferred 保留与私有 rollback 锚点各有局部直接 consumer。退出与删除责任见 [ADR-017](../../../architecture/adr/017-legacy-installation-upgrade.md)，ADR-015/016 不改。
