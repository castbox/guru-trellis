# ADR-026 补充候选

用户显式选择已合并 PR 和已有 Task/Delivery，原 Merge 仍负责归属和记录。当原 Publication 不存在时，候选采用两类事实。Git 中的 Task/Delivery 关系及当前接受范围证明归属。GitHub 与 Git 双父、第二父和目标第一父历史证明真实合并。仅从共同基点继承的 Task 元数据不足以证明关系。

原 DeliveryFact 的 Candidate 保持 PR head 语义。原字段 `merge_commit` 与经核实的第一父定位实际落地差异。原 Completion 同时读取两段范围及实际 CI，独立判断整个 Task 的验收义务。证据未满足时保留原证据缺口路线。原 Closure 和 Finish 承接对应的完成事实。

采用完整匹配 preset 后，当前显式 adoption 入口可用。已有 Publication 的恢复继续使用原 profile 和事实。公共 Task2/API 1.0、DeliveryFact 与 Completion handoff 形状仍适用。
