# #38 完善 trellis-finish-work 示例，强制展示 PR body 文件与 dry-run 流程

## 目标

修正 Guru Team `trellis-finish-work` 入口的推荐命令示例，避免 AI 看到无 `--body-file` / `--body-artifact` 的单行示例后直接执行 finish-work，导致 reviewed PR body 缺失问题延后到 finish 阶段才失败。

## 背景与证据

- GitHub Issue: https://github.com/castbox/guru-trellis/issues/38
- 现有 `trellis-finish-work` 文案已经说明 non-draft publish 需要 reviewed PR body，但主命令示例仍是：

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work
```

- 官方 Trellis `custom-workflow` 文档说明 workflow 行为由 `.trellis/workflow.md` 这类 Markdown 在运行时读取，调整流程不需要改 Python、hook 或重新发布 Trellis。
- 官方 Trellis `custom-spec-template-marketplace` 文档说明 spec template marketplace 只承载可复用工程约定、测试规则、review checklist 和去敏示例，不应放 active task 或运行状态；本任务不修改 spec template marketplace 内容。

## 需求

1. `trellis-finish-work` 主入口示例必须优先展示 task-local `--body-file`，并展示先 `--dry-run` readiness preview、再正式执行的顺序。
2. 示例前必须明确先写或审查 task-local PR body，例如 `{TASK_DIR}/pr-body.md`。
3. PR body 必须包含中文 section：`变更摘要`、`影响范围`、`验证结果`、`Review Gate`、`Issue 关闭范围`、`安全说明`。
4. `--body-artifact <path>` 可以作为替代方式保留说明，但示例以 `--body-file` 为主。
5. canonical overlay、Codex/Claude/Cursor/通用入口副本和 workflow 文案不得出现平台语义漂移。
6. 补充测试或快照断言，确保 finish-work skill/overlay 含 `--body-file` 或 `--body-artifact` 示例，并包含 `--dry-run` readiness 预检。

## 范围

### 本次修改

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md` dogfood 副本
- `trellis/presets/guru-team/overlays/**/trellis-finish-work*`
- preset apply 后生成的 dogfood 入口副本
- 相关测试断言
- 必要的 task artifacts

### 不做

- 不修改 Trellis 上游源码、全局 npm 包或 `node_modules`。
- 不改变 `finish-work.sh` / `publish-pr.sh` 的执行语义。
- 不改 spec template marketplace 内容。
- 不创建新的 publish 用户入口。

## Docs SSOT

仓库存在 `docs/requirements/`，其中 `docs/requirements/requirement-main.md` 已记录 non-draft publish 需要 `--body-file` / `--body-artifact` 和 dry-run readiness preview。本任务只收紧入口示例和 overlay 文案，不新增长期产品/架构/API/部署合同；若实现阶段发现 README 或 requirement docs 内存在误导性 finish-work 示例，再同步更新 durable docs。

## 中台知识门禁

不适用。本任务不涉及 go-guru、proto-guru、Unity3D Guru SDK、Flutter Guru SDK 或其它中台 SDK / framework 用法。

## 验收标准

- [ ] `trellis-finish-work` skill / command / prompt 的主命令示例不再只展示无 `--body-file` / `--body-artifact` 的 finish-work 调用。
- [ ] 新文案明确 non-draft publish 前必须先生成或审查 reviewer-readable PR body。
- [ ] 新文案明确先 dry-run，再正式执行。
- [ ] Codex、Claude、Cursor、通用 `.agents` overlay 和 dogfood 副本同步。
- [ ] 测试覆盖 finish-work overlay 示例含 `--body-file` 或 `--body-artifact`，且含 `--dry-run`。
- [ ] dogfood overlay drift 检查通过，无未处理 `.new` / `.bak`。
