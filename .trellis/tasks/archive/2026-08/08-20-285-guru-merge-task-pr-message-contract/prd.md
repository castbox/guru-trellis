# #285 修复 guru-merge-task-pr 中文 merge message 承接

## 目标与用户价值

恢复正常 `guru-merge-task-pr` 路径对 reviewed 中文 `chore(merge)` subject/body 的唯一、完整、可验证承接，使维护者无需一次性人工 workaround，也能在 expected-head 保护下生成符合仓库质量合同的 GitHub merge commit。

## 背景与已确认事实

- Live Issue #285 于 2026-08-20 仍为 `OPEN`，无评论覆盖正文；前序 #260 已通过 PR #284 完成，当前 `main` 与 `origin/main` 均为 `11d150dece429f75e1c1609e1bf54fe039e6bb29`。
- `format-merge-commit` 已能生成固定中文 subject/body 和带 `--subject`、`--body-file` 的 merge 命令；现有合同示例位于 `.trellis/spec/workflow/data-contracts.md:1146`。
- current executor 只传递 repo binding、`--match-head-commit` 和 merge method，未消费 subject/body：`trellis/skills/guru-team/packages/guru-merge-task-pr/runtime/owner.py:923`。
- current package test 只断言 expected-head，并保护“不直接关 Issue、不同步 main、不清理资源”的边界：`trellis/skills/guru-team/packages/guru-merge-task-pr/tests/test_contract.py:412`。
- current `ready_for_merge` public input 只含 PR/head/base/close scope；Finalizer output 通过 target-authored consumer seed 交给 Merge Skill，语义 owner 可补充 authoring fields，无需扩大 Finalizer 的持久化输出。
- `Current Merge Gate And Results` 只声明 expected-head 与 merge method，和 formatter 合同不一致：`.trellis/spec/workflow/data-contracts.md:1375`。

## 范围内需求

### R1. Active public input 与 authoring contract

1. 为 `ready_for_merge` 和 `standalone_merge` 建立新版本 public input schema，新增最小 `reviewed_merge_message`：
   - `primary_issue`
   - `summary`
   - `subject`
   - `body`
2. Finalizer 保持现有 seed output；只更新它对 Merge Skill 的 consumer authoring contract，使 Merge semantic owner 在 invocation 前完成 message authoring/review。
3. current 1.0 input/gate schema 与示例保持 immutable compatibility asset；active Interface 显式选择新版本，不静默改变旧 schema bytes。

### R2. Semantic merge gate

AI Review Gate 必须同时审查：

- summary 为具体中文摘要；
- subject 精确符合 `chore(merge): #{pull_request} 合并 #{primary_issue} {summary}`；
- body 精确符合固定中文段落合同，PR、primary Issue、head/base 引用一致；
- body 不含 `Closes`、`Fixes`、`Resolves`、`Close`、`Fix`、`Resolve` close keyword；
- PR number/URL、primary Issue、expected head、base/head branch、close scope 与 live authority 一致；
- merge method、checks、reviews、mergeability、repository policy 和 Issue 状态继续满足现有 gate。

### R3. Recorder、checker 与 private state

- private gate 绑定完整 current public input、live PR/facts、expected head、pre-merge base head、选定 merge method 和 reviewed message identity。
- recorder/checker 不记录用户授权，不代替语义判断。
- stale head、branch、close scope、message、PR/Issue identity 或 live base head 均 fail closed。

### R4. Deterministic executor 与短生命周期 body file

- 执行唯一 repo-bound 命令：
  `gh pr merge <pr> --repo <repo> --match-head-commit <sha> --merge --subject <subject> --body-file <ephemeral-file>`。
- body file 仅写入 gitignored owner-private merge runtime 目录，内容必须与 reviewed body bytes 一致。
- 正常成功、命令失败、terminal recovery 和最终 output consumer 均清理 body file；未知 residue fail closed。
- 保留现有幂等 terminal recovery，不重复 merge mutation。

### R5. Post-merge live verifier

合并后重新读取并验证：

