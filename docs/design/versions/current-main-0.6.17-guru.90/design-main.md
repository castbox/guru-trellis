# #531 design-main

版本：`current-main-0.6.17-guru.90`；状态：`active`；predecessor：`current-main-0.6.17-guru.89`。完整继承[不可变前驱](../current-main-0.6.17-guru.89/design-main.md)，承接[唯一#531增量](../../../requirements-design-test-contributions/531-task-delivery-lifecycle/design.md)；Architecture继承`current-main-0.6.17-guru.87/active`。

D531-01..08分别拥有公共模型薄投影、identity/Planning、返工退出、candidate/gate、事务事实、整体收尾、迁移及全局平台路由。step-local合同仍由各canonical Skill独占。

[双向trace](../../../requirements-design-test-contributions/531-task-delivery-lifecycle/traceability.md)与[唯一Test](../../../requirements-design-test-contributions/531-task-delivery-lifecycle/test.md)拥有实际结果和边界。promotion新diff须fresh Phase2/TaskCommit/不同reviewer完整BranchReview，不证明软件发布、原业务恢复或Task已完成。
