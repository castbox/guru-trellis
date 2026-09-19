# #436 技术设计：Post-Delivery Completion、Issue Closure 与 Finish 持久化

状态：Phase 1 candidate。设计只描述 owner topology、公共合同、持久化边界与验证承接；不表示实现或
production graph 已激活。

## 1. 设计原则与现状绑定

采用 `target_native`：把 task completion、Issue closure、Finish bookkeeping、resource cleanup 与正常
结束后的 Reactivate 从 #435 Delivery 中拆出，避免一次 Delivery merge 重新成为 task terminal 状态。

现状绑定：

- Requirements/Design/Test/Architecture current identity：`current-main-0.6.17-guru.55` / `active`；
- #435 已提供 additive Delivery capability，当前 registry 为 26 packages / 114 exits / 96 commands；
- production workflow 仍为 22 mandatory invokes / 98 exits；
- #434 独占 graph activation 与旧 edge retirement；
- 现有 `guru-restore-archived-task` 只负责 Merge 发现 task-work finding 后的 Phase 2 回退，不承接正常结束 task 的 Reactivate。

所有 public Skill 均遵守当前 Skill package contract：独立 input、每个 exit 独立 output、consumer-owned input、
薄 projection、private checkpoint 不跨 owner 读取；semantic Skill 的顺序为 AI 判断 -> 必要确认 -> recorder/checker
-> 单一 typed exit。

## 2. Owner topology

### D436-01 Completion owner

`guru-review-task-completion` 是唯一 completion semantic owner。其 input 只承接：`task_ref`、accepted scope
locator/freshness、Delivery fact selector、current evidence selector、source disposition 与调用 profile。
它自己 fresh 读取 live authority，不读取 #435 或自身的 private checkpoint。

Typed exits：

| Exit | 最小 handoff | 唯一 consumer |
| --- | --- | --- |
| `remaining_work` | `task_ref`, `resume_target=active-task` | 当前 task 的既有 plan/implementation router |
| `evidence_pending` | `task_ref`, `resume_target=evidence-refresh` | `guru-review-task-completion:evidence_refresh` |
| `additional_delivery_required` | `task_ref`, `resume_target=delivery-planning` | #435 Delivery/Planning owner |
| `requirements_revision_required` | `task_ref`, `resume_target=requirements` | 现有 clarification/Planning owner |
| `implementation_revision_required` | `task_ref`, `resume_target=phase-2` | `guru-resume-implementation` |
| `completed` | `task_ref`, `completion_ref`, `closure_input_ref` | `guru-complete-task-closure` |
| `blocked` | `reason_code`, `remediation` | `task-completion-blocked` stop |

`evidence_refresh` 是同一 Skill 的 profile，不是第二 completion owner。它必须以 fresh evidence 请求进入，
不得携带 `completed=true` 或伪造 Delivery identity。

### D436-02 Closure owner

`guru-complete-task-closure` 只接受 Completion `completed` 的最小 DTO。AI 判断 source Issue 是否可关闭及
no-mutation disposition；deterministic executor 负责 repo-bound GitHub CLI read/mutation 与 post-check。

Typed exits：

| Exit | 最小 handoff | 唯一 consumer |
| --- | --- | --- |
| `no_mutation` | `task_ref`, `disposition_ref` | `guru-finish-task` |
| `closed` | `task_ref`, `issue_ref`, `closure_ref` | `guru-finish-task` |
| `resume_closure` | `task_ref`, `transaction_ref` | Closure owner itself |
| `blocked` | `reason_code`, `remediation` | `task-closure-blocked` stop |

`closure_ref` 只绑定目标 repo/Issue、动作与 provider terminal identity；完整 Issue snapshot、授权过程、
confirmation 文本与执行 transcript 保持 private。no-Issue/reference-only/follow-up/parent 不生成 Issue
identity，也不调用 close API。

### D436-03 Finish owner

`guru-finish-task` 是唯一 terminal bookkeeping owner。它消费 Closure `closed|no_mutation`，但仍需 fresh
校验 Completion/Closure identity、当前 task binding 与目标基线。其内部拆成 semantic preparation/review 与
deterministic bookkeeping executor，但对外只暴露 Finish Skill 的公共合同。

Finish transaction 顺序：

1. 重新读取 task、archive、binding、目标基线、当前 Git/GitHub facts，确认本次 finish plan 未过期；
2. 在 owner-private state 中准备 active -> archive 的净变化、terminal metadata、finish-summary 与 allowlist；
3. 由 AI 审核 bookkeeping diff：只能包含本 task active 删除、必要旧 archive 删除/更新、最终 archive、
   finish-summary 与必要 metadata；禁止业务代码、其它 task、共享 tracked journal/runtime；
4. 在副作用前展示精确 commit/push/PR/merge action，分别取得当前对话确认；
5. 用 expected-head-bound deterministic Git/GitHub primitives 创建/接管唯一 bookkeeping PR，验证 draft/ready/
   merge terminal facts；
6. merge 后在目标基线读取 archive identity、active removal、metadata 与 PR identity；不满足时返回 blocked，
   不返回 success；
7. 只在 post-merge check 通过后发出 `success`，并把最小 binding-exit facts 交给 Cleanup。

