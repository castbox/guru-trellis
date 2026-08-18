# #260 Test contribution

- `SCN-011`：`claude|codex|cursor × clean|existing` 六个独立 cell 全部绑定
  exact `0.6.15` 并通过，最终 recursive `.new/.bak = 0`；当前 HEAD 的两次
  PATH-runtime driver 重跑共享稳定 matrix SHA-256
  `660422848f6efba9f1c3c6fcf2d9d23a1e8b710af8ffd10bf0f12e0954910f49`。
- `SCN-012`：dogfood official update 将 `.trellis/.version` 提升到 `0.6.15`，
  保留已分类 local customization，workflow preview/switch 与 preset reapply 后
  ownership、mode、source/installed/platform closure 无漂移。
- `SCN-013`：before/after capability projection 对 active ids、interfaces、schemas、
  exits、commands、consumers、routes、managed assets、modes 与 Docs locators 做 exact
  set comparison；未知 loss 阻塞。
- `SCN-014`：每个安装场景调用 #263/#264 的四个 profile 与 #265 的三个 profile，
  同时验证 #266 versioned docs 和最小 spec projection 未被 update 删除或覆盖。
- `SCN-015`：A/B 双向 merge、task-local archive、零跨 task metadata、Finish/provider/
  cleanup failure 同 owner 恢复、cleanup retained refs/reachability 均通过；B 的 PR
  read/create 为零，workspace journal 保持 untracked。
- `SCN-016`：A 的 dedicated private disposable GitHub repo 已在单独确认后完成真实
  push、PR #2、expected-head rebase merge、Issue #1 closure、remote branch/repository
  cleanup；source head `6a7b721adfd8a70be9cc56883bf5e2b2133fdf84`，merge commit
  `a5c73c49ca38e593e11bafb62a2f142ca208f97f`，closure 晚于 merge 一秒，provider
  `github_api_unavailable` 由同一 Finalizer transaction 恢复。

矩阵使用 `public_plus_local_candidate` workflow evidence，证明 current local candidate
与 public marketplace 的组合兼容，不冒充尚未发布的 `.37` stable source。stable tag 与
GitHub Release 仍由 #267 拥有。
