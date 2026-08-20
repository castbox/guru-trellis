# #285 Test contribution

- `SCN-017`：active 2.0 input/gate schemas、examples、Interface selector 与 Finalizer
  authoring seed 通过；1.0 input/gate/example 固定 hash 保持不变，cross-version substitution
  被拒绝。
- `SCN-018`：message tests 接受合规中文 summary/subject/body，拒绝 GitHub 默认
  `Merge pull request ...`、直接 PR title、错误 PR/primary Issue、primary Issue 不在
  非空 close scope、非中文/占位摘要、段落/refs 漂移、body 尾随换行，以及
  summary/subject/body 任意位置的 Issue close-keyword 引用，包括九种词形与 local /
  `owner/repository#issue` 引用；同时接受 `expected_close_issues=[]` 且保留
  `primary_issue` 引用的合法 refs-only merge；live PR close-scope parser 接受九种 local
  close-keyword 词形并拒绝无法映射到当前 `list[int]` ledger 的跨仓关闭引用。
- `SCN-019`：executor tests 精确断言 repo binding、expected head、唯一 `--merge`、
  `--subject`、`--body-file`、body bytes、失败 cleanup 与 terminal recovery 零重复 mutation；
  即使 live repository 同时允许 squash/rebase，recorder/checker 也拒绝非 `merge` route。
- `SCN-020`：post-merge tests 拒绝 PR/merge SHA、双 parents、subject/body、pre-base、
  remote base、Issue closure/timestamp 任一漂移，并保持三个 typed exits。
- `SCN-021`：source/installed package、contract/eval、installed closeout fake GitHub、preset
  apply/reapply、ownership、dogfood drift、all-platform parity 与 recursive zero sidecars 通过。
- `SCN-022`：代表性 clean throwaway install/update 使用完整 preset runtime，验证 active
  Merge package、2.0 input、executor message 参数与 post-merge verifier；不冒充 release-wide
  多平台矩阵。
- `SCN-023`：经独立副作用确认后，隔离 GitHub repository 的真实 PR 在
  expected-head 绑定下产生合规中文 merge commit，并验证 subject/body、parents、remote
  base 与 Issue closure；proof 资源按已展示计划清理。

2026-08-20 live proof：临时 private repository
`wesleywu/guru-trellis-285-merge-proof-20260820` 中，默认
`Merge pull request ...` subject 被 public preview 以非零退出拒绝，stale expected head
被明确报告为 `expected head SHA changed`，两者均未触发 mutation。第一次真实 merge
揭示尾随换行与 GitHub 持久化正文不一致并被 post-merge verifier 阻断；修正后 PR #4
绑定 expected head `ac59fd712a5d0d5f11ada22f367710c0fee00a96`，以 pre-merge base
`2928f24d5bd86ce0bbf72ad72b73f48e85b02949` 生成双亲 merge commit
`f501a012f323bbac5f46517cfd4cf368927fed58`。commit subject/body 与 reviewed bytes
完全一致，remote `main` 指向该 SHA，Issue #3 在 merge 后关闭，private gate 与
`merge-body.md` 均为零；随后删除整个临时 repository 与本地 proof 目录。
