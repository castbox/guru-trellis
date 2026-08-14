# #222 v0.6.5-guru.6 执行计划

## Phase A：Live authority 与 release preparation

- [x] 读取 live #222、#227、#219、#217、#218、相关 PR、AGENTS.md、remote
  `main`、tags/releases 与当前 manifest。
- [x] 确认 PR #224/#225/#226/#228 已 merge，四个 merge commit 均在
  `origin/main`；#223/#208/#164/#220 排除。
- [x] 经用户确认修订 #222 prerequisite chain。
- [x] 从 exact `efb7a7eb859f59b345350cf30e1c4b581b70765e` 创建独立 task workspace。
- [x] 将 stable tag/source 从 `.5` 更新为 `.6`，extension revision 从 `.27`
  更新为 `.28`；不得猜测 future candidate commit。
- [x] 更新 manifest、public README、workflow/preset README、安装与升级命令、版本
  映射、release identity fixtures/tests 与本 task release notes 草稿。
- [x] 运行 canonical preset apply，同步 dogfood/platform installed copies，处理全部
  `.new`/`.bak`/conflict/removal/unknown sidecar。

## Phase B：实现检查与 preparation 合入

- [x] 读取 `trellis-before-dev` 指定规范并完成变更。
- [ ] 运行 task validation、package/runtime/preset/ownership/drift/diff checks。
- [ ] 执行 `guru-check-task` semantic gate；finding 修复后全量重跑。
- [ ] 仅 stage 本 task 文件，执行 `guru-create-task-commit`。
- [ ] 对完整 `origin/main...HEAD` 执行 `guru-review-branch`，处理所有 P0-P3 finding。
- [ ] 完成 publication readiness、push、PR 与 merge；每个 Git/GitHub 副作用按当前
  owner 展示精确动作并确认。

## Phase C：Fresh exact candidate 与完整 pre-tag gate

- [ ] merge 后刷新 `origin/main`，要求 checkout clean 且 HEAD/local/remote 三方相等，
  冻结唯一 candidate commit/tree；任何演进使证据 stale。
- [ ] 以 exact candidate 正式执行一次 `guru-verify-extension-installation`，AI adequacy
  review 只在所有 required capability 有 fresh evidence 时返回 `verified`。
- [ ] 验证 clean workflow install、existing preview/switch、preset apply、official
  update、preset reapply 与受管 Python runtime identity/reapply 幂等。
- [ ] 验证 source/installed/platform equality、managed inventory、executable mode、
  dogfood drift 与递归零 sidecar。
- [ ] 真实执行 Branch Review `record -> check -> invoke -> retire/retain`。
- [ ] 真实执行 Finalizer/Merge single-JSON、fresh transition、ready/terminal recovery、
  closure mismatch 与重复调用零 mutation。
- [ ] 在隔离业务仓副本执行 `.5 -> candidate` pinned upgrade smoke，并验证 2130 路径
  Publication Review/Finalizer preflight；确认真实业务 checkout/remote 零变化。
- [ ] 汇总命令、exit code、candidate/tree/revision、实际 PASS 与未验证边界。任一 required
  gate 非 PASS 时停止。

## Phase D：Tag-pinned gate

- [ ] live revalidate candidate、candidate tree、remote tag absence 与 manifest revision。
- [ ] 展示 exact annotated tag/push 命令和副作用，等待用户确认。
- [ ] 创建并 push immutable `v0.6.5-guru.6` annotated tag。
- [ ] 核对 tag object、peeled commit、candidate tree、manifest revision 与 exact source。
- [ ] 从 tag-pinned source 执行最小 clean install/upgrade entry smoke；仅在 bytes mismatch
  或入口暴露新问题时重跑完整 pre-tag 内部测试。

## Phase E：Release 与 #222 closure

- [ ] 准备中文 Release notes，覆盖 #219/#217/#218/#227、`.5 -> .6` 升级、版本映射、
  验证证据、限制、安全与部署影响。
- [ ] 展示 exact GitHub Release title/body/target，等待用户确认后创建并 live reread。
- [ ] 展示 exact #222 去敏证据评论，等待用户确认后发布并 live reread。
- [ ] 展示 exact #222 close 动作，等待用户确认后关闭。
- [ ] 最终核验 Issue Closed、Release published、tag/release/candidate/manifest identity
  一致；#223/#208/#164/#220 状态未被本 task 改变。

## 核心验证命令族

- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-14-222-release-v065-guru6`
- `python3 trellis/skills/guru-team/tests/test_skill_packages.py`
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
- `python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`
- `trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `trellis/presets/guru-team/scripts/bash/verify-managed-python-runtime.sh --repo . --json`
- 正式 `guru-verify-extension-installation` public wrapper invocation
- `git diff --check`

完整命令参数、fixture、candidate identity 与结果从执行时 live contracts/scripts 生成，
不在计划阶段伪造 PASS。
