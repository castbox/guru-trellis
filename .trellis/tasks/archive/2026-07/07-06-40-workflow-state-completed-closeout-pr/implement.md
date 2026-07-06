# 实施计划：completed closeout breadcrumb

## 前置结论

- Issue #40 仍存在：`[workflow-state:completed]` 仍是旧的一句话。
- 原建议方案没有过时，但近期 PR 已经解决了 finish-work 入口和脚本层的多数内容，因此本任务只做 workflow breadcrumb 同步和测试。
- 官方文档依据见 `research/official-trellis-workflow-docs.md`。

## 执行步骤

1. 更新 canonical workflow：
   - 修改 `trellis/workflows/guru-team/workflow.md` 的 `[workflow-state:completed]`。
   - 保持 tag 格式不变，避免破坏 parser。
2. 同步 dogfood active workflow：
   - 对 `.trellis/workflow.md` 做同样修改。
3. 补 hook 回归测试：
   - 在 `.codex/hooks/test_inject_workflow_state.py` 增加 completed breadcrumb 测试。
   - 测试只验证 workflow parser 读取文案，不把业务逻辑写进 hook。
4. 运行验证：
   - `python3 .codex/hooks/test_inject_workflow_state.py`
   - `python3 ./.trellis/scripts/get_context.py --mode phase`
   - `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
   - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-06-40-workflow-state-completed-closeout-pr`
   - `git diff --check`
5. 记录 Phase 2 check：
   - 覆盖 requirements、design、code、tests、spec_sync、docs_ssot、cross_layer、security、deployment。
6. 提交与 review gate：
   - 只 stage 本任务相关文件。
   - 提交后进行独立 Branch Review Gate。

## Docs SSOT 与 overlay

- 长效 docs SSOT 是 workflow Markdown 本身；README 已覆盖 finish-work closeout 入口，本任务没有新增公开命令。
- 未计划修改 `trellis/presets/guru-team/overlays/`；如果后续 diff 确认无 overlay 改动，dogfood overlay apply/drift 门禁不适用。

## 回滚

如测试或 review 发现 breadcrumb 过长或语义误导，回滚 workflow block 到旧文案并重写为更短版本；不涉及数据迁移或脚本行为回滚。
