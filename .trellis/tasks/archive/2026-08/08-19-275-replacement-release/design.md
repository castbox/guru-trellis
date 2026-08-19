# 设计

1. Finalizer 正常完成 archive、Ready PR 与 gate/transaction/plan retirement 后，不再尝试恢复已退休的进行中 Publication authority。调用方必须传入精确 retired owner locator；runtime 只从六文件 archive 的 durable summary 与当前 local/remote/Ready PR/title/body/base/branch/issue-scope facts 重建 terminal authority，任何缺失或漂移继续 fail closed。
2. inventory 从 canonical extension registry/interface validation 派生 active ids、commands、complete package ids，与 source/installed manifest 比较，不维护第二份数量常量。
3. canonical package 为源，preset apply 同步 dogfood/installed/platform projections，再执行 drift、ownership、mode、schema 和 focused integration tests。
4. replacement identity 为新 immutable annotated tag `v0.6.5-guru.10` 与 canonical extension revision `0.6.5-guru.36`。发布只消费 current-HEAD 独立 review 与 exact-candidate gate；历史 tag/Release 不变。
