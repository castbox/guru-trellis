# #290 Design contribution

## Two-stage resolver

- `D290-01`：`select_base` 只读取 caller explicit value、repo config、exact local/remote
  refs 与 remote default，返回 source/base/remote/ordered candidates；该阶段不读取
  current branch 或 worktree inventory。
- `D290-02`：`authority_checkout` 在 selection 后解析
  `git worktree list --porcelain -z`。NUL field 与空 NUL record separator 分开处理，
  只接受 branch field exact 等于 `refs/heads/<selected_base>` 的唯一 record。
- `D290-03`：binding 复核 candidate exact toplevel、same common-dir、symbolic branch、
  registered HEAD、live HEAD/local ref 与 clean state；所有正常 mismatch 使用稳定
  owner error，由 public wrapper 投影 `blocked`。

## Execution and validation

- `D290-04`：resolve-only 的既有 `decision_checkout` 语义为 authority branch/head；
  authority path 只在 invocation 内由 shared binder 重建，不加入 result schema或 digest。
- `D290-05`：execute 在 authority cwd explicit fetch；local==remote 时不 merge，local
  是 remote ancestor 时执行 `merge --ff-only`，diverged/remote-behind 时 blocked。
- `D290-06`：checker 从 schema-valid result 的 selected base 复用 binder，重算 pre/post
  resolution 与 facts digest，验证 exact refs、fast-forward flag、clean 和
  `authority HEAD == local ref == remote ref`。内部返回 authority locator 给 invoke。
- `D290-07`：invoke 仅把 checker-passed locator 写入既有
  `handoff_repo_locator` / `transition.repo_locator`；其他 public shape 与 consumer 不变。
- `D290-08`：下游 `guru-create-task-workspace.reviewed_base_freshness` 按 provenance
  `source` 对 explicit/config/config-candidate/remote-default 四级 live authority 做
  package-local revalidation；source、selected base 与完整 candidates 必须 exact 匹配
  transition provenance。`prepare()` 只消费通过 freshness gate 的 selected base/candidates，
  不在 gate 前执行 config-only resolution，也不导入 producer private runtime。

## Distribution and ownership

Producer canonical owner 是 `trellis/skills/guru-team/packages/guru-sync-base/`；受影响的
freshness consumer owner 是 `guru-create-task-workspace/runtime/prepare.py`。preset apply 只
生成 `.trellis/guru-team` 与 Shared/Codex/Claude/Cursor managed projections及
`extension.json` inventory/hash；schema、Interface、README 和 shared current Docs 不变。
Architecture target-native 边界与 ADR-006 仍由 task-owned candidate 承载。
