# #435 Active Task Delivery Loop Design contribution

状态：`candidate`。采用 `target_native`，Architecture candidate 为
[`ADR-012`](../../architecture/adr/012-active-task-delivery-loop.md)。

- `D435-01`：`guru-review-task-delivery` 使用 semantic profile：AI authoring -> private recorder -> objective
  checker -> one typed projection。成功投影退休 checkpoint；semantic output丢失必须 fresh重跑。
- `D435-02`：`guru-publish-task-delivery` 使用 Delivery-only transaction：`push_content -> bind_pr ->
  converge_metadata -> mark_ready -> ready`。每个 mutation前fresh reread并先持久化同计划恢复所需最小私有
  state；terminal `ready` 可零mutation重物化 DTO。
- `D435-03`：`guru-merge-task-delivery` 在 current semantic gate 后展示一次 exact action plan，使用
  `gh pr merge --merge --match-head-commit --subject --body-file`。post-read验证 exact message、parents、base与
  reviewed head；已合并事实支持零第二merge恢复。
- `D435-04`：merge message trailers 是 versioned closed identity：`Guru-Task-Identity`、
  `Guru-Delivery-Schema: 1`、`Guru-Delivery-Head`。Discovery 以 repository/base/PR/commit/parents交叉验证，
  不新增 ledger 或 PR-body identity reader。
- `D435-05`：Delivery Review/Publish/Merge public DTO 每个 exit 独立 schema，只包含唯一 consumer 必需字段。
  Confirmation只存在当前对话，不进入 gate、transaction、output或archive。
- `D435-06`：Planning/Check/Branch Review加入 slice、remaining与independent conditions semantic evidence；
  Task Commit继续消费 fresh Check并拥有 exact staged commit，不新增通用dirty commit入口。
- `D435-07`：Reconcile新增 resolved candidate profile，绑定 HEAD、MERGE_HEAD、stage-0 tree、index digest、
  ordered parents、message、task/worktree/branch与fresh Check DTO；零 unresolved/unstaged/untracked/其他 sequencer。
  已存在同parents/tree/message commit时只恢复。
- `D435-08`：registry登记三个 active/deferred packages，installer完整分发 canonical package与声明平台投影；
  installed workflow validator只对 `integrated` rows要求mandatory markers。
- `D435-09`：#435不修改production workflow markers。#434在#435/#436 ready后一次切换；不存在 old-output
  adapter、dual runtime graph、squash/rebase fallback或Delivery ledger。
