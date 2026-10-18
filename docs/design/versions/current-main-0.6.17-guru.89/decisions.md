# #530 decisions

版本：`current-main-0.6.17-guru.89`；状态：`active`；predecessor：`current-main-0.6.17-guru.88`。完整继承[不可变前驱](../current-main-0.6.17-guru.88/decisions.md)，承接[唯一 #530 增量](../../../requirements-design-test-contributions/530-clean-committed-reentry/design.md)；Architecture 继承 `current-main-0.6.17-guru.86/active`。

本次 additive profile 直接演进原 owner，原 dirty exact executor 与 diagnostics/recovery 有真实消费者；旧安装需要完整匹配 preset，新入口无 dual reader。Architecture .86/active 与原 ADR-005/009/011/015 保持职责边界。

[唯一测试结果](../../../requirements-design-test-contributions/530-clean-committed-reentry/test.md)保留 scope-required 实际验证与未验证边界。晋升产生的新 diff 必须 fresh Phase2、TaskCommit 与不同 reviewer 完整 BranchReview；Delivery、Completion/Closure/Finish 与 Release 仍由各原 owner 判断，知识晋升不证明软件发布或生产效果。
