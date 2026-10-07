# 独立迁移设计

版本：`current-main-0.6.17-guru.73`；状态：`active`；predecessor：`current-main-0.6.17-guru.72`。完整继承[不可变前驱合同](../current-main-0.6.17-guru.72/design-main.md)；仅下文明确承接的验收来源/事实更新取代前驱待验收描述，其余无人员/current-only、source disposition、owner、NFR 与历史拒绝边界继续有效。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.73` / `active`。知识版本不是软件发布。

`D495-INVENTORY/CORE/MIXED/GURU/LIFECYCLE/RECOVERY/DISTRIBUTION` 完整继承前驱。验收设计增量由 [唯一 contribution](../../../requirements-design-test-contributions/495-legacy-installation-upgrade-acceptance/design.md) 拥有：native 旧 creator 与正式 writer 正常执行后只读保存非 terminal 快照，新 `source_locked` public migration 明确 deferred/preserve；直接旧目标仍拒绝，新 current neighbor 正常创建。没有新生产 writer/恢复 authority。
