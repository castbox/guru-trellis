# #285 Requirements contribution

本 contribution 修复 current `guru-merge-task-pr` 正常路径丢失 reviewed 中文
`chore(merge)` subject/body 的合同断裂，不改变 current shared authority 版本，也不
声明 tag、Release 或生产发布。

- `REQ-021`：`ready_for_merge` 与 `standalone_merge` 的 active input 必须显式携带
  `primary_issue`、中文 `summary`、exact `subject` 与 fixed Chinese `body`；旧 1.0
  schema/example/gate bytes 保持 immutable compatibility。2.0 body 的 canonical form
  以最后一行 `Refs #<primary_issue>` 结束且无尾随换行，与 GitHub commit API 的实际
  持久化正文完全一致。
- `REQ-022`：semantic gate、recorder 与 checker 必须绑定 repo/PR、expected head、
  base/head branches、close scope、reviewed message identity 与 pre-merge base head；
  `primary_issue` 必须属于 reviewed close scope，授权不得持久化。
- `REQ-023`：executor 只执行 repo-bound merge commit 路径，并同时传递
  `--match-head-commit`、唯一 `--merge`、`--subject` 与 `--body-file`；body file 只在
  ignored owner runtime 中短生命周期存在。
- `REQ-024`：post-merge verifier 必须验证 PR merge SHA、双 parents、exact
  subject/body、PR/Issue refs、remote base ref 与 Issue closure/timestamp；任何 mismatch
  不得返回 `merged`。
- `REQ-025`：保留 `merged|merge_blocked|closure_mismatch`、expected-head、close-scope、
  terminal recovery，以及零主动 Issue close、零 local main sync、零 task cleanup。
- `REQ-026`：canonical、dogfood、installed、Shared/Codex/Claude/Cursor、preset/eval/
  closeout harness 必须一致；普通 Issue 只要求一个代表性 clean throwaway install/update
  与一个单独确认后的隔离 GitHub live merge proof。

未纳入：#223、#106、#247/#249/#250/#261/#248/#252、#283、#267、仓库/org
rules、Trellis upstream、历史重写、tag/Release 与生产部署。
