# #290 Requirements contribution

本 contribution 修复 `BEH-001` 标准 Intake 在 detached Codex session 中无法使用
既有 selected-base checkout 的正常路径缺陷，并保持 `DES-004` lifecycle 与
`DES-008` 分层证据边界。它以 task-isolated contribution 完成独立 review，并经
serialized promotion 纳入 `.39` shared current authority。

- `R290-01`：base selection 必须保持固定优先级：显式 `base_branch`、config scalar、ordered existing candidate、remote default。
- `R290-02`：current branch 和 worktree availability 不得参与 base selection，也不得改变已选 base。
- `R290-03`：selected base 确定后，resolver 必须从同一 Git common-dir 的 registered worktrees 中查找绑定 `refs/heads/<selected_base>` 的 checkout。
- `R290-04`：session checkout 处于 detached HEAD 时继续处理；其 branch 不再作为 base authority 判断输入。
- `R290-05`：authority checkout 缺失、dirty、branch/HEAD/ref identity mismatch 时必须稳定 `blocked`，不得回退到其他 base。
- `R290-06`：authority checkout 已是当前 session checkout 时保持现有成功路径。
- `R290-07`：执行阶段的 Git mutation 集合仅包含 explicit refspec fetch 和 `merge --ff-only`；不得 checkout、switch、创建 branch/worktree、reset、rebase、stash 或 force update。
- `R290-08`：resolve、execute、validator 必须共享同一 selection/binding resolver 和同一 pre/post digest freshness 链。
- `R290-09`：成功后必须满足 authority checkout HEAD `==` local selected-base ref `==` remote-tracking ref，且 authority checkout clean。
- `R290-10`：`base_current.repo_locator` 必须指向实际 authority checkout；`synced`、`skipped`、`blocked` 及 downstream transition 保持兼容。
- `R290-11`：canonical package、dogfood installed package、Shared/Codex/Claude/Cursor 投影与 preset overlay 必须一致，reapply 后无 drift。
- `R290-12`：fresh equality 成立前不得读取 Intake authority 或创建 Issue、branch、worktree、task。

本 contribution 的 promotion 只更新 #290 的 shared current RDT/Architecture knowledge
authority；它不修改 runtime schema、Interface 或 extension revision，不扩张其他 Issue、
业务 repository、#267 release matrix、tag 或 Release。
