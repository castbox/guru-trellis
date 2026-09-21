# #459 修复 guru-reactivate-task 日期前缀任务定位

## 1. 背景

Trellis 正常任务目录使用 `MM-DD-slug` 形式，而任务的稳定业务身份保存在
`task.json.id` 中。当前 `guru-reactivate-task` 把 `task_ref`、`archive_ref`
的 basename 和 `task.json.id` 强制视为同一个值，因此会拒绝以下合法状态：

- active locator：`.trellis/tasks/09-19-147-unified-api-contract`
- archive locator：`.trellis/tasks/archive/2026-09/09-19-147-unified-api-contract`
- stable task id：`147-unified-api-contract`

该拒绝发生在写入前，导致正常完成的 archived task 无法按现有 Reactivate
合同恢复。

## 2. 目标

在不改变 Reactivate public API 和 mapping 合同的前提下，使 active/archive
locator 使用相同日期前缀 basename 时能够恢复稳定 `task.json.id` 对应的任务。

## 3. 功能需求

### R1 Locator 配对身份

- `task_ref` basename 必须与 `archive_ref` basename 完全相同。
- 不从 `MM-DD-` 前缀、suffix 或 `endswith(task_id)` 推导任务身份。
- 两个 basename 不一致时必须在 branch/worktree/task/mapping 写入前 fail closed。

### R2 稳定任务身份

- `task_id` 继续严格来自 public input 和 archived `task.json.id` 的精确匹配。
- archive 中 `task.json.id != task_id` 时必须在移动 archive 目录前 fail closed。
- archive 中 `status != completed` 时继续在移动目录前 fail closed。

### R3 Mapping 身份

- workspace mapping 和 task mapping 的文件 stem 必须继续精确等于 `task_id`。
- 不新增 locator alias、mapping alias、dual-read、迁移记录或 compatibility shim。
- Reactivate 完成后的 mapping payload 继续使用稳定 `task_id` 作为
  `workspace_slug`、`task_slug`。

### R4 既有恢复语义

- `reuse_exact` 和 `create_new` 两条路径均支持日期前缀 locator。
- output-loss recovery 对相同日期前缀输入返回同一结果，不重复创建 worktree、
  移动目录、递增 lifecycle generation 或重写 mapping。
- 既有无前缀 locator 继续工作。

### R5 分发一致性

- canonical package 是唯一实现来源。
- dogfood/installed package projection 与 canonical runtime 保持字节一致。
- preset reapply、dogfood drift 和 zero-sidecar 门禁通过。

## 4. 验收标准

- [ ] 日期前缀 locator 的 `reuse_exact` Reactivate 成功，任务恢复为
      `in_progress`，stable `task.json.id` 不变。
- [ ] 日期前缀 locator 的 `create_new` Reactivate 成功，并绑定预审 branch 和
      worktree。
- [ ] 日期前缀 locator 的 output-loss recovery 在两种 disposition 下均不重复
      mutation。
- [ ] active/archive basename 不一致时返回 `stale_identity`，archive 未移动。
- [ ] archive `task.json.id` 与 public `task_id` 不一致时返回 `stale_identity`，
      archive 未移动。
- [ ] workspace/task mapping stem 不等于 `task_id` 时继续 fail closed。
- [ ] 既有无前缀正向 fixture 和 identity mismatch 回归继续通过。
- [ ] canonical package tests 通过。
- [ ] canonical 与 `.trellis/guru-team/skills/packages/guru-reactivate-task`
      installed projection 一致。
- [ ] preset reapply、dogfood overlay drift、source/installed package validation、
      recursive `.new`/`.bak` sidecar 检查通过。

## 5. 非目标

- 不实施或修改 Issue #454 的长期 lifecycle substrate。
- 不退役或重命名 task/workspace mappings。
- 不修改 Reactivate public schema、DTO、typed exit、consumer 或 workflow route。
- 不新增日期前缀 parser、正则 identity 推导或 basename 到 task id 的转换。
- 不发布版本，不更新业务仓库，不重试业务 task Reactivate，不执行额外 GitHub
  mutation。

## 6. 约束与风险

- 目录 basename 只承担 active/archive 位置配对；`task.json.id` 和 mapping stem
  承担稳定 task identity，两个概念不得重新混合。
- 校验顺序必须保证 archive metadata 不匹配时目录尚未移动。
- 本 Issue 是普通 workflow defect，只运行 accepted scope 所需的 package、
  canonical/installed、preset reapply 和 drift 验证，不扩张为完整多平台
  Throwaway installer 或 Release Gate 矩阵。

## 7. Authority

- Source Issue: <https://github.com/castbox/guru-trellis/issues/459>
- Related future architecture: <https://github.com/castbox/guru-trellis/issues/454>
