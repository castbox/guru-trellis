# #547 Design 责任增量

前驱：RDT `.90` / D531-06/07 与 #436 D436-01..04/07/08；ADR-013/024 保留其 owner 与公共模型。此处只拥有职责映射；step-local行为唯一由 canonical Skill拥有，来源设计处置由 Task design 的唯一矩阵拥有。

| Responsibility | 唯一 owner / 实现落点 |
| --- | --- |
| D547-01 | 原 Task scope API 与 Completion；whole current accepted_scope，不改 source/generation |
| D547-02 | guru-complete-task-closure：retain_open、blocked 顺序、原事务恢复及 exact source 公共 fact |
| D547-03 | guru-finish-task：共享 snapshot 所需 OPEN/CLOSED 校验、原 archive/bookkeeping 三阶段与 Cleanup 分离 |
| D547-04 | Closure input + Finish snapshot schemas/interface/examples；原 refs/exits、不新增 DTO/store |
| D547-05 | task-delivery-migration 支持合同；匹配新安装与完整旧安装分开，无双 writer |

[canonical Closure](../../../trellis/skills/guru-team/packages/guru-complete-task-closure/SKILL.md) 与 [Finish](../../../trellis/skills/guru-team/packages/guru-finish-task/SKILL.md) 拥有动作执行和恢复合同。[迁移合同](../../../trellis/presets/guru-team/spec/workflow/task-delivery-migration.md) 拥有匹配采用边界。共享 reader已完整透传，无需扩展。

Architecture contribution/ADR 当前为 task-owned reviewed candidate；shared promotion 仍须首次 committed 独立完整 Review 后由原 owner执行，新增 promotion diff fresh gates。此 RDT reconciliation不替代 Architecture晋升或软件发布。
