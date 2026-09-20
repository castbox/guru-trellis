# #454 详细设计导航

## 设计方法

本文件只维护问题顺序、依赖关系与收敛状态。每个核心问题使用独立设计文件，完成当前问题的反例审查
后才进入下一个问题。任何单项设计通过都不代表整体模型已经成立；最终必须由组合状态矩阵证明全部
设计能够同时成立。

状态定义：

- `未开始`：尚未形成设计结论；
- `草案`：已有具体设计，但尚未完成当前问题审查；
- `单项收敛`：当前问题的状态、失败行为和迁移边界已经闭合；
- `组合验证`：该设计已进入全量状态矩阵，且未与其他设计冲突。

## 问题序列

| 顺序 | 问题 | 独立设计文件 | 当前状态 | 完成条件 |
| --- | --- | --- | --- | --- |
| 01 | 稳定 Task Identity 与可变 Task Locator | `design/01-stable-task-identity.md` | 组合验证 | create、rename、archive、Reactivate、legacy establishment 和唯一性无歧义。 |
| 02 | Task Source、Accepted Scope、Delivery Target 与 Closure 分离 | `design/02-task-authority-relations.md` | 组合验证 | source、scope、target 与 closure 各有唯一 owner。 |
| 03 | Lifecycle Incarnation 与 terminal result 隔离 | `design/03-lifecycle-incarnation.md` | 组合验证 | Reactivate 不复用旧 session、Finish 或 Cleanup authority。 |
| 04 | 预建 checkout 与 Guru provision 的双入口 | `design/04-checkout-acquisition.md` | 组合验证 | 两种入口产生同一 task state，ownership 投影唯一。 |
| 05 | Current Branch Association 与显式 rebind | `design/05-task-branch-association.md` | 组合验证 | 任一时刻恰好一个 current branch，历史 resource 不冲突。 |
| 06 | Live Execution Checkout Resolution | `design/06-live-checkout-resolution.md` | 组合验证 | move、跨机器、零/多 checkout 均有唯一结果或恢复入口。 |
| 07 | 自动推导、候选选择与显式指定 | `design/07-resolution-and-selection.md` | 组合验证 | 自动和人工 target 使用同一验证合同，不发生错误推导或永久 fail close。 |
| 08 | Path-free Session Association | `design/08-session-association.md` | 组合验证 | resume、跨 session、A→B→A 与 binding loss 均不串线。 |
| 09 | Resource Ownership、Finish 与 Cleanup | `design/09-resource-ownership-cleanup.md` | 组合验证 | caller-owned 保留、Guru-owned 可清理、unknown ownership 可人工处置。 |
| 10 | 统一状态矩阵与迁移切换 | `design/10-composition-and-migration.md` | 组合验证 | 全部 reachable state 有唯一 owner、route 或 terminal stop，旧 mappings 退出。 |
| 11 | Public Skill I/O 与迁移闭包 | `design/11-public-contract-migration.md` | 组合验证 | 全部新增与实质变化 owner 具有完整 exit、minimal output、唯一 consumer 与旧 identity 处置。 |

## 整体可行性结论

问题01至11已分别完成单项审查，并通过`design/12-final-consistency-review.md`对16个lifecycle scenario、
22条acceptance criteria、31条reachability constraint、8组active runtime-loss组合、forbidden states与public
owner completeness执行联合复核。47个finding已全部回写owning design。当前结论是在PRD声明边界内整体
设计可实现，不存在已知矛盾、冲突或缺漏。

该结论只覆盖设计，不代表实现、测试、业务 repository 安装或 production cutover已经完成。本 task继续
保持 `planning`，后续进入实现前仍需完成正式 Phase 1 planning artifacts 与 approval boundary。
