# #222 v0.6.5-guru.7 执行计划

## Phase A：Live authority 与 planning

- [x] 重新读取 live #222、#219、#217、#218、#227、#231、PR #224/#225/#226/#228/
  #230/#232、AGENTS.md、official Trellis docs、fresh remote `main`、tags/releases 与
  当前 manifest。
- [x] 确认五个 prerequisite 均 merged/closed 且完整 merge result 位于
  `origin/main@2aef3cb9481c2413fbfe6c93af5246ba873049f8`。
- [x] 确认 #223/#208/#164/#220 独立排除，#222 fixed chain 已包含 #231。
- [x] 创建全新 `codex/222-release-v065-guru7` worktree/task；未复用 `.6` workspace。
- [x] 分配新映射 `.7` / `.31` / CLI `0.6.5`，不复用旧 candidate、SHA 或证据。
- [x] 完成 `prd.md`、`design.md`、`implement.md` 与 Docs SSOT Plan。
- [x] 运行 planning wording review 与 `guru-approve-task-plan`，只在用户确认后激活 task。

## Phase B：Release preparation 实现与合入

- [x] 读取 `trellis-before-dev` 指定 specs，并更新 canonical manifest、public/workflow/
  preset README、安装升级命令、stable source 映射、fixtures/tests 与中文 notes 草稿。
- [x] 执行 `apply.sh --repo . --all-platforms` 同步 dogfood/platform projections；逐项处理
  tracked drift、managed removal、`.new`/`.bak`/conflict/unknown sidecar。
- [x] 运行 task validation、manifest/package/preset/ownership/equality/drift/diff checks。
- [x] 执行 `guru-check-task` semantic gate；finding 修复后按影响范围重跑。
- [ ] 仅 stage 本 task 文件，执行 `guru-create-task-commit`。
- [ ] 对完整 `origin/main...HEAD` 执行真实 `guru-review-branch` lifecycle，关闭所有 P0-P3。
- [ ] 完成 publication readiness；分别展示并确认 commit/push/PR/merge 副作用。

## Phase C：Fresh exact candidate 与完整 pre-tag gate

- [ ] preparation merge 后刷新 `origin/main`，要求 clean checkout 且 HEAD/local/remote
  三者 identity 完全一致，冻结唯一 candidate commit/tree；旧 base/branch evidence 不转用。
- [ ] 对 exact candidate 正式执行一次 `guru-verify-extension-installation`，只有全部 required
  capability 有本轮 fresh evidence 时返回 `verified`。
- [ ] 验证 clean workflow install、existing preview/switch、preset apply、official update、
  preset reapply，并证明用户级共享 managed runtime 对相同 identity 重复 reapply 的结果不变。
- [ ] 验证 source/installed/platform equality、managed inventory、executable mode、dogfood
  drift 与递归零 sidecar/removal/conflict。
- [ ] 真实执行 Branch Review `record -> check -> invoke -> retire/retain`。
- [ ] 真实执行 Finalizer/Merge single-JSON、fresh transition、ready/terminal recovery、
  closure mismatch 与重复调用零 mutation。
- [ ] 在隔离业务仓副本执行 `.5 -> candidate` pinned upgrade；重放原 2130 路径的
  Publication Review/Finalizer preflight；对真实业务 checkout/remote 做前后零变化证明。
- [ ] 汇总 exact command、exit、facts、candidate/tree/revision 与未验证边界；任一 required
  gate 非 PASS 时停止。

## Phase D：Tag-pinned gate

- [ ] live revalidate candidate、tree、remote tag absence、manifest `.31` 与 exact source。
- [ ] 展示 annotated tag message、`git tag -a` 和 exact push refspec；取得当前确认后执行。
- [ ] 创建并 push immutable `v0.6.5-guru.7` annotated tag。
- [ ] 核对 tag object、peeled commit、candidate tree、manifest revision 与 source bytes。
- [ ] 从 tag-pinned source 执行最小 clean install/upgrade 入口 smoke；仅在 mismatch 或入口
  暴露问题时重跑完整 pre-tag 矩阵。

## Phase E：Release 与 #222 closure

- [ ] 完成中文 Release notes，覆盖 #219/#217/#218/#227/#231、`.5 -> .7` 升级、
  `.31` 映射、fresh evidence、已知限制、安全和部署影响。
- [ ] 展示 exact GitHub Release title/body/target，确认后创建并 live reread。
- [ ] 展示 exact #222 去敏证据评论，确认后发布并 live reread。
- [ ] 展示 exact #222 close 动作，确认后关闭。
- [ ] 最终核验 Issue Closed、Release published、tag/release/candidate/manifest 一致，且
  #223/#208/#164/#220 未被修改。

## 核心验证入口

- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-14-222-release-v065-guru7`
- `python3 trellis/skills/guru-team/tests/test_skill_packages.py`
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
- `python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`
- `trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `trellis/presets/guru-team/scripts/bash/verify-managed-python-runtime.sh --repo . --json`
- 正式 `guru-verify-extension-installation` public wrapper invocation
- `git diff --check`

精确 fixture、candidate identity、temporary roots 和结果从执行时 live package contracts
生成，不在 planning 阶段伪造 PASS。
