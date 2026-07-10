# #96 技术设计：任务启动上下文与本机运行态边界

## 设计原则

1. Markdown workflow / skill / prompt 负责阶段、判断和 review gate；Python / shell 只做确定性 executor、validator、recorder。
2. 每项数据必须只有一个明确 owner、生成阶段和写入位置；可移植事实、本机状态和共享配置不得混写。
3. task-local tracked artifact 不得携带本机绝对路径；local runtime cache 不得成为 portability 必需条件。
4. canonical source 优先，dogfood 安装副本由 preset installer 同步。
5. 不保留旧 handoff fallback，不新增 tracked runtime index。

## 数据归属模型

| 数据面 | Owner / Writer | 写入时机 | 写入位置 | Git 属性 |
| --- | --- | --- | --- | --- |
| 任务启动上下文 | `prepare-task --create-task` executor | task 创建成功并得到 repo-relative task dir 后 | `.trellis/tasks/<task-dir>/task-start-context.json` | tracked |
| workspace runtime mapping | `prepare-task --create-worktree/--create-task` executor | worktree 创建/复用后 | `.trellis/.runtime/guru-team/workspaces/<workspace-slug>.json` | ignored |
| task runtime mapping | `prepare-task --create-task` executor | task 创建成功后 | `.trellis/.runtime/guru-team/tasks/<task-slug>.json` | ignored |
| 可重算 Git 状态 | 各命令 validator | 每次命令执行 | 不落盘 | 无 |
| 团队共享配置 | install/update 或明确 config task | 安装、升级或受审查的配置变更 | workflow/config/schema/preset/overlay | tracked |

## Task Start Context Contract

新增 canonical schema `trellis/workflows/guru-team/schemas/task-start-context.schema.json`，删除 `intake-handoff.schema.json`。schema 使用 allowlist + `additionalProperties: false`，对所有 path-like 字段增加相对路径或 portable slug 约束。

固定逻辑结构：

```json
{
  "schema_version": "1.0",
  "source_issue": {},
  "source_repo": {},
  "task_slug": "096-task-runtime-boundary",
  "task_title": "...",
  "task_artifact_dir": ".trellis/tasks/07-10-096-task-runtime-boundary",
  "branch_name": "codex/096-task-runtime-boundary",
  "base_branch": "main",
  "base_ref": "main",
  "base_head_sha": "...",
  "remote_head_sha": "...",
  "workspace_slug": "096-task-runtime-boundary",
  "task_workspace_id": "096-task-runtime-boundary",
  "assignee": "wumengye",
  "actor": {},
  "issue_scope_ledger_seed": {},
  "intake_summary": {
    "duplicate_decision": {},
    "naming_quality": {},
    "confirmation": {}
  }
}
```

实现中以 Issue 固定字段为准，不为了复用旧 payload 携带完整 `preflight` 或 executor 输出。writer 在 task 创建后写入 task dir，validator 同时执行 schema 校验和敏感 path/forbidden-key 扫描。

## Local Runtime Contract

新增 helper 统一计算 `.trellis/.runtime/guru-team/` producer namespace：

- `workspaces/<workspace-slug>.json` 保存 workspace slug、本机绝对 worktree path、repo root/source checkout 映射和必要 executor 时间戳。
- `tasks/<task-slug>.json` 保存 task slug、workspace slug、repo-relative task artifact dir 和本机 runtime workspace 映射。

runtime 文件使用原子写入，不进入 extension artifact contract，不复制到 task context，不建立 index。读取顺序固定为：显式参数 → 当前 checkout/task context → 对应 runtime cache → `git worktree list` 重建；cache 读取失败或路径失效时重新探测并覆盖本机 cache。

## Prepare Task 时序

### Planner-only

未传 executor flag 的 `prepare-task --json` 继续 stdout-only：读取 issue、duplicate/naming、base freshness 和候选 workspace，但不创建 issue/worktree/branch/task，也不写 task context 或 runtime cache。

### Create Worktree

1. 重新 fetch/校验 base freshness。
2. 创建或复用 worktree。
3. 写 `workspaces/<workspace-slug>.json`。
4. 返回 executor payload；不写 tracked task artifact。

### Create Task

1. 完成 create-worktree 流程。
2. 在目标 worktree 创建/复用 Trellis task，并解析实际 repo-relative task dir。
3. 设置 branch/base/scope 和 issue scope ledger seed。
4. 写 task dir 内 `task-start-context.json`。
5. 写 `tasks/<task-slug>.json`。
6. 返回 `task_start_context_path`、`runtime_workspace_state_path`、`runtime_task_state_path` 三个新路径字段；删除 `handoff_path` / `handoff_written` 公共输出。

## Workspace Boundary 重构

`check-workspace-boundary` 输入以 `--task <repo-relative-task-dir>` 为主：

