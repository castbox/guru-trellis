# #164 技术设计

## 1. Architecture

本任务沿用现有两段式控制面，不新增 package：

```text
file-changing request without active-task route
  -> guru-select-workflow-mode (semantic owner)
      -> standard_intake -> existing Phase 0 graph
      -> task_free -> guru-task-free-current-checkout
                       -> checkout suitability
                       -> bounded edit + targeted checks
```

Selector 负责意图、范围、风险、证据充分性和 mode 选择。Task-free consumer 负责执行位置、
活动 task scope、dirty overlap、限定编辑和风险扩大后的暂停。两者通过现有最小 DTO 连接，
不共享私有 artifact。

## 2. Selector Semantic Contract

### 2.1 Explicit intent

AI 按语义识别多语言、大小写、连字符、上下文和同义表达。Issue 中列出的短语仅作为公开
示例，不形成脚本关键词表。`帮我改一下` 与 `不要开 Issue` 均不直接产生 task-free 结论。

### 2.2 No explicit intent

AI 读取完成判断所需的有限本地事实，然后输出三种处理结果：

| Evidence conclusion | Behavior |
| --- | --- |
| 边界清楚、局部、可逆、无明显高风险影响 | 直接 `task_free` |
| 倾向 task-free，但 scope/risk 证据不足 | 打开一次 mode 问题 |
| 运行时行为影响明显或风险较高，或涉及跨层合同、public API、schema、CI、install/update、deploy、permission、security 或 data | 直接 `standard_intake` |

一次问题的肯定答案进入 `task_free`，拒绝进入 `standard_intake`；同 scope 重试复用已选 mode。
当前 schema 只记录最终 selection 与 continuation identity，授权过程不持久化。

## 3. Checkout Suitability Consumer

`guru-task-free-current-checkout` 在写入前按下列顺序判断：

1. 读取当前 branch/worktree 与 repository identity。
2. 读取活动 Trellis task 及其 branch/worktree/scope authority。
3. 对比本次请求与活动 task/Issue 的 scope。
4. 枚举 dirty/untracked，并检查与目标文件是否重叠。
5. 输出原地执行、返回活动 task、进入 scope-change、询问目标 checkout 或询问执行位置。

该步骤仅使用本地事实。不得调用 GitHub Rules、branch protection 或其他远端发布状态。

## 4. Execution Evolution

- 自动 task-free：scope/risk 扩大后停止写入，由 selector 重新判断；`standard_intake` 结论可
  自动进入现有 Intake。
- 显式 task-free：scope/risk 扩大后停止写入，不静默升级；用户决定缩小范围或进入 Intake。
- Checkout 冲突：留在 consumer 内处理，不触发风险分级概念。

## 5. Source And Projection Ownership

| Layer | Source or projection |
| --- | --- |
| Canonical workflow | `trellis/workflows/guru-team/workflow.md` |
| Dogfood workflow | `.trellis/workflow.md` |
| Canonical Skill | `trellis/skills/guru-team/packages/guru-select-workflow-mode/` |
| Installed Skill | `.trellis/guru-team/skills/packages/guru-select-workflow-mode/` |
| Discovery projections | `.agents/skills/`, `.codex/skills/`, `.claude/skills/`, `.cursor/skills/` |
| Public docs | `README.md`, workflow README, preset README |
| Installer/upgrade | preset apply、dogfood drift、throwaway install/update/reapply |

实现必须先修改 canonical，再运行 preset apply 同步 dogfood 与平台投影。不得反向把生成投影
当作 SSOT。

## 6. Public I/O And Compatibility

- 保留 exits：`task_free`、`standard_intake`、`blocked`。
- 保留 public input/output schema 与 direct projection；checkout suitability 不进入 DTO。
- 保留 semantic `judgment_mode`；runtime checker 仅校验结构、mapping 和最终选择。
- 现有显式 task-free、拒绝、same-scope retry、unrelated dirty 与 blocked 行为继续兼容。

## 7. Test Design

### Package semantic evals

- explicit task-free；
- high-confidence prompt without explicit intent；
- insufficient-evidence prompt and one affirmative/refusal branch；
- obvious complex request；
- simple / insufficient / complex Issue；
- equal file-count but different semantic risk；
- same-scope retry；
- scope/risk expansion for automatic and explicit task-free；
- checkout matrix and no branch-protection lookup trace。

### Deterministic tests

- Interface、schema 与 projections 保持现行最小形状；
- canonical / installed / platform package byte identity；
- workflow marker 和 target closure；
- README 与 prompt 统一表达；
- preset apply、dogfood overlay drift、fresh install、update/reapply、sidecar absence。

## 8. Docs SSOT Plan

Strategy: `ssot_first`。

1. 在 canonical workflow 与 selector contract 定义完整语义。
2. 在三份公共 README 解释用户入口、三分判断、checkout suitability 与副作用边界。
3. 通过 preset apply 生成 dogfood 与平台投影。
4. 用 drift、source/installed validation 和 throwaway update/reapply 证明所有投影来自同一 SSOT。

## 9. Risk And Rollback

- 主要风险是把 checkout 判断混入 selector，或让脚本替代 AI 风险判断；review 必须阻止两者。
- 次要风险是只更新 dogfood 或单一平台；identity/drift/throwaway 检查必须阻止缺失投影。
- 回滚以完整 task commit 为单位；不迁移 public schema，因此无数据或 API 回滚步骤。
