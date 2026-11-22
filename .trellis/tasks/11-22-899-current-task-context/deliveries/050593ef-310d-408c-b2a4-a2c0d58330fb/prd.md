# D1 标准续接的只读上下文

## 1. 整体来源与术语

本批使用 [Task 整体 PRD](../../prd.md) 的已接受范围和 AC1、AC2。直接来源是 [#899 的行为要求和验收](https://github.com/castbox/guru-trellis/issues/899)。[#736 第 2 项及 AC3](https://github.com/castbox/guru-trellis/issues/736) 解释一次解析的来源。使用当前 checkout、Task generation 和 Delivery 选择的既有合同。

## 2. 整体与本批目标、非目标

D1 覆盖 #899 的全部交付范围。标准续接调用方通过一次公开只读调用取得足以定位下一步的 Task、checkout 和 Delivery 信息。原身份、选择、写入恢复和阶段决策职责继续由其既有 owner 承担。

## 3. 本批起点、前序结果、依赖与剩余责任

起点为 `origin/main@f06eddb6ccf97ddd2d1a41c117692f5957cb2dc7`。本 Task 无前序 Delivery。复用已有只读 C4/C5、session 与 Delivery 查询及无写入续接能力。D1 覆盖全部验收。实际 Delivery 交付后，原 Completion owner 检查整体范围和验证证据。

## 4. 本批调用方、场景与流程

| 场景 | 触发条件 | 结果 |
| --- | --- | --- |
| D1-S1 标准续接 | 当前会话绑定受支持 Task | 定位当前 Task、已验证 checkout 和可续接 Delivery。无 Delivery 时进入该 Task 的现有义务。选中的 Delivery 已终止时，交原终态入口。 |
| D1-S2 再次续接 | 同一会话执行第二次调用，相关事实保持或发生普通变化 | 采用仍适用的事实，刷新关系变化所影响的部分。 |
| D1-S3 缺失或不一致 | 没有当前 Task、显式查询、缺少续接所需绑定、或原查询返回诊断 | 无当前 Task 交原入口。显式只读查询按原合同处理。需要实际续接时交原绑定恢复。保留普通 stale、冲突、歧义及旧记录的诊断、owner 和解除条件。 |

## 5. 完整行为、条件与约束

- D1-R1 承接整体 R1。返回当前 TaskId、generation、经校验的 checkout 和区分三种 Delivery 情况所需的最小信息。存在适用 Delivery 时返回可交给原入口的定位。
- D1-R2 承接整体 R2。TaskId、generation、分支与 checkout、session、当前 Delivery 或相关来源变化后重新验证受影响事实。复用仅用于当前会话仍适用的事实。
- D1-R3 承接整体 R3、R4。保持显式只读查询和实际续接所需绑定的分界。保留正常失败的原诊断以及支持范围。
- D1-R4 承接整体 R5。查询前后 Task、绑定和 Git 资源状态一致。写入恢复由原事务保存合法进度。同步受影响调用的前置、最小示例、结果、诊断和兼容说明。

## 6. 本批验收、验证方式与未决项

- AC1 从标准续接入口观察有当前 Delivery、无当前 Delivery 和终态的分流。记录实际公开解析调用次数。用同会话的重复调用和正常关系变化验证采用与刷新。对比 Task、绑定和 Git 资源的前后状态。
- AC2 从同一入口观察无当前 Task、已知 Task 的显式查询或缺失绑定、正常 stale 或冲突以及受支持旧记录。核对诊断能否交给原 owner。采用仍适用的恢复证据，补验本次调用形态影响的路径。
- 对受影响的声明平台检查实际安装投影。当前无待确认的需求选择。调用和复用机制由本批设计细化。

## 7. Canonical 引用与本轮差额

生命周期 [历史续接测试](../../../../../docs/test/current/task-delivery-lifecycle.md) 记录原可续接与恢复约束。[Workflow Context](../../../../../docs/architecture/03-domains/workflow-context.md) 和 [ADR-035](../../../../../docs/architecture/adr/035-current-continuation-scope-routing.md) 约束现有职责及执行入口。差额是标准入口通过一次公开调用取得当前义务定位，并使普通变化刷新和诊断承接仍可观察。
