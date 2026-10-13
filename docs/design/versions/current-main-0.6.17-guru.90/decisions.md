# #531 decisions

版本：`current-main-0.6.17-guru.90`；状态：`active`；predecessor：`current-main-0.6.17-guru.89`。完整继承[不可变前驱](../current-main-0.6.17-guru.89/decisions.md)，承接[唯一#531增量](../../../requirements-design-test-contributions/531-task-delivery-lifecycle/design.md)；Architecture继承`current-main-0.6.17-guru.87/active`。

Architecture .87及ADR-024拥有责任变更；public model不复制，旧安装保持成套固定，公共Plan2/Guru私有迁移各归原owner，无双reader/state authority。

[双向trace](../../../requirements-design-test-contributions/531-task-delivery-lifecycle/traceability.md)与[唯一Test](../../../requirements-design-test-contributions/531-task-delivery-lifecycle/test.md)拥有实际结果和边界。promotion新diff须fresh Phase2/TaskCommit/不同reviewer完整BranchReview，不证明软件发布、原业务恢复或Task已完成。
