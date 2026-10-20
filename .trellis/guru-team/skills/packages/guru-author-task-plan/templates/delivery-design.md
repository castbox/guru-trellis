# 〈Delivery 标题〉设计

写作前实际加载 [共享正文合同](../references/planning-body.md)、当前候选的真实 Architecture candidate_assessment 及必要 PRD 引用。按以下九节展开本批实际方案；`plan_ready` 前完成适用内容。

## 1. 设计目标、需求承接与内容基线

关联本批需求/场景/AC、Task 整体责任及本批目标。按原 [authoring 固定范围合同](../references/authoring.md#fixed-delivery-range) 写 development baseline B 及其来源，区分内容范围、Planning H0 和 PR 目标。定位阶段适用 Architecture authority/constitution/change contract 与真实候选结论，不预填最终实现结果。

## 2. 当前系统、边界与目标差额

写现有能力、真实文件/模块、起点与目标状态、本批改动和不改边界。后续 Delivery 写前序已实现能力及本轮差额；全量 D1 写明没有前序。事实与计划分开。

## 3. 来源设计处置（唯一）

有规范性来源设计时，填写唯一矩阵：来源 locator/条款、原承诺、处置 retain/change/reject、具体正文落点、理由、影响、上游处置。逐承诺核对而非宽泛编号。没有规范性来源设计时，说明来源及依据，不保留空表。PRD/implement 引用本节，不复制矩阵。

## 4. 模块、职责与设计取舍

明确每个实际模块/owner 的输入、行为、输出与边界，定位改动文件。说明当前选择的理由、适用替代与影响，不为未来猜测预留机制。Architecture contribution 和共享晋升仍沿原 owner 合同。

## 5. 接口与数据

有接口/数据变化时写名称、方向、生产者/消费者、字段/值、约束与失败结果；共享完整规格可明确引用，本批差额仍展开。workflow 可写原 profile/输入→加载→原出口/consumer。无新 API/字段则明确已有接口如何承接，不造对象填表。

## 6. 状态、顺序、正常与失败流程

写实际状态/转换、条件分支、必要顺序和各失败结果；无状态变化时写执行顺序。覆盖正常成功、正常错误及适用例外。图表辅助理解，不代替说明，不增设来源没有的攻击或压力场景。

## 7. 恢复、兼容、迁移与集成

逐项展开适用的重试/恢复点、已发布 consumer 兼容、迁移及前后 Delivery 集成。无迁移或恢复协议时说明具体理由，不能笼统“不适用”。偏离回真实 upstream owner，保持历史事实和原 freshness。

## 8. 验证设计

按验证 ID 写对应要求/场景/AC、测试层、入口和输入、预期观察、证据限制。实际 Agent 行为、确定性检查、安装和外部链路分别说明。设计能让实施者执行、审核者核对；不把模板存在或预定命令当作成功证据。

## 9. Canonical 引用、本轮差额与实际未决项

定位命中的 repo requirement/behavior、design、test、Architecture authority 及本轮差额；写真实 task-owned contribution/必要 ADR 候选的责任和原晋升路径。必要问题给原 owner/影响/停点，没有则说明；不预创建空 contribution 或直接改共享导航。
