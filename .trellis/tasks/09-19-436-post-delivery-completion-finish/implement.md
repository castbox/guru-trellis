# #436 执行计划

状态：Phase 1 candidate。只有规划批准并执行 `task.py start` 后才进入本计划；本轮不执行。

## 1. 实施顺序

1. 每轮操作前运行 workspace boundary check，fresh 回读 #436、#435、#434、task metadata、current diff、RDT/Architecture identity 与 package registry。
2. 建立 `guru-review-task-completion` canonical package：completion 与 evidence-refresh profiles、7 个 exits、AI gate、private checkpoint、recorder/checker、独立 schemas/examples/evals/tests。
3. 建立 `guru-complete-task-closure`：Completion `completed` consumer、no-mutation/reference-only 分类、exact Issue close transaction、GitHub CLI read/mutation/post-check 与 same-transaction recovery。
4. 建立 `guru-finish-task`：Closure consumer、archive/terminal metadata 生成、bookkeeping allowlist、expected-head PR transaction、merge 后目标基线验证与 success projection。
5. 建立 `guru-cleanup-task-resources`：只消费当前 Finish success，资源发现、scope confirmation、删除 executor、失败保留前序结果与旧 success 隔离。
6. 建立 `guru-reactivate-task`：正常结束 archived task identity 验证、workspace 复用/重建、archive -> active 唯一 move、requirements/planning/implementation/evidence-refresh typed routes。
7. 对既有 workflow/lifecycle 合同做最小 additive 调整：Completion 只接 #435 `delivered` 与 evidence-refresh；旧 `guru-restore-archived-task` 继续只接 Merge Phase 2 re-entry；不增加旧 output adapter。
8. 增加端到端 fixtures：多 Delivery completion、remaining work、external evidence pending、additional delivery、no-Issue/reference-only closure、closure output loss、bookkeeping PR、Cleanup retry、Reactivate business/validation-only、同月/跨月 archive、旧格式 archive。
9. 更新 canonical registry/interface/consumer schemas、workflow/spec/README、preset manifest/installer 与 source package tests；应用 preset 同步 dogfood/installed/Shared/Codex/Claude/Cursor projections，逐项处理 `.new/.bak`。
10. 建立 task-owned RDT contribution 与必要 Architecture contribution/ADR；不直接竞争 shared current，promotion 由 Architecture/RDT owner 单写。
11. 执行定向验证、Phase 2、Task Commit、独立 committed full-diff Branch Review；若 promotion 产生新 diff，重新执行 Phase 2/Commit/Branch Review。#434 activation 与 Release matrix 留给对应 owner。

## 2. 需求—设计—测试映射

| Requirement | Design | Test group |
| --- | --- | --- |
| R436-01 Completion | D436-01, D436-03 | T436-01..10 |
| R436-02 Closure | D436-02 | T436-11..17 |
| R436-03 Finish persistence | D436-03, D436-04 | T436-18..30 |
| R436-04 Cleanup | D436-04 | T436-31..35 |
| R436-05 Reactivate | D436-05 | T436-36..48 |
| R436-06 Migration/cutover | Sections 1, 5 | T436-49..56 |

## 3. 验证矩阵