1. `git rev-parse --show-toplevel` 获取 actual repo root。
2. 读取 task-local `task-start-context.json`，校验 `task_artifact_dir` 与传入 task 匹配。
3. 读取当前 branch、dirty status、base branch/head、remote head 和 worktree list；当命令合同要求校验 remote freshness 时执行 fetch，并记录本次事实。
4. 使用 current checkout、task context、runtime mapping 和 `git worktree list` 推导 expected workspace，不读取 committed absolute path。
5. 输出 machine facts 与 mismatch errors；不得把本次诊断回写 tracked artifact。

原 source checkout fixed handoff 检查删除。source checkout 安全改为检查本次命令写入 allowlist 和当前 task/source checkout 的实际 diff，不以固定 artifact 是否存在判断。

## 普通 Task 写入边界

新增确定性 validator 或测试 helper，根据 task scope 判断普通 task 命令产生的 tracked diff 是否落入：

- 当前 task active/archive dir；
- 当前 issue 明确修改范围；
- 其他路径一律作为共享配置变更进入 fail-closed 检查。

脚本只验证 path 集合；“当前 issue scope 是否覆盖 workflow/preset/config 修改”仍由 AI 在 planning、Phase 2 check、Branch Review Gate 和 PR readiness 中判断并记录。

## 调用点迁移

逐项替换 `configured_handoff_path()`、`workspace_handoff_path()`、`write_handoff()`、`load_handoff()`：

- prepare/create：写 task context 和 runtime mapping。
- check-workspace-boundary：读取 task context并实时重算。
- finish/check/review/publish：从当前 task context 获取 base/source issue/portable task facts，从当前 Git checkout/runtime mapping 获取本机事实。
- issue scope ledger：创建时从 task context seed 物化到 task-local ledger，后续以 ledger 为 SSOT。
- artifact/path resolver：只接受 repo-relative task artifact dir，不接受 handoff absolute workspace path。

## Canonical 与文档同步

必须修改：

- canonical Python、tests、schema、config template、extension manifest；
- canonical workflow 和 workflow/preset README；
- preset overlays 中 `.agents/skills/`、`.codex/prompts/`、`.codex/skills/`、`.cursor/commands/`、`.claude/commands/trellis/` 入口；
- `docs/requirements/README.md`、`requirement-main.md`、`guru-team-trellis-flow.md`；
- `.trellis/spec/workflow/**` 中把旧 handoff data contract 更新为 task start context/runtime contract；
- 运行 preset apply 后同步 dogfood `.trellis/guru-team/`、`.trellis/workflow.md` 和平台副本。

Docs SSOT Plan：行为合同以 `trellis/workflows/guru-team/workflow.md` 和 task-start-context schema 为主 SSOT；实现约束同步写入 `.trellis/spec/workflow/data-contracts.md`、`companion-scripts.md`、`workflow-contract.md`；公共安装/使用说明分别由两个 README 和 `docs/requirements/**` 承接。平台入口只引用流程，不重复定义字段 schema。

## 已废弃 Managed Artifact 清理

当前 preset installer 只复制当前 `MANAGED_ASSET_PATHS`，dogfood drift checker 也只比较 canonical 仍存在的文件；从列表删除旧 schema 不会自动清理既有安装中的 `.trellis/guru-team/handoff.json` 或 `schemas/intake-handoff.schema.json`。

installer 必须增加版本化、显式、确定性的 obsolete managed artifact 清单：

- 只删除 Guru Team 明确拥有且内容或 hash 可识别为旧 managed copy 的文件。
- 用户修改过的旧 managed file 不得静默删除；必须保留冲突证据并 fail safe，交由升级流程显式处理。
- dogfood drift 与 throwaway upgrade 验证必须检查“canonical 已删除但目标仍残留”的 obsolete file。
- 删除旧 fixed handoff 文件属于 Guru Team preset 升级合同，不依赖 `git clean`、手工删除或修改 Trellis upstream update。

## 兼容与回滚

- 无 legacy fallback；旧 handoff schema/file/config key 删除后，测试必须断言不存在。
- `task-start-context.json` schema version 从 `1.0` 开始，未来 breaking change 使用新 version，不复用旧 handoff version。
- runtime cache 可直接删除重建；任何命令不得因 cache 缺失而永久阻塞。
- 若 workspace boundary 或 finish/review 调用点迁移未完成，回滚整个代码改造，不以同时读新旧 artifact 的过渡状态提交。

## 安全

- schema 和 validator 同时阻塞 Unix/macOS/Windows 风格绝对路径、file URI、runtime path 和 forbidden keys。
- 测试 fixture 不写真实 developer home、token、repo secret、signed URL 或客户数据。
- CLI JSON 输出可展示本次 local facts，但不得把它们写入 tracked task artifact 或 PR evidence 原文。
