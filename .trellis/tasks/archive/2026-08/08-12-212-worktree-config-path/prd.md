# #212 修复 task workspace 配置路径回归

## 目标

恢复 `guru-create-task-workspace` package-local runtime 对现行
`workspace_mode` 与 `worktree_root` 配置合同的完整支持，使语义计划、
executor、checker、reuse/recovery、ignored runtime mapping 和 installed copy
使用同一绝对 workspace identity。

## 需求

1. `workspace_mode: worktree` 且 `worktree_root` 为空时，workspace 根目录为
   `<repo-parent>/<repo-name>-worktrees`。
2. 绝对 `worktree_root` 原样作为根目录；相对 `worktree_root` 相对 repository
   root 解析并规范化。
3. `workspace_mode: current` 使用当前 repository checkout，不创建额外
   worktree。
4. planner/recorder、executor、checker 和 reuse/recovery 使用同一 package-local
   确定性配置解析语义，不恢复 shared monolith 或 compatibility fallback。
5. public result、tracked task artifact 与 public DTO 不包含 machine-local
   absolute path；ignored runtime mapping 的 `workspace_path` 与实际 workspace
   完全一致。
6. 缺失/不支持的 mode、不可接受路径、既有冲突、stale/mismatch 在任何业务
   写入前 fail closed。
7. canonical package、dogfood installed package、shared/Codex/Claude/Cursor
   projections、preset manifest 与直接相关文档保持一致。

## 验收标准

- [ ] 真实 Git 测试证明默认空 root 创建并检查
  `<repo-parent>/<repo-name>-worktrees/<workspace-slug>`。
- [ ] 绝对 root 的 create、exact reuse、conflict 与 checker 路径一致。
- [ ] 相对 root 相对 repository root 解析，executor/checker/mapping 一致。
- [ ] `current` 模式不创建 worktree，并遵守 task artifact 与 workspace
  boundary。
- [ ] invalid mode、路径冲突、stale/mismatch 在 branch/worktree/task/mapping
  部分写入前阻塞。
- [ ] package-local tests、canonical/installed parity、source/installed
  validators、dogfood drift 与 `git diff --check` 通过。
- [ ] clean initial install、existing preset reapply、official Trellis update
  后配置路径矩阵通过且无 `.new`/`.bak`/conflict sidecar。
- [ ] 独立 current-HEAD Branch Review 无未关闭 P0-P3 finding。

## 边界

- 不修改、移动、删除、重建或清理 Issue #211 的 worktree、branch、task 或
  runtime mapping。
- 不实现 Issue #152 的 warm worktree pool。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`。
- 不扩展到恶意输入、并发竞态、锁、额外 crash consistency 或跨 OS 原子性。
- 保持 stable Skill id、typed exits、consumer projection、confirmation
  lifecycle 与 public schema。

## 权威来源

- GitHub Issue: https://github.com/castbox/guru-trellis/issues/212
- Regression origin: https://github.com/castbox/guru-trellis/issues/195
- Distinct future mode: https://github.com/castbox/guru-trellis/issues/152
- Independent task: https://github.com/castbox/guru-trellis/issues/211
