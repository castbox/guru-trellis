# #495 最终验收设计增量

状态：隔离 successor candidate。继承 [`.72` Design](../../design/versions/current-main-0.6.17-guru.72/design-main.md) 的 `D495-INVENTORY/CORE/MIXED/GURU/LIFECYCLE/RECOVERY/DISTRIBUTION` 与 [ADR-017](../../architecture/adr/017-legacy-installation-upgrade.md)；不新增生产 writer、公共 Skill/API 或恢复 authority。

`D495-INVENTORY / D495-LIFECYCLE` 的验收样本：固定旧 source 的正式 native creator、branch/context/start 写出合法旧任务。旧 builder、recorder/checker、serializer/schema、transaction writer/executor、正式 archive 和本地 Git commit/push 实际执行。writer observer 先调用原 writer，再复制首次 `push_content` 非 terminal 状态；原执行正常结束并删除 terminal owner state。旧 canonical test 已有 provider/runtime doubles 明确列入构造证据，不能提升为 live provenance。

快照复制到独立 repo/bare 后，仅将复制 Git origin 指向复制 bare；旧任务、plan/gate/transaction 不改。新 source-loaded `guru-upgrade-installation` 使用 `source_locked`、同一远端 Guru provider 与正式 Fork，明确 deferred 该旧任务、保留旧事务。新 current-only identity owner 直接选择旧任务返回 `unsupported_legacy_task`，无关新任务可由 native current creator 创建并解析。旧 gate 不参与当前 lifecycle。

旧 PR 分别核对远端 head、branch、base 与旧 task：`pr_url=null` 不证明未发布，旧 base 不成为 live base authority；merged PR 没有确认 TaskRef 时不构造 MergeResult/Completion。current identity、branch、checkout、session 与 Planning/dev/check 接续仍由既有七场景证明。

恢复复用现有同 owner public resume；首次失败结果保留。rollback 沿既有固定 task-content/control 基线保护升级后新工作，不重取新 bytes 作可覆盖基线。生产机制与已验证 `6a563f5f` 完全相同，本轮只补验收与文档；后继 Git HEAD 的验证等价性须按实际 canonical diff 审查，不自动继承 exact HEAD 声明。
