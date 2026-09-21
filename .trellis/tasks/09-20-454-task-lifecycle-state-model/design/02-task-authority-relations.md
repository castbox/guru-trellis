# 02 Task Source、Accepted Scope、Delivery Target 与 Closure 分离

## 1. 要解决的问题

当前合同把外部 Issue identity 与 Closure disposition 一起放入 `source_issue`，随后由 Completion、Closure
和 Finish 反复传递。该结构导致以下四类事实共享一个可变对象：

- task 最初从哪个 Issue 或 no-Issue 请求建立；
- 当前 accepted scope 包含哪些交付与 Issue 关系；
- Delivery 最终集成到哪个 target branch；
- task 完成后是否关闭某个 Issue，以及关闭动作是否成功。

这四类事实的 owner、变化时机和 freshness 完全不同。根本修复是拆开 authority，而不是继续扩展
`source_issue.disposition` 的枚举。

## 2. 唯一 authority

| 事实 | 唯一 authority | 允许的变化 |
| --- | --- | --- |
| 当前 task source identity | tracked `task.json.source` | 仅显式 source-relation correction |
| Accepted scope 与 Issue 关系角色 | 当前 requirement/planning authority | 仅正式 scope mutation |
| Delivery target | tracked `task.json.base_branch` | 仅正式 retarget mutation |
| target ref 当前 HEAD | live Git/GitHub facts | 随 repository 正常演进 |
| Completion 结论 | 当前 generation 的 Completion result | 每次 Completion review 重建 |
| Closure action 与结果 | 当前 generation 的 Closure result | 每次 Closure transaction 唯一形成 |

任何 projection 只引用上述 authority，不产生第二份可独立修改的事实。

## 3. Task source identity

### 3.1 Durable 结构

`task.json.source` 只允许以下两种封闭形态：

```text
IssueSource = { kind: "issue", repo_ref: RepositoryRef, number: PositiveInteger }
NoIssueSource = { kind: "no_issue" }
```

固定规则：

- `repo_ref` 是 portable repository identity，不是本机 remote name、URL 或 path；
- `number` 只标识该 repository 内的 Issue；
- `no_issue` 是完整合法 source，不创建占位 Issue；
- source 不保存 title、state、labels、body snapshot、closing keyword 或 disposition；
- source 不保存 branch、base HEAD、PR、checkout、session 或 ownership；
- source 不代表该 Issue 最终必然被关闭。

### 3.2 建立与修正

Create 在 fresh intake 已确定 source 后写入该字段。Issue creation 与 task creation 是两个独立 mutation；
创建 Issue 成功后必须重新读取 live Issue，再进入 task creation。

Legacy source缺失时，`guru-reconcile-task-source:establish_missing`展示legacy Issue/scope hints作为非权威候选，
接受用户选择的exact Issue或`no_issue`，重新验证repository/Issue identity与current accepted scope后首次写入。
它不得因唯一候选而自动写入。

已有source只在用户明确要求纠正来源、AI重新审查scope authority、并完成
`guru-reconcile-task-source:correct_existing`后才改变。PR body、branch name、Issue mention、task title 和唯一搜索命中都
不能改写 source。修正 source 不改变 TaskId 或 lifecycle generation，但固定使旧 Planning approval、base
reconcile、Task Commit pair、Phase 2 check、Branch Review、closeout Publication、Delivery Review、Delivery
Publication、Completion、Closure 与 Finish eligibility
失效。

当前 generation 已有 sealed Finish 时禁止原地修正。`guru-reconcile-task-source:prepare_reactivation_correction`
对 archived TaskLifecycleKey、current source 与目标 source完成语义审查，只产生绑定 exact archived generation 的
`SourceCorrectionReadyDTO`，其中固定包含archived TaskArtifact identity、current source、reviewed source、
accepted-scope identity与target relation identity，不修改 tracked task。`guru-reactivate-task`是该 DTO 的唯一
consumer，在同一原子transaction中先验证current source未变化，再建立 generation `g+1`、写入已审查
source/scope/target并完成checkout acquisition。Reactivate不得
自行重新判断 source，也不得在旧 generation 上改写历史 Closure/Finish authority。

## 4. Accepted scope 与 Issue 关系

Accepted scope 是 task 要完成什么的语义 authority。它独立表达以下关系：

