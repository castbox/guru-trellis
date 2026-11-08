# Current-schema Task copies：需求差额

状态：proposed。来源为 [Issue #752](https://github.com/castbox/guru-trellis/issues/752) 完整正文与 Task 已接受的 R1–R5 / AC1–AC5。适用完整前驱为 Git `2ab135ed2d3908966785bb23ad42ada0790f0c81:docs/requirements/current/native-compatibility.md`。本贡献只扩展该既有完整单元的 current-schema copies 迁移能力，不创建第二 current 或全局登记。

完整拟生效定义由 [proposed Requirements](./proposed/docs/requirements/current/native-compatibility.md) 单写。R752-01..05 分别拥有全部 roots 与唯一 authority、peer 保留/私有排除、正常 mismatch 写前阻塞、同计划恢复/回滚、matching source pair 实际安装。R630-01..06 和 R687-01..03 的原约束保持；#687 当时来源及 Test 不改写为 successor 采用事实。

触发场景为多 worktree 安装迁移、公共 Fork 与 Guru consumer 协同、来源切换和正常恢复/回滚。需求明确实际调用方、输入对象、写前失败、保留结果与可观察验收，不新增在线 SLA、攻击、竞态或完整 Release 矩阵。设计与测试关系由 [traceability](./traceability.md) 定位。共享 current 尚未写入；实际执行由 [Test](./test.md) 单写，知识候选不代表实现验收或 Task Completion。
