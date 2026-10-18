# #530 requirement-main

版本：`current-main-0.6.17-guru.89`；状态：`active`；predecessor：`current-main-0.6.17-guru.88`。完整继承[不可变前驱](../current-main-0.6.17-guru.88/requirement-main.md)，承接[唯一 #530 增量](../../../requirements-design-test-contributions/530-clean-committed-reentry/requirements.md)；Architecture 继承 `current-main-0.6.17-guru.86/active`。

本版行为为 R530-01..06 / BEH530-CONTINUE、IDENTITY、READONLY、RECOVER、FULLREVIEW、DISTRIBUTE，详见唯一增量需求。原 dirty 提交、stale/base 恢复与首次完整独立 Review 的必要性保持。

[唯一测试结果](../../../requirements-design-test-contributions/530-clean-committed-reentry/test.md)保留 scope-required 实际验证与未验证边界。晋升产生的新 diff 必须 fresh Phase2、TaskCommit 与不同 reviewer 完整 BranchReview；Delivery、Completion/Closure/Finish 与 Release 仍由各原 owner 判断，知识晋升不证明软件发布或生产效果。
