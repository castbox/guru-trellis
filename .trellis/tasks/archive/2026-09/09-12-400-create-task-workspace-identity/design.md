# 设计

## 身份模型

`guru-create-task-workspace` 的创建身份由以下事实闭合：

- `task.json` 的 task id、branch、base branch、task artifact locator 和 `worktree_path`；
- task-local `issue-scope-ledger.json`；
- source/target ignored runtime mapping；
- 当前 checkout 与 `git worktree list`；
- session current-task locator。

`source_checkout` 只表示 mapping provenance，不单独决定 task 归属。

## 前置链

Readiness transition 增加来自 `guru-discover-change-context` 的最小 `context_result_sha256`。后续 readiness producer 保留该 identity，workspace recorder/checker 验证其存在并与当前 continuation、target 和 repo 闭合；不跨边界传递 Discovery 私有 payload。

## 创建与校验

workspace resolver 只计算一次规范 workspace path。executor 用该 path 同时生成 task.json 与两份 mapping；checker 复用同一 resolver，并校验 task、ledger、session、mapping 和 live Git worktree。任一关系不闭合返回 `invalid_task_state`，不执行 repair。

## 兼容边界

旧 task 格式不迁移。当前 schema 和安装投影同步升级；测试 fixture 改为显式提供新的 identity 字段。Issue #356 的既有行为仅作为历史参考，不作为恢复输入。

## 验证

- package contract/runtime 单元测试；
- installed workspace invocation 的正向完整链；
- 缺失 discovery identity、缺失 worktree_path、session mismatch、mapping mismatch 的 zero-write 负向用例；
- dogfood overlay drift 与 Python/Bash/schema 校验。
