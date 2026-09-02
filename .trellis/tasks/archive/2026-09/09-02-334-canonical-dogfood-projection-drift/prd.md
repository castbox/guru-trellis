# PRD: 修复 canonical 与 dogfood 投影漂移

## 1. 背景

Issue #325 与 #327 已分别通过 PR #326、PR #328 合入 `main`，但当前
`main@c3003568dae6773378f0eca3cdb6c69fcc5cb232` 仍存在两处 canonical/dogfood
投影漂移。实现阶段的 fresh apply 与历史复核进一步明确了精确方向：

- canonical preset spec
  `trellis/presets/guru-team/spec/workflow/data-contracts.md` 缺少 #325 已在
  `.trellis/spec/workflow/data-contracts.md` 生效的 Finalizer provenance 合同；
- canonical `guru-finalize-task` package test 已同时包含 #325 provenance 断言与
  #327 workspace-boundary 回归；installed dogfood test 仍停留在 PR #326 的不完整
  投影，缺少 canonical 中的 #325 manifest-preservation 断言和 #327 回归。

installed test 当前 SHA-256 与 manifest 记录的 previous managed hash 不一致，
因此首次 all-platform apply 正确 fail closed，并保留 canonical 后像为相邻
`.new`，而不是静默覆盖。该 `.new` 与 canonical test 字节一致。问题不是需要把
installed 内容反向复制到 canonical，而是需要修复 canonical spec 后，对这一处
已确认的历史投影漂移执行受控 conflict resolution，再由 canonical apply 重建
manifest 与所有声明投影的一致状态。

## 2. 目标

- 将 #325 已合并的 Finalizer provenance 合同恢复到 canonical preset spec。
- 保持已完整承接 #325/#327 的 canonical `guru-finalize-task` test 不变，并将其
  作为 installed dogfood test 的唯一目标后像。
- 对首次 apply 产生的 test `.new` 做三方历史核对后，显式解决这一处
  `unknown_local_edit`；不静默覆盖其它未知 edit。
- 从 canonical source 执行 all-platform preset apply/reapply，使 canonical、
  dogfood、installed、Shared、Codex、Cursor、Claude 投影重新一致。
- 证明 ownership、package tests、platform parity、dogfood drift 与 recursive
  sidecar 检查通过。
- 保持 runtime 行为、public Skill interface、schema 与 workflow graph 不变。

## 3. 范围

### 3.1 In Scope

1. 以 live PR #326/#328、对应 merge commit 和当前 canonical/dogfood bytes 为
   事实证据，将 #325 spec 合同的最小差异补回 canonical source。
2. 保留首次 apply 的 fail-closed `.new`，证明其与 canonical test 字节一致且
   installed-only 差异均为遗漏/旧格式，不含需要反向保留的新语义。
3. 仅对该已审查 test conflict 执行显式替换并移除对应 `.new`，随后运行
   `apply.sh --repo . --all-platforms --json`，并再次运行证明 reapply 幂等。
3. 验证 canonical 与 installed `guru-finalize-task` tests 均包含并执行 #327
   回归。
4. 验证 source/installed package、upstream ownership、dogfood drift、声明平台
   字节一致性和 `.new`/`.bak` 数量为 0。
5. 保留 task planning、Issue Scope Ledger 和必要验证证据。

### 3.2 Out of Scope

- 不实现或修改 #333 的 Issue creation recovery/idempotency 行为。
- 不修改 Finalizer runtime、public interface、schema 或 workflow routing。
- 不创建 Release、不打 tag、不部署生产。
- 不执行或宣称完整 release-wide 多平台 Throwaway installer 矩阵。
- 不触碰、覆盖、stash、迁移或清理 #333 的 dirty worktree。

## 4. 验收标准

1. 两组受影响 canonical/dogfood 文件字节一致。
2. all-platform apply 后不会回退 #325/#327，第二次 reapply 为幂等结果。
3. canonical 与 installed `guru-finalize-task` contract tests 均通过，且 #325
   manifest-preservation 断言与 #327 的
   `test_workspace_boundary_does_not_rebuild_missing_runtime_mapping` 均在两侧存在
   并执行。
4. preset upstream ownership、source/installed validation、dogfood drift 和
   Shared/Codex/Cursor/Claude parity 通过。
5. 仓库递归扫描不存在未处理的 `.new` 或 `.bak`。
6. 最终 diff 不包含 #333 实现、runtime 行为、public interface、schema、Release
   或部署变更。

## 5. Docs SSOT Plan

- `docs_state`: current authority 已存在，无需 bootstrap 或 repair。
- `strategy`: `ssot_first`。
- `evidence_paths`:
  - `trellis/presets/guru-team/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py`
  - `.trellis/guru-team/skills/packages/guru-finalize-task/tests/test_contract.py`
- `durable_docs`: 先修复 canonical preset spec，再由 preset apply 更新
  `.trellis/spec/workflow/data-contracts.md`；不修改 repository RDT 或 Architecture
  authority，因为本任务不引入新需求、设计或架构语义。
- `task_artifact_deltas`: 仅本 task 的规划、执行和检查文件。
- `merge_checkpoint`: Phase 2 必须在最终 check 前完成 canonical 到 installed/
  platform 的投影并验证零 sidecar；Branch Review 只验证已完成的 reconciliation。
- `deferred_boundary`: 完整 release-wide 多平台 Throwaway 矩阵由专门 Release/
  compatibility Issue 拥有，本任务不执行。

## 6. 开放问题

无。Issue #334 与当前 repository evidence 已确定 source、投影方向、验证范围和
排除项。
