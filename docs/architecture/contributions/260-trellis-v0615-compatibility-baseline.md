# #260 Architecture contribution

目标 baseline identity：`current-main-0.6.5-guru.37`。来源是 #260 task delta；
完整矩阵、A/B compatibility 与真实 GitHub A route 已通过；本文件已完成 semantic
review，等待本次 promotion 投影，不单独构成 CURRENT authority。

- `ARCH-CUR-008`：current source 与 dogfood 的 official Trellis target/project
  version 为 `0.6.15`；canonical extension candidate 为 `0.6.5-guru.37`。
- `ARCH-CUR-009`：兼容 verifier 从 live registry/interface/manifest/ownership
  生成完整 capability projection，不使用固定 package/command/platform count 作为
  authority；HEAD、tracked/untracked candidate bytes/modes 与 candidate tree 共同绑定
  source state，三类 file mode、recursive Docs authority、extension identity 与
  post-archive history discovery 分别 fail closed。
- `ARCH-INT-006`：每个 declared platform cell 同时安装 shared `.agents` public
  projection 与唯一 selected platform projection；package-private validator scripts
  不分发到 platform roots。
- `ARCH-DOM-007`：A/B compatibility harness 只证明当前 task-local lifecycle、
  provider isolation、archive/merge/recovery/reachability；它不成为 #248 Acceptance
  或 #252 cleanup 的 public owner。
- `ARCH-CUR-010`：真实 GitHub A route 已以 source head `6a7b721a…` 完成 PR #2
  expected-head rebase merge与 Issue #1 closure；provider failure 同 transaction 恢复，
  remote branch/repository cleanup 后 retained-ref reachability 仍通过。
- `ARCH-GAP-005`：`.37` stable tag/Release 与 tag-pinned release smoke 仍由 #267 拥有；
  本任务只证明 `public_plus_local_candidate` compatibility，不把 candidate 称为已发布。

Fitness gate：六个 cell 全部保持现有 21 active Skills、89 external exits、
RDT/Architecture/Bootstrap contracts、History/Finish/naming routes 与声明平台入口；
版本 binding 和已审查 official migration mapping 之外没有差异。matrix summary
的精确 final candidate tree/source identity/digest 只保留在 runtime/conversation evidence，
不写回 tracked 文档以避免自引用；matrix 继续保持 `real_github_verified:false`。
