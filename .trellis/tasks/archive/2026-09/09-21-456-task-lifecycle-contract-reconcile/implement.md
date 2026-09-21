# Implementation Plan: #456 Reconcile Documents

## 1. Current Delivery Boundary

本 task 只写：

- `prd.md`
- `design.md`
- `implement.md`
- `reconcile/01-current-contract-inventory.md`
- `reconcile/02-contract-mapping.md`
- `reconcile/03-migration-boundary.md`
- `reconcile/04-reconcile-result.md`
- workflow owner 正常产生的 ignored runtime evidence

禁止修改 production surface、#454、#443/#436/#434 历史 task 和 #434 worktree。

## 2. Phase 1 Steps

### Step 1. Refresh Authority

- [x] 重新读取 live Issue #456 与评论。
- [x] 识别 `2026-09-21T06:17:54Z` 的最新 scope/target authority 并保持 Phase 1。
- [x] 将 task 返回 `planning`。
- [x] 绑定 #454 完整 commit SHA 和五个必读文件。

### Step 2. Build Three-Group Inventory

- [x] 完成 #443 session consumer inventory。
- [x] 完成 #436 lifecycle consumer inventory。
- [x] 完成 #434 workflow/projection/package consumer inventory。
- [x] 核对 canonical、installed、registry、manifest 与平台 projection locator。

### Step 3. Close Mapping And Migration Boundaries

- [x] 为全部 Item ID 指定唯一 disposition。
- [x] 为全部 replace/retire 项绑定 owner、#454 dependency、forbidden activation、blocking 和 successor task。
- [x] 固定 session/workspace/Reactivate/resource/Finish/Cleanup/#434 authority 边界。
- [x] 证明四份文档 Item ID 集合闭合且无未分类项。

基线已更新为 `#454@b695adc928c2064bd27f07e2bb3bbbd034540571`；旧 SHA 的阻塞记录已被完整 mapping 取代。

### Step 4. Re-run Phase 1 Gates

- [ ] `guru-review-contract-wording:planning_artifacts`
- [ ] `guru-maintain-architecture-baseline:task_impact_sync(stage=planning)`
- [ ] `guru-approve-task-plan`
- [ ] `task.py validate` 与 `git diff --check`
- [ ] 展示更新后的 approved plan，并在重新激活前取得单独确认。

以上门禁必须针对当前新 SHA 和当前四份 reconcile 文档 fresh 执行，不得复用旧基线结果。

## 3. Required Validation

```bash
python3 ./.trellis/scripts/task.py validate \
  .trellis/tasks/09-21-456-task-lifecycle-contract-reconcile
git diff --check -- \
  .trellis/tasks/09-21-456-task-lifecycle-contract-reconcile
```

文档闭包验证必须确认：

- Inventory Item IDs = Mapping Item IDs；
- Mapping replace/retire Item IDs = Migration Boundary Item IDs；
- 四份文档只引用完整 #454 SHA；
- 每个 replace/retire 行的 owner、dependency、forbidden activation、blocking、successor task、completion proof 非空；
- 不存在 production-surface 或 historical-task dirty path。

## 4. Stop Conditions

- #454 exact commit 存在设计缺口或不可读取。
- 三组 consumer 中存在无法从 live repository authority 判定的 public contract。
- 任一 Item ID 无唯一 disposition 或 replace/retire 无唯一承接边界。
- 需要在本 Issue 中实现代码或保留 dual-read/dual-write/alias 才能闭合。
- 需要修改 #454、历史 task 或 #434 dirty worktree。

## 5. Completion Statement

完成时只能声明：#443/#436/#434 三组 public consumer 已与 #454 exact contract 完成文档级 reconcile，并为全部迁移动作建立唯一承接边界。

不得声明：substrate、package、schema、workflow 或 production graph 已实现、迁移、验证或激活。
