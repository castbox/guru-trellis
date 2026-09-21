# Implementation Plan: Reactivate 日期前缀任务定位

## 1. 执行前门禁

1. 保持 task status 为 `planning`，完成 planning wording review 和
   `guru-approve-task-plan`。
2. 单独取得用户对当前 planning summary 的确认。
3. 仅通过 `.trellis/guru-team/scripts/bash/start-task.sh` 激活 task；未确认前不改
   runtime/test/installed 文件。
4. 激活后再次运行 workspace boundary 和 task validation。

## 2. 实现步骤

### Step 1: 收窄 locator 校验

修改 canonical
`trellis/skills/guru-team/packages/guru-reactivate-task/runtime/invoke.py`：

- `task_ref` basename 与 `archive_ref` basename 精确比较；
- workspace/task mapping stem 继续分别与 `task_id` 精确比较；
- 不解析日期前缀，不使用 suffix/`endswith`；
- 保持 archive `task.json.id/status` 的现有 pre-move 校验顺序。

### Step 2: 扩展 canonical contract tests

修改
`trellis/skills/guru-team/packages/guru-reactivate-task/tests/test_reactivate_contract.py`：

- fixture 支持 locator basename 与 stable task id 分离；
- 新增 date-prefixed `reuse_exact`；
- 新增 date-prefixed `create_new`；
- 新增 date-prefixed output-loss recovery 两 disposition；
- 新增 active/archive basename mismatch no-mutation；
- 新增 archive `task.json.id` mismatch no-mutation；
- 保持无前缀正向、mapping mismatch、finish-branch fast-forward 既有测试通过。

### Step 3: 同步 installed/dogfood projection

运行 canonical preset apply：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo . \
  --platform claude --platform codex --platform cursor --json
```

检查实际 diff 仅包含本任务需要的 canonical/installed runtime、测试和 managed
provenance。处理 reapply 产生的 sidecar，禁止保留 `.new`/`.bak`。

## 3. 定向验证

### 3.1 Package behavior

```bash
pytest -q trellis/skills/guru-team/packages/guru-reactivate-task/tests/test_reactivate_contract.py
```

若仓库要求 managed interpreter，则通过当前 checkout 的 managed resolver/既有
测试入口运行同一测试文件，不以 PATH Python 依赖结果代替 package evidence。

### 3.2 Canonical/installed parity

```bash
cmp \
  trellis/skills/guru-team/packages/guru-reactivate-task/runtime/invoke.py \
  .trellis/guru-team/skills/packages/guru-reactivate-task/runtime/invoke.py
```

同时运行 source/installed package validator，确认 package projection 未包含
canonical private tests，且 active package inventory 无漂移。

### 3.3 Preset 与 drift

```bash
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
find .trellis/guru-team trellis/presets/guru-team -type f \
  \( -name '*.new' -o -name '*.bak' \) -print
```

sidecar 查询必须为空。

### 3.4 基础质量门禁

```bash
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages \
  -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
python3 ./.trellis/scripts/task.py validate \
  .trellis/tasks/09-22-459-reactivate-date-prefixed-task-locator
git diff --check
```

## 4. 验证结果记录要求

- 分别记录 package tests、canonical/installed parity、preset reapply、ownership、
  drift、sidecar、task validation 和 `git diff --check` 的结果。
- 任一未运行项标记为未验证，不以其它测试替代。
- 不声称完整多平台 Throwaway installer、upgrade/update 或 Release Gate 已通过。

## 5. 停止与回退条件

- 若实现需要 public schema/DTO/exit/consumer/workflow route 变化，停止并返回
  requirements clarification，不自行扩 scope。
- 若必须解析日期前缀或新增 alias/dual-read 才能通过，停止并重新审查设计。
- 若 preset reapply 产生与本任务无关的 managed diff 或无法消除 sidecar，停止并
  报告 drift，不覆盖未知本地修改。
- 若 archive metadata mismatch 在目录移动后才被发现，视为设计不满足，回到
  实现修订后重新执行完整定向验证。
