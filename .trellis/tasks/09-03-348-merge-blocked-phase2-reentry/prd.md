# #348 merge_blocked 归档任务 Phase 2 re-entry

## 目标

为当前稳定安装图补齐一条受控、可审计、fail-closed 的恢复路径：当 task 已归档、PR 仍 open 且 merge gate 发现属于当前 Issue scope 的可修复 finding 时，恢复原 task、原 branch、原 worktree、原 remote branch 和原 PR，并回到 Phase 2 implementation。

用户价值是保留安全阻断的同时，让修复能够沿原任务继续，不被迫手工移动 archive、绕过 workflow 或创建重复对象。

## 背景与已确认事实

- 基线为 `main`，2026-09-03 的 `HEAD` 为 `bc33c58febe74648036ed68c890abaa0be55f605`。
- `guru-merge-task-pr` 当前只有 `merged`、`merge_blocked`、`closure_mismatch` 三个出口；`merge_blocked` 的唯一 consumer 是 terminal stop。
- 当前 blocked DTO 不绑定 task/archive identity、PR head、finding references 或合法 resume target。
- Publication 的 `return_to_task_work` 只服务 Publication Review，不能承担 Merge 阶段的归档任务恢复。
- official `task.py` 没有 reopen/unarchive 命令；现有 Finalizer recovery 只覆盖 Finalizer transaction 中断。
- #348 无重复 Issue。#223、#248、#261 是相关边界，不是本任务的直接实现范围。

## 需求

### R1 可恢复 finding 与外部 blocker 分流

只有语义 owner 证明 finding 属于当前 task/Issue scope，且修复需要修改 task 内容时，才能返回新的 task-work re-entry typed route。provider、权限、Ruleset、外部服务故障、scope drift、identity drift、已 merge 或身份歧义必须继续 `blocked` 且零业务写入。

### R2 最小 re-entry DTO

新出口或等价闭环合同至少绑定：repository、PR number、expected immutable PR head、canonical task/archive identity、exact finding references、`resume_target=phase-2`。不得携带授权、完整 GitHub payload、本机路径、旧 gate/checkpoint 或 merge authorization。

### R3 受控恢复事务

恢复前必须 fresh 校验 PR open、base/head branch、expected head、remote/local branch、Issue/closure intent、archive commit、task status、finish summary、runtime mapping、worktree dirty state 和 active-task 占用情况。通过后恢复原 task 到 active locator，将状态改为 `in_progress` 并移除 `completedAt`，重建 owner-private mapping，清除旧 check/review/publication/finalization authority，并路由到 Phase 2。

### R4 幂等与完整重跑

interrupted 或 stdout 丢失时，同一 identity 的重试不得重复 archive move 或创建对象。恢复后必须重新执行 task check、task commit、full-diff Branch Review、Publication Review、Finalizer/Delivery 和 expected-head Merge gate；旧证据不可复用。

### R5 投影同步

canonical source、installed preset、workflow targets、schemas、examples、evals、README/spec 以及 Shared/Codex/Claude/Cursor 声明入口必须保持同步。

## 验收标准

1. archived task + Open PR + same-head task-work finding 可通过唯一 typed route 恢复原任务到 Phase 2。
2. 恢复前完成 task/archive/PR/head/base/branch/closure/worktree 的 fresh identity 校验。
3. 恢复不创建第二个 Issue、task、branch、worktree 或 PR。
4. 外部 blocker、scope drift、head drift、已 merge、身份歧义和 dirty conflict 均 fail closed 且零业务写入。
5. interrupted/lost-result recovery 幂等，不重复 archive move 或状态变更。
6. 恢复后旧下游 authority 失效，并强制重跑 Phase 2 到 Merge 的完整图。
7. source、canonical、installed、平台投影、workflow targets、schemas、examples、evals 和 README/spec 同步。
8. eval 覆盖成功恢复、外部 blocker、head drift、scope drift、dirty worktree、重复 active task、已 merge 和中断恢复。

## 非目标与边界

- 不自动绕过、rerun 或 override failed checks。
- 不把外部平台故障伪装成 task-work finding。
- 不允许 merge 后回到 requirement、planning 或 implementation。
- 不创建替代 task、branch、worktree 或 PR。
- 不把手工 `mv` archive 或直接编辑 `task.json` 作为公开操作。
- 不改变 #223 的 required-check 语义，也不吸收 #248/#261 的目标态原子 cutover。

## 未决问题

无阻塞产品或范围问题。具体 owner/consumer 拆分、archive locator 和 authority invalidation 的技术选择在 `design.md` 中明确，并在 Architecture Baseline planning gate 中复核。
