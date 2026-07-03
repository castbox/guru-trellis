# #18 设计：PR 发布边界硬化

## 设计原则

1. **官方 Trellis 优先**：流程语义继续放在 marketplace workflow 和平台 overlay Markdown 中，不改 Trellis 上游源码。
2. **Markdown 决策，脚本校验**：是否应该发布 PR 是 workflow/finish-work 阶段定义；脚本只验证调用上下文和客观条件。
3. **Fail closed**：直接 `publish-pr` 默认失败，除非调用方能证明来自 `finish-work` 或显式 recovery/debug override。
4. **兼容恢复场景**：保留内部 helper 能力，但 recovery/debug flag 必须显式，且仍复用所有已有 gate。
5. **单一源头同步**：canonical workflow 和 preset overlay 是长期源头，dogfood 副本通过 installer 同步。

## 当前行为分析

`cmd_publish_pr()` 当前直接执行：

1. 解析 task / handoff / base branch / repo。
2. 校验非 metadata dirty path。
3. 校验 Branch Review Gate。
4. 校验 Issue Scope Ledger。
5. dry-run 返回 payload，非 dry-run 执行 `git push` 和 `gh pr create`。

`cmd_finish_work()` 当前在 archive、journal、metadata commit 后构造 namespace 调用 `cmd_publish_pr()`。问题是 `publish-pr` CLI 子命令和 `finish-work` 内部调用之间没有可验证区别，因此 AI 可以在 `trellis-continue` 阶段误调用 `publish-pr` 并完成 push/PR。

## 目标调用合同

### 日常路径

```text
trellis-continue
  -> implement/check/spec decision/commit
  -> AI Review
  -> review-branch.sh records Branch Review Gate
  -> stop and instruct trellis-finish-work

trellis-finish-work
  -> check review gate
  -> reject non-metadata dirty paths
  -> task.py archive
  -> add_session.py journal
  -> commit metadata if needed
  -> cmd_publish_pr(from_finish_work=true, allow_metadata_after_gate=true)
  -> push + non-draft PR
```

### Direct publish 默认路径

```text
publish-pr
  -> if not from finish-work and not explicit recovery flag:
       fail before dirty/gate/ledger/push checks
```

### Recovery/debug 路径

```text
publish-pr --recovery-after-finish-work
  -> require all existing publish validations
  -> dry-run or publish
```

该 flag 命名刻意包含 `recovery-after-finish-work`，表示只能用于 finish-work 已完成 archive/journal 但 publish 失败后的人工恢复，而不是 continue 阶段的常规发布。

## 脚本变更

### 新增 parser 参数

`publish-pr`：

- `--from-finish-work`：内部 flag，help 标记 internal；由 `cmd_finish_work()` 传入。
- `--recovery-after-finish-work`：显式恢复/debug flag；允许 CLI 直接调用。

### 新增校验函数

新增 `validate_publish_invocation(args)`：

- 如果 `args.from_finish_work` 或 `args.recovery_after_finish_work` 为真，则通过。
- 否则抛出 `WorkflowError(exit_code=2)`，错误说明：
  - `publish-pr` 是内部 helper；
  - 日常发布必须运行 `.trellis/guru-team/scripts/bash/finish-work.sh --json`；
  - recovery/debug 需显式 `--recovery-after-finish-work`。

校验放在 `cmd_publish_pr()` 前段，确保不会执行 push 或 PR create。

### finish-work 内部调用

`cmd_finish_work()` 构造 `publish_args` 时设置：

- `from_finish_work=True`
- `recovery_after_finish_work=False`

## Markdown / overlay 变更

### Workflow

在 Phase 3.7 明确：

- `publish-pr.sh` 拒绝普通直接调用；
- `publish-pr.sh` 只接受 `finish-work` 内部调用或显式 recovery/debug override；
- `trellis-continue` 到 Branch Review Gate 后必须停止或引导 finish-work。

### Continue overlays

加强最后一句：

- 不 push；
- 不创建 PR；
- 不调用 `publish-pr`；
- 下一步是 `trellis-finish-work`。

### Finish overlays

明确：

- archive task 和 journal 成功后才 publish；
- publish 由 finish helper 内部执行。

### README

补充日常入口和发布边界，避免用户/AI 把 `publish-pr` 当成可直接运行的命令。

## 测试策略

### 单元/脚本级

在 `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 中补充或创建测试：

- 构造最小 repo / task / gate / ledger 环境；
- 调用 `cmd_publish_pr()` 不带 flag，断言 `WorkflowError` 且不会进入 push；
- 调用带 `recovery_after_finish_work=True` + `dry_run=True`，断言可生成 payload；
- 调用 `cmd_finish_work(dry_run=True)`，断言 publish payload 可生成且内部 flag 生效。

### 集成/验收

- `bash -n` 检查 wrappers。
- `py_compile` 检查 Python。
- `task.py validate` 检查 task artifact。
- preset `apply.sh --repo .` 同步 dogfood。
- `check-dogfood-overlay-drift.sh` 验证 overlay 无漂移。
- 必要时运行 throwaway install，验证新项目安装后包含更新后的 overlay 和脚本。

## 风险与兼容性

- 风险：已有手工恢复流程直接运行 `publish-pr` 会失败。
  - 缓解：提供显式 `--recovery-after-finish-work`，并在错误信息和文档中说明用途。
- 风险：脚本测试环境难以完整模拟 `task.py archive` / journal。
  - 缓解：优先测试 `cmd_publish_pr()` 的硬门禁和 recovery dry-run；finish-work dry-run 用可控 fixture 或集成 dry-run 覆盖。
- 风险：只改 canonical 忘记 dogfood 副本。
  - 缓解：运行 preset apply 和 drift check。

## 不变项

- Branch Review Gate 的 AI/human review 仍由 workflow 阶段负责。
- `review-branch.sh` 仍只是 recorder/validator。
- `publish-pr` 仍复用已有 dirty/gate/ledger/gh auth 检查。
- PR 默认仍为 non-draft，base branch 仍来自 intake/task。
