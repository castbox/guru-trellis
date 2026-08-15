# #164 技术设计

## 1. Architecture

本任务使用两个职责独立的 semantic closed-loop Skills：

```text
file-changing request without active-task route
  -> guru-select-workflow-mode (semantic owner)
      -> standard_intake -> existing Phase 0 graph
      -> task_free -> guru-execute-task-free-change (semantic owner)
                       -> checkout suitability + AI Review Gate
                       -> bounded edit + targeted checks
                       -> typed completion / routing / re-entry
```

Selector 只负责进入 task-free 或 standard Intake 的 mode 选择。
`guru-execute-task-free-change` 独占执行位置、活动 task scope、dirty overlap、限定编辑、
必要交互和风险扩大后的暂停/re-entry。两者通过 selector 现有最小 DTO 与 target-owned
authoring seed 连接，不共享私有 artifact，也不把 checkout facts 塞回 selector。

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

## 3. Task-Free Execution Skill

`guru-execute-task-free-change` 声明 `judgment_mode=semantic`，按
forward behavior -> AI Review Gate -> 必要交互 -> recorder/checker -> typed exit
完成一个闭环。它在写入前按下列顺序判断：

1. 读取当前 branch/worktree 与 repository identity。
2. 读取活动 Trellis task 及其 branch/worktree/scope authority。
3. 对比本次请求与活动 task/Issue 的 scope。
4. 枚举 dirty/untracked，并检查与目标文件是否重叠。
5. 选择原地 bounded edit、返回活动 task、进入 scope-change，或询问目标
   checkout/执行位置。
6. 对原地执行完成限定编辑与 targeted checks，再复核 scope/risk evolution。

该步骤仅使用本地事实。不得调用 GitHub Rules、branch protection 或其他远端发布状态。
Python/shell 只记录并校验 AI 已完成的 route 结果，不判断 scope、risk 或 checkout suitability。

稳定 exits 为：`completed`、`resume_active_task`、`scope_change`、
`location_required`、`reselect_mode`、`explicit_choice_required`、`blocked`。
其中两个交互出口 self-reentry；其余出口各有唯一 workflow/stop consumer。Unknown、multiple、
unmapped 或 stale 结果 fail closed。

## 4. Execution Evolution

- 自动 task-free：scope/risk 扩大后停止写入，Skill 输出 `reselect_mode`，由 selector
  重新判断；`standard_intake` 结论可自动进入现有 Intake。
- 显式 task-free：scope/risk 扩大后停止写入，Skill 输出
  `explicit_choice_required` 并 self-reentry；用户决定缩小范围或进入 Intake。
- 两个 post-write expansion route 的 owner-private evidence 必须绑定真实 partial edit、
  scope/risk expansion、检测后立即停止、未执行的剩余写入与适用 targeted checks；native eval
  在 tracked baseline 上验证后续目标保持原字节。
- Checkout 冲突：留在 consumer 内处理，不触发风险分级概念。

## 5. Source And Projection Ownership

| Layer | Source or projection |
| --- | --- |
| Canonical workflow | `trellis/workflows/guru-team/workflow.md` |
| Dogfood workflow | `.trellis/workflow.md` |
| Canonical Skills | `trellis/skills/guru-team/packages/guru-select-workflow-mode/`、`guru-execute-task-free-change/` |
| Installed Skills | `.trellis/guru-team/skills/packages/` 下对应包 |
| Discovery projections | `.agents/skills/`, `.codex/skills/`, `.claude/skills/`, `.cursor/skills/` |
| Public docs | `README.md`, workflow README, preset README |
| Installer/upgrade | preset apply、dogfood drift、throwaway install/update/reapply |

实现必须先修改 canonical，再运行 preset apply 同步 dogfood 与平台投影。不得反向把生成投影
当作 SSOT。

## 6. Public I/O And Compatibility

- 保留 exits：`task_free`、`standard_intake`、`blocked`。
- 保留 selector public input/output schema；其 `task_free` 输出通过 target-owned authoring
  seed 进入新 Skill，不增加 selector 字段。
- 新 Skill 使用独立 input profiles、per-exit schemas、consumer contracts 与最小 re-entry DTO。
- `completed` public DTO 仅向 workflow completion consumer 返回实际 edited paths、精简
  validation summary 和 unverified boundaries；命令 transcript、AI review narrative 与完整
  execution evidence 保持 private。
- 保留 semantic `judgment_mode`；runtime checker 仅校验结构、mapping 和最终选择。
- 现有显式 task-free、拒绝、same-scope retry、unrelated dirty 与 blocked 行为继续兼容。

## 7. Test Design

### Selector semantic evals

- explicit task-free；
- high-confidence prompt without explicit intent；
- insufficient-evidence prompt and one affirmative/refusal branch；
- obvious complex request；
- simple / insufficient / complex Issue；
- equal file-count but different semantic risk；
- same-scope selection retry。

### Task-free execution semantic evals

- bounded edit completed on default/non-default checkout；
- same-scope active task、scope expansion；
- unrelated worktree、dirty overlap、position evidence insufficient；
- automatic risk re-selection、explicit risk choice self-reentry；
- blocked 与 no branch-protection trace。

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

- 主要风险是把 checkout 判断混入 selector、让 workflow target 继续拥有 step-local behavior，
  或让脚本替代 AI 风险判断；package/interface/workflow tests 必须阻止三者。
- 次要风险是只更新 dogfood 或单一平台；identity/drift/throwaway 检查必须阻止缺失投影。
- 回滚以完整 task commit 为单位；不迁移 public schema，因此无数据或 API 回滚步骤。
