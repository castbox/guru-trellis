# 版本系列升级设计决策

版本：`current-main-0.6.17-guru.75`；状态：`active`；predecessor：`current-main-0.6.17-guru.74`。薄继承[不可变前驱](../current-main-0.6.17-guru.74/decisions.md)；本版只承接修复后证据与既有机制说明，来源范围、owner与兼容退出不扩张，前驱有效合同及历史边界继续继承。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.75` / `active`。知识版本不表示软件发布。

继承 [ADR-018](../../../architecture/adr/018-legacy-installation-version-families.md) 的来源系列与串行晋升合同；其余 ADR-017 所有权及兼容退出不变。必需 Skill/overlay 协调共享一个 required projection，并复用既有 preimage 校验；canonical-only 可回退，暂停新增内容阻塞回退。不新增 checkpoint/anchor/writer。
