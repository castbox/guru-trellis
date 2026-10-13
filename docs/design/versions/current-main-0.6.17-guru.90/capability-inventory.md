# #531 capability-inventory

版本：`current-main-0.6.17-guru.90`；状态：`active`；predecessor：`current-main-0.6.17-guru.89`。完整继承[不可变前驱](../current-main-0.6.17-guru.89/capability-inventory.md)，承接[唯一#531增量](../../../requirements-design-test-contributions/531-task-delivery-lifecycle/design.md)；Architecture继承`current-main-0.6.17-guru.87/active`。

live registry/interfaces是inventory authority；当前38 packages/187 exits/114 commands，workflow36 invokes/180 exits。新create/activate-delivery取代旧activate-task，原Author、Check/Commit/Review/Completion能力迁移保持。

[双向trace](../../../requirements-design-test-contributions/531-task-delivery-lifecycle/traceability.md)与[唯一Test](../../../requirements-design-test-contributions/531-task-delivery-lifecycle/test.md)拥有实际结果和边界。promotion新diff须fresh Phase2/TaskCommit/不同reviewer完整BranchReview，不证明软件发布、原业务恢复或Task已完成。
