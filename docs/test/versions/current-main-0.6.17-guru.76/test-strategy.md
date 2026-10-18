# 身份职责测试策略

版本：`current-main-0.6.17-guru.76`；状态：`active`；predecessor：`current-main-0.6.17-guru.75`。薄继承[不可变前驱](../current-main-0.6.17-guru.75/test-strategy.md)；本版仅用已审查的 #503 职责修订取代身份占用对完整 lifecycle schema 的依赖，其余有效合同及历史证据继承。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.76` / `active`。知识版本不表示软件发布。

继承前驱策略；[唯一风险匹配增量](../../../requirements-design-test-contributions/503-mixed-task-identity-reservation/test.md)覆盖正式 source 与代表性 clean-installed create/ensure/bind/ref-id、占用拒绝、selected 严格校验、bytes/modes 保全与恢复。无关非身份字段变化不影响身份占用。
