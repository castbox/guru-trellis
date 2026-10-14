# #557 Requirements 增量

状态：reviewed_promoted；RDT .96 继承 immutable .95 与 Architecture .90。
规范来源是 [#557](https://github.com/castbox/guru-trellis/issues/557) 的目标、
合并事实/验证责任与验收1..9；没有额外 scope。
task-local R557-01..09 对应
[规划来源快照](https://github.com/castbox/guru-trellis/blob/6bba4880362a2e0ff31b535809e4895b7fa1a84d/.trellis/tasks/10-15-557-manual-merged-delivery-recovery/prd.md)，
来源承诺处置保留在同一提交的 task design 快照，当前产品责任由本贡献 design.md 与 canonical 合同承接。

| Behavior identity | Source | Responsibility |
| --- | --- | --- |
| BEH-557-01 | 验收1/2，R557-01/02 | 原 Merge 基于已有唯一公开关联承接真实手动终态；不依赖消息/gate，不执行第二次 merge。 |
| BEH-557-02 | 验收3/4，R557-03/04/05 | 合入事实、实际候选、原 gate 与真实 CI 分离；原 Completion 保留整体范围与证据判断。 |
| BEH-557-03 | 验收5/6，R557-06/07 | 输出丢失、base推进、branch删除不丢失已记录事实；只读 history 排除 bookkeeping。 |
| BEH-557-04 | 验收7/8/9，R557-08/09 | 既有 expected-head/schema1/2 与旧输出恢复保持；明确版本/成套迁移，验证层分列。 |

本候选选定普通 two-parent merge；squash/rebase 未支持。只做 Guru #557，
不承担原业务 Task/PR、安装采用、业务联合验收或完整 Release 矩阵。
