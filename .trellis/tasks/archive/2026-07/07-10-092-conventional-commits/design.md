# #92 设计

## 设计目标

以 Markdown workflow 合同承载 AI 判断流程，以 companion script 承载 objective 校验与格式化，强制 `guru-team` workflow 使用中文 Conventional Commits。实现必须覆盖 canonical source、dogfood copy、preset installer、公共文档和测试。

## Docs SSOT Plan

- docs state：`partial_docs`
- evidence paths：
  - `trellis/workflows/guru-team/workflow.md`
  - `.trellis/workflow.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
- strategy：`ssot_first`
- reason：本任务修改长期 workflow / publish / merge 合同，必须先把 durable workflow 与 spec 写成 SSOT，再按 SSOT 实现脚本和测试。
- affected durable docs：
  - `trellis/workflows/guru-team/workflow.md`
  - `.trellis/workflow.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
- task artifact deltas to merge back：issue #92 的 subject/body/merge 规则、validator 入口、finish/publish metadata commit 规则、开箱验证清单。
- merge checkpoint：Phase 2 check 前，durable workflow/docs/spec 必须已更新并被测试覆盖。
- task-history-only content：Phase 0 handoff、规划审批记录、review gate 记录、PR readiness 记录只保留在 task artifact。

## 分层

### Markdown 合同层

修改 `trellis/workflows/guru-team/workflow.md`，并同步 `.trellis/workflow.md`。合同必须定义：

- 工作提交 subject：`{type}({scope}): #{primary_issue} 中文描述`
- metadata 提交 subject：同格式，metadata 动作用中文表达，body 为空
- merge commit subject：`chore(merge): #{pull_request} 合并 #{primary_issue} 中文 PR 摘要`
- 工作提交 body 固定小节与 `Refs`
- merge commit body 固定小节与 `PR` / `Refs`
- `Closes` 只能出现在 PR body 的 close scope
- Phase 2 check、Branch Review Gate、PR readiness 必须检查 commit message 合同

### Companion script 层

在 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 增加纯函数和 CLI：

- `validate_commit_subject`
- `validate_work_commit_body`
- `validate_metadata_commit_body`
- `validate_merge_commit_body`
- `check-commit-messages`
- `format-merge-commit`

脚本只做格式、字段、路径、Git history 的客观校验和 subject/body 格式化。脚本不得判断业务范围是否足够、review 是否充分、issue 是否能关闭。

### Finish / publish 接入

- finish-work metadata commit message 使用 `chore(trellis): #<primary_issue> 固化任务收尾元数据`。
- publish 在 dry-run 和正式输出中包含 `merge_commit.subject`、`merge_commit.body`、`merge_commit.command`。
- 正式 publish 创建 PR 后从 PR URL 提取 PR number，再生成无 placeholder 的 merge commit 指令。
- dry-run 在 PR number 未存在时使用 `<pull_request>` placeholder，并在 payload 标记 `ready=false`。

### Preset / dogfood 同步

修改 canonical 后运行：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

若 installer 更新 `.trellis/guru-team/scripts/` dogfood copy，必须把这些 installed copy 纳入本分支。

## 数据合同

### commit message check payload

`check-commit-messages --json` 输出：

```json
{
  "status": "ok|blocked",
  "base_ref": "origin/main",
  "head": "<sha>",
  "range": "origin/main..HEAD",
  "primary_issue": 92,
  "checked_commits": [],
  "errors": []
}
```

### merge commit payload

publish payload 新增：

```json
{
  "merge_commit": {
    "ready": true,
    "subject": "chore(merge): #91 合并 #92 中文 Conventional Commits 提交规范",
    "body": "合并：\n...",
    "command": ["gh", "pr", "merge", "91", "--merge", "--subject", "...", "--body-file", "<path>"]
  }
}
```

`command` 中的 body file 路径只能指向临时文件或提示 payload body 写入文件；脚本不自动执行 merge。

## 兼容性

- 旧安装缺少新增配置字段时，脚本使用内置常量运行。
- 新 CLI 命令向后兼容；已有 `prepare-task`、`record-phase2-check`、`review-branch`、`publish-pr`、`finish-work` 参数保持不变。
- metadata commit subject 变更只影响本任务后生成的提交，不改写历史。

## 风险与控制

- 风险：校验器误把 AI 判断写入脚本。控制：脚本只检查正则、section、footer、Git diff metadata path。
- 风险：只改 dogfood copy。控制：所有 runtime 改动先落在 `trellis/workflows/guru-team/scripts/` 与 `trellis/workflows/guru-team/workflow.md`。
- 风险：publish 输出 merge 指令但 README/workflow 未说明。控制：workflow README、preset README 与 workflow 同步。
- 风险：开箱验证取 public remote 而非当前分支。控制：记录验证 source；若无法验证当前分支 marketplace，最终报告明确未覆盖项。

## 回滚

- 若脚本校验误伤，回滚 Python helper、wrapper、README 和 workflow 文案同一组提交。
- 若 dogfood apply 产生冲突，停止实现并记录 `.new` / `.bak` 路径，不提交未审查副本。
