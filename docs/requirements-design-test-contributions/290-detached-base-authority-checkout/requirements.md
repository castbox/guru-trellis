# #290 Requirements contribution

本 contribution 修复 `BEH-001` 标准 Intake 在 detached Codex session 中无法使用
既有 selected-base checkout 的正常路径缺陷，并保持 `DES-004` lifecycle 与
`DES-008` 分层证据边界。它是 task-isolated candidate，不是 shared current authority。

- `R290-01`：base selection 固定按 explicit `base_branch`、config scalar、ordered
  existing candidate、remote default 执行；current branch 与 worktree availability
  不参与 selection，选定后不得回退其他 base。
- `R290-02`：selected base 确定后，只能绑定同一 Git common-dir 中 registered、exact
  `refs/heads/<selected_base>`、clean 且 branch/HEAD/ref identity 一致的唯一 checkout。
- `R290-03`：session checkout 允许 detached；fetch、可选 `merge --ff-only`、checker
  三向 equality 与 downstream repository locator 只使用 authority checkout。
- `R290-04`：authority missing、ambiguous、dirty 或 identity mismatch 稳定返回
  `blocked`；不得 checkout、switch、创建 branch/worktree、reset、rebase、stash、force
  update 或重选 base。
- `R290-05`：authority checkout 已是 invocation checkout 时保持原成功路径；behind
  base 只允许 explicit remote-tracking refspec fetch 与 `merge --ff-only`。
- `R290-06`：保持 `guru-base-sync-result-1.0`、public synced/skipped/blocked schemas、
  Interface 1.4、typed exits 与 transition shape；既有 `repo_locator` 字段指向真实
  authority checkout，checker 的 invocation-local locator 不进入 closed result。
- `R290-07`：canonical、dogfood installed package、Shared/Codex/Claude/Cursor
  projection、extension inventory/hash、preset reapply 与 executable mode 必须一致，
  `.new`/`.bak`/unknown sidecar 为零。
- `R290-08`：代表性 installed Codex detached wrapper 必须在同 common-dir 的 clean
  selected-base authority 上通过；#267 release matrix、tag 和 Release 不属于本任务。

本 contribution 不修改 shared current RDT/Architecture、schema、Interface、README、
其他 Issue/task 或业务 repository。
