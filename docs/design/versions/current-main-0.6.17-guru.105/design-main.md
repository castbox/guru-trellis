# #600 晋升前移设计

版本：`current-main-0.6.17-guru.105`；状态：`active`；predecessor：`current-main-0.6.17-guru.104`。

完整继承 main 上 #589 的 [不可变前驱](../current-main-0.6.17-guru.104/design-main.md) 的有效合同；与 #600 晋升时机冲突的旧顺序片段由本版增量替代。本版承接 D600-01..04 / CON600-01..04，职责和合同由 [唯一增量](../../../requirements-design-test-contributions/600-promotion-before-check/design.md)拥有。 [双向追踪](../../../requirements-design-test-contributions/600-promotion-before-check/traceability.md)连接完整需求、责任与验收。

本 Task 的比较起点与适用 Architecture 为 `current-main-0.6.17-guru.95/active`，原 constitution、owners、GAP lifecycle 与软件四轴保持。Architecture 的本次后继由其原 owner 单独审查和晋升；本层不代写 Architecture 结论。

[唯一 Test](../../../requirements-design-test-contributions/600-promotion-before-check/test.md)单写实际验证、首次失败、恢复与未验证边界。知识晋升不证明实现通过、Delivery、整体 Task 完成、Release、业务安装或部署。最终 Check、Task Commit、committed 独立 Architecture 与完整 Branch Review 仍须覆盖实际候选。
