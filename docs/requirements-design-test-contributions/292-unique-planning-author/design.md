# #292 设计增量

| Design identity | 唯一 owner / locator |
| --- | --- |
| D292-AUTHOR | [Author 合同](../../../trellis/skills/guru-team/packages/guru-author-task-plan/references/authoring.md) 与八 profile schemas；runtime 只检查，不写业务规划。 |
| D292-SOURCE | TaskId `292-unique-planning-author` / generation `0`，planning document `design.md#D2`：来源承诺处置的唯一矩阵。 |
| D292-ARCHITECTURE | [Architecture contract](../../../trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md)：planning 3.0 两 purposes，非 planning 2.0 保留。 |
| D292-CONSUMERS | [canonical workflow](../../../trellis/workflows/guru-team/workflow.md)：Author mandatory invocation、薄 router、Wording/final/Approval 邻接与原执行回程。 |
| D292-QUALIFICATION | 三个原 qualifier 的 author_candidate_set；原 Approval/incident 因果 owners 不变。 |
| D292-DISTRIBUTION | [迁移合同](../../../trellis/presets/guru-team/MIGRATION-292.md)、canonical preset/apply、registry/manifest5 与平台投影。 |

Architecture 来源方案定位为同一 TaskId/gen0 的 planning document `design.md#D9/#D10`；当前公开决定由 [Architecture `.85`](../../architecture/README.md) 与其 durable contribution/ADR拥有，本文件不复制矩阵或独立评估。RDT 按不可变 `.87` 晋升至 `.88`；promotion 差异仍须原owners fresh gates，旧shared authority保持历史语义，不由晋升推定Delivery或Release。