| ID | 场景 | 通过条件 |
| --- | --- | --- |
| T436-01 | one Delivery completion | fresh delivered fact + accepted scope + evidence 只在满足条件时返回 `completed` |
| T436-02 | two sequential Deliveries | A/B facts 聚合，B remaining work 不提前完成 |
| T436-03 | remaining work | 返回 `remaining_work`，task active，无 Closure/Finish |
| T436-04 | evidence pending | 返回 `evidence_pending`，只允许 evidence-refresh，不伪造 completed |
| T436-05 | additional Delivery | 返回 `additional_delivery_required`，不生成 Closure/Finish |
| T436-06 | requirements revision | 需求 authority 变化回 requirements/Planning owner |
| T436-07 | implementation revision | 实现 finding 回 Phase 2，保持同一 task |
| T436-08 | stale identity | Delivery/requirement/evidence/base 任一 stale 时零 completed |
| T436-09 | evidence-refresh | Reactivate validation-only 与 evidence_pending 更新共享同一 profile |
| T436-10 | Completion output loss | fresh semantic rerun，不从旧摘要重建 pass |
| T436-11 | no-Issue/reference-only | Closure 返回 `no_mutation`，不调用 close API |
| T436-12 | parent/follow-up | 不关闭 parent，不创建 follow-up Issue |
| T436-13 | exact source Issue | 展示 repo/Issue/action/reason 后一次独立 close confirmation |
| T436-14 | closure provider failure | 同一 transaction recovery，不重复 close |
| T436-15 | closure output loss | live terminal facts 重建同一 closure DTO |
| T436-16 | Issue state mismatch | identity/permission/provider uncertainty fail closed |
| T436-17 | Delivery closing keyword | Delivery/Finish PR 使用 `Refs`/无 closing keyword |
| T436-18 | Finish precondition | 未有 Closure completed 时不得生成 Finish success |
| T436-19 | archive projection | active removal、archive task、finish-summary、metadata identity 一致 |
| T436-20 | bookkeeping allowlist | 业务代码、其它 task、共享 journal/runtime path 一律阻断 |
| T436-21 | expected-head binding | base/head drift 或 multiple PR 在 mutation 前阻断 |
| T436-22 | bookkeeping PR | 只产生行政 PR，不创建 task、不产生 Delivery result |
| T436-23 | bookkeeping output loss | same PR/merge transaction recovery，零重复 mutation |
| T436-24 | merge post-check | archive 未在目标基线、active 未移除或 metadata 不一致时无 success |
| T436-25 | Finish success | 仅 post-merge archive identity 验证通过后发出 success |
| T436-26 | same-month rearchive | 不重复目录、不嵌套、不保留双 identity |
| T436-27 | cross-month rearchive | 旧 archive 精确删除/更新，新 archive 唯一可发现 |
| T436-28 | old format archive | fresh identity 验证后可正常承接，不批量 backfill |
| T436-29 | Finish no recursion | bookkeeping PR 不触发 Completion、Delivery discovery 或自身 Finish |
| T436-30 | Finish blocked | archive 偶发中断只报告 blocked/remaining actions，不虚假 success |
| T436-31 | Cleanup target set | 只发现本轮 owned branch/worktree/runtime resources |
| T436-32 | Cleanup confirmation | 精确删除目标展示并独立确认 |
| T436-33 | Cleanup failure | 不回滚 Completion/Closure/Finish，保留剩余资源事实 |
| T436-34 | old success isolation | Reactivate 后旧 Finish success 不可驱动当前 Cleanup |
| T436-35 | consumer preservation | 用户 checkout、其它 task、archive、有 consumer runtime 不被删除 |
| T436-36 | archived identity | 目录名/Issue closed 单独不足，必须验证完整 archive evidence |
| T436-37 | same task identity | Reactivate 不创建替代 task/follow-up，Issue 关联保持 |
| T436-38 | reuse workspace | 适合复用的 branch/worktree 重新绑定前 fresh 验证 |
| T436-39 | prepare workspace | 资源清理后从当前 base 准备新 branch/worktree 并绑定原 task |
| T436-40 | active/archive move | 同一 identity 唯一 active copy，无双副本 |
| T436-41 | reactivation routing | requirements/planning/implementation/evidence-refresh 各有唯一 typed consumer |
| T436-42 | old completion facts | 上轮 Completion/Closure/Finish 仅作历史，不作为本轮 pass |
| T436-43 | business reactivation | 有业务 diff 时进入新 Delivery，不重开旧 merged PR |
| T436-44 | validation-only reactivation | 无业务 diff 时 evidence-refresh -> Completion，无空业务 PR/result |
| T436-45 | rearchive | 再次完成后 archive 路径无冲突，Finish summary 表达本轮结果 |
| T436-46 | reactivate output loss | 恢复 deterministic transaction 同一 workspace/binding，不重复创建 task |
| T436-47 | invalid scope/base | 无法证明 scope/base/resource identity 时 blocked |
| T436-48 | Issue reopen boundary | Issue reopen 不被 Reactivate 隐式执行 |
| T436-49 | additive registry | 五个 package、schemas、consumers、tests closure 完整 |
| T436-50 | production graph boundary | #434 前 22 invokes/98 exits 与旧 edge 字节/行为不变 |
| T436-51 | no adapter/dual graph | 不存在 old-output adapter、ledger、第二 lifecycle writer |
| T436-52 | projection parity | canonical/installed/platform package bytes、modes、manifest 一致 |
| T436-53 | preset reapply | clean install/reapply 正常，`.new/.bak` 按合同处理，无 managed drift |
| T436-54 | package closure | interface/schema/consumer/command/eval/source-installed inventory 通过 |
| T436-55 | task/RDT/Architecture trace | task artifacts、contribution、ADR、测试与 owner identity 可追溯 |
| T436-56 | repository checks | task validate、JSON/schema、Python/shell、ownership、dogfood drift、`git diff --check` 通过 |

## 4. 验证范围与停止条件

执行普通 Issue 的定向 source/installed/package/runtime、代表性 clean throwaway、preset reapply、projection
parity 与 task checks；不把本任务扩张为专门 Release Issue 的完整多平台矩阵。任何缺失 GitHub auth、外部 evidence、
provider access 或环境依赖均记录为 blocked/unverified，不得当作通过。规划通过前不运行 `task.py start`；规划
批准后仍须由 Phase 2 semantic check、Task Commit 与 independent committed full-diff Branch Review 放行。

## 5. 预期变更位置

canonical 优先：`trellis/skills/guru-team/`、`trellis/workflows/guru-team/`、`trellis/presets/guru-team/` 与
对应 `schemas/consumers/tests`。`.trellis/**`、`.agents/**`、`.codex/**`、`.claude/**`、`.cursor/**` 仅由 preset
apply 生成/同步；不把 dogfood 副本作为唯一源头。无关 dirty/untracked 文件不 stage、不覆盖、不清理。
