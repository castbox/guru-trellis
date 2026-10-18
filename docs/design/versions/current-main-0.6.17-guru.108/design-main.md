# #154 规划正文合同设计

版本：`current-main-0.6.17-guru.108`；状态：`active`；predecessor：`current-main-0.6.17-guru.107`。

完整继承 [不可变前驱](../current-main-0.6.17-guru.107/design-main.md) 的有效合同。本版承接四类规划正文、来源处理、Delivery上下文、原owners加载与受管分发的责任。D154-01..03 / CON154-01..03 的唯一设计职责为 [本轮增量](../../../requirements-design-test-contributions/154-planning-body-contract/design.md)。正文规则唯一归canonical Author package，不在版本入口复制第二套规则。

[双向追踪](../../../requirements-design-test-contributions/154-planning-body-contract/traceability.md) 连接需求、设计与唯一Test。继承本Task适用的 Architecture `current-main-0.6.17-guru.98/active`、ADR-022/024及原constitution/change-contract；Architecture晋升由其原owner独立执行。

[唯一Test](../../../requirements-design-test-contributions/154-planning-body-contract/test.md) 分别报告真实Agent、确定性检查和安装证据。V1–V7的实际结论只由唯一Test维护；不得把正文、教学示例、工具安装或知识晋升当作Delivery/Task Completion。晋升差额仍进入最终Check、TaskCommit及独立完整Branch Review。完整多平台Release、软件发布及业务仓采用不在本轮验证范围。
