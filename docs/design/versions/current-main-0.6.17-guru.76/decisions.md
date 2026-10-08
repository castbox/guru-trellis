# 身份职责设计决策

版本：`current-main-0.6.17-guru.76`；状态：`active`；predecessor：`current-main-0.6.17-guru.75`。薄继承[不可变前驱](../current-main-0.6.17-guru.75/decisions.md)；本版仅用已审查的 #503 职责修订取代身份占用对完整 lifecycle schema 的依赖，其余有效合同及历史证据继承。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.76` / `active`。知识版本不表示软件发布。

直接替换越界占用分类与无 consumer wrapper；不新增索引或第二 store/writer。最小 field_path/remediation 仅由原 create stop 消费。ADR-017/018 和既有 migration 分类、owner、退出不变，无新 ADR。
