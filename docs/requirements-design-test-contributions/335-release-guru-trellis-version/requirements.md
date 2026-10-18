# #335 Repository-private release orchestration Requirements contribution

本 contribution 定义 `castbox/guru-trellis` 正式发布的仓库私有编排合同。它继承 active
`current-main-0.6.5-guru.42` Requirements、Design、Test 与 Architecture authority，只形成
task-isolated candidate，不修改 shared current。

- `R335-01`：正式发布入口的 Skill ID 必须固定为 `release-guru-trellis-version`，只存在于
  本仓库 Shared、Codex、Claude、Cursor project-local discovery roots；公共 Skill package、
  marketplace、preset、overlay、registry、extension manifest 和业务仓库 installed projection
  必须不包含它。
- `R335-02`：每次 invocation 必须从当前请求取得 repository、current release Issue、target
  repo tag、target extension revision、official Trellis CLI version 和 predecessor tag，并 fresh
  读取 live Issue、Git、GitHub、version surfaces 与现有 lifecycle owner contracts。
- `R335-03`：preparation 阶段必须复用 standard intake、Phase 2、`guru-create-task-commit`、一次
  完整 `guru-review-branch`、`guru-review-task-publication`、`guru-finalize-task` 和
  `guru-merge-task-pr`；Skill 不复制、替代、缩短或削弱这些 owner 的 gate、typed route、
  freshness、confirmation 或 fail-closed 合同。
- `R335-04`：preparation merge 后必须丢弃 preparation HEAD、旧 Review、Publication 与 release
  evidence，从 fresh `origin/main` 冻结可证明 lineage 的 exact candidate；所有 post-merge checks
  与后续动作必须绑定同一 candidate identity。
- `R335-05`：PR title/body 必须由 Publication 根据 live Issue、完整 diff、验证结果和当前
  candidate identity 即时生成并语义审查；GitHub Release title/body 必须在 Release 动作前按
  post-merge exact candidate 即时生成并语义审查。两者只交给对应 consumer，不建立 task-local
  body handoff。
- `R335-06`：release task 不得创建 `release-notes*.md`；`implement.md` 只保存稳定实施计划，
  不使用动态执行 checklist。tracked task 和 durable docs 不得保存 HEAD、阶段进度、Gate
  pass/fail、finding closure、tag、smoke、Release、时间或用户授权状态。
- `R335-07`：owner-private runtime checkpoint 只按既有 owner 合同短期存在和退休；正常 lifecycle
  metadata 不改变 reviewed-content identity，不产生 release-status metadata commit 或第二次内容
  Review loop。
- `R335-08`：Skill、source、durable docs、配置、schema、script 或 test bytes 变化必须使受影响的
  Phase 2、Branch Review、Publication、Finalizer 或 exact-candidate gate stale，并返回对应 owner
  重新验证。
- `R335-09`：stale、cross-SHA、lineage 不可证明、live identity mismatch、FAIL、SKIP、unknown、
  multiple 或 unmapped exit 必须停止在当前 owner；不得以 metadata commit 记录进度、伪造恢复点
  或继续发布副作用。
- `R335-10`：merge、annotated tag、tag-pinned smoke、GitHub Release、Issue closure 和 cleanup
  必须保持独立动作；每次动作前 fresh 展示精确目标、refs、命令和预期结果，并取得不可复用、
  不可持久化的当前对话确认。
- `R335-11`：post-merge minimum gate 必须覆盖 predecessor-to-candidate full diff、版本映射、
  source/installed validators、四平台 parity、install/update/reapply、secret scan、residue check 和
  tag-pinned smoke；本 contribution 不把 #335 扩张为完整累计多平台 Release Gate 矩阵。
- `R335-12`：本工作不得发布 `v0.6.15-guru.5`，不得创建、移动或删除 tag/GitHub Release，
  不得读取或复用 #332 的 task/worktree/runtime/review/未提交文件，也不得修改 Trellis upstream、
  全局 npm、`node_modules` 或业务仓库。
