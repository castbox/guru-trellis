# #531 decisions

版本：`current-main-0.6.17-guru.90`；状态：`active`；predecessor：`current-main-0.6.17-guru.89`。完整继承[不可变前驱](../current-main-0.6.17-guru.89/decisions.md)，承接[唯一#531增量](../../../requirements-design-test-contributions/531-task-delivery-lifecycle/requirements.md)；Architecture继承`current-main-0.6.17-guru.87/active`。

ADR-024拥有公共Delivery单一authority及旧Task开发writer退出决定；Task整体责任、原独立语义门禁和私有事务owner保持。

[双向trace](../../../requirements-design-test-contributions/531-task-delivery-lifecycle/traceability.md)与[唯一Test](../../../requirements-design-test-contributions/531-task-delivery-lifecycle/test.md)拥有实际结果和边界。promotion新diff须fresh Phase2/TaskCommit/不同reviewer完整BranchReview，不证明软件发布、原业务恢复或Task已完成。
