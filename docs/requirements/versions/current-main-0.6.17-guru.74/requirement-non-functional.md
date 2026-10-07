# 非功能需求继承

版本：`current-main-0.6.17-guru.74`；状态：`active`；predecessor：`current-main-0.6.17-guru.73`。薄继承[不可变前驱](../current-main-0.6.17-guru.73/requirement-non-functional.md)；仅本版明确的来源系列、迁移和证据增量取代前驱限制，其余合同及历史边界继续有效。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.74` / `active`。知识版本不表示软件发布。

不新增非功能要求、writer、持久状态或正常 runtime 双读。普通 stale/re-entry、去敏、实际来源回退、新业务工作保护及副作用控制继承前驱；不扩大攻击、竞态或 crash 范围。
