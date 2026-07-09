# #56 branch type 的前缀不要固定 codex，应该自动判定

## Goal

让 Guru Team `prepare-task` 在未显式传入 `--branch` 时，根据请求或 GitHub issue 的变更类型生成 Conventional Branch 前缀，不再固定使用 `codex/`。

## Background

- Source issue: https://github.com/castbox/guru-trellis/issues/56
- Issue 标题: `branch type 的前缀不要固定 codex，应该自动判定`
- Issue 正文列出的合法分支类型为 `feat`、`fix`、`refactor`、`perf`、`test`、`docs`、`style`、`build`、`ci`、`chore`、`revert`。
- 当前证据显示默认分支前缀固定在 `trellis/workflows/guru-team/config-template.yml` 的 `branch_prefix: "codex/"`，并由 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 的 `DEFAULTS.branch_prefix` 与 `prepare_naming_payload()` 拼装成 `codex/<slug>`。
- README、workflow README、canonical workflow 与 dogfood workflow 仍公开推荐 `codex/NNN-business-capability`。

## Requirements

1. `prepare-task` 在 `--branch` 缺省时，必须生成 `<branch-type>/<NNN-business-capability>` 格式。
2. `branch-type` 必须属于 issue 正文列出的 11 个类型之一。
3. 脚本必须使用确定性规则推断类型，不得调用 AI、LLM、网络服务或 Trellis 上游源码。
4. 显式 `--branch` 必须保持最高优先级，脚本只对自动分支名生效。
5. 旧配置中的 `branch_prefix` 必须继续被解析，避免旧安装直接失败；新默认行为必须不再依赖 `codex/`。
6. `naming_quality.suggested_override_flags` 必须输出自动判定后的 branch type 示例，避免继续提示 `--branch codex/...`。
7. 单测必须覆盖至少 `feat`、`fix`、`docs`、`test`、`ci`、`build`、`refactor`、`perf`、`style`、`chore`、`revert` 的显式类型或关键词映射，并覆盖 unknown fallback。
8. Durable docs 必须同步更新旧的 `codex/NNN-business-capability` 文案。

## Acceptance Criteria

- [ ] 未传 `--branch` 且 issue/request 文本含 `docs` 或文档更新语义时，`payload.branch_name` 为 `docs/<slug>`。
- [ ] 未传 `--branch` 且文本含 bug/fix/修复语义时，`payload.branch_name` 为 `fix/<slug>`。
- [ ] 未传 `--branch` 且文本无可识别类型时，`payload.branch_name` 使用安全 fallback 类型 `chore/<slug>`。
- [ ] 显式传入 `--branch custom/slug` 时，`payload.branch_name` 保持 `custom/slug`。
- [ ] `config-template.yml` 不再把新安装默认前缀固定为 `codex/`。
- [ ] README、workflow README、canonical workflow 与 dogfood workflow 不再推荐 `codex/NNN-business-capability`。
- [ ] `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 通过。
- [ ] 标准 workflow/preset validation 命令通过，或在最终报告中逐项说明未验证项。

## Out Of Scope

- 不创建新的 GitHub issue。
- 不改变 task slug、workspace slug、issue close ledger 或 PR publish 语义。
- 不修改 Trellis 官方 npm 包、`node_modules` 或上游源码。
- 不实现 AI 语义分类器；本次只实现可审计的关键词和显式类型规则。

## Docs Impact

本次改变长期公开的 Guru Team workflow 行为，durable docs 状态为 `partial_docs`：已有 README、workflow README、requirements 与 workflow 文档，但当前分支格式说明与目标行为冲突。策略为 `ssot_first`，实现时必须先同步 canonical workflow/docs，再调整脚本和测试。
