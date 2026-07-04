# #17 PR body 质量标准设计

## 设计目标

本任务把 PR body 发布质量分成两层：

- AI 判断层：在 `trellis-finish-work` / workflow 中要求 AI 生成或审查面向 GitHub reviewer 的 PR body readiness，确认内容真实、自解释、风险边界充分。
- 脚本校验层：`publish-pr` 只验证 body file / fallback body 的客观结构、必填 section、禁用低信息量短语、issue close/ref 语义和 validation 非占位，随后执行 push / PR create。

这符合本仓库“Markdown 定义流程，脚本执行事实”的边界：脚本不能替代 reviewer 判断，但可以 fail-closed 阻塞明显不可审阅的 PR body。

## 影响面

- `trellis/workflows/guru-team/workflow.md`：canonical workflow，增加 PR body readiness 与内容质量标准。
- `.trellis/workflow.md`：dogfood active workflow，同步 canonical 内容，保证本仓库运行时注入一致。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`：增加 body file / artifact 支持、body 结构校验、低信息量短语阻塞、fallback body 改写。
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：补单元测试。
- `trellis/presets/guru-team/overlays/**/trellis-finish-work*`：finish 入口要求 AI 先完成 PR readiness body。
- `.agents/skills/trellis-finish-work`、`.codex/prompts/trellis-finish-work`、`.codex/skills/trellis-finish-work`：由 preset apply 同步的 dogfood 副本。
- `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`.trellis/spec/workflow/*`：记录公开质量标准和验证要求。

## PR body 输入合同

新增或复用 `publish-pr` / `finish-work` 参数：

- `--body-file <path>`：AI 审阅后的 Markdown PR body。路径可绝对或相对 repo root。publish 优先使用此文件。
- `--body-artifact <path>`：可选 JSON artifact，供后续扩展。若实现成本较低，可支持 `body_file`、`body`、`ready`、`reviewed_by` 等字段；若本次只实现 body file，也必须在 workflow 中允许 readiness artifact 以 body file 形式落地。

校验规则：

- body 必须包含中文 section：`变更摘要`、`影响范围`、`验证结果`、`Review Gate`、`Issue 关闭范围`、`安全说明`。
- non-draft PR body 不允许主要摘要包含 `当前 Trellis task`、`已提交实现与文档更新`、`详见 artifact` 等低信息量短语。
- `变更摘要` section 必须有至少一个具体 bullet，不能只有泛化占位。
- `影响范围`、`验证结果`、`安全说明` 不能是空、`无` 或 `详见` 占位。
- `Issue 关闭范围` 中只能对 `issue-scope-ledger.json.close_issues` 使用 close keyword；`related_issues` / `followup_issues` 只能是引用或后续语义。现有 ledger 校验继续保留。

## Fallback body 策略

没有 `--body-file` 时，`build_pr_body()` 仍可生成 fallback body，但必须：

- 不再使用 Trellis 内部语境摘要。
- 使用 `Review Gate` summary、changed files / deployment impact、validation lines 和 Issue Scope Ledger 生成更具体的结构。
- 如果 validation lines 缺失，non-draft publish 应被 body 校验阻塞，而不是把 `详见 Trellis task artifact` 当作可发布内容。

## 兼容性

- 新参数为 additive，不破坏已有 `finish-work` 调用；但 non-draft publish 会更严格，旧的低信息量 fallback 在缺少 validation/body file 时会被阻塞，这是 issue 要求的行为变化。
- 默认 `publish.draft=false` 时执行严格校验；draft PR 如后续需要放宽，本任务仍建议校验同一质量标准，避免 draft -> ready 时漏检。
- config template 不需要新增复杂 YAML，避免扩大 `load_config()` 解析面。

## Docs SSOT

长期文档更新集中在现有 README 和 workflow/preset README。任务 planning artifact 只记录本次实现证据；可复用规则补进 `.trellis/spec/workflow/quality-guidelines.md` 或 `workflow-contract.md`。

## 风险与回滚

- 风险：过严的校验误伤合法 PR body。缓解：只检查核心 section 与明确低信息量短语，不要求固定 emoji 或完全固定标题。
- 风险：只改 canonical overlay 忘记 dogfood 副本。缓解：修改 overlay 后运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 和 `check-dogfood-overlay-drift.sh`。
- 回滚：恢复 Python body 校验与 workflow/prompt 文案即可；无数据库、runtime config 或部署资产迁移。
