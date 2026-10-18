# 版本系列升级设计

版本：`current-main-0.6.17-guru.75`；状态：`active`；predecessor：`current-main-0.6.17-guru.74`。薄继承[不可变前驱](../current-main-0.6.17-guru.74/design-main.md)；本版只承接修复后证据与既有机制说明，来源范围、owner与兼容退出不扩张，前驱有效合同及历史边界继续继承。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.75` / `active`。知识版本不表示软件发布。

[设计增量](../../../requirements-design-test-contributions/495-upgrade-version-families/design.md)拥有 INVENTORY/FAMILY、CORE/GURU、LIFECYCLE/RECOVERY 责任。Fork显式 migrate 单写 core/task，Guru来源/资产迁移复用官方 marketplace/preset；正常 lifecycle current-only。当前 task/control/session 原字节及合法状态保留，known legacy 仅在一次性边界转换，已发布/在途逐案 deferred，不制造新 gate。来源 receipts/old source 决定 ownership，定制保留并协调必须的接口；既有备份恢复真实 before，新工作阻止覆盖。
