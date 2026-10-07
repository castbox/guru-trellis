# 候选证据与最终验收边界

版本：`current-main-0.6.17-guru.73`；状态：`active`；predecessor：`current-main-0.6.17-guru.72`。完整继承[不可变前驱合同](../current-main-0.6.17-guru.72/test-plan.md)；仅下文明确承接的验收来源/事实更新取代前驱待验收描述，其余无人员/current-only、source disposition、owner、NFR 与历史拒绝边界继续有效。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.73` / `active`。知识版本不是软件发布。

全部 MIG-495-01..09 的最终增量结果以 [固定来源验收](../../../requirements-design-test-contributions/495-legacy-installation-upgrade-acceptance/test.md) 为唯一入口，前驱 EVD-048 保留本地候选历史，current Architecture 对应 EVD-049。七场景首轮为 5/7、exit 1；两原失败样本后续 same-owner 恢复及剩余断言通过，没有单轮 7/7。明确 registry timeout 的 provider 重试成功；未归类 internal/node 失败原因保持未知。MIG06 的旧正式 writer 构造快照、真实 PR195 deferred/merged PR 诊断及新 source_locked preserve 分开记录，不证明原始真实在途或真实 GitHub 发布。

晋升 diff 仍必须 fresh Architecture/Phase2、TaskCommit 与不同 reviewer 完整 Branch Review，随后才可 Delivery Review/Publication/merge/Completion。此文不宣称这些后续 gates 已通过；软件 tag/Release、真实业务安装和完整累计矩阵未执行。
