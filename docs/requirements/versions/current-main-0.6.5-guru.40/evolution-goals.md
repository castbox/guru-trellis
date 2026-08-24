# Guru Trellis Evolution Goals

版本：`current-main-0.6.5-guru.40`；状态：`accepted_target`；确认日期：
`2026-08-24`。

## Authority 与消费规则

本文件是 Guru Trellis 下一阶段产品进化目标的唯一语义 SSOT。它定义最终要
交付的产品结果，不声明 current runtime 已经实现、验证或发布这些结果，也不
授权任何具体 Issue、task、分支、PR、cutover 或 Release。

- 后续重构 Issue、Trellis planning、Architecture contribution、Branch Review 和
  exact-candidate Release 必须引用本文件 locator 及适用的 `EVO-*` identity。
- 下游文档只记录 goal identity、覆盖关系、具体 delta 和验收证据，不复制本文件
  正文，不建立第二份目标清单。
- 每个重构计划必须说明覆盖哪些 goal、哪些 goal 明确不受影响，以及如何证明未
  造成目标倒退。无法建立该映射时不得声称计划完整。
- current 实现事实继续由 canonical workflow、Skill package、Git/live facts 和
  current Requirements/Design/Test/Architecture authority 提供；本文件不能被用来
  把 target direction 冒充为 current behavior。
- 修改、删除、合并或弱化任一 `EVO-*` goal，必须先取得新的明确产品决定并更新
  本 SSOT；Issue body、历史会话或实现便利不能静默改变目标。

## 北极星

> 把 Guru Trellis 进化成一个由 current authority 驱动、Architecture Baseline
> 全程治理、AI semantic owner 闭环执行、低交接低上下文成本，并能从需求进入
> 一直可靠完成到交付清理的工程工作流。

## `EVO-001` 需求与既有设计被准确理解

- GitHub Issue 可以同时承载需求、约束和已经审阅的设计。
- Phase 0 无损形成 requirement authority 和 reviewed-design commitments。
- 信息充分时零提问；信息不充分时，每轮只询问一个最高价值问题。
- `prd.md` 始终忠实表达产品意图，不能为了适应 current Architecture 而静默
  修改、弱化或反转需求。

## `EVO-002` Architecture Baseline 成为设计与演进过程的一部分

- 第一次实质编写 `design.md` 前，必须读取 current Architecture Baseline、设计
  宪法和 Architecture change contract。
- `design.md` 是 Architecture alignment 的主要载体，不在三份 planning 文档中
  重复复制 baseline 正文。
- current baseline 能够正常承接的需求直接对齐；requirement 与 baseline 冲突时
  保留产品意图并显式决策。
- baseline 不足时形成 task-local Architecture contribution 或 ADR candidate；
  Planning 不直接修改 shared current authority。
- shared Architecture 演进继续经过独立 review、serialized promotion、fresh
  Phase 2、Task Commit 和 committed full-diff Branch Review。

## `EVO-003` 从流程 artifact 驱动进化为 current authority 驱动

- shared Architecture、Requirements、Design、Test 和 Docs SSOT 是持久 authority。
- Trellis task 文档、Git、GitHub 和 Trellis live facts 提供任务当前状态。
- 不依赖 Issue Scope Ledger、跨阶段 aggregate、共享 handoff、历史 checkpoint 或
  重复摘要推导 current facts。
- authority、identity 或 scope 变化时，最早受影响结果立即失效并返回正确 owner。

## `EVO-004` 每项语义判断只有一个 owner

- Phase 0、Workspace、Planning Author、Architecture、Approval、Implementation、
  Check、Branch Review、Publication、Acceptance、Delivery、Merge、Finish 和
  Cleanup 的语义边界清晰且无重复 owner。
- AI 负责意图、充分性、冲突、finding、revision 和 route 判断。
- Python/shell 只执行、记录或校验确定性事实。
- 不存在双 writer、只做转发的 wrapper Skill、重复 reviewer，或要求 consumer
  读取 producer-private result 的反向依赖。

## `EVO-005` 正常工作流显著更短、更快、更安静

- 不制造 planning handoff、Architecture report、Issue ledger、共享 cache、第二
  capsule 或没有直接 consumer 的 gate artifact。
- public DTO 只传递下一 owner 无法从 current authority 重新获得的最小事实；
  private evidence 被 consumer 使用后立即卸载。
- context compression 只保留最小 continuation；没有真实选择时不提问。
- 不增加额外 wrapper、routine question 或重复 semantic gate。
- 相对 current baseline，整体 model/tool rounds、重复读取量、context compression
  和 wall-clock 必须有可复现的实质改善，而不是只证明没有明显变慢。

## `EVO-006` 从请求进入到资源清理形成完整闭环

目标生命周期是：

~~~text
需求进入
-> Phase 0 requirement authority
-> Workspace / official task
-> Architecture-aware Planning
-> Implementation / Check / Task Commit
-> committed full-diff Branch Review
-> 必要时 Architecture promotion
-> Publication Review / pre-delivery Acceptance
-> Delivery / Merge
-> deterministic Finish
-> owned-resource Cleanup
-> workflow normal completion
~~~

每种支持的 normal、revision、refresh、recovery、blocked、no-Issue、`github_pr` 和
`none` 路径必须有唯一回程或终点，不依赖 Agent 猜测下一步，也不在远程不可逆
副作用后重新进入产品需求、Planning 或实现修订。

## `EVO-007` 所有交付形态保持同一能力

- Shared、Codex、Claude 和 Cursor 使用同一 semantic contract。
- canonical、dogfood、installed、preset、apply/reapply/update 不发生未审查漂移。
- official Trellis upgrade/update 后，Guru Team 能通过官方扩展面恢复完整能力。
- exact-candidate Release 证明完整业务 runtime、Architecture lifecycle、性能、
  platform/install/update matrix 和 post-publish smoke，而不是把若干局部验证相加
  后冒充全链通过。

## 最终用户结果

> 用户给出一个新需求或已审阅设计后，Guru Trellis 能用最少必要交互理解它，
> 在写设计前真正消费现有架构，必要时提出受治理的架构演进建议，只写一次权威
> planning 文档，然后沿清晰的 owner 链完成实现、审查、交付与清理；全程不依赖
> 冗余交接文件，也不会在阶段之间丢失语义。

## 整体完成口径

Guru Trellis 的本轮进化只有在同一个 exact candidate 上对 `EVO-001..007` 全部
建立 current、可复现、无互相矛盾的端到端证据后才算完成。单个 Skill、单个
Issue、静态 schema、历史运行或局部平台通过，只能证明对应局部结果，不能替代
整体完成。
