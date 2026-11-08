# #752 支持 Plan2 保留 current-schema Task worktree 副本

## 1. 来源与术语

Direct Source 为 https://github.com/castbox/guru-trellis/issues/752 完整正文。该来源定义整体要求和验收，未预定 Plan2 wire schema。现有合同为 `trellis/skills/guru-team/packages/guru-upgrade-installation/references/delivery-migration.md`，拥有完整 inventory、原 binding、公共/私有 owner、恢复及 rollback 边界。工程约束来自 `AGENTS.md` 第2、2.1、6、7节。

current-schema 指 Task schema 2.0。authority 指原 branch binding 与 live registered checkout 对应的唯一当前 Task 执行来源。副本指正常 Git checkout 继承的同 Task 非权威记录，保留业务内容但不产生第二套 lifecycle、Delivery、session selection 或 private migration authority。

## 2. 背景与问题

后续 Git worktree 能继承已提交的 current Task，完整迁移 inventory 因而包含同 Task 的多个记录。当前固定 Fork `ca0e8b931d19ccb87802d6866abd2113a6f707c0`、CLI/Core `0.7.0-castbox.6` 的 migration2.ts defer 分支只调用 predecessor 校验，重复 active group 则要求唯一 current/convert_active。缺少 current peer 保留语义，阻塞合法 topology 的 preview。Guru 已提供原 binding 和完整 inventory，不应复制上游 group 判定。

## 3. 目标与非目标

通过匹配的 Guru 与 Fork successor source pair 完成 current-schema 多 worktree 副本迁移。整体完成覆盖下述五项要求及实际 installed 验证，单次 Delivery 合并不能代替 Task Completion。

不改写、合并、删除或重建用户 Task、binding、session、Delivery、archive。不忽略 registered worktree，不把 current record 伪装成 legacy。不 patch installed CLI、node_modules 或不可变 release tag。不扩展攻击模型、并发压力、锁或 crash 加固。不发布 Guru tag/npm release。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置和触发 | 处理与可观察结果 |
| --- | --- | --- |
| S1 正常副本 | Upgrade owner 盘点多个 registered roots，同 Task 有唯一原 binding checkout，提交 Plan2 | preview 唯一 authority；迁移保留 peer 原内容、业务元数据与 modes，不产生额外 lifecycle/Delivery/selection/private conversion |
| S2 不一致 | 普通内容、generation、source、binding、checkout mismatch 或 authority 歧义；调用 preview | 阻塞且原 Task/session 不变，不静默合并或丢弃 |
| S3 恢复 | 正常暂停后原 Upgrade owner 消费同一冻结计划 resume | 不换包、不刷新 rollback anchors；Task/session 及 peer 继续保留 |
| S4 回滚 | 原 owner 审查当前状态符合 rollback 条件并执行 | 恢复原 bytes/modes，移除本次新增资产；不 reset Git 或修改远端 |
| S5 实际采用 | 完整匹配 successor source pair，在多 worktree 代表性安装升级 | installed runtime 识别唯一 authority，peer 不进入 selection、Delivery 或 private conversion |

## 5. 行为要求

- R1：纳入全部 eligible registered worktrees，按原 branch binding 和 live checkout 唯一选择 authority。
- R2：合法 current-schema peer 及业务元数据原样保留，不进入 lifecycle、session selection、Delivery 或 private-owner migration。
- R3：Task 内容、generation、source、binding、checkout 不一致或 authority 非唯一时，preview 阻塞；不静默合并、丢弃或修复原记录。
- R4：多 workspace current copies 覆盖 Plan2 dry-run、迁移、同计划 resume、rollback，独立断言 Task/session 保留或恢复。
- R5：Guru projection、Fork CLI/Core schema/executor 和 source lock 使用同一兼容语义；实际安装采用完整匹配 pair，并验证 installed runtime。

## 6. 约束与依赖

Fork 独占公共 Task/session/schema/group 与 Plan2 executor；Guru 原 Upgrade owner 拥有安装、私有迁移编排及恢复。私有 owner 只消费其 workspace 中被投影的 Task。AI 判断 disposition、充分性和 route，脚本只执行和校验事实。

需要演进独立 Fork 源码并取得可固定 successor commit。canonical、dogfood、installed 和声明平台投影沿原安装 owner 同步；用户修改与 .new/.bak 按原机制处理。完整多平台 Release 矩阵由独立 owner 承担，本 Task 验证 current-copy 专项与代表性多 workspace 安装。wire schema 交原 Author/Architecture 设计。

## 7. 可观察验收与验证方式

- AC1（R1/S1）：公共 Plan2 preview 输入正常形成的多 worktree current copies 与原 binding，全部 roots 在 inventory，只有一个 authority。
- AC2（R2/S1/S5）：migrate 和 installed public query 验证 peer bytes、metadata、modes 保留，且无 peer lifecycle/selection/Delivery/private migration authority。
- AC3（R3/S2）：普通内容、generation、source、binding、checkout mismatch 和歧义测试，preview 阻塞且原 Task/session 不变。
- AC4（R4/S3/S4）：同冻结计划 dry-run、执行、resume、rollback，Task/session 保留或恢复，不生成 peer Delivery 或 private conversion。
- AC5（R5/S5）：matching source lock、单元/集成和代表性多 workspace 升级；实际 installed runtime、canonical/dogfood/平台、drift/sidecar 检查通过。

测试从要求导出独立断言，不以 fixture 自证或固定版本字符串代替实际迁移。源码、集成、实际安装和完整 Release 矩阵分别报告，此处不预填通过。

## 8. 实际未决项

没有待解需求选择。wire schema、算法细节和 successor 版本由 Delivery Author/Architecture 规划。实际迁移、恢复、rollback 和 installed 结果尚待实施验证。
