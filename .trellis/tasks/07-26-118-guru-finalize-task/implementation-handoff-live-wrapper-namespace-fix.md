# Issue #118 live public wrapper Namespace 修复交接

## 触发证据

- 已确认的 closeout plan `closeout-plan:59ce5a04a6e9470d7d5e99ab76f8821af0b1ae8cc0448f0ded08b205021d88f6` 成功把 exact reviewed HEAD `d420a6842eca05bd0bf7472bdf06e3b519bace5f` push 到 `origin/feat/118-guru-finalize-task`，transaction state 进入 `content_pushed`。
- 随后真实执行 `.agents/skills/guru-finalize-task/scripts/invoke.sh` 时，`cmd_invoke_stage0_skill -> check_finalization_gate_result -> finalization_preview_context -> prepare_closeout` 访问 public parser `Namespace` 中不存在的 `finish_summary_index_file`，抛出 `AttributeError`，未产生合法 typed exit。
- 这是 honest normal path 上的 #118 current-scope correctness defect；当时未创建 Draft PR、未归档、未标记 Ready，也未修改任何 Issue 状态。

## 根因与实现

- `invoke-stage0-skill` 的 public parser 只拥有 public input 与 owner-result 参数，符合最小 public DTO 合同；finalization owner checker 却直接把该 Namespace 传给需要 private closeout 参数的 `prepare_closeout()`。
- 新增 `finalization_public_wrapper_checker_args()`：仅当 exact task-local `closeout-plan.json` 是安全 regular file 且通过 immutable plan validator 时，才从该 plan 与固定 task-local `finish-summary-index.json`、`pr-body.md` 重建 checker-private 参数。
- `cmd_invoke_stage0_skill` 使用上述 private Namespace 副本执行 owner checker；public CLI、public input schema 和跨 Skill DTO 均未增加 private 字段。
- 当 immutable plan 不存在时，helper 保持 private 参数为空，initial preview/recorder 仍必须显式接收 reviewed finish summary 与 PR body，不允许 public wrapper 猜测或绕过门禁。

## 修改文件

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`

## 实现代理验证

- Targeted re-entry：3 tests passed。
- `-k finalization`：13 tests passed。
- `-k wrapper`：7 tests passed。
- `guru-finalize-task` package contract：5 tests passed。
- canonical/dogfood runtime byte parity、三文件 `py_compile`、scoped `git diff --check` 通过。
- 修改后的 live 旧 gate 不再 traceback，而是返回结构化 `owner_result_not_checked`；direct checker 证明原因是本轮 source drift 使旧 `d420` plan identity、current facts 与 route `plan_ref` stale。实现未为旧 gate 放宽 freshness。

## Docs SSOT 与范围

- 继续采用批准的 `ssot_first` strategy。
- Durable inputs：`.trellis/spec/workflow/data-contracts.md`、`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/workflow/skill-package-contract.md` 与 `guru-finalize-task` package contract 已定义 owner-private plan/recovery 与真实 public wrapper 行为。
- 本补丁只修复实现偏离，未改变 public I/O、transaction order、recovery semantics、workflow route、preset/overlay、安装清单或平台分发，因此 `no_docs_update_needed`。
- 本文件仅保留 failure、修复与验证历史，不承担 durable contract。
- 只关闭 #118；#115 继续 related，#119/#132 继续 follow-up，#105 transaction semantics 不变。

## 后续门禁

- 必须由未参与实现的独立 `trellis-check` agent 完整复核当前 scope、runtime 全量、#105 transaction matrix、Skill/package/eval、canonical/dogfood parity、clean throwaway 安装/update/reapply 与 live-wrapper normal path。
- Fresh Phase 2、task commit、独立 Branch Review、publication review 和新 immutable plan/digest confirmation 必须全部重做。
- 旧 plan `59ce5a04...` 与旧 finalization gate 不得恢复执行；远端 feature branch 当前仍是 `d420a684...`，PR 不存在。
