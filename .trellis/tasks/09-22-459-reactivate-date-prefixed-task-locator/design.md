# Design: Reactivate 日期前缀任务定位

## 1. 当前行为

`trellis/skills/guru-team/packages/guru-reactivate-task/runtime/invoke.py` 的
`validate_task_identity()` 当前把四个 locator 都与 `public.task_id` 比较：

1. `Path(task_ref).name`
2. `Path(archive_ref).name`
3. `Path(workspace_mapping).stem`
4. `Path(task_mapping).stem`

该模型错误地把带日期前缀的 task directory locator 当作稳定 task identity。
后续 `reactivate()` 已经在移动 archive 前精确检查 archived `task.json.id` 和
`status=completed`，因此真正缺失的是 locator 配对规则，不是新的 identity
解析器。

## 2. 设计原则

- 日期前缀属于 locator basename，不参与 stable task id 推导。
- active/archive locator 通过 basename 彼此绑定。
- archive metadata 和 mapping stem 继续通过精确等值绑定 stable `task_id`。
- 不增加 helper abstraction，除非实现中确有重复；本修复优先保持局部、直接、
  可审计。
- public contract 和 workflow route 完全不变。

## 3. 目标校验模型

### 3.1 写入前 public/plan 校验

`validate_task_identity(public, plan)` 执行两类独立检查：

```text
task_basename = Path(task_ref).name
archive_basename = Path(archive_ref).name

require task_basename == archive_basename
require Path(workspace_mapping).stem == task_id
require Path(task_mapping).stem == task_id
```

禁止执行：

- 去除 `MM-DD-`；
- `basename.endswith(task_id)`；
- 从 locator 覆盖或重写 `task_id`；
- 接受 active/archive 不同 basename 的兼容分支。

active/archive 不一致时返回现有 `stale_identity` 错误族，并保持所有资源未写。
mapping stem mismatch 继续保留当前 field-specific 错误。

### 3.2 Workspace 选择后的 archive 校验

`reactivate()` 的现有顺序保持不变：

1. 校验 archive 是唯一安全目录且 active target 不存在；
2. 读取 archive 内 `task.json`；
3. 精确校验 `task.id == public.task_id`；
4. 精确校验 `task.status == completed`；
5. 仅在上述检查通过后移动 archive 到 active locator；
6. 更新 lifecycle metadata 和 stable-id mappings。

这使 locator 配对和 stable identity 校验保持分层，同时保证 metadata mismatch
不会发生目录移动。

### 3.3 Output-loss recovery

`recover_completed_reactivation()` 继续使用：

- public locator 定位恢复后的 active 目录；
- `task.json.id == task_id` 校验 stable identity；
- stable `task_id` mapping stem 和 payload 校验 mapping identity；
- lifecycle generation、branch、base HEAD、worktree registration 判定已完成结果。

日期前缀不需要独立 recovery 分支。相同 public/plan 输入应自然复用现有恢复
路径并返回第一次执行的 generation。

## 4. 测试设计

### 4.1 Fixture 参数化

保留 stable `task_id="demo"`，repository/public fixture 显式接收
`locator_basename`：

- 无前缀：`demo`
- 日期前缀：`09-19-demo`

mapping 路径始终为 `.../demo.json`，从 fixture 层明确区分 locator identity 和
stable task identity。

### 4.2 正向场景

- 既有无前缀 `reuse_exact` 测试保持通过。
- 新增日期前缀 `reuse_exact`。
- 新增日期前缀 `create_new`。
- 日期前缀 `reuse_exact|create_new` output-loss recovery 参数化测试。

### 4.3 负向场景

- active/archive basename 不一致，校验错误且 archive 保持原位。
- archive `task.json.id` 改为其它值，校验错误且 archive 保持原位。
- 既有 workspace/task mapping stem mismatch 测试继续通过。
- 保留无前缀 public locator mismatch coverage；当既有 field-path 断言与新的
  locator-pair ownership 冲突时，只调整该 field-path 断言，不弱化
  `stale_identity` 和 no-mutation 断言。

## 5. 文件与分发边界

| 文件 | 变更原因 |
| --- | --- |
| `trellis/skills/guru-team/packages/guru-reactivate-task/runtime/invoke.py` | 修正 canonical locator/stable-id 校验职责 |
| `trellis/skills/guru-team/packages/guru-reactivate-task/tests/test_reactivate_contract.py` | 增加真实日期前缀和 no-mutation 回归 |
| `.trellis/guru-team/skills/packages/guru-reactivate-task/runtime/invoke.py` | 由 preset reapply 从 canonical 同步的 installed/dogfood projection |
| `.trellis/guru-team/extension.json` | preset reapply 产生的 managed-hash/provenance 更新（如实际需要） |

不直接手工维护 installed projection；以 canonical 修改后运行 preset reapply。
若 reapply 产生 `.new`/`.bak`，必须按 installer 合同处理并在完成前达到零 sidecar。

## 6. 兼容性与替换边界

- 无 public API 版本变化，不新增 compatibility reader。
- 无 schema/interface/registry/commands/workflow marker 变化。
- Issue #454 未来替换旧 validator/mapping 模型时，本修复整体随旧模型退出，
  不形成单独迁移合同。

## 7. 未验证边界

本任务不承担完整多平台 clean/existing/update/workflow-switch/Release Candidate
矩阵。该矩阵属于专门兼容性、Trellis upgrade/update 或 Release Gate owner。
