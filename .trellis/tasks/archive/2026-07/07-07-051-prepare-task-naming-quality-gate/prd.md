# #51 修正 prepare-task 命名质量门禁

## Goal

修正 Guru Team `prepare-task` 的 slug / branch / worktree / task 命名门禁，避免脚本在中文或语义不足的 issue 标题上静默创建 `issue-52`、`52-issue-52` 等低信息名称。脚本只做确定性拼装、冲突检查和质量阻断；语义英文 short-name 必须由 agent 读完 issue 后显式传入。

## Requirements

- `prepare-task --json` 只读输出必须新增 `naming_quality` 字段，至少包含：
  - `ok: boolean`
  - `reason: string`
  - `requires_semantic_name: boolean`
  - `current_slug`
  - `suggested_override_flags`
- 保留英文标题的确定性自动命名能力；当自动 slug 包含足够业务 token 时，planner 和 executor 都应允许继续。
- 对中文、非 ASCII、或无法提取足够业务 token 的标题，脚本不得引入第三方 transliteration、不得机械转拼音、不得假装理解中文语义。
- 只读 planner 可以继续输出 branch/workspace/task 计划，但必须标记 `naming_quality.ok=false` 且 `requires_semantic_name=true`，提示 agent 使用显式语义覆盖参数。
- `--create-worktree` / `--create-task` executor 路径必须阻断低信息命名；错误信息必须明确指出使用 `--short-name` / `--workspace-slug` / `--branch` / `--task-slug` 覆盖。
- 显式覆盖参数优先于自动生成，但覆盖值本身低信息时，create 路径也必须阻断，不能静默创建。
- 需要识别的低信息 slug 至少包括：
  - `issue-<n>`
  - `<n>-issue-<n>`
  - 只含编号
  - 只含 `bug`、`fix`、`task`、`work`、`update`、`change` 等通用词
  - 过短、无业务关键词、或业务 token 数不足
- 推荐命名格式必须写入 workflow / README：
  - worktree/task slug: `NNN-business-capability`
  - branch: `codex/NNN-business-capability`
  - 示例：`052-resume-detail-inline-attachment-preview`

## Acceptance Criteria

- [ ] 英文 issue title 可自动生成有业务语义的 slug，并通过 `naming_quality.ok=true`。
- [ ] 中文 issue title `简历详情页的原始简历查看功能应该强化` 在未传显式语义名称时，不得创建 `52-issue-52`；只读输出标记 `requires_semantic_name=true`。
- [ ] 中文 issue title 未传显式语义名称时，`--create-worktree` / `--create-task` 路径返回用户可操作错误并阻断。
- [ ] 显式传入 `--short-name 052-resume-detail-inline-attachment-preview` 等覆盖参数时，通过 quality gate，并生成对应 worktree/task/branch 名称。
- [ ] 低信息显式覆盖如 `--short-name issue-52` 在 create 路径被阻断。
- [ ] `naming_quality` 被写入 planner stdout JSON、handoff JSON 和 intake-handoff schema。
- [ ] canonical workflow、dogfood `.trellis/workflow.md`、README / workflow README / preset README 说明 agent 负责语义英文 short-name，prepare 脚本负责确定性拼装、冲突检查和低信息命名门禁。
- [ ] canonical 脚本、preset 脚本、dogfood 安装副本保持一致，无 overlay drift。
- [ ] 相关单元测试与最小 CLI 验证通过。

## Notes

- Issue: https://github.com/castbox/guru-trellis/issues/51
- 官方 Trellis 扩展边界已核对：workflow 行为放在 Markdown workflow，脚本只做确定性 executor / validator / recorder。
- Docs SSOT：本仓库 README、workflow README、preset README 是用户安装与日常入口说明；本任务需要同步更新。
- Middle-platform Knowledge Gate：不适用，本任务只修改 Trellis workflow companion script / docs / tests。
