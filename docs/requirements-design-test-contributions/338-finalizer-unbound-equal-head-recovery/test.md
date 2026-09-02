# #338 Test contribution

- `T338-01`（R338-01）：fresh equal-HEAD、无 transaction fixture 继续返回
  `existing_pr_unbound_equal_head`。
- `T338-02`（R338-02..04）：ordinary/push-content/unbound、remote/PR/Publication equal fixture 返回
  `existing_pr_recovery`、exact PR、`ancestry=equal`、`push_required=false` 与 Ready/Draft action。
- `T338-03`（R338-04/06）：Publication body 与 live body 仅差末尾 LF 时，preview 的 title match 为 true、body
  match 为 false、metadata update required 为 true。
- `T338-04`（R338-05）：conversion 保留 task/repo/base/branch/review/publication/plan/payload/scope identity，写入
  原始 `metadata_comparison`、`metadata_update_required` 与 `bind_pr` recovery，并移除 ordinary
  `pre_push_remote_head` transition field；private schema 同时接受新 shape 和旧 strict-ancestor shape。
- `T338-05`（R338-05/08）：preview-to-execute metadata 漂移返回 `existing_pr_recovery_drift`，transaction write
  call count 为零；unchanged path 恰好写入一次 converted transaction。Equal-HEAD `bind_pr` resume 对缺失或
  内部不一致 decision、live title/body 相对原始 binding 漂移 fail closed，匹配 binding 正常继续。
- `T338-06`（R338-06/07）：existing metadata convergence regression 证明差异路径一次 edit、相等路径零 edit、
  PR create 为零；Ready preservation 与 Draft-to-Ready 现有 fixture 保持通过。
- `T338-07`（R338-07/08）：existing real-topology recovery fixture 保持 archive interruption/retry、force-push、
  scope drift、unknown stage 与 terminal retry 零重复副作用覆盖。
- `T338-08`（R338-09）：运行 canonical/installed Finalizer tests、preset all-platform apply/reapply、dogfood
  drift、ownership/parity、task validation、recursive sidecar scan 与 `git diff --check`。
- `T338-09`（R338-09）：最终报告明确 full multi-platform Throwaway、tag-pinned、Release 与真实 PR #337
  mutation 均未执行。