Finish PR 的 merge commit/PR body 不得带 #435 Delivery trailer 或 Issue closing keyword，且不进入 Delivery
history discovery。Finish 不调用 Completion，不重新执行业务 Delivery Review/Branch Review，不创建 task。

### D436-04 Cleanup owner

`guru-cleanup-task-resources` 只消费 Finish `success`。它 fresh 重新计算本轮资源集合并进行 semantic scope review；
确认后由确定性 executor 删除精确 target。Cleanup output loss 可以从 Finish success 与 live resource facts
重新进入同一 cleanup call，但旧 success、旧 workspace 或新的 Reactivate binding 不可复用。

### D436-05 Reactivate owner

`guru-reactivate-task` 与 `guru-restore-archived-task` 使用不同 interface/schema，不复用旧 public I/O。
它的 input profile 为 `reactivate_completed_task`，另有 `evidence_refresh` 只补验证入口由 Completion
消费。AI fresh 判断 exact task identity、正常结束证据、原 scope、历史 Delivery、current base、恢复原因与
资源适用性；确定性 workspace executor 只执行已确认的 branch/worktree/binding/task move。

Typed exits：

| Exit | 最小 handoff | 唯一 consumer |
| --- | --- | --- |
| `reactivated_to_requirements` | `task_ref`, `resume_target=requirements` | clarification/Planning owner |
| `reactivated_to_planning` | `task_ref`, `resume_target=planning` | Planning owner |
| `reactivated_to_implementation` | `task_ref`, `resume_target=phase-2` | `guru-resume-implementation` |
| `reactivated_to_evidence_refresh` | `task_ref`, `resume_target=evidence-refresh` | Completion evidence-refresh profile |
| `reactivate_blocked` | `reason_code`, `remediation` | `task-reactivate-blocked` stop |

不设“回最早 owner”模糊出口；每个恢复目标必须在 workflow/router 中有可执行唯一 consumer。

## 3. 状态与 identity

task identity、Issue identity、workspace/branch identity 与 Delivery identity 分离：

- task identity：原 `task_ref` 与 task metadata stable identity，Reactivate 不变；
- Issue identity：Closure 只对 exact source Issue 生效，no-Issue/reference-only 保持无 mutation；
- workspace identity：可复用旧资源或新建资源，但始终只保留一个 active/archive task copy；
- Delivery identity：继续由 #435 merge trailer + Git/GitHub facts 重建；Finish PR 无 trailer；
- terminal identity：本轮 Completion/Closure/Finish 通过最小 refs 连接，旧轮结果不具备本轮 freshness。

## 4. bookkeeping allowlist 与 rollback

Finish 生成 expected allowlist，至少覆盖：

- 本 task active directory 的移除；
- 目标 archive directory 的最终 `task.json`、`prd.md`、`design.md`、`implement.md`、`finish-summary.json`；
- 必要的 archive index/history/terminal metadata；
- Reactivate 同月/跨月时旧 archive 路径的精确删除或更新。

allowlist 明确排除业务源文件、其它 task、共享 tracked journal、runtime、未绑定 overlay 与 Delivery PR 内容。
任何额外路径、active/archive 双副本、目录嵌套、错误 task identity 或 base/head 漂移均 fail closed。

Rollback 以 owner transaction 为单位：Completion/Closure/Finish/Cleanup/Reactivate 各自只恢复同一 owner 的
未完成 deterministic transaction；不回滚已经确认的前序语义结果，不重复业务 Delivery，不引入通用跨阶段
checkpoint 或恢复状态机。

## 5. Additive distribution 与 cutover

canonical source 预计新增：

- `trellis/skills/guru-team/packages/guru-review-task-completion/`
- `trellis/skills/guru-team/packages/guru-complete-task-closure/`
- `trellis/skills/guru-team/packages/guru-finish-task/`
- `trellis/skills/guru-team/packages/guru-cleanup-task-resources/`
- `trellis/skills/guru-team/packages/guru-reactivate-task/`

并同步 registry/interface、consumer schemas、workflow/spec/README、preset manifest/installer、installed 与
平台 projections、package-local tests/evals。当前 production workflow 只保留现有 graph markers；#434 在两组
capability ready 后统一接入新 edges，禁止本任务提前增加 mandatory invoke 或 retirement。

## 6. 失败矩阵摘要

| 场景 | 结果 |
| --- | --- |
| delivery facts/requirements/evidence stale | Completion 非 `completed`，回最早受影响 owner |
| remaining work 未完成 | `remaining_work`，task active |
| 需要新业务 PR | `additional_delivery_required`，不执行 Closure/Finish |
| source Issue 不应关闭 | Closure `no_mutation` |
| close provider unknown/output loss | same closure transaction recovery |
| bookkeeping allowlist 越界 | Finish blocked，绝不发 success |
| merge 成功但 archive/base post-check 不一致 | Finish blocked，不 Cleanup |
| Cleanup 失败 | 保留 Completion/Closure/Finish，报告剩余资源 |
| archived identity/scope/base 无法证明 | Reactivate blocked |
| Reactivate 仅补验证且无业务 diff | evidence-refresh -> Completion，无空 Delivery |
| production graph 尚未切图 | 新 packages additive，旧 graph 保持可运行 |
