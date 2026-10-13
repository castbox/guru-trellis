# #530 test-strategy

版本：`current-main-0.6.17-guru.89`；状态：`active`；predecessor：`current-main-0.6.17-guru.88`。完整继承[不可变前驱](../current-main-0.6.17-guru.88/test-strategy.md)，承接[唯一 #530 增量](../../../requirements-design-test-contributions/530-clean-committed-reentry/test.md)；Architecture 继承 `current-main-0.6.17-guru.86/active`。

T530-01..06 覆盖实际公开调用链、dirty、stale/base/branch/history、readonly、投影安装；原 empty-stage prepare 反事实继续暴露缺陷。fixture semantic authoring 只证明客观调用链，不能代替真实独立语义 gates。

[唯一测试结果](../../../requirements-design-test-contributions/530-clean-committed-reentry/test.md)保留 scope-required 实际验证与未验证边界。晋升产生的新 diff 必须 fresh Phase2、TaskCommit 与不同 reviewer 完整 BranchReview；Delivery、Completion/Closure/Finish 与 Release 仍由各原 owner 判断，知识晋升不证明软件发布或生产效果。
