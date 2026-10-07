# 迁移需求决策

版本：`current-main-0.6.17-guru.72`；状态：`active`；predecessor：`current-main-0.6.17-guru.71`。完整继承[不可变前驱合同](../current-main-0.6.17-guru.71/decisions.md)；除下文明确修订的独立迁移边界外，既有 requirement/design/test、无人员模型、source disposition、owner、历史拒绝边界、NFR 与 trace 继续有效。前驱 source、计数和证据只表示历史快照。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.72` / `active`。知识版本不是软件发布。

本版仅以一次性独立迁移支持替换 #481 的迁移拒绝，完整保留无人员/current-only 和历史原字节保留。新代 gate 必须 fresh 执行，已有 commit/push/PR/merge 按 live facts 读取而不重复；采用 [ADR-017](../../../architecture/adr/017-legacy-installation-upgrade.md)。不授予自动关闭旧任务/Issue 的意图。
