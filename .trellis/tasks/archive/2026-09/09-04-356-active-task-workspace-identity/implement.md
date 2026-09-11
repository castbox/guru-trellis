# Implementation Plan

## Ordered Work

1. 读取当前 active-task route、create-workspace package contract/interface、
   schema、preset ownership 与 installed projection；建立新 typed exit 的完整
   producer/consumer 图，不先修改官方 Trellis-owned 文件。
2. 在 `guru-create-task-workspace/runtime/` 增加创建事务的 identity preflight、
   session/runtime 定位闭合、final boundary 及 invocation-local rollback；保持
   Issue 创建与 workspace/task 创建互斥。
3. 在 `guru-create-task-workspace/runtime/check.py` 与 package schemas 增加完整
   identity 校验和 `invalid_task_state` stop projection；更新 `interface.json`、
   `errors/catalog.json`、examples 与 references/contract.md。
4. 在 Guru workflow canonical Markdown 增加 active-task-first 路由、唯一
   invalid-state stop target 和不进入 Intake/restore/rebuild 的规则；同步 workflow
   README 与相关 `.trellis/spec/workflow/{workflow-contract,data-contracts,
   quality-guidelines}.md`。
5. 增加真实 Git fixture 回归：成功闭合、branch/worktree/ledger/task mapping/
   workspace mapping/session pointer 各失败点、最终 boundary 失败、既有资源保护、
   complete active-task 优先、invalid exit 唯一消费与 projection drift。
6. 运行 preset reapply，将 canonical 变更同步到 dogfood/installed/platform
   projection；逐个处理 `.new`/`.bak` sidecar，不覆盖用户内容。

## Docs SSOT Plan

- `prd.md`：唯一拥有 #356 目标、范围、验收和排除项。
- `design.md`：唯一拥有 identity model、创建事务、路由和兼容/回滚设计。
- `implement.md`：唯一拥有执行顺序、测试集合、side-effect 边界和风险回滚。
- `.trellis/spec/workflow/workflow-contract.md`：承接长期 global route/typed
  consumer 合同；`data-contracts.md`：承接 identity/exit 数据约束；
  `quality-guidelines.md`：承接定向验证 ownership。
- `trellis/workflows/guru-team/workflow.md` 与 README 是可执行 workflow 的
  canonical/user-facing projection；`.trellis/workflow.md` 由 preset 同步，不能
  反向成为 SSOT。
- 不新增业务产品文档，不把 active task、runtime mapping、授权或本 task journal
  写入公共 spec/template。

## Validation

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -print0 | xargs -0 python3 -m py_compile
python3 -m py_compile trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/09-04-356-active-task-workspace-identity
git diff --check
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

另行运行变更 package 的 contract/runtime tests、真实 wrapper fixture、workflow
context reads、preset reapply/ownership/installed parity 和 declared platform
projection checks。完整多平台 Throwaway、Trellis upgrade/update 专项和 Release
Gate 明确不在本 task 验证范围。

## Side-Effect Boundary

实现阶段只在已确认的 #356 worktree 写 source/test/spec/projection；不创建 Issue、
不创建新 task/worktree、不开启官方 task 状态、不清理其他任务。提交、push、PR、
merge 和归档分别需要后续独立确认。
