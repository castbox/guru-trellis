# #292 decisions

版本：`current-main-0.6.17-guru.88`；状态：`active`；predecessor：`current-main-0.6.17-guru.87`。完整继承[不可变前驱](../current-main-0.6.17-guru.87/decisions.md)，承接[已审查 #292 增量](../../../requirements-design-test-contributions/292-unique-planning-author/design.md)；Architecture继承 `current-main-0.6.17-guru.85/active`。

本版只承接已独立完整审查的 #292 accepted 增量，运行步骤仍由 canonical workflow / Skill package 独占。前驱有效合同及历史证据完整继承；不引入第二规划 writer、来源矩阵或 runtime authority。

Architecture `.85/active` 与 ADR-022/023 拥有唯一 Planning writer、candidate/final 回程和 scope_ready-before-planning 决定。RDT 只继承公开 locator/version/status，保留原 qualifier、causal semantics及生命周期 owners；见[Architecture](../../../architecture/README.md)与[设计增量](../../../requirements-design-test-contributions/292-unique-planning-author/design.md)。

晋升产生的新差异必须由原owners fresh Phase2、TaskCommit与不同reviewer完整Branch Review；Delivery、Publication、Merge、Completion、Closure、Finish及Release分别判断。知识晋升不证明软件发布或生产升级。
