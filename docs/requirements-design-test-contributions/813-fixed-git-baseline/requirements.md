# #813 需求差额

来源为 Issue #813 与 Task 根 PRD R1—R6/AC1—AC5。适用 B 为 `5c6a4591db7165ece045e6b0eb789c21d06d7d38`。完整拟写位于 `proposed/docs/requirements/current/runtime-location.md`；本贡献不建立第二份 current。

本项修改原 R718-07—11，区分固定对象、Task integration branch 和 delivery target；保留 primary 旧 main/dirty，exact source/acquisition、仓库/common-dir、Task/generation/binding 与原 session 边界。恢复不重复创建。旧输入成套迁移与原完整 provider 恢复由 MIGRATION-813 单写。稳定 identity、R760/R769 和历史截止保留。AC6 合并后由原 Completion/Closure/Finish 负责，不以此贡献证明。
