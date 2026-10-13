# #530 capability-inventory

版本：`current-main-0.6.17-guru.89`；状态：`active`；predecessor：`current-main-0.6.17-guru.88`。完整继承[不可变前驱](../current-main-0.6.17-guru.88/capability-inventory.md)，承接[唯一 #530 增量](../../../requirements-design-test-contributions/530-clean-committed-reentry/design.md)；Architecture 继承 `current-main-0.6.17-guru.86/active`。

live registry/interfaces/checker 是 inventory 来源；没有新增 Skill、command id 或 typed exit。原 TaskCommit public invoke 增加互斥输入 profile，原 DTO 和消费者保持，无第二内容算法或 store。

[唯一测试结果](../../../requirements-design-test-contributions/530-clean-committed-reentry/test.md)保留 scope-required 实际验证与未验证边界。晋升产生的新 diff 必须 fresh Phase2、TaskCommit 与不同 reviewer 完整 BranchReview；Delivery、Completion/Closure/Finish 与 Release 仍由各原 owner 判断，知识晋升不证明软件发布或生产效果。
