# #309 Package-local Phase 2 Gitlink Content Identity

## Goal

修复 package-local `guru-check-task` 在仓库包含 Git mode `160000` Gitlink
时拒绝 Phase 2 content identity 的缺陷，使文档等不涉及 submodule 的任务
无需初始化 submodule 即可完成检查，同时继续对真实 Gitlink 漂移 fail closed。

## Background

- 当前缺陷位于
  `trellis/skills/guru-team/packages/guru-check-task/runtime/common.py:38-58`：
  `file_set()` 只接受 regular file 和 symlink，Gitlink 目录直接触发
  `Unsupported reviewed-content path type`。
- Issue #186/PR #190 已为旧 companion runtime 定义未初始化且未修改 Gitlink
  的回退语义；#195 package-local 迁移未承接该行为。
- Phase 2 使用私有短生命周期算法
  `guru-phase2-worktree-content-1.0`；它不同于 Branch Review、Publication、
  Finalizer、Verification 共享的 `guru-reviewed-content-1.0`。

## Requirements

### R1 Gitlink identity

- 未初始化、未修改且 index Gitlink OID 与 `HEAD:<path>` 一致时，使用
  superproject index 中的 mode `160000` 与 OID 生成稳定 identity。
- 已初始化 Gitlink 仅在 submodule root 精确、HEAD 可解析、worktree clean，
  且 submodule HEAD 等于 index OID 时被接受。
- Gitlink entry 必须以确定性 path/mode/OID 语义参与现有 Phase 2 digest。

### R2 Fail-closed states

以下状态必须拒绝并返回可定位的 `stale_identity`：dirty、submodule HEAD
drift、index/commit pointer drift、删除、替换为普通文件或目录、root mismatch、
unmerged/index ambiguity，以及无法唯一解析 Gitlink OID 的状态。

### R3 Compatibility and ownership

- 保留 `guru-phase2-worktree-content-1.0`：旧实现对 Gitlink 不产生任何合法
  digest，本次是对原先 unsupported atomic entry 的向后兼容扩展；普通文件、
  executable、symlink、missing 的 payload 和 digest 不变。
- 不把 Phase 2 identity 替换为 durable `guru-reviewed-content-1.0`，不扩大
  public DTO 或 checkpoint schema。
- `guru-create-task-commit` 继续拥有“待提交 Gitlink 必须 initialized + clean”
  的更严格 staging 合同；Phase 2 接受无关、未初始化 Gitlink，不削弱提交门禁。

## Acceptance Criteria

- AC1：真实 Git fixture 中，未初始化且未修改 Gitlink 可完成 source
  package-local Phase 2 record/check，identity 使用 index OID。
- AC2：initialized-clean Gitlink 通过；dirty、HEAD drift、pointer drift、
  deletion、replacement、root mismatch 分别失败。
- AC3：普通 file/symlink/missing identity 的既有结果保持稳定。
- AC4：`guru-check-task` 与 `guru-create-task-commit` 的分层合同通过测试，
  未初始化 Gitlink 不会被错误放宽为可提交 Gitlink。
- AC5：source package tests、installed package parity、preset reapply/drift、
  ownership 与相关 integration/eval 通过。

## Out Of Scope

- 不初始化、下载或更新业务仓库 submodule。
- 不修改 `guru-reviewed-content-1.0` 或四消费者共享 helper。
- 不新增 hostile-input、并发、锁、TOCTOU 或 crash consistency 机制。
- 不执行完整多平台 Release/Throwaway installer 矩阵；该矩阵仍由专门
  release/compatibility Issue 负责。
