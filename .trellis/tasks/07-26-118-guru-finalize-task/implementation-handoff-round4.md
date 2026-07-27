# Issue #118 Branch Review Finding 修复交接（Round 4）

## 1. 结论

本轮已实现 open P1 `F-FINAL-LEGACY-01` 的 Phase 2 修复：
`guru-finalize-task` 现在可对现有 #105 engine 合法持久化的同月 partial
`closeout-plan.json` 执行一次、plan-bound 的 private gate takeover。Generic #105
仍拒绝该 gate 及其它未声明 artifact。另已同步 #118 激活 finalizer 后遗漏的 ownership
stable-facts acceptance assertion。未运行 Phase 2 recorder/checker、Branch Review
recorder、commit、push、PR、archive、finish-work 或 GitHub mutation；下一步交给独立
`trellis-check`。

## 2. 实现与设计承接

- 新增独立 `build_closeout_finalizer_gate_takeover_plan()` 与
  `closeout_finalizer_gate_takeover_errors()`，不复用 cross-month supersession。
- takeover 只接受：finalizer mode、同 archive month、旧 plan 尚未拥有
  `task-finalization-gate.json`、合法 pre-draft predecessor state，以及除 exact gate 外
  没有其它新增 task artifact。
- augmented candidate 精确补齐 `move_paths`、`untracked_archive_outputs`、archive
  `metadata_allowlist`、summary artifacts/changed/search paths；committed predecessor 另绑定
  exact evidence parent HEAD 与最小 plan/readiness evidence tail。
- Preview、semantic recorder、checker 与 verification-required transition 均不改旧 plan
  bytes；human confirmation 和 private gate 绑定 augmented candidate digest。
- Formal transition 重新检查 predecessor plan bytes/state、同月、commit state、exact
  task-local gate 与 augmented plan，再一次性替换 plan/readiness。迁移成功后不再进入
  takeover 分支。
- 未增加 public DTO/interface migration field；cross-month reprepare 仍由原独立机制拥有。

## 3. 本轮实现文件

- Canonical runtime：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
- Dogfood runtime：
  `.trellis/guru-team/scripts/python/guru_team_trellis.py`，与 canonical byte-identical、执行位一致。
- Runtime regressions：
  `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`。
- Ownership acceptance regression：
  `trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`，只同步 canonical
  validator 已发布的 stable counts 与 facts digest。
- Task-local history：本文件。既有 `agent-assignment.json`、
  `task-commit-plans/001.json` 与 `review-gate.json` / `review.md` / `reviews/**` 未由本实现轮
  改写或清理。

## 4. Docs SSOT Plan

批准策略为 `ssot_first`。主要实现输入是现有 durable finalizer contracts：
`.trellis/spec/workflow/skill-package-contract.md`、`workflow-contract.md`、
`companion-scripts.md` 与 `quality-guidelines.md`；task `prd.md` / `design.md` /
`implement.md` 和 `F-FINAL-LEGACY-01` 是具体 delta 与历史证据。

本轮结论为 `no_docs_update_needed`。Durable docs 已要求 #105 为唯一 deterministic
transaction engine、standalone/same-plan partial recovery、显式 finalizer-only private gate
ownership、generic checker strictness 与 extra-path fail-closed；实现现在满足该合同，没有
改变 public I/O、global Finish route、安装 inventory 或 docs 导航状态。README、durable
spec、canonical/dogfood workflow、upstream `trellis-finish-work` assets、preset overlays 与
official `.trellis/scripts/task.py` 均保持无 diff。Takeover 的 finding、实现细节、验证和
已知基线缺口只保留在 task history。

## 5. 验证

- Focused takeover regressions：4 passed。
- `CloseoutTransactionContractTest`：93 passed。
- Canonical runtime full：615 passed，13 skipped，exit 0。
- Skill package full：178 passed，exit 0。
- Preset installer full：45 passed，exit 0。
- Finalizer package：4 passed，exit 0。
- Source/installed package validation：均 passed；13 active、0 planned、0 legacy，installed
  2644 managed files、0 removal/conflict/sidecar。
- Dogfood overlay drift、upstream ownership validator、Python compile、`git diff --check`、
  task validation、canonical/dogfood byte identity：均 exit 0。
- Ownership regression：9 passed，exit 0；stable facts 为 active/planned/managed
  `13/0/58`，`facts_sha256=b99e67e59cb2e14679917bd31494f5ed32a87c72425f65b4fa41bd27470fc072`。
- Recursive `.new` / `.bak` inventory：0。

## 6. Preset Apply 处置

一次默认 `apply.sh --repo .` 按本地 selected platforms `codex,cursor` 卸载了 520 个 tracked
Claude package paths，并重写 installed extension manifest。该结果不作为有效验证证据。
依据 apply 前精确 status 基线，仅恢复了本次命令造成的 `.claude/skills/**` 删除和
`.trellis/guru-team/extension.json` 变化；恢复后两处 diff 均为空，sidecar 为零，且未再次
运行 apply。保留的 dogfood runtime sync 继续与 canonical byte-identical。

## 7. 交给 trellis-check

1. 复核 `F-FINAL-LEGACY-01` 的同月 legacy partial preview -> recorder -> checker ->
   transition 路径，并确认 formal takeover 只应用一次。
2. 复核 augmented digest confirmation、旧 plan pre-formal byte immutability、committed
   predecessor evidence HEAD/minimal tail 与 exact gate ownership。
3. 复核 generic #105、其它新增 artifact、跨月 reprepare 和 public DTO 均未被放宽或改写。
4. 按 `ssot_first` 复核 durable contract 与 `no_docs_update_needed` 判断，确认 workflow、
   upstream Finish assets、preset overlays 与 official task runtime 无 diff。
5. 复核 ownership baseline assertion 只同步 canonical stable facts；validator、registry、
   inventory、manifest 与 #132 overlay semantics 均保持无 diff。
6. 重新运行完整 Phase 2 并记录新的 gate evidence；实现角色没有改写现有
   `phase2-check.json`。

## 8. 风险与未执行项

- 未重跑 clean throwaway marketplace/install/update/reapply；本轮 finding 只改变已同步的
  companion runtime 与 regression，既有 Round 3 clean-install evidence 不应被表述为本轮
  fresh evidence。
- 默认 apply 的 platform-selection 行为说明 source dogfood reapply 必须显式选择完整平台集；
  本轮已恢复所有越界变化，但没有再执行 mutation validation。
- #119 继续拥有 global Finish activation/combined acceptance；#132 继续拥有 upstream
  overlay cleanup。本轮没有承接这两个边界。
