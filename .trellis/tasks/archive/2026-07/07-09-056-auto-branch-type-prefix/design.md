# #56 Design

## Technical Design

### Scope

本次改动只覆盖 Guru Team companion `prepare-task` 的自动分支命名和公开文档，不改变 Trellis task 生命周期、worktree 创建、GitHub issue 创建、review gate 或 publish 流程。

### Contract

自动分支名合同：

```text
input: requirement text, issue title, optional issue body, optional --branch
output: branch_name
```

- 当 `--branch` 存在时，`branch_name = --branch`。
- 当 `--branch` 缺省时，`branch_name = <inferred_branch_type>/<unique_prefix>`。
- `inferred_branch_type` 只能取 `feat`、`fix`、`refactor`、`perf`、`test`、`docs`、`style`、`build`、`ci`、`chore`、`revert`。
- 未命中任何规则时，`inferred_branch_type = chore`。

### Deterministic Inference

在 `guru_team_trellis.py` 中新增单一推断入口，避免多个调用点重复解析：

- 先识别显式类型标记：`feat:`、`fix:`、`docs:`、`[docs]`、`type=docs`、`branch type: docs`。
- 再识别常见英文和中文关键词：
  - `fix`: fix, bug, error, failure, broken, 修复, 缺陷, 错误, 失败
  - `docs`: docs, doc, readme, documentation, 文档, 说明
  - `test`: test, tests, testing, 测试
  - `ci`: ci, github actions, workflow, 持续集成
  - `build`: build, dependency, dependencies, package, 构建, 依赖
  - `refactor`: refactor, cleanup, restructure, 重构
  - `perf`: perf, performance, optimize, 优化, 性能
  - `style`: style, format, formatting, lint, 格式
  - `revert`: revert, rollback, 回滚
  - `feat`: feature, add, support, enable, 新增, 支持
  - `chore`: chore, maintenance, housekeeping, 维护
- 规则顺序必须稳定；更具体的非 `feat` 类型先于 `feat`。

### Compatibility

- `branch_prefix` 保留解析，标记为 legacy compatibility；旧安装中的 `branch_prefix: "codex/"` 不参与新的默认自动分支名生成。
- 新字段 `branch_type_default: chore` 控制未命中规则时的 fallback 类型。
- `--branch` 保留完全覆盖能力，因此 AI 在特殊场景仍能传入明确分支名。
- `naming_quality` 仍检查分支名中的业务 token；类型前缀不参与业务语义判断。

### Docs SSOT Plan

- docs state: `partial_docs`
- evidence paths:
  - `README.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/workflows/guru-team/workflow.md`
  - `.trellis/workflow.md`
  - `docs/requirements/requirement-main.md`
- strategy: `ssot_first`
- reason: 旧文档公开推荐 `codex/NNN-business-capability`，与 issue 目标冲突；代码实现前必须把长期 workflow 合同改成自动类型分支。
- affected durable docs:
  - `README.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/workflows/guru-team/workflow.md`
  - `.trellis/workflow.md`
  - `docs/requirements/requirement-main.md`
- task artifact deltas to merge back: 自动分支类型合同、fallback 类型、显式 `--branch` 覆盖规则、validation 结果。
- merge checkpoint: Phase 2 check 前必须完成 durable docs 与代码一致性校验。

### Official Trellis Alignment

官方 Trellis 自定义 workflow 文档将 workflow 行为放在项目 workflow 定义中；官方自定义 spec template marketplace 文档将 reusable conventions 放在 marketplace 模板中。本次遵守该边界：canonical workflow/docs 与 companion script 同步更新，不修改 Trellis 上游源码或全局 npm 包。

### Risks

- 关键词规则无法覆盖所有自然语言意图。风险由显式 `--branch` 覆盖和 `chore` fallback 控制。
- 旧安装若依赖 `branch_prefix` 期望固定前缀，新默认行为会改变 planner 输出。需要在 config template 和 README 中说明旧字段为 legacy，并引导使用显式 `--branch`。
- `workflow` 和 `.trellis/workflow.md` 双副本若不同步，会导致 dogfood 运行态和 marketplace 合同漂移。
