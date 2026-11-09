# worktree 配置路径设计贡献

Status：promoted。完整目标为 [runtime-location](proposed/docs/design/current/runtime-location.md)，
保留 `RDT-DES-RUNTIME-LOCATION` 和 D718 合同，追加 D760-01—03。
Architecture 继承 `guru-trellis-architecture` / constitution v1 / ADR-RUNTIME-LOCATION；
本Task Architecture完整拟写由原 owner 单写于 `docs/architecture/contributions/760-worktree-config-path/`。

共享确定性事实只负责 topology/config/path；create-task 原 acquisition 与 task-free 普通 Git
各自消费。AI 保留策略、命名、冲突处置及精确副作用审查，未增加机制或授权记录。
当前基线与完整 proposed 交给独立 Architecture/候选 Check；candidate Check 后原 RDT owner
重读真实目标，final_integration整合与回读，implementation重绑实际 after 再进入最终质量链。
提案中的相对链接按真实目标目录解释；未改变共享根/索引或其它 Task 贡献。

原 RDT owner在实际 candidate_checked 后重读真实目标、整合并写回/读回。定义修订为
`worktree-config-path-760`；实际 current 完整单元：[runtime-location](../../design/current/runtime-location.md)。
本贡献保留来源，不替代普通查询的 current 正文；最终实际候选重绑与质量链由原 owners 承接。
