# #250 设计增量

| Design identity | 唯一 owner / locator |
| --- | --- |
| D250-01 profiles/source choices | [Clarify contract](../../../trellis/skills/guru-team/packages/guru-clarify-requirements/references/contract.md)、独立 profile schemas 和 [迁移合同](../../../trellis/skills/guru-team/packages/guru-clarify-requirements/references/MIGRATION-250.md)。 |
| D250-02 caller-aware context return | [Discovery contract](../../../trellis/skills/guru-team/packages/guru-discover-change-context/references/contract.md)；四分支 return_identity，公有输出薄投影；private owner 不跨 consumer。 |
| D250-03 controlled relay | current stage0 transition schemas、Wording/readiness interfaces；Interface 1.8 仅以 producer 的 handoff_profile 选择已声明输入，无表达式或新路由 owner。 |
| D250-04 owner/Planning/resume | [canonical workflow](../../../trellis/workflows/guru-team/workflow.md)；保留初始 Sync→Discovery→Clarify，task-created 身份 DTO 不变，来源丢失回原 Clarify。 |
| D250-05 distribution | canonical preset apply 与 current platform projections；上游 start/continue/brainstorm 保持 upstream ownership。 |

没有新 Skill、cache、ledger、授权记录、task.json 来源模型、未来 #292 前置或上游 patch。所有 semantic 充分性、来源和取舍仍由 AI；脚本仅校验合法输入/身份/薄 projection。Architecture 独立候选由 manifest 所列原 owner 维护，不在此复制其判定。结果只在 [test](test.md)。
