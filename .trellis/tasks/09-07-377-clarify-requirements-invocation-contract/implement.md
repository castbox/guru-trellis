# 实施计划

## 1. 进入实现前

- [x] 运行 workspace boundary check，确认 branch/worktree/task identity。
- [x] 重新读取 Issue #377、当前 main、canonical package 和相关 workflow/spec。
- [x] 完成 direct-evolution 与 solution-mechanism qualification：真实支持入口
      是现有 `scripts/invoke.sh --invocation -`，消费者是现有 typed-exit
      projections；缺陷来自公开 schema 与 runtime 的正常路径不一致。直接让
      runtime 从 checked owner result 生成 DTO，不引入兼容 wrapper 或第二执行路径。

## 2. 合同与实现

- [x] 定义并落实唯一 public invocation envelope 语义。
- [x] 修改 canonical schema/runtime/Skill/interface/reference，使 runtime 与
      声明合同一致，并保留 freshness、duplicate、target、owner-result 和
      typed-exit 校验。
- [x] 更新 eval adapter，删除依赖未声明顶层字段的调用样例。
- [x] 补充真实 wrapper 回归：合法 envelope -> `clear`，并覆盖错误/过期输入。

## 3. 验证

- [x] package contract/runtime tests。
- [x] envelope Draft 2020-12 schema validation、声明外字段和错误出口测试。
- [x] stale target、duplicate snapshot、live target freshness 回归。
- [x] canonical/installed/platform equality、preset apply、dogfood drift、
      sidecar 检查。
- [ ] 一个代表性 clean throwaway 安装并运行 Phase 0 public wrapper；不宣称
      完整多平台或 Release Gate 通过。
- [x] `git diff --check`、JSON/Python/Bash 静态校验和 task validate。

## 4. 后续门禁

- [ ] 运行 fresh Phase 2 `guru-check-task`，覆盖完整 task scope；当前已完成
      AI 语义复核和相关 deterministic checks，但未伪造 Phase 2 owner artifact。
- [ ] 仅在 Phase 2 passed 后进入 commit/review；本 task 当前不执行 commit、
      push、PR、merge 或 release。
