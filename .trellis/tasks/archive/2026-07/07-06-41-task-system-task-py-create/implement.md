# 实施计划：Task System 命令目录 reference-only 提示

## 执行清单

1. 更新 `trellis/workflows/guru-team/workflow.md`：
   - 在 `### Task System` 下、任务目录说明前插入 reference-only 说明。
   - 保留原命令目录不变。
2. 同步更新 `.trellis/workflow.md`：
   - 插入与 canonical workflow 相同的说明。
3. 不修改 overlays、scripts、schema、README，除非验证发现用户入口文案与新增说明冲突。
4. 更新 `issue-scope-ledger.json` 的 issue #41 验收证据。
5. 运行验证：
   - `rg -n "Reference only|prepare-task|source checkout|workspace_path" trellis/workflows/guru-team/workflow.md .trellis/workflow.md`
   - `python3 ./.trellis/scripts/get_context.py --mode phase`
   - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-06-41-task-system-task-py-create`
   - `git diff --check`

## 上下文与规范

- 官方文档：`https://docs.trytrellis.app/advanced/custom-workflow`
- 官方文档：`https://docs.trytrellis.app/advanced/custom-spec-template-marketplace`
- 本仓库规范：`.trellis/spec/workflow/workflow-contract.md`
- 本仓库规范：`.trellis/spec/workflow/quality-guidelines.md`
- 本仓库规范：`.trellis/spec/docs/public-docs.md`

## Docs SSOT Reconciliation

本次不改变长期产品、API、部署、数据或测试合同，只修正 workflow runtime contract 的局部文案提示；task artifact 保存 issue #41 的需求与验收证据，无需更新 `docs/requirements/`。

## 回滚点

如果验证发现 `get_context.py` phase 解析异常，回滚两个 workflow 文件中新增段落；不需要回滚脚本或 task lifecycle 状态。
