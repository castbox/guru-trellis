# #348 实施计划

## 顺序

1. 读取当前 Architecture Baseline、Requirements/Design/Test SSOT 和相关 package specs，确认 recovery owner、target 和 schema 归属。
2. 在 merge package 中定义 task-work re-entry 的 semantic input/output、typed exit 和 finding reference 最小 DTO。
3. 实现 recovery owner 的 live identity validator、archive locator resolver、active-task conflict guard 和幂等恢复 executor。
4. 实现旧 authority invalidation 与 Phase 2 workflow target，保持 terminal blocked route 的唯一性和外部 blocker 语义。
5. 同步 canonical package、preset installed projection、workflow targets、schemas、examples、README/spec 与 Shared/Codex/Claude/Cursor 入口。
6. 补齐 runtime/unit/contract/eval 测试，覆盖成功及八类负面/中断场景。
7. 运行针对 package/runtime 的测试和安装投影 drift 检查；按质量规范记录未验证的完整矩阵边界。
8. 运行 `trellis-check` 完整语义检查；通过后再进入 Branch Review 和发布准备。

## 预期变更区域

- `trellis/skills/guru-team/packages/guru-merge-task-pr/`
- 新增的 recovery skill package 及其 schemas/runtime/tests
- `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md`
- `trellis/presets/guru-team/` 的 installer、README/spec、platform overlays、examples/evals
- `.agents/skills/`、`.codex/skills/`、`.claude/skills/`、`.cursor/skills/` 中声明投影（以 canonical reapply 为准）
- task-local `implement.jsonl`、`check.jsonl` 仅记录可复用的 spec/research 与验证入口，不记录授权或完整审计历史

## 定向验证

- merge/recovery package contract、schema 和 runtime tests
- workflow registry/target consumer uniqueness checks
- archived task success、external blocker、PR/head/base/scope drift、dirty worktree、duplicate active task、merged PR、interrupted/lost-result recovery
- canonical -> installed preset reapply 和 `check-dogfood-overlay-drift.sh`
- 声明平台入口与 README/spec consistency
- `get_context.py`、`trellis-check` 以及完整 diff Branch Review

## 风险与停止点

- 如果 Architecture Baseline 判定 owner/constitution 冲突，回到 planning 修订，不实现。
- 如果发现 #261/#248 已在当前 base 改变 owner 图，重新做 scope/contract review，不静默叠加两套恢复路径。
- 如果 recovery executor 不能证明 identity 唯一匹配，保持 blocked，不提供手工补救命令。
- 不执行 commit、push、PR、merge、Issue closure 或 release。
