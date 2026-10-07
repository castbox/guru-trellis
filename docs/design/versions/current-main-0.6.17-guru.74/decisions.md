# 版本系列升级设计决策

版本：`current-main-0.6.17-guru.74`；状态：`active`；predecessor：`current-main-0.6.17-guru.73`。薄继承[不可变前驱](../current-main-0.6.17-guru.73/decisions.md)；仅本版明确的来源系列、迁移和证据增量取代前驱限制，其余合同及历史边界继续有效。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.74` / `active`。知识版本不表示软件发布。

采用 [ADR-018](../../../architecture/adr/018-legacy-installation-version-families.md) 的来源系列与本地 slice 晋升顺序；其余 ADR-017 所有权及兼容退出不变。必需 Skill/overlay 协调共享一个 required projection，并复用既有 preimage 校验；canonical-only 可回退，暂停新增内容阻塞回退。不新增 checkpoint/anchor/writer。
