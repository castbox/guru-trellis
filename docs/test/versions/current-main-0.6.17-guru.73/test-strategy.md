# 旧安装迁移测试策略

版本：`current-main-0.6.17-guru.73`；状态：`active`；predecessor：`current-main-0.6.17-guru.72`。完整继承[不可变前驱合同](../current-main-0.6.17-guru.72/test-strategy.md)；仅下文明确承接的验收来源/事实更新取代前驱待验收描述，其余无人员/current-only、source disposition、owner、NFR 与历史拒绝边界继续有效。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.73` / `active`。知识版本不是软件发布。

策略 `T495-PREVIEW/INSTALL/TASK/RESUME/DELIVERY/RECOVERY/ROLLBACK/DISTRIBUTION/MIXED/DEFERRED` 保持；`T495-DELIVERY` 采用 [accepted 样本来源](../../../requirements-design-test-contributions/495-legacy-installation-upgrade-acceptance/requirements.md)。[固定来源结果](../../../requirements-design-test-contributions/495-legacy-installation-upgrade-acceptance/test.md) 区分首次失败、same-owner 恢复、构造/provider doubles、真实 live PR/merge 和 actual installed。
