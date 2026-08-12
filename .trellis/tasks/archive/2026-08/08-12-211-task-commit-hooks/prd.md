# #211 修复 package-local task commit hooks

## 目标

恢复 `guru-create-task-commit` package-local executor 对业务仓库真实 commit hooks
的支持，使 exact reviewed candidate 在不污染真实 branch、live index 和无关工作区状态
的前提下，执行普通 `git commit` 所适用的 `pre-commit`、
`prepare-commit-msg`、`commit-msg` 和 `post-commit`，并诚实区分 ref 发布前失败与
commit 已创建后的 recovery。

## 当前事实

- Live authority 为 GitHub Issue #211；它是本 task 唯一 `close_issue`。
- `main@8d52f2b5bfa64c29a64deb616e9f5b4a7c4ebce8` 的
  `trellis/skills/guru-team/packages/guru-create-task-commit/runtime/execute.py`
  使用 `git commit-tree`，不会执行 repository commit hooks。
- 当前合同已经要求 isolated index、detached commit transaction、真实 hooks、
  conditional `update-ref` 和 pre-ref/post-ref failure 边界；本任务修复实现回归，
  不通过弱化合同文字规避问题。
- #195 已把 record/check/execute 迁入 package-local runtime；本任务不得恢复共享
  `guru_team_trellis.py` 单体或 compatibility fallback。
- 当前仓库 `codex.dispatch_mode=sub-agent`，实现与检查必须使用 Trellis sub-agent；
  不创建 `implementation-handoff.md`。

## 需求

### R1 真实 hook 语义

1. executor 必须经由真实 `git commit --cleanup=verbatim -F <message-file>` 运行
   `pre-commit`、`prepare-commit-msg`、`commit-msg` 与 `post-commit`。
2. hook 必须观察本次 exact candidate 的 index、worktree、message file 与 parent
   HEAD；不得审查 live worktree 中另一份不相关状态。
3. 未声明的 message 改写一律在真实 branch ref 发布前 fail closed；不得静默提交
   不同于 AI 已审核 bytes 的 message。

### R2 exact candidate 与 mutation 门禁

1. hook 前后的 exact index tree、每个 reviewed path 的 blob/mode、完整 tree、
   parent、raw message 与 committed path set 必须可验证。
2. hook 新增、删除、rename、stage、unstage 或修改任何未获授权的路径时，在真实
   branch ref 发布前阻断；未声明的 exact-path 内容或 mode 变化同样阻断。
3. `pre-commit`、`prepare-commit-msg` 或 `commit-msg` 非零退出不得推进真实 branch
   ref，且 live index、candidate 与 Phase 2 checkpoint 保持可重试。

### R3 post-commit recovery

1. `post-commit` 运行时 commit 已在隔离 transaction ref/HEAD 创建；其失败或 mutation
   必须返回包含 created commit identity 的有界 recovery 结果。
2. 该结果不得声称 commit 未发生，也不得删除 candidate 或 Phase 2 checkpoint。
3. 只有所有 postconditions 通过后，才以 conditional `update-ref <live-ref> <new> <old>`
   发布真实 branch，并按既有合同清理 checkpoint。

### R4 无关状态与兼容性

1. 成功和失败都必须保留无关 staged、unstaged、untracked 与 gitlink 状态。
2. live index 比较继续基于 `mode/blob/stage/path` 语义，不比较 `.git/index` 原始 bytes；
   stat-cache-only 刷新不得误报。
3. 保持现有 candidate 5.0、public input/output、typed exits、package-local ownership、
   AI semantic review 和 dialogue-only commit authorization。
4. 不修改 Finalizer、Extension Verification 或 #208 Ready PR recovery。

### R5 分发与文档一致性

1. canonical package、dogfood installed package、shared/Codex/Claude/Cursor projections、
   preset manifest 与直接相关文档保持一致。
2. clean initial install、existing repo update/reapply 和 official Trellis update 后仍可用，
   且无未处理 `.new`、`.bak` 或 conflict sidecar。

## 验收标准

- AC1：真实临时 Git repo 证明四类 hooks 按 Git 时机运行，并能观察 exact candidate
  的 index/worktree/message/HEAD。
- AC2：正常 hooks 通过时，仅 exact reviewed paths 被提交，parent、raw message、
  blobs/modes、complete tree 与 current HEAD 全部匹配。
- AC3：`pre-commit` 与 `commit-msg` 拒绝在真实 branch ref 发布前阻断，candidate、
  Phase 2 checkpoint、live index 和无关工作区状态保持。
- AC4：hook 引入额外 tracked/untracked/staged path、修改 exact path、unstage path、
  rename 或改写 message 均 fail closed，不发布未审核 commit。
- AC5：`post-commit` 失败或 mutation 返回 created commit identity 和稳定 recovery，
  不删除恢复输入。
- AC6：stat-cache-only index 刷新通过，测试明确断言 semantic entries 而非 index bytes。
- AC7：package-local positive/negative/recovery tests、canonical/installed byte parity、
  source/installed validators、dogfood drift 与 `git diff --check` 通过。
- AC8：clean throwaway initial install、existing repo update/reapply、official Trellis
  update 验证通过，无 sidecar。
- AC9：独立 current-HEAD Branch Review 无未关闭 P0-P3 finding。

## 非目标

- 不实现 #208 existing Ready PR adoption。
- 不修改 #205 的业务仓库 verifier 不可达合同。
- 不新增 hostile hook、恶意篡改、并发竞态、TOCTOU、锁、fault injection、额外
  crash consistency 或跨 OS 原子性范围。
- 不创建 push、PR、archive 或 merge 行为。