- exact source；
- reference-only；
- follow-up；
- parent；
- 其它由当前 requirement authority 明确定义的关系。

`task.json.source` 只保存一个当前 source identity。多个 Issue、关系角色、关闭资格和完成条件写在当前
requirement/planning authority 中，不复制进稳定 task metadata。自由文本中仅出现 Issue URL 不自动产生
受控关系；`guru-clarify-requirements` active-task profile必须把实际参与验收或Closure的关系写成明确scope条款。

关系角色变化属于 scope mutation。mutation 完成后，依赖旧 scope 的 Planning approval、base reconcile、Task
Commit pair、Phase 2 check、Branch Review、closeout Publication、Delivery Review、Delivery Publication、Completion、
Closure 与 Finish eligibility 全部失效。

## 5. Delivery target

### 5.1 Durable target

`task.json.base_branch` 表达当前 task 的 portable target branch。它只保存规范化 branch ref 关系，不保存：

- base HEAD；
- merge-base；
- remote-tracking ref 的当前 SHA；
- review range；
- PR number 或 PR state。

Task Commit、Branch Review、closeout Publication、Delivery Review、Delivery Publication、Completion 与 Finish 在
各自调用时重新读取所需的 exact HEAD、merge-base、ancestry 和 live PR facts。不存在跨阶段共享的 durable
`base_head`。

### 5.2 Reconcile 与 retarget

普通 base reconcile 只处理 target ref 的内容演进，不修改 `task.json.base_branch`。旧 HEAD 变为新 HEAD
属于 live Git 变化，不是 task metadata mutation。old base、new base、merge-base与task HEAD只允许存在于当前
pair-guard/Reconcile/Review operation及其相邻consumer DTO中，不形成跨阶段通用`base_head` authority。

Pre-review profile固定分为`post_plan`、`post_check`与`post_commit`。Pair guard每次fresh解析selected base：只有
selected base已是current task HEAD祖先时才是`unchanged`；否则从live Git唯一merge-base派生operation-scoped old
base。Compatible reconcile必须在用户确认exact expected prior task HEAD、new base、candidate tree、双亲顺序、merge
message与零远端副作用后，创建parents为`[prior_task_head, new_base_head]`的本地merge commit。它不得仅记录
candidate后返回一个未把new base纳入task history的`reconciled`结果。

`guru-reconcile-task-base`成功后固定执行以下 transition：

- Task Commit pair、Phase 2 check、Branch Review、closeout Publication、Delivery Review、Delivery Publication、
  Completion、Closure与Finish eligibility全部 stale；
- semantic impact未改变需求、设计或验收合同时，Planning approval保持current；
- semantic impact改变需求、设计或验收合同时，Planning approval变为stale，并进入现有Planning/scope re-entry；
- `post_plan`保留原`task_activation` resume target；`post_check`与`post_commit`固定回fresh Phase 2；
- 新 evidence只能由各原owner基于reconciled committed HEAD重新形成，reconcile result不得替代任一 semantic pass。

首次/full Branch Review只接受selected current base是review HEAD祖先的committed range，并审查
`origin/<base>...reconciled-HEAD`。`post_commit`不得进入bounded continuity。Bounded continuity只适用于已存在prior
full Branch Review的`post_branch_review`、`post_publication`与`finalizer_base_mismatch`，并要求prior review commit、
new base都是current reconciled HEAD祖先且candidate tree identity匹配；它不能替代首次full review。

Target缺失与target relation变化均由`guru-retarget-task-delivery`处理。缺失时使用`establish_missing` profile，
已存在关系变化时使用`retarget_existing` profile；两者均执行以下流程：

1. 读取当前 accepted scope、当前 branch association 与 live target facts；
2. 判断新 target 是否改变需求、设计、验证、Publication 或 Closure 假设；
3. 展示 exact old target 与 new target；
4. 在当前对话确认 mutation；
5. 只更新 `task.json.base_branch` 与直接依赖该 target relation 的 current planning authority；
6. 使旧 Planning approval、base reconcile、Task Commit pair、Phase 2 check、Branch Review、closeout Publication、
   Delivery Review、Delivery Publication、Completion、Closure 与 Finish eligibility 失效。

Retarget 不改变 TaskId、generation、current task branch 或 resource ownership。

