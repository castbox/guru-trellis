# 版本系列升级测试策略

版本：`current-main-0.6.17-guru.74`；状态：`active`；predecessor：`current-main-0.6.17-guru.73`。薄继承[不可变前驱](../current-main-0.6.17-guru.73/test-strategy.md)；仅本版明确的来源系列、迁移和证据增量取代前驱限制，其余合同及历史边界继续有效。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.74` / `active`。知识版本不表示软件发布。

完整继承已有策略；按安装清单、ownership、task/control 实际差异选择代表，不逐 tag 重复。19 tag 全覆盖归属，G1..G8 各 actual before/preview/upgrade/真实来源 rollback/smoke，任务格式与状态独立横向覆盖。新增场景与结果见[唯一验收增量](../../../requirements-design-test-contributions/495-upgrade-version-families/test.md)。
