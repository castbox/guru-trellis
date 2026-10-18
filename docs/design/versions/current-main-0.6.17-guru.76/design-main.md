# 身份占用与生命周期职责设计

版本：`current-main-0.6.17-guru.76`；状态：`active`；predecessor：`current-main-0.6.17-guru.75`。薄继承[不可变前驱](../current-main-0.6.17-guru.75/design-main.md)；本版仅用已审查的 #503 职责修订取代身份占用对完整 lifecycle schema 的依赖，其余有效合同及历史证据继承。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.76` / `active`。知识版本不表示软件发布。

[设计增量](../../../requirements-design-test-contributions/503-mixed-task-identity-reservation/design.md)拥有 D503-CLASSIFY/RESERVE/DIAGNOSTIC/DISTRIBUTION/EXIT。reservation 仅消费合法 id/ref；selected 再严格完整 current 校验，inventory/migration 仍完整分类；Fork 官方 writer 与 Guru substrate reader 各守原 owner。