## 6. Completion 与 Closure 的固定边界

### 6.1 Completion

Completion 只判断当前 TaskLifecycleKey 的 accepted scope、Delivery history 和 required evidence 是否完整。
`completed` 结果至少绑定：

- TaskLifecycleKey；
- current accepted-scope identity；
- current Completion result identity。

Completion 不决定 `close` 或 `no_mutation`，不写 Issue，不把 disposition 写入 task metadata，也不把旧
`source_issue` 对象传给 Finish。Closure 调用方根据 Completion identity 重新读取 current source、scope 和
Issue relations，形成当前调用的 closure candidate set。

### 6.2 Closure

Closure 是唯一 disposition owner。它同时读取：

- current TaskLifecycleKey；
- current accepted scope；
- current Completion result；
- `task.json.source`；
- scope 中声明的 Issue relation；
- live Issue state 与 repository identity。

Closure 对 current scope 中每个受控 Issue relation 只产生以下一个 action：

- `close`：当前 scope 明确要求关闭 exact eligible Issue，且 live facts 满足关闭条件；
- `no_mutation`：no-Issue、reference-only、follow-up、parent、已关闭 Issue 或 scope 明确不产生关闭动作。

`close` 与 `no_mutation` 组成 Closure action set，不回写 `task.json.source`。Closure result 记录每个 exact
Issue identity 的 action与执行结果，并绑定 TaskLifecycleKey。没有 Issue mutation时整体 typed result为
`no_mutation`；至少一个 close mutation成功且其余 action均收敛时整体 typed result为 `closed`。Finish只消费
该 Closure result identity与完整 action-set result，不重新决定任一 Issue disposition。

Issue-backed 不等于自动 `close`。no-Issue 不等于缺失 source。Closure 对多个 Issue 逐一按 current scope
角色判定，只有 scope 明确拥有关闭责任的 exact Issue 进入 `close`；其余关系固定为 `no_mutation`。同一
Issue identity在 action set中只能出现一次；重复或互相冲突的关系先返回 scope conflict。

### 6.3 Multi-Issue transaction 与部分成功恢复

Closure mutation 开始前固定 action set identity，绑定 TaskLifecycleKey、Completion result identity、accepted
scope identity、Delivery target identity 与按 Issue identity 排序的完整 action set。Transaction 未收敛期间
source、scope、Delivery target、base reconcile、branch rebind、checkpoint、machine handoff、Publication、Completion、
Finish与Reactivate mutation全部不可达；只读诊断与同一Closure transaction恢复可达。每个 Issue item独立记录 `pending`、
`satisfied_no_mutation`、`closed_verified` 或
`external_change_conflict`，整体只有以下结果：

- 全部 item 为 `satisfied_no_mutation`：整体 `no_mutation`；
- 至少一个 item 为 `closed_verified` 且其余 item均已满足：整体 `closed`；
- 仍有 `pending`：整体 `closure_in_progress`，由同一 Closure owner继续；
- 已验证关闭的 item 后续重新 open，或 live Issue identity/eligibility 变化：整体进入
  `closure_external_change_conflict`，重新执行 semantic Closure review，不自动再次关闭。

`satisfied_no_mutation`必须同时记录固定 satisfaction basis：`relation_has_no_close_authority`或
`already_closed_at_review`。前者覆盖reference-only、follow-up、parent与scope明确不关闭的关系，不依赖后续
live Issue open/closed变化；后者依赖review时的live closed state。`already_closed_at_review` item后续重新open
时固定进入`external_change_conflict`。No-Issue task的action set为空，整体直接形成`no_mutation`，不制造伪
Issue item。

每次进入或恢复 transaction 都按固定 action set逐项重新读取 live Issue。已满足 item不重复 mutation；open
且仍为 `close` 的 pending item执行 close并立即重读；单项失败保留其它已完成 mutation，不回滚已经关闭的
Issue。Close 成功但本地结果丢失时，exact transaction identity与 live closed state足以把该 item恢复为
`closed_verified`。只有全部 item收敛后才形成供 Finish 消费的整体 Closure result。

### 6.4 Finish entry freshness

Closure result形成后不冻结外部Issue。Finish在开始任何archive、association或ledger mutation前，对完整action set
执行只读freshness validation：

