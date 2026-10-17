# #599 清晰技术写作测试策略

版本：`current-main-0.6.17-guru.103`；状态：`active`；predecessor：`current-main-0.6.17-guru.102`。

完整继承[不可变前驱](../current-main-0.6.17-guru.102/test-strategy.md)的有效合同。本版通过[#599 双向追踪](../../../requirements-design-test-contributions/599-clear-technical-writing/traceability.md)承接 T599-01–06 / AC1–AC8。继承 Architecture `current-main-0.6.17-guru.95/active`。

[唯一 Test](../../../requirements-design-test-contributions/599-clear-technical-writing/test.md)拥有实际命令、场景、首次失败与修订、通过结果和未验证边界。本层只定位策略，不复制实际结果，也不把源码或投影一致替代实际Agent行为。

语义保持由AI在原职责内判断；机械检查覆盖分发、引用、用户指令保护、reapply与drift。实际Codex覆盖主会话、恢复、独立child及缺失恢复。其他平台的实际行为和完整升级/Release矩阵维持未验证边界。知识晋升不代表交付或整体完成。
