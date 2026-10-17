# #589 Git 对象读取设计

版本：`current-main-0.6.17-guru.104`；状态：`active`；predecessor：`current-main-0.6.17-guru.103`。

完整继承[不可变前驱](../current-main-0.6.17-guru.103/design-main.md)的有效合同。本版承接[#589 设计增量](../../../requirements-design-test-contributions/589-git-object-performance/design.md)；[双向追踪](../../../requirements-design-test-contributions/589-git-object-performance/traceability.md)连接 R589/BEH589、D589 和 T589。

继承 Architecture `current-main-0.6.17-guru.95/active`。候选摘要改用上游公开 Git 内容 owner；旧物化实现退出，恢复、隔离和每输入独立检查责任继续继承。当前验收以不必要读取/hash消除与有界资源为准；耗时和 RSS 完整观测，旧数字门槛和失败记录保留。

[唯一 Test](../../../requirements-design-test-contributions/589-git-object-performance/test.md)拥有实际结果与未验证边界。正式 Task/installed 工具采用、受影响真实调用链、Architecture 晋升及整体 Completion 仍由原 owners 完成。此知识晋升不表示上述步骤已通过，也不承担 #575 完整 Release 矩阵。新增差额须 fresh Check、TaskCommit 与独立完整 Branch Review。
