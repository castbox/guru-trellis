# 非功能需求继承

版本：`current-main-0.6.17-guru.75`；状态：`active`；predecessor：`current-main-0.6.17-guru.74`。薄继承[不可变前驱](../current-main-0.6.17-guru.74/requirement-non-functional.md)；本版只承接修复后证据与既有机制说明，来源范围、owner与兼容退出不扩张，前驱有效合同及历史边界继续继承。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.75` / `active`。知识版本不表示软件发布。

不新增非功能要求、writer、持久状态或正常 runtime 双读。普通 stale/re-entry、去敏、实际来源回退、新业务工作保护及副作用控制继承前驱；不扩大攻击、竞态或 crash 范围。
