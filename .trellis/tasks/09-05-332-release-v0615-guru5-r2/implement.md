# #332 v0.6.15-guru.5 执行计划

## Phase 1：规划与激活

- [x] 以当前 `origin/main@3f888c1ad2d0bad5f257794b1f09da24af73f397`、Issue #332 和
  `current-main-0.6.5-guru.43` 完成规划 wording review。
- [x] 执行 `guru-maintain-architecture-baseline:task_impact_sync(stage=planning)`，
  只消费当前 `baseline_current` 或明确的无影响出口。
- [x] 执行 `guru-approve-task-plan`，通过后展示三份规划文档与未验证边界；取得当前
  Phase 1 plan acceptance 后运行官方 `task.py start`。

## Phase 2：preparation 实现与检查

- [x] 进入新 task worktree，按 `trellis-before-dev` 重读 relevant workflow/preset/docs
  specs，并确认当前 task/worktree boundary。
- [x] 搜索所有 `.3/.39` release-facing 引用，按 owner 分类后将适用面更新为
  `.5/.40/CLI 0.6.15`；历史 authority、历史 tag/Release 和 #267 历史边界保持不变。
- [x] 运行 preset apply/reapply，校验 canonical/dogfood/installed/platform projection、
  manifest、README、fixtures、registry/interface/schema、ownership、mode、overlay
  drift 与 recursive zero-sidecar。
- [x] 运行 package/runtime/integration/eval、Issue recovery、Finalizer/Publication、
  preset installer、upgrade/update/reapply 和声明平台定向验证；不把 focused test
  冒充完整 Release Gate。
- [ ] 准备中文 release notes 草案，明确版本映射、升级路径、安全/部署影响、assets
  与所有未验证边界。
- [ ] 执行 `guru-check-task` 完整 semantic check；finding 修复后按影响范围重跑。

## Phase 3：提交、独立审查与合并

- [ ] 展示精确 staged paths、commit message 与预期结果，取得独立 task commit 确认，
  执行 `guru-create-task-commit`。
- [ ] 对完整 `origin/main...HEAD` 执行 fresh Branch Review；确认 PR 中文标题/正文、
  `Refs #332` 语义、验证结果、安全说明、部署影响、Docs SSOT 与 Issue close scope。
- [ ] 通过 Publication Review 与 Finalizer；push、PR、merge 分别按当前 gate 取得确认。
- [ ] merge 后 fresh fetch/freeze candidate commit/tree，任何 stale 或内容变化都重新
  执行受影响 gate。

## Post-merge Release Gate

- [ ] 从 exact candidate 重新运行完整 Release Gate，覆盖 #311/#333/#339/#358/#361、
  clean throwaway、existing install/update/reapply、installed business repository
  Publication/Finalizer 代表性链路、平台入口、secret scan 和 zero-residue。
- [ ] 展示 candidate SHA/tree、annotated tag message 与精确 push refspec；取得独立确认
  后创建并 push `v0.6.15-guru.5`，live 回读 tag object 与 peeled candidate。
- [ ] 展示 immutable tag-pinned 临时验证范围；取得独立确认后执行 install/update/reapply
  与 smoke。失败时停止，不移动或删除 tag。
- [ ] 展示中文 GitHub Release title/body/target/draft/prerelease/assets；取得独立确认后
  创建正式 Release 并 live 回读。
- [ ] 展示 `gh issue close 332` 的精确副作用；取得独立确认后关闭，并最终回读 Issue、
  tag、peeled commit、Release、latest stable 与相关 Issue 边界。

## 风险与停止条件

- required gate 的 FAIL、SKIP、stale、cross-SHA、unknown/multiple/unmapped exit 均停止。
- 发现版本轴混淆、历史事实被改写、scope 超出 #332、共享 authority 需要未批准变更，
  或 projection 不能从 canonical source 重建时停止并回到对应 owner。
- 不执行 cleanup；任何旧 branch、旧 task、其他 worktree 和非本任务 dirty 文件均保留。
