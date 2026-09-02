# #338 Requirements contribution

本 contribution 修复 current `.43` Finalizer 同计划恢复缺口，不改变 public Skill、typed exits、owner-private
transaction schema id/version 或 Merge consumer。

- `R338-01`：fresh、无 owner transaction 的 equal-HEAD Open PR 必须继续以
  `existing_pr_unbound_equal_head` 拒绝。
- `R338-02`：仅当 current transaction 精确为
  `ordinary_publication/push_content` 且 `pr`/`adopted_pr` 未绑定、完整 plan identity current 时，才可识别
  未绑定 equal-HEAD recovery。
- `R338-03`：唯一 Open PR 必须属于同 repository/base/head/head repository、非 fork，且 remote/PR/
  Publication HEAD 三者相等；live close scope 必须精确等于 reviewed `close_issues`。
- `R338-04`：preview 必须 side-effect-free 投影 exact PR、`ancestry=equal`、`push_required=false`、原始
  Draft/Ready、title/body 字节比较、metadata decision 与 Ready action。
- `R338-05`：execute 必须在 PR edit、archive 或 Ready mutation 前把同一个 ordinary transaction 转换并
  持久化为 `existing_pr_recovery/bind_pr`，绑定原始 live title/body comparison 与 metadata convergence
  decision；不得创建第二个 transaction、重复 publication push 或创建 PR。
- `R338-06`：title/body 任一字节差异触发一次 current Publication metadata convergence；末尾 LF 属于差异，
  update 后必须 exact reread，metadata 相等路径零 edit。
- `R338-07`：Ready 保持 Ready，Draft 仅执行一次 Draft-to-Ready；same-plan retry 从 exact transition 恢复，
  不重复 edit、archive move/commit/push 或 Ready mutation。
- `R338-08`：preview 后 PR identity/HEAD/title/body/scope drift、multiple/closed/fork/mismatch、stale plan/gate/
  review/publication、已有不同 binding、archive conflict 与 unknown stage 均在首个外部 mutation 前阻断。
- `R338-09`：canonical、installed 与 Shared/Codex/Claude/Cursor 投影通过 preset reapply 收敛；完整
  multi-platform Throwaway/Release matrix 保持未验证边界。

本 contribution 不修改 #333/PR #337 真实状态，不重开 #208/#249/#251，不执行 commit、push、PR、merge、
Issue closure、release 或 worktree cleanup。
