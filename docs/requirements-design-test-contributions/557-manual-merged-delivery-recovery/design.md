# #557 Design 增量

状态：reviewed_promoted；来源处置与权衡保留于
[不可变 task design](https://github.com/castbox/guru-trellis/blob/6bba4880362a2e0ff31b535809e4895b7fa1a84d/.trellis/tasks/10-15-557-manual-merged-delivery-recovery/design.md)。
行为 SSOT 是 canonical Merge/Completion Skill 与 workflow；本文仅拥有责任追踪。

| Responsibility | Owner and implementation |
| --- | --- |
| DES-557-01 terminal attribution | 原 [Merge contract](../../../trellis/skills/guru-team/packages/guru-merge-task-delivery/references/contract.md#manual-merged-recovery)，runtime/manual_recovery.py，独立 input/review1.0；唯一公开 Publication 与实际 repo/PR/head/merge/parents/base。 |
| DES-557-02 actual candidate and truth | 同 owner 的 immutable Git snapshot/public hash 与完整差额；原 [Completion](../../../trellis/skills/guru-team/packages/guru-review-task-completion/SKILL.md) 单写 whole-scope 结论。旧 gate/Publication 不追认 actual head。 |
| DES-557-03 public history and recovery | 原 Merge/runtime/history.py，明确 query2；existing exact DeliveryFact 只读恢复。没有 importer、第二 writer 或 ledger。 |
| DES-557-04 distribution and compatibility | [MIGRATION-557](../../../trellis/presets/guru-team/MIGRATION-557.md)、原 workflow 与 preset；aggregate2、新 profile/query2 成套采用。query1 具名旧消费者及退出归原 Merge，支持不扩张。 |

Architecture .90 的[已晋升贡献](../../architecture/contributions/557-manual-merged-delivery-recovery.md)与 ADR-026 承接责任；RDT .96 将本增量纳入 current，immutable .89/.95 由历史保留。晋升新差额重新进入必要 gates，不复用晋升前审查作为 Publication 证明。
