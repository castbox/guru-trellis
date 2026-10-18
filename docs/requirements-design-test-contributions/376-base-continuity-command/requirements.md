# #376 Base-continuity command Requirements contribution

本 contribution 承接 live Issue #376 及其 accepted scope expansion。它以正文与 release facts
immutable 的 `current-main-0.6.5-guru.45` 为 expected predecessor，并在独立 committed review 与
serialized promotion 后形成唯一 active `.46` Requirements/Design/Test 与 Architecture authority；promotion
可为 `.45` 增加 predecessor lifecycle locator，并校正其 Design manifest 的历史错误 command count。

- `R376-CONT-01`：integration clock 与 authority/task-content clock 必须独立；base 前进本身不得使
  planning stale，真实 Issue、scope、approved assumptions 或 task content 变化仍必须进入原 owner route。
- `R376-CONT-02`：完整 Branch Review 后的 compatible base advance若只需要刷新 current reviewed-content
  identity，Reconcile 必须返回 `review_continuity_required`，不得伪造 full-review identity或强制重新实施。
- `R376-CONT-03`：Reconcile semantic owner 在展示并取得当次确认后，必须通过 package-private
  expected-head executor 创建唯一 local reconciliation commit；dirty/stale/head/tree/ancestry mismatch 必须零写入失败。
- `R376-CONT-04`：bounded continuity 必须分别绑定 prior full-review commit 与 current reconciled HEAD，
  只审查 exact base delta、冲突解决、candidate tree 与受影响验证，并把 current HEAD 交给严格 Publication gate。
- `R376-CONT-05`：public Skill/exit identity 保持不变；current-only schema 直接演进且旧 checkpoint stale，
  不新增 legacy dual-read、兼容 wrapper、第二状态机、remote mutation 或授权持久化。
- `R376-CONT-06`：current graph 必须从 live registry/interface 派生为 23 Skills / 97 exits / 78 commands；
  新增 command 仅为 `guru-reconcile-task-base` package-private executor。
