# #427 修复正式发布 Finalizer 分段确认与原子事务合同冲突

## Goal

使仓库私有 `release-guru-trellis-version` 正式发布编排与 current
`guru-finalize-task` Happy Path 使用同一个可执行的确认模型：一次完整、精确的
Finalizer transaction preview/confirmation，随后由 Finalizer 原子执行；Merge 与发布后续
动作继续保持独立确认边界。

## Requirements

- 以 live Issue #427、#330、#335、#410、current `.trellis/workflow.md`、
  `guru-finalize-task` 和 `release-guru-trellis-version` 合同为 authority。
- 删除 release owner 对 Finalizer 内部 branch push、PR creation、archive/Ready
  三次中途暂停确认的要求，改为一次覆盖完整固定 transaction 的确认。
- 保留 Finalizer 与 Merge 的独立确认，不允许 Finalizer 确认授权 Merge。
- 保留 annotated tag、tag-pinned smoke、GitHub Release、release Issue closure 和
  cleanup 的独立确认边界。
- 不修改 Finalizer public schema、field、exit、consumer、transaction state 或 owner。
- 同步 Shared、Codex、Claude、Cursor 的仓库私有 Skill 投影和定向 regression。
- 不修改 #426 delivery bytes，不执行 #410 release mutation，不实现 #261/#398。

## Acceptance Criteria

- [ ] Canonical release contract 与 current Finalizer/workflow 对确认次数和 transaction
      边界一致。
- [ ] 定向测试证明 Finalizer 只要求一次 exact transaction confirmation，且 Merge、tag、
      smoke、Release、closure、cleanup 仍是独立边界。
- [ ] Shared/Codex/Claude/Cursor 投影字节一致。
- [ ] Source/installed validator、ownership、preset reapply、dogfood drift、focused tests、
      `git diff --check` 和 residue 检查通过。
- [ ] 不改变 Finalizer public I/O 或其它 delivery bytes。
- [ ] PR 使用中文 title/body，`Closes #427`、`Refs #410`，不声称 #410 已发布。

## Notes

- 本任务是阻断 #410 的窄范围流程合同修复。
- #427 合并后，#410 必须从新的 `origin/main` 冻结全新 candidate 并从零重跑 Stage 2。