- `closed_verified` item必须仍指向同一repository/Issue identity且live state仍为closed；
- satisfaction basis为`already_closed_at_review`的item必须仍为closed；
- satisfaction basis为`relation_has_no_close_authority`的item不因live open/closed变化失效；
- no-Issue空action set不读取伪Issue；
- 任一需要closed的item重新open，或Issue identity/eligibility发生变化时，Finish不重新判断disposition、不开始
  terminal mutation，固定返回`guru-complete-task-closure:external_change_conflict`。

Finish freshness通过只证明Closure action set仍满足，不替代Closure semantic review。Finish transaction一旦开始，
普通lifecycle mutation不可达；外部Issue随后变化不回滚已经开始的本地terminal transaction。

## 7. Public handoff 约束

固定最小边界如下：

| Producer -> Consumer | 必需 handoff | Consumer fresh reread |
| --- | --- | --- |
| Create -> Planning | TaskId、TaskRef、generation | source、scope、delivery target |
| Completion -> Closure | TaskLifecycleKey、Completion result identity | source、scope、Issue relations、live Issue |
| Closure -> Finish | TaskLifecycleKey、Closure result identity、完整action-set result | current task artifact、target relation、每个live Issue freshness |
| Finish -> Cleanup | TaskLifecycleKey、Finish result identity | resource ledger 与 live Git |

`source_issue` 聚合对象不再跨上述边界传递。任何 consumer 需要 source 时都从 TaskId 对应的 current task
artifact 读取，并验证 TaskLifecycleKey。

## 8. Failure matrix

| 状态 | 唯一结果 |
| --- | --- |
| Issue source 与 live repository/number 匹配 | source valid |
| `kind=no_issue` | source valid，不进入 Issue mutation |
| source 缺失或结构非法 | `source_relation_invalid`，阻塞 semantic lifecycle mutation |
| source 与用户要求不一致 | 进入显式 source-relation correction |
| base ref HEAD 前进 | 正常 live evolution，不改 task metadata |
| base reconcile 成功且无 planning impact | Planning保持current；Task Commit pair及全部下游 evidence stale |
| base reconcile 发现 planning impact | Planning及全部下游 evidence stale，进入Planning/scope re-entry |
| delivery target relation 变化 | 进入显式 retarget |
| Completion 未通过 | 不进入 Closure |
| Completion 通过但 scope/Issue facts 已变化 | Closure 拒绝旧输入并重新读取 |
| exact eligible Issue 仍 open | Closure 选择 `close` |
| no-Issue 或非关闭关系 | Closure 选择 `no_mutation` |
| close mutation 成功但结果丢失 | Closure 按 exact transaction 与 live Issue state恢复 |
| 一个 Issue 已关闭、后续 Issue mutation失败 | 保留已完成 item，整体 `closure_in_progress`，同 owner只继续 pending item |
| 已验证关闭的 Issue 后续重新 open | `closure_external_change_conflict`，重新 semantic review，不自动重关 |
| 因 `already_closed_at_review` 满足的 Issue 后续重新 open | `closure_external_change_conflict`，重新 semantic review |
| 因 relation 无关闭权而满足的 Issue open/closed变化 | 原 `satisfied_no_mutation` 保持有效 |
| Closure 已收敛但 Finish 前 required-closed Issue重新 open | Finish不开始mutation，返回`closure_external_change_conflict` |
| Closure result generation 不匹配 | Finish 拒绝并返回 current generation owner |

## 9. 当前设计结论

本问题固定以下结论，最终状态仍由全量审核决定：

1. `task.json.source` 只保存 current source identity；
2. Issue relation roles 与 closing eligibility 只属于 accepted scope；
3. `task.json.base_branch` 只保存 portable Delivery target；
4. base HEAD 永远是调用期 live fact；
5. Completion 不拥有 Closure disposition；
6. Closure result 独占 close/no-mutation action 与结果；
7. 多 Issue Closure 使用固定 action set 与逐项幂等恢复，不回滚已完成外部 mutation；
8. Closure in-progress冻结全部会改变其输入或evidence lineage的mutation；
9. Finish在terminal mutation前fresh验证Closure action set，外部变化返回Closure owner；
10. 现有 `source_issue.disposition` 跨 Skill 聚合合同必须整体退出。
