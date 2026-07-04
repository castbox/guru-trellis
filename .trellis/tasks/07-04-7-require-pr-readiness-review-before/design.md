# 设计：#7 PR readiness source 门禁

## 总体设计

本任务在现有 `finish-work -> publish-pr` 流程上增加 reviewed body source 门禁。核心原则：

- #17 继续负责 PR body 内容质量标准。
- #7 只负责发布机制：non-draft publish 必须有 AI-reviewed source。
- `reviewed-pr-body.md` / `pr-readiness.json` 是 task metadata，最终 publish 读取 archive 后 artifact。
- companion script 只做 executor / validator / recorder，不替代 AI readiness 判断。

## 受影响资产

### Canonical runtime

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/README.md`

### Preset / overlay

- `trellis/presets/guru-team/README.md`
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-finish-work/SKILL.md`
- `trellis/presets/guru-team/overlays/.codex/prompts/trellis-finish-work.md`
- `trellis/presets/guru-team/overlays/.codex/skills/trellis-finish-work/SKILL.md`
- `trellis/presets/guru-team/overlays/.claude/commands/trellis/finish-work.md`
- `trellis/presets/guru-team/overlays/.cursor/commands/trellis-finish-work.md`

### Dogfood copies

- `.trellis/workflow.md`
- `.agents/skills/trellis-finish-work/SKILL.md`
- `.codex/prompts/trellis-finish-work.md`
- `.codex/skills/trellis-finish-work/SKILL.md`
- `.claude/commands/trellis/finish-work.md`
- `.cursor/commands/trellis-finish-work.md`

## 数据与路径合同

### Reviewed source 类型

`resolve_pr_body()` 继续支持三类 source：

1. `body-file:<path>`
2. `body-artifact:<path>`
3. `generated`

新增规则：

- non-draft publish：只允许 `body-file:*` 或 `body-artifact:*`。
- draft publish：允许 `generated`，但仍必须通过 #17 的客观 body quality checks。
- dry-run：应返回 payload，包含 `body`、`body_source`、`reviewed_source_required`、`reviewed_source_ok`，便于 AI 审阅；如果真实 non-draft 会被阻塞，dry-run 不应执行副作用。

### Readiness artifact

`--body-artifact` JSON 至少支持：

```json
{
  "ready": true,
  "body_file": "reviewed-pr-body.md"
}
```

或：

```json
{
  "ready": true,
  "body": "## 变更摘要\n..."
}
```

客观校验：

- `ready` 必须为 `true`；缺失、`false` 或其它值都不能作为 non-draft publish readiness evidence。
- 必须有非空 `body` 或 `body_file`。
- 相对 `body_file` 以 artifact 所在目录为基准解析。
- body 内容继续走 #17 的 `validate_pr_body_quality()`。

### Archive 后路径解析

新增 helper 负责把 active task 路径映射到 archived task 路径：

- 输入 `.trellis/tasks/<task>/reviewed-pr-body.md`
- archive 之后映射为 `.trellis/tasks/archive/YYYY-MM/<task>/reviewed-pr-body.md`

适用范围：

- `finish-work` 内部 publish 参数。
- 用户传入 absolute path 时，如果 path 位于 active task dir 下，也应映射为 archived task path；否则保持原路径。
- artifact 内相对 `body_file` 不在这里预先改写，由 `load_pr_body_artifact()` 以 artifact 所在目录解析。

## 流程设计

### finish-work 前夕

AI 在 active task 目录写：

- `review.md`
- `review-gate.json`
- `reviewed-pr-body.md` 或 `pr-readiness.json`

这些均是 Trellis metadata，可以未提交。

### finish-work 执行

1. 校验 `--from-trellis-finish-work`。
2. 校验 Branch Review Gate，允许 metadata-only tail。
3. 校验无 non-metadata dirty path。
4. 对 non-draft publish 做 readiness preflight：
   - 必须有 `--body-file` 或 `--body-artifact`。
   - active task 路径必须存在并可读取。
   - body/artifact 客观可解析，body quality checks 通过。
5. `task.py archive` 移动 task。
6. `add_session.py` 写 journal。
7. 提交剩余 metadata。
8. 把 body source 参数映射到 archived task path。
9. 内部调用 `cmd_publish_pr()`，从 archived artifact 读取 body。

### publish-pr 执行

1. 校验调用来源：finish-work 内部或 recovery flag。
2. 校验 dirty state、review gate、issue ledger。
3. 解析 body source。
4. 校验 body quality。
5. non-draft 且 source 为 `generated`：阻塞。
6. dry-run 返回 payload；真实发布执行 `git push` 和 `gh pr create`。

## 兼容性

- 旧任务如果没有 reviewed body source，non-draft publish 将失败，这是有意的安全收紧。
- draft/recovery preview 仍可用 generated body 辅助检查 body 格式。
- 不新增 config 字段，避免升级配置迁移。
- 不改变 Issue Scope Ledger、Review Gate JSON schema。

## 风险与缓解

- 风险：archive 前 preflight 通过，但 archive 后路径映射错误。缓解：新增单测覆盖 active task path -> archived task path，以及 artifact 内相对 `body_file`。
- 风险：`task.py archive` 默认可能 auto-commit archive，导致 metadata commit 分裂。缓解：不依赖单一 metadata commit；只要求 publish 读取 archive 后已存在 artifact。
- 风险：dry-run 语义不清。缓解：payload 中明确 `reviewed_source_required` 与 `reviewed_source_ok`。
