# #599 清晰技术写作设计

版本：`current-main-0.6.17-guru.103`；状态：`active`；predecessor：`current-main-0.6.17-guru.102`。

完整继承[不可变前驱](../current-main-0.6.17-guru.102/design-main.md)的有效合同。本版采用[#599 设计增量](../../../requirements-design-test-contributions/599-clear-technical-writing/design.md)中的 D599-01–04 / CON599-01–04；[双向追踪](../../../requirements-design-test-contributions/599-clear-technical-writing/traceability.md)连接需求与测试。

继承 Architecture `current-main-0.6.17-guru.95/active`。唯一规则正文通过既有managed-spec安装，AGENTS有界区块、workflow、Guru Skills与平台入口只提供定位。原写作和审核owners保持职责；不新增语言审批、公共I/O、hook或持久状态。完整正文、例外和示例不在本层复制。

安装投影与实际行为由[唯一 Test](../../../requirements-design-test-contributions/599-clear-technical-writing/test.md)分别记录。旧安装采用、upstream update/upgrade冲突、其他平台实际行为及完整Release矩阵保留其边界。晋升差额继续经过原fresh gates。