- PR 为 `MERGED`，merge SHA 完整；
- merge commit 恰有两个 parents，第一 parent 等于 gate 记录的 pre-merge base head，第二 parent 等于 expected head；
- commit subject/body 与 reviewed bytes 完全一致；
- subject/body 中 PR 与 primary Issue 引用正确且 body 无 close keyword；
- remote expected base branch 指向该 merge SHA；
- GitHub 对 `expected_close_issues` 的关闭结果和时间仍满足现有规则。

### R6. Canonical、installed 与平台一致性

同步下列表面：

- canonical package、registry/interface/contracts/consumers；
- dogfood `.trellis/guru-team/**`；
- shared `.agents/skills/**`；
- Codex、Claude、Cursor 及仓库声明支持的全部平台 projection；
- preset installer、installed manifest/runtime、README、workflow/spec/data contracts/quality guidelines；
- examples、evals、package/runtime/contract tests 与 installed closeout fake GitHub harness。

### R7. 文档 SSOT

- 通过 RDT `task_impact_sync` 建立 #285 contribution，记录 Requirements、Design、Test 与 traceability。
- 本次不改变系统域、组件 ownership 或 target architecture，Architecture Baseline 判定为 `no_change`；若实现中发现真实 ownership 变化，必须先重新澄清 scope。
- 不直接覆盖 current `.37` authority；promotion 由 RDT Skill 按当前合同决定。

## 验收标准

1. Active public input、private gate、recorder/checker/executor/post-verifier 均显式承接 reviewed subject/body，并保持 public/private 分层。
2. executor 精确包含 repo binding、`--match-head-commit`、唯一 `--merge`、`--subject`、`--body-file`。
3. 测试拒绝 GitHub 默认 `Merge pull request ...`、直接 PR title、错误/缺失 PR 或 primary Issue、非中文摘要、缺段落/引用、close keyword、stale head/base/message/live authority。
4. 测试接受合规中文 subject/body，并验证临时文件内容、参数、清理和 terminal recovery 零重复 mutation。
5. post-merge verifier 验证 SHA、双 parent、subject、body、PR、primary Issue、remote base identity 和 Issue closure，而非只看 merge SHA。
6. canonical/dogfood/preset/installed/全部声明平台 projection 无漂移；旧 1.0 compatibility bytes 不被改写。
7. package、runtime、contract、eval、preset apply/reapply、dogfood drift 和代表性 clean throwaway install/update 通过。
8. 至少一个隔离 GitHub repository 的 live proof 证明默认路径被阻断，正常 Skill 路径在 expected-head 绑定下产生合规中文 merge commit。
9. `guru-merge-task-pr` 保留原有三 typed exits、merge method、close-scope、mergeability、recovery，以及不主动关 Issue、不同步本地 main、不清理 task resources 的边界。
10. PR 仅关闭 #285；不吸收或修改 #223、#106、#247/#249/#250/#261/#248/#252、#283、#267。

## 明确不在范围

- 不改写既有 `main` 历史。
- 不创建 GitHub App，不修改 repository/org ruleset、branch protection、权限或 bypass actor。
- 不实现自动合并 authority、required CI 配置或 Draft/Ready 时序。
- 不修改 Trellis upstream、全局 npm 包、tag、Release 或生产环境。
- 不创建 repair Issue，不修改其他 Issue 正文。

## 关键决策

- reviewed message 由 Merge Skill semantic owner 在 Finalizer seed 之后 author，不扩大 Finalizer output；这样 message 仍受当前 live PR/Issue/head/base gate 约束。
- 使用新版本 public input/gate schema 并保留 1.0 immutable assets，避免静默破坏公共 API。
- post-merge parent 校验绑定 pre-merge base head 与 expected head，证明实际 merge commit 是本次 reviewed merge，而非仅验证一个返回 SHA。
- body file 只作为 GitHub CLI 的短生命周期 executor 适配，不成为 public artifact 或长期 gate authority。

## 阻塞问题

无。Issue 正文、现有公共 I/O graph、formatter 合同和仓库范围边界已确定产品与兼容性决策。
