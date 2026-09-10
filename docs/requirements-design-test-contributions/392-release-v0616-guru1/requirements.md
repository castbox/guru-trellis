# #392 Release v0.6.16-guru.1 Requirements contribution

状态：`reviewed_promoted`；predecessor：
`current-main-0.6.5-guru.47` / `immutable superseded`；promoted successor：
`current-main-0.6.5-guru.48` / `active`。

本 contribution 绑定 live Issue
[#392](https://github.com/castbox/guru-trellis/issues/392) 与 task
`392-release-v0616-guru1`。它已由 serialized promotion owner 投影为 `.48` shared
Requirements/Design/Test authority；`.47` 仅保留为 immutable superseded predecessor。

- `R392-01`：canonical、dogfood 与 installed manifest 必须一致声明 Guru Team
  extension `0.6.16-guru.41`；target、required 与 tested Trellis CLI 均保持
  `0.6.16`。
- `R392-02`：current release-facing README、workflow/preset 文档、fixture、schema、
  validator 与稳定安装入口必须收敛到唯一 mapping：repository tag / GitHub Release
  `v0.6.16-guru.1`、extension `0.6.16-guru.41`、CLI `0.6.16`、framework source
  `castbox/Trellis@ad332e3fe5a19d7274cb03e7c2f3e2128f8de291`。
- `R392-03`：current surfaces 必须删除旧 target、旧候选状态与
  “`v0.6.15-guru.6` 尚未发布”等过期陈述；历史 released/superseded 文件继续保留
  当时事实。
- `R392-04`：Requirements、Design、Test 与 Architecture 必须从 immutable predecessor
  `.47` 派生唯一 `.48` successor，并建立 #392 requirement/design/test/scenario 与
  Architecture contribution trace；serialized promotion 前 `.48` 只可称为 candidate。
- `R392-05`：Stage 1 preparation 必须在 serialized Architecture/RDT promotion 前后
  分别完成 fresh Phase 2、task commit 与覆盖 `origin/main...HEAD` 的独立 Branch Review；
  repository-private release orchestration 的四平台投影必须承接该顺序。任何 open P0-P3
  finding 或 promotion-created 未复核 diff 均阻止进入 Publication/Finish owner。
- `R392-06`：preparation PR 合并后必须 fresh-fetch `origin/main` 并冻结一个 commit/tree
  exact candidate；Stage 1 HEAD、#378 focused evidence 或其他 SHA 的结果不得复用。
- `R392-07`：同一 exact candidate 必须完成 #392 与 release contract 要求的
  source/installed、四平台投影、ownership、dogfood drift、clean/existing install、update、
  workflow preview/switch、preset reapply、Fork source/build、代表性业务仓库 installed
  smoke、secret scan 与递归 residue 验证。
- `R392-08`：task commit、push、PR、merge、annotated tag、tag-pinned smoke、GitHub
  Release、Issue close 与 cleanup 必须分别读取 live authority，并在各自 owner/动作边界
  独立处理；一个动作的确认不得授权另一个动作。
- `R392-09`：发布流程不得创建 task-local release notes、PR/Release body handoff、动态
  checklist 或 tracked lifecycle 状态，也不得持久化 HEAD、Gate 结果、时间或用户授权。

`BEH-017`：发布生命周期先交付 Stage 1 preparation bytes，再在合并后从 fresh
`origin/main` 建立 Stage 2 exact candidate；任何 required `FAIL`、`SKIP`、stale、
cross-SHA 或 unknown/multiple/unmapped exit 都在 release mutation 前停止。

以上条目已 promotion 为 `.48` current authority。该 promotion identity 只证明稳定
predecessor/successor 与 shared-current 关系；promotion-created diff 仍需由后续 owner 执行
fresh Phase 2、commit 与独立 Branch Review，且不证明 Publication、merge 或发布结果。
