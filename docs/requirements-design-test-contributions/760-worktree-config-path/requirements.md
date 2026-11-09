# worktree 配置路径需求贡献

Status：promoted。适用来源为 Issue #760 完整正文、
已激活 D1 PRD/design，固定基线 `8c158381b5bdb61fd961cbb89e23c2d1f659c9aa`。
完整目标为 [runtime-location](proposed/docs/requirements/current/runtime-location.md)，
保留 `RDT-REQ-RUNTIME-LOCATION` 和 R718 行为，追加 R760-01—05。
这是同一能力的完整定义整合，不建立 Issue-specific current 或共享索引。

变更只补新建位置的配置承接、真实显式位置与采用/恢复分流、原 owner 执行和迁移。
不改变独立 runtime/Task/branch/worktree 身份，不接管业务恢复、Codex 清理或完整 Release。

原 RDT owner在实际 candidate_checked 后重读真实目标、整合并写回/读回。定义修订为
`worktree-config-path-760`；实际 current 完整单元：[runtime-location](../../requirements/current/runtime-location.md)。
本贡献保留来源，不替代普通查询的 current 正文；最终实际候选重绑与质量链由原 owners 承接。
