# #794 Design 贡献

状态：proposed，未晋升。完整结果定义在 [生命周期设计](proposed/docs/design/current/task-delivery-lifecycle.md) 与 [知识维护设计](proposed/docs/design/current/knowledge-maintenance.md)，精确公共 shape/argv 由当前 canonical packages 单写。

原 guru-review-branch 同时承接 check/full_review 语义角色，一次独立完整审查后分别记录真实充分性和完整覆盖。TaskCommit 新 pre-review profiles 保原 exact executor/hook、路径边界及同提交恢复，去除 Check 前置，只交固定候选 Review。原 Reconcile 判断实际 Task/base 归属、冲突和集成影响，caller 不缩固定 B..H；工程事实和原覆盖按适用性采用，真正缺口补足。

原 RDT impact/promotion3.0 与 Architecture 非 Planning6.0/Delivery4.0 成套切换。RDT candidate_ready定位完整拟写；原promotion实际写入/readback才ssot_current，输出不表示独立质量通过。Architecture final_integration 以批准 Planning、完整实施、真实工程和完整 targets整合，只返回 integrated_pending_review；before_authority/candidate 直接由原router交 implementation/Review以保持原比较来源和真实after，不交TaskCommit private状态。TaskCommit纳入after；同一次新独立Review真实判断committed before/after后才reviewed_promoted。Publication/Finish eligibility仅接受no_change或reviewed_promoted。

expected-current、逐 target before/content、完整组合语义、实际readback、普通partial及output-loss同intent恢复仍归各原 maintenance owner。R710 authoring/完整结果消费/恢复保留正常入口分工，R711完整单元与局部导航不变；退出重复阶段不删除真实恢复责任。旧 provider 只按实际旧阶段/已发生动作及MIGRATION-794处理，pending远端动作回当前独立审核/readiness；无双parser、第二quality状态或授权持久化。

Architecture 正文、必要 ADR 和九 concerns由原Architecture owner在其隔离贡献/完整targets中单写。本三层贡献不写架构结论，不替代Planning或实施独立Architecture pass。
