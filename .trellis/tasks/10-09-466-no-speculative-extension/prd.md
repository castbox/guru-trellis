# #466 需求规划

## 目标与 authority

Source：[Issue #466](https://github.com/castbox/guru-trellis/issues/466)，当前正文更新于 2026-10-09；该正文拥有本次范围与验收。TaskId：`466-no-speculative-extension`，generation：0。

本任务强化现有 `minimum-necessary-complexity` / 最小必要复杂度，使 Planning、设计、Phase 2 和 Branch Review 能区分当前必要能力与未来预留能力。原则正文与解释只由 `docs/architecture/00-foundation/design-constitution.md` 拥有；本规划通过 identity 与 Issue 条款引用，不建立第二份原则正文。

## 当前事实

- current Architecture 与 RDT 均为 `current-main-0.6.17-guru.76` / active；设计宪法为 `guru-trellis-design-constitution-v1` / current。
- 当前原则已有最小复杂度方向，但能力类型与 Requirement 自身投机内容的回程解释不完整。
- 已存在 Architecture conflict、机制修订、Scope Change 与 Planning revision 路径。#404 独立审查方法/调度范围独立，本任务不接管其实现。

## 需求与验收映射

| Task requirement | Source 条款与完成结果 |
| --- | --- |
| R466-01 | Issue 设计要求 1、2：唯一宪法 authority 补齐新增能力覆盖及当前必要性依据；“未来可能需要”、扩展灵活性与避免未来修改本身不形成当前义务。字段/DTO、状态/转换/枚举、API/exit/callback/plugin、配置/switch、存储/缓存/锁/双读写/compatibility、扩展容器、wrapper/抽象/通用机制全部覆盖。 |
| R466-02 | Issue 设计要求 1、3：删除判据覆盖全部当前适用合同及职责；必要职责隔离/可维护性抽象和真实兼容、迁移、安全、发布、平台及已批准分阶段交付被接受。真实兼容/迁移必须给出 owner、边界、当前依赖、验证及退出删除条件。 |
| R466-03 | Issue 设计要求 4：机制多余回设计/实现修订；Requirement 本身投机回现有需求/Planning 修订，取得新 current authority 后重审；缺必要性证据或有真实选择进入已有澄清/blocked，不自行删除 accepted scope 或以批准覆盖冲突。 |
| R466-04 | Issue Authority 与消费边界：只消费稳定 identity、适用结论和 evidence；不新增第六原则、机械评分器、关键词判定、逐字段持久化或公共 DTO。 |
| R466-05 | Issue 工作范围 4：完成六类正反例；测试既证明当前必要能力/必要抽象被接受，也证明未来预留及污染 Requirement 被正确修订；future candidate 留作 non-goal/unknown/limitation/follow-up，不进入当前合同。 |
| R466-06 | Issue 工作范围 1、5、6：task-isolated contribution、独立 Architecture review、expected-current promotion，以及 promotion 后 fresh Phase 2/commit/完整 Branch Review；canonical、dogfood 与适用安装投影一致。 |

上述每项以 live Issue 对应条款为判据。功能测试全绿、已有实现、既有批准或关键词命中均不单独证明语义充分性。

## 非目标与验证边界

不批量整改历史代码/Schema/配置/API，不删除无独立 Requirement 的现有兼容机制，不修改业务仓需求体系，不引入攻击模型、并发压力或异常 crash consistency。完整多平台 upgrade/Release matrix、真实业务仓安装和部署属于独立 owner，本任务不声称覆盖。

## Delivery policy

本次单个业务 Delivery 覆盖 R466-01..06 的完整增量；无计划拆分的剩余业务功能。候选必须包含原则增量、语义消费、六类示例、定向验证与已 promotion 的 current authority，且 promotion 后 gates 对当前候选重新通过，方具备独立交付条件。Delivery 使用 Refs #466；Completion/Closure/Finish 依现有独占 owner 承接。本轮仅完成 Planning，不启动实现或发布。
