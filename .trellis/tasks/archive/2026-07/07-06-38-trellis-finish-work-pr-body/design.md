# #38 设计

## 设计边界

本任务是 Guru Team workflow / preset overlay 的 Markdown 行为合同修订。流程判断继续由 AI 按 workflow/skill/prompt 执行，脚本仍只负责确定性 gate、readiness、archive、journal、publish 校验与执行。

## 官方扩展面核对

- `https://docs.trytrellis.app/advanced/custom-workflow.md`：Trellis workflow 由 `.trellis/workflow.md` Markdown 定义，运行时读取；修改流程文案应改 Markdown，不需要修改 hook Python 或 Trellis 上游源码。
- `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`：spec template marketplace 只放可复用工程约定和 review checklist；本任务不把 active task 或平台 prompt 放入 spec template。

## 变更策略

1. 更新 canonical finish-work overlay：
   - `.agents/skills/trellis-finish-work/SKILL.md`
   - `.codex/prompts/trellis-finish-work.md`
   - `.codex/skills/trellis-finish-work/SKILL.md`
   - `.claude/commands/trellis/finish-work.md`
   - `.cursor/commands/trellis-finish-work.md`
2. 每个入口都用同一顺序：
   - 写 task-local PR body：`{TASK_DIR}/pr-body.md`
   - `finish-work.sh --json --from-trellis-finish-work --body-file "{TASK_DIR}/pr-body.md" --dry-run`
   - dry-run 通过后正式执行：`finish-work.sh --json --from-trellis-finish-work --body-file "{TASK_DIR}/pr-body.md"`
3. 更新 canonical workflow 与 dogfood `.trellis/workflow.md` 中的 helper 示例，避免 workflow 主文案仍展示无 body source 的 finish-work 调用。
4. 运行 preset apply 同步 dogfood 安装副本，再用 drift check 验证 canonical overlay 与 dogfood 副本一致。
5. 添加测试断言直接读取 overlay 文件，确保以后不会回退到无 reviewed body / 无 dry-run 的示例。

## 兼容性

- 不改变 helper CLI 参数；`finish-work.sh` 已支持 `--body-file`、`--body-artifact`、`--dry-run`。
- `--body-artifact` 仍作为替代方式保留，不作为主示例。
- 对已有项目升级时，preset overlay 会把已知 Guru Team 入口更新为新文案；未知本地编辑仍由 installer 写 `.new`，不静默覆盖。

## 风险与回滚

- 风险：只改 canonical overlay 而未同步 dogfood 副本，会让当前仓库仍暴露旧入口。缓解：运行 `apply.sh --repo . --all-platforms` 和 drift check。
- 风险：只改 finish-work skill，不改 workflow 示例，AI 仍可能从 workflow helper sequence 复制旧命令。缓解：同步改 canonical workflow 与 dogfood workflow。
- 回滚：回退本任务的 Markdown 和测试改动即可；没有数据迁移或运行时状态迁移。
