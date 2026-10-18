# 追踪

| 行为 | 设计 | Test | 主要实现 |
| --- | --- | --- | --- |
| BEH567-01 | DES567-01 | T567-01/03/07 | runtime/delivery_projection；Author；Check/TaskCommit/Review；implementation/eval consumers |
| BEH567-02 | DES567-02/06 | T567-02/04/05/07 | workflow；Reconcile；TaskCommit；Review；Merge；Finish |
| BEH567-03 | DES567-03 | T567-06/07/08 | Approval/Architecture/RDT原owner合同与workflow |
| BEH567-04 | DES567-04 | T567-02/04/07 | Reconcile executor/common；Merge资格与实际操作 |
| BEH567-05 | DES567-05 | T567-01/02/03/07 | 原Check/Review/Readiness/Merge rework；resolved projection |
| BEH567-06 | DES567-07 | T567-07/08 | Completion bounded history与Finish |
| BEH567-07 | DES567-06/07/CON567-01 | T567-04/05/06/08 | MIGRATION-567；Interfaces/schema/examples；preset shared specs/README |

package路径均相对trellis/skills/guru-team；workflow相对trellis/workflows/guru-team；preset相对trellis/presets/guru-team。Test是实际结果与未验证边界唯一正文。
