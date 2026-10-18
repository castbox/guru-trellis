# 身份占用与选中任务需求

版本：`current-main-0.6.17-guru.76`；状态：`active`；predecessor：`current-main-0.6.17-guru.75`。薄继承[不可变前驱](../current-main-0.6.17-guru.75/requirement-main.md)；本版仅用已审查的 #503 职责修订取代身份占用对完整 lifecycle schema 的依赖，其余有效合同及历史证据继承。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.76` / `active`。知识版本不表示软件发布。

[需求增量](../../../requirements-design-test-contributions/503-mixed-task-identity-reservation/requirements.md)拥有 R503-01..06，修订 R495-08 的占用读取职责。合法 id/ref 保留占用；无关非身份字段不赋予 current 能力；selected 与新建目标完整校验、migration 分类各保留原合同。
