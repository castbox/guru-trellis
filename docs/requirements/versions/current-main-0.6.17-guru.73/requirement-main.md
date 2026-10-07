# 旧安装单向迁移需求

版本：`current-main-0.6.17-guru.73`；状态：`active`；predecessor：`current-main-0.6.17-guru.72`。完整继承[不可变前驱合同](../current-main-0.6.17-guru.72/requirement-main.md)；仅下文明确承接的验收来源/事实更新取代前驱待验收描述，其余无人员/current-only、source disposition、owner、NFR 与历史拒绝边界继续有效。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.73` / `active`。知识版本不是软件发布。

`R495-01..08` 与 `MIG-495-01..09` 完整继承前驱；唯一需求调整是 [R495-05 样本来源](../../../requirements-design-test-contributions/495-legacy-installation-upgrade-acceptance/requirements.md)，依据 [live 范围说明](https://github.com/castbox/guru-trellis/issues/495#issuecomment-6028281048) 接受旧正式 writer 生成的隔离在途快照。构造 provider 不证明真实发布或业务原始事务；已有 PR/merge 继续读取真实 live facts。最终固定来源验收见 [本版 Test](../../../test/versions/current-main-0.6.17-guru.73/test-plan.md)。
