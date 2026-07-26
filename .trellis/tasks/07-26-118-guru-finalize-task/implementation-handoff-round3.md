# Issue #118 Phase 1 实现交接（Round 3 findings 修复）

## 1. 结论

本轮已修复 `phase2-worker-report-round3.md` 的五个 current-scope finding：
`F-RECOVERY-03`、`F-MATERIALIZATION-04`、`F-LOCATOR-05`、
`F-IDENTITY-06`、`F-STATE-07`。实现、durable SSOT、canonical/installed/platform
copies 与适用回归已经同步；未运行 Phase 2 recorder/checker，下一步必须由独立
`trellis-check` 重新执行完整 Phase 2。

## 2. 实现承接

- 保持 #117 generic owner checker 严格且未修改；新增 finalizer-only、immutable-plan-bound
  augmentation，绑定 active/archive locator、plan ref、reviewed HEAD、repository、remote
  ref、evidence allowlist、validated evidence commit、committed archived plan/evidence blobs
  与 exact archive transaction。任何额外 path、identity 或 commit drift 都 fail closed。
- `published` 的 tracked gate 从 pre-executor 到 archive 始终只保存 exact private marker；
  public wrapper 严格复查 terminal archive + ready PR facts，只在内存中物化 public DTO，
  不隐式执行 transition，也不把 DTO 写回 gate。
- `published.task_ref` 使用 immutable plan 的 archive locator；active input 仅允许按同一
  committed plan 精确投影到 archive locator。
- `verification_required.repo_ref` 必须等于 immutable plan repository。
- `resume_finalization` 仅允许 `content_pushed`（且已有 current verified/not-required
  evidence）、`evidence_ready`、`evidence_pushed`、`draft_bound`、
  `projection_validated`、`archive_moved`、`archive_pushed`、`archived`；拒绝
  `prepared`、`reprepare_required`、stale 与 terminal `ready`。
- eval staging 的 verified/not-required published recipes 改为 terminal `ready`，gate
  使用 private marker，public output 使用 archive locator；actual-exit schema 仍先于
  expected-exit comparison。

## 3. 本轮文件

- Runtime：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`，以及 installed
  `.trellis/guru-team/scripts/python/guru_team_trellis.py`。
- Runtime regression：
  `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`。
- Eval adapter：`trellis/skills/guru-team/adapters/eval/native_adapter.py`，以及 installed
  `.trellis/guru-team/skills/adapters/eval/native_adapter.py`。
- Step-local contract：
  `trellis/skills/guru-team/packages/guru-finalize-task/references/contract.md`，以及
  installed shared、Agents、Codex、Claude、Cursor byte-identical copies。
- Durable specs：`.trellis/spec/workflow/skill-package-contract.md`、
  `.trellis/spec/workflow/workflow-contract.md`、
  `.trellis/spec/workflow/companion-scripts.md`、
  `.trellis/spec/workflow/quality-guidelines.md`。
- Task-local history：本文件；Round 3 两个 probe 与 worker report 保持 task-local。

## 4. Docs SSOT Plan

策略为 `ssot_first`。实现以 approved durable finalizer/package/workflow/script contracts
为主要输入，以 `prd.md`、`design.md`、`implement.md` 和 Round 3 findings 作为 task delta。
本轮先把 finalizer-only #117 augmentation、terminal materialization、archive locator、repo
identity 与 recovery-state 合同合并到 step-local contract 和四份 durable workflow specs，
再同步 runtime/tests/platform copies。

README、workflow marketplace README、preset README 本轮无需追加：active `13/52`、deferred
global `12/46/27`、#119 activation 与 #132 overlay cleanup 状态均未变化；Round 3 的内部
恢复算法属于 step-local/script SSOT，复制到导航文档会制造第二份行为定义。Global workflow、
dogfood workflow、upstream `trellis-finish-work` assets、preset overlays 与 official
`.trellis/scripts/task.py` 均保持 baseline 无 diff。Probe、worker report 与本交接只记录
task history，不进入 durable docs。

## 5. 验证

- Focused Round 3 regressions：9 passed，0 failed，0 skipped。
- Runtime full：611 tests，13 skipped，exit 0。
- Skill packages full：178 tests，exit 0。
- Preset full：45 tests，exit 0。
- Finalizer package：4 tests，exit 0。
- Installed shared real public wrapper eval：8/8 passed；三个 `published` case 均输出
  `.trellis/tasks/archive/2026-07/current`。
- Round 3 recovery probe：exit 0；无 plan/repo 绑定的普通 HEAD drift 仍由 generic #117
  checker 阻断，control 通过。新增回归另证明 exact finalizer augmentation 正向与 drift
  负向路径。
- Round 3 published probe：exit 1，首个旧漏洞路径被
  `The persisted published route must retain the exact private executor marker.` 阻断；该
  probe 按旧漏洞成功条件编写，非零是预期修复信号。
- Source/installed package validation、contract/eval discovery、ownership、shell syntax、
  Python compile、`git diff --check`、task validation、executable modes、surface hygiene、
  byte identity、overlay drift 与 no-write assertions 全部 exit 0。
- Preset apply 首轮因保护机制生成 7 个 `.bak`、无 `.new`；确认目标已与 canonical
  byte-identical 后精确清理 sidecar，第二轮 apply exit 0，conflicts/sidecars 均为空。
- Clean throwaway exit 0：覆盖 public marketplace discovery、local unpublished canonical
  sample、initial install/reapply、`trellis update`、managed hash/sidecar recovery、两类
  developer identity、全平台 distribution、package/eval/wrapper、closeout recovery、
  ownership 与最终 hygiene。

## 6. 交给 trellis-check

独立检查重点：

1. 逐项关闭五个 Round 3 finding，特别复核 generic #117 checker 没有被放宽，augmentation
   只能由 finalizer 在 immutable-plan-bound 正常路径使用。
2. 复核 pending marker、terminal ready facts、archived gate 与 public in-memory DTO 的先后
   关系；确认 public wrapper 不执行 transition。
3. 复核 active-to-archive locator projection、wrong repo、extra dirty path、wrong archive
   commit、`prepared`/`ready` resume negative cases。
4. 复核 `ssot_first` reconciliation、canonical/installed/platform byte identity、#119/#132
   ownership与所有 no-write assertions。
5. 重新运行完整 Phase 2 验证并记录新的 `phase2-check.json`；本轮实现角色没有记录或修改
   Phase 2 gate artifact。

## 7. 风险与未执行项

- 没有在本仓库执行真实 GitHub draft PR create/ready、archive commit/push、Issue mutation、
  production write 或真实 remote-ref #117 clean install；这些副作用不在本实现授权内。
- Clean throwaway 与 fixture transaction 覆盖安装/升级和 deterministic closeout，但不能
  替代独立 Phase 2 semantic review，也不能被表述为真实 GitHub publication evidence。
- #119 仍负责 global Finish activation/combined acceptance；#132 仍负责 upstream overlay
  cleanup。本轮没有提前承接这两个边界。
