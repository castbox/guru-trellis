# #454 建立统一 task lifecycle state model

## 目标

建立一个统一、封闭、可恢复的 task lifecycle 领域模型，彻底消除
`task_workspace` 将 task identity、branch、checkout path、session、Git HEAD 与资源 ownership
混为同一对象所造成的重复 authority。

完成后，Guru Team 必须同时满足以下用户结果：

- 同一 task 在 rename、checkout 移动、跨 session、跨机器、branch rebind、archive 和 Reactivate
  过程中保持同一稳定身份；
- 调用方在首个 prompt 前预建 checkout，以及 Guru 在 task 创建时新建 checkout，两种入口得到同一
  lifecycle 语义；
- 当前执行位置只通过 live Git facts 解析，不依赖 tracked 绝对路径、历史 mapping 或目录命名约定；
- 自动解析无法得到唯一合法目标时，流程向用户提供候选或接受用户显式指定，并对选定目标执行完整
  live validation；
- runtime control state 丢失后，合法 lifecycle 能恢复，无法证明的历史 ownership 不会被猜测；
- branch rebind、Publication、Finish 和 Cleanup 在同一状态模型中闭合，不产生互相矛盾的局部规则；
- 正常 Cleanup 只删除 Guru 明确拥有的资源；未知 ownership 与 caller-owned 资源只能在用户另行选择并
  确认的手工清理路径中删除。

本 task 已完成规划并进入分阶段实施，不修改 Issue #454。C1、C2、D0 与 C3 已完成；PR #465 只完成
C3，不表示 C3-C7 已全部完成。当前交付为 C4 branch association、establishment 与 rebind substrate。
C5-C7、D443、D436、E434 与 #434 activation 仍未完成；完整 Skill package、production graph、
installed/platform projection 与 predecessor retirement 仍由 E434 在同一原子激活边界交付。

## 背景与已确认事实

### 当前问题

当前生产合同把下列事实重复写入 tracked task metadata、ignored runtime mapping 与 session state：

- task identity；
- branch 与 base；
- checkout path、slug 和 topology；
- HEAD 与 base HEAD；
- session binding；
- lifecycle generation；
- branch、worktree 与 remote branch ownership。

这些事实具有不同的稳定性、owner 和生命周期。绝对路径会因 worktree move、重新 clone、跨机器恢复
而变化；HEAD 会随正常提交、base reconcile、Publication 和 Finish 演进；session 只在本地短期有效；
resource ownership 则必须跨 rebind 保留至 Cleanup。同步更多副本不能消除这些差异，只会扩大 stale、
mismatch 和不可恢复状态。

### 现有 authority 边界

- #329 已完成 developer identity 与 `.trellis/workspace/**` journal/index 退役；该结论继续有效。
- #329 中将 `task.json.worktree_path` 与 task/workspace runtime mappings 保留为 task identity authority 的
  条款，由本需求取代。
- #443 已证明稳定 task identity、短期 session binding、跨 session resume 与 generation invalidation
  的必要性；其对 task/workspace mappings 和固定 checkout path 的依赖属于待替换现状。
- 当前 Architecture 已固定 Completion、Closure、Finish、Cleanup 和 Reactivate 为五个独立 semantic
  owner；本需求不得重新合并这些职责。
- #434 独占 production lifecycle graph 激活。本需求只定义该 graph 必须消费的统一 task lifecycle
  substrate，不提前执行 #434 的全局切图。

## 领域边界

统一模型必须明确区分以下九类领域事实。每类事实只有一个语义 owner，任何 projection 不得成为第二
authority。

| 类别 | 稳定性与职责 |
| --- | --- |
| Task Identity | repository lifecycle history 内稳定且不可复用的 task 身份；rename、archive、Reactivate 和 branch rebind 均不改变它。 |
| Task Source Relation | task 与外部 Issue 或 no-Issue 来源之间的 durable 关系；它不承载 checkout、branch、session、Delivery、Completion 或 Closure 状态。 |
| Delivery Target | task 计划集成到的 portable repository/ref 关系；current target ref 的 HEAD 始终是调用期 live fact，不进入 durable task authority。 |
| Lifecycle Incarnation | 区分初次 active lifecycle 与每次 Reactivate 后的新一代 lifecycle；旧一代控制状态和 terminal receipt 不得驱动新一代。 |
| Current Branch Association | 当前 lifecycle incarnation 与一个 portable Git branch ref 的唯一关系；显式 rebind 改变该关系，但不改变 task identity。 |
| Execution Checkout | 当前调用用于读取或写入 task 的 live Git checkout；路径与 topology 是调用期事实，不是 durable task identity。 |
| Session Association | 当前 session 与 task identity、lifecycle incarnation 的短期关系；不保存 checkout path、branch authority 或用户授权。 |
| Resource Ownership | 每次资源取得与 branch rebind 产生的 local branch、linked worktree、remote branch 的 cleanup 责任；它独立于 current branch association。 |
| Lifecycle Results | Delivery、Completion、Closure、Finish、Cleanup 和 Reactivate 各 owner 产生的最小 durable result；一个结果不得替代另一个阶段的判断。 |

`task_workspace` 不再是领域对象。Git checkout 与 Git linked worktree 继续作为执行资源存在，但不形成
新的同义长期对象。

## 不可违反的 Invariants

### I-454-01 稳定 task identity

- 每个 task 在同一 repository lifecycle history 中拥有一个稳定 identity。
- rename 只改变可变 locator 与 display information，不改变 task identity。
- archive 与 Reactivate 沿用原 task identity。
- 已被无关 task 使用过的 identity 不得再次分配。
- 缺失合法稳定 identity 的 legacy task 不得通过目录名、Issue number、branch name 或 checkout path
  自动猜测；流程必须进入显式 identity establishment，由用户指定 candidate，并在写入前执行与新 task
  相同的格式、repository-local uniqueness 和冲突校验。

### I-454-02 Durable task facts 最小且可移植

- Durable task facts 只包含 task lifecycle 的稳定事实与具有直接长期 consumer 的 portable facts。
- checkout path、worktree root、checkout topology、branch authority、Git HEAD、base HEAD、session identity、
  platform identity、runtime profile 和 resource ownership 不属于 durable task identity。
- base reconcile、commit、review、publication 和 finish 各自读取本步骤所需的 fresh Git identity；不存在
  跨阶段通用 `base_head` authority。
- Delivery target 只表达 portable repository/ref 关系。target ref 的 HEAD 演进不要求改写 task metadata；
  target relation 本身发生变化时，必须由独立的 Delivery-target mutation 明确更新。
- Legacy extra fields 不触发 tracked metadata 清理提交；生产 reader 停止把它们当作 authority。

### I-454-03 Source、scope 与 Closure 分离

- 外部 source identity、task accepted scope、Completion 结论和 Closure disposition 是四类独立事实。
- no-Issue task 是完整合法路径，不创建虚构 Issue，不生成隐含关闭语义。
- Issue-backed task 的 source identity 不从自由文本 scope、branch、session、PR body 或 title 反推。
- Closure 只能消费 fresh accepted scope、Completion result 与 live Issue facts 作出 disposition；Closure
  disposition 不写回稳定 task identity 作为可变 authority。
- 一个 task 引用多个 Issue 时，关系角色与关闭资格必须由受控 scope authority 明确表达，不得用单一
  source 字段同时冒充 identity、关系角色和 Closure 决策。

### I-454-04 Current branch 唯一且支持显式 rebind

- 每个稳定active lifecycle incarnation恰好存在一个current branch association。计划内machine handoff在source
  release与destination consume之间进入唯一`handoff_released` transaction state，此时零个current
  association且只允许handoff recovery/consume；任何状态均不得同时存在两个current association。
- task 与 branch name 相互独立；branch name 不编码 task identity。
- branch rebind 是显式 lifecycle mutation。成功后 task identity 与 lifecycle incarnation 保持不变，
  current branch association 只指向新 branch。
- dirty working tree 只允许 `same-checkout-new-ref` route：在同一 registered checkout、同一 HEAD 上创建并
  切换到尚不存在的新 branch ref，index 与 working tree 必须逐字节保持不变。
- existing-target route 要求 source checkout clean、target checkout 已包含 exact TaskLifecycleKey artifact，且
  target content identity 已由当前 workflow owner 判定为合法接续点。
- rebind 不复制、丢弃或改写未提交内容，不迁移未交付提交，也不隐式执行 stash、cherry-pick、rebase、
  merge、reset 或 force push。不同历史只能先进入显式 reconcile，再重新发起 existing-target rebind。
- 同一 Git ref 在同一时刻最多对应一个尚未收敛的 resource incarnation。历史 ref 只有在前一 resource
  incarnation 已完成保留或清理责任、且不再存在 identity 冲突后，才具备再次成为 current target 的资格。
- branch association 缺失属于可恢复状态；重复、冲突或无法通过 live facts 验证的 association 属于
  invalid state。

### I-454-05 Checkout 只由 live facts 解析

- checkout path、目录名、slug 和 `source_checkout` 不构成 task identity。
- 每次需要工作树内容的操作，均从 stable task identity、current branch association 与 live Git facts
  解析唯一 execution checkout。
- execution checkout 必须属于当前 repository，绑定 current branch，并包含匹配的 current task artifact。
- `git worktree move`、目录重命名与机器路径变化不要求修改 task metadata、session state 或 branch
  association。
- 无 checkout、多个 checkout、detached checkout、foreign repository、branch mismatch 和 task artifact
  mismatch 均产生明确且互斥的 resolution result，不得猜测。
- 不需要工作树内容的 repository control operation 不依赖任一历史 checkout path。

### I-454-06 自动推导与人工选择使用同一验证合同

- 自动解析只在恰好存在一个合法 candidate 时自动选定。
- 零 candidate 与多个 candidate 均进入 selection-required 交互，不得终止整个 lifecycle。
- selection-required 向用户提供足以区分候选的当前事实；这些事实只服务当前交互，不进入 durable
  task 或 session authority。
- 用户既能选择已发现 candidate，也能显式指定未列出的 branch 与 checkout acquisition target。
- 用户选择只决定待验证 target，不覆盖 repository identity、task identity、lifecycle incarnation、branch
  exclusivity、task artifact identity、checkout suitability 和 live freshness validation。
- 选定 target 在 mutation 前必须重新读取 live facts。候选已变化时旧选择失效并返回新的 resolution。
- 自动推导失败不得成为拒绝合法人工恢复的理由；人工指定也不得成为接受不合法 target 的理由。

### I-454-07 Session binding 短期、无路径、可重建

- session association 只绑定 session context、task identity 与 lifecycle incarnation；task locator 每次从
  stable task identity 重新解析。
- session association 的领域 payload 恰好是 `task_id + lifecycle_generation`；不保存 `task_ref`。公开 handoff
  使用同构的 `TaskLifecycleDTO`，需要读取 task artifact 的 consumer 按 TaskId fresh 派生并验证 TaskRef。
- session association 不保存 branch authority、checkout path、HEAD、resource ownership、semantic pass 或
  用户授权。
- context key 不可用时不写 session record，也不阻塞或回滚已成立的 lifecycle；当前 invocation 进入
  `explicit_task_mode`，后续 invocation 重新要求显式 TaskId 或 candidate selection。
- session association 丢失时，基于 durable task facts、current branch association 与 live Git facts重建。
- 同一 task 能先后由多个 session 继续；同一 session 能受控从 task A 切换到 task B，再返回 task A。
- session switch 分别验证 source task 与 target task，不覆盖另一个 task 的 current state。
- Reactivate 后，旧 lifecycle incarnation 的 session association 自动失效。

### I-454-08 Resource ownership 独立且保守

- Resource ownership 在 branch、worktree 或 remote branch 被取得时确定，不从资源当前存在状态、命名、
  task identity、branch association 或用户后续选择反推。
- Guru 创建的资源标记为 Guru-owned；调用方在 Guru mutation 前已创建的资源标记为 caller-owned。
- 无法证明的历史 ownership 固定按 caller-owned 处理。
- branch rebind 不丢弃旧 resource incarnation。旧 Guru-owned resource 继续由后续 Cleanup 处理；旧
  caller-owned resource 解除 current 关系后在普通 lifecycle 中保持不变，只能进入用户定向 manual cleanup。
- 非 current 的 caller-owned resource 不再承担 task freshness 责任；其 HEAD 后续变化不得阻断 current
  task lifecycle。
- Guru-owned retired resource 必须保留足以在 Finish 后进行 identity-safe Cleanup 的 portable identity。
- 正常 Cleanup 只删除 Guru-owned resource。caller-owned 与 ownership 丢失的 terminal lifecycle 不执行
  自动删除。
- terminal recovery 中的手工清理是独立的用户定向删除路径。系统只接受用户本次显式选择的资源，
  重新验证后再次展示 exact deletion plan，并在当前对话确认后删除；该路径不得把用户选择改写为历史
  Guru ownership。

### I-454-09 Lifecycle owner 与 terminal 顺序保持独立

- Planning approval 不等于 implementation activation；唯一 activation owner负责`planning -> in_progress`，
  recovery不得重复执行status mutation。
- Delivery success 不等于 Completion。
- Completion 不等于 Closure。
- Closure 不等于 Finish。
- Finish开始terminal mutation前必须fresh验证Closure action set仍满足；需要closed的Issue重新open时返回Closure
  owner，不由Finish重判或自动重关。
- Finish 负责形成当前 lifecycle incarnation 的 terminal task result，但不隐式执行 Cleanup。
- Cleanup 只消费 current Finish identity 与 resource ownership，不从 archive presence、Issue state 或
  branch absence 推断成功。
- Reactivate 保留 task identity，创建新的 lifecycle incarnation，并使旧 session association、current
  branch association、Finish receipt 和 Cleanup receipt 失去驱动新 lifecycle 的资格。

### I-454-10 一个统一模型拥有全部组合规则

- Create、Resume、Establish Binding、Rebind、Publication、Completion、Closure、Finish、Cleanup 与
  Reactivate 必须共享同一组 identity、incarnation、branch、checkout 和 ownership invariants。
- 任一模块不得私自定义第二套 task identity、workspace identity、branch freshness 或 cleanup owner。
- 所有 public contracts、runtime state、schemas 与 migration steps 都是统一模型的投影；局部 projection
  不得补充与根模型冲突的状态规则。
- 每个可达状态必须存在唯一正常下一步、唯一 recovery route 或明确 terminal stop；不得存在依赖调用
  顺序才能解释的隐式状态。

## 生命周期场景要求

### R-454-01 新建 Issue-backed task

Issue creation 与 task creation 是两个独立 mutation。Issue 创建成功后必须重新读取 live Issue 并重新进入
fresh intake。task creation 只消费已经审查的 source 与 accepted scope，不兼任 Issue 选择、创建或修改。

### R-454-02 新建 no-Issue task

standalone request 直接建立 task identity 与初始 lifecycle incarnation，不创建 Issue，不生成关闭关系，
后续 Planning、Delivery、Finish 与 Cleanup 保持完整可达。

### R-454-03 采用调用方预建 checkout

当 invocation checkout 已在首个 prompt 前存在时，task creation 在 mutation 前验证 repository、branch、
cleanliness、current reviewed head、task exclusivity 与 checkout registration。验证通过后采用该 checkout，
不创建第二个 worktree；既有 branch 与 linked worktree 保持 caller-owned。

预建 checkout 本身不代表已有 task，系统不得从路径、目录名或 branch name 推断 task identity。

### R-454-04 由 Guru provision checkout

当调用方未提供合格 checkout 时，task creation 根据已审查的 acquisition plan 创建或精确复用执行资源。
新建资源记录为 Guru-owned，复用的既有资源记录为 caller-owned。机器路径只存在于当前副作用计划和
执行事务中。

### R-454-05 普通 resume 与跨 session resume

resume 先解析 stable task identity、current lifecycle incarnation、current branch 与唯一 live checkout，
再建立当前 session association。旧 session 的授权、semantic pass 与临时 checkpoint 不被复用。

### R-454-06 control state 丢失恢复

branch association、session association 与 resource ownership 分别视为独立可丢失状态：

- session association 单独丢失时，只重建 session association；
- branch association 单独丢失且 current ownership 仍完整时，恢复 target 必须匹配唯一 current resource
  incarnation，原 ownership 保持不变；
- active resource ownership 单独丢失时，保留已验证 current branch，既有资源固定恢复为 caller-owned；
- branch association 与 active ownership 同时丢失时，先确定合法 current target，再建立新的 current
  control state，事务前已存在的资源固定为 caller-owned；
- terminal ownership 丢失时，不重造历史 ownership，进入人工 cleanup selection。

恢复不得创建第二个 task、第二个 Issue，不得伪造 Completion、Closure、Finish、Delivery、semantic pass
或用户授权。

### R-454-07 显式 task-branch rebind

rebind 前必须证明 current work 已处于不需要隐式迁移提交的边界，并验证 target branch、target checkout、
task artifact、repository 与 exclusivity。成功后 current branch 原子切换，session 后续解析到新 branch，
旧资源按各自 ownership 进入保留或后续 Cleanup。

`same-checkout-new-ref` 是 active task 在 planning 或 implementation dirty 状态下的固定 rebind route。它只在
target ref 尚不存在、current checkout 唯一且未处于 Git operation、current HEAD 不变时执行 branch create +
switch；mutation 前后 index、working tree 与 task artifact bytes 必须完全一致。`existing-target` 是 clean
boundary route；target 不得依靠 rebind 获得 source branch 的 commit 或 working tree 内容。

rebind 失败或结果恢复不得同时留下两个 current branch，也不得丢失旧 resource responsibility。

### R-454-08 Publication 与 remote resource

Publication 只更新当前 resource incarnation 的 remote delivery facts 与 remote cleanup responsibility。
remote identity 必须绑定 repository 与完整 ref，不能仅凭短 branch name 定位。Publication 不改变 task
identity、lifecycle incarnation 或 source authority。

### R-454-09 Finish 与 Cleanup

Finalizer与Merge只形成Publication/Delivery结果，不移动task到archive。Merge结果必须先进入Completion与Closure；
Finish 在 task terminal result 与完整 resource responsibility inventory 均被封存后，结束 current branch
association；此时资源尚未被 Cleanup 删除。Cleanup 根据 current Finish identity 逐项解析 Guru-owned
local branch、linked worktree 与 remote branch。正常 Cleanup 保留 caller-owned 与 unknown-ownership
resources；已不存在的 Guru-owned resource 按 idempotent already-absent 收敛；identity 或 freshness 冲突
只阻断对应 cleanup step，不重放 Finish。

已由planned machine handoff转入source-machine handoff Cleanup或转移给destination的resource，不再属于后续
Finish inventory；handoff transaction必须在destination恢复普通active state前证明这些责任已经唯一归属。

### R-454-10 Reactivate

Reactivate 从 exact archived task identity 与 current base authority 建立严格递增的新 lifecycle incarnation，
并复用与初次 task creation 相同的 checkout acquisition 和 ownership 规则。旧 incarnation 的 branch、
session、Finish 与 Cleanup state 不得成为新 incarnation authority。

### R-454-11 Rename、archive 与 checkout move

rename、archive 与 checkout move 后，stable task identity 保持不变。task locator 变化必须由拥有该 mutation
的步骤更新其直接 back-reference；branch association、session association 与 resource ownership 不得通过
绝对路径维持关联。

### R-454-12 并行 task 隔离

同一 repository 内的多个 active task 各自拥有独立 identity、incarnation、current branch、session
association 与 resource ownership。一个 task 的 rebind、Finish、Cleanup、Reactivate 或恢复不得改变另一
task 的状态。

### R-454-13 Archived task 意图隔离

面对同一 archived task，Finish recovery 与 Reactivate 是两个互斥意图。调用方必须先声明当前意图，
resolver 再按该意图验证 archived task、lifecycle incarnation、terminal result 与 target base。系统不得从
archive presence、checkout availability、旧 receipt 或唯一候选推断意图，也不得让同一次 resolution
同时满足 Finish recovery 与 Reactivate。

### R-454-14 跨机器恢复

跨机器恢复只消费已经进入可传输Git object并由显式ref可达的task artifact。源机器先通过
`guru-checkpoint-task-state`建立只包含当前task control/planning artifact的checkpoint，并通过用户已确认的
Git transport使该ref在目标机器可获取；普通Task Commit随后已由Publication传输，或Publication本身已满足
同一条件时不得重复创建checkpoint。Checkpoint不冒充Phase 2 check或Task Commit；新commit使旧base reconcile、
Task Commit pair、Phase 2 check、Branch Review、closeout Publication、Delivery Review、Delivery Publication、
Completion、Closure与Finish eligibility失效。未提交working tree、ignored association/session/
ledger与本机path不属于跨机器恢复范围。

计划内active handoff由`guru-transfer-task-machine`独占：源机器先把Guru-owned local resource封存进独立
handoff-cleanup inventory，关闭源association/session，再向
`refs/heads/guru-task-lifecycle/<TaskId>`发布只有目标机器直接消费的path-free handoff
   artifact；artifact只携带TaskLifecycleKey、current branch ref、checkpoint identity与全部未收敛portable remote resource
responsibility，并保留每个resource的原binding epoch/revision、state与responsibility role。
目标机器消费后建立新binding epoch/revision 0、按实际acquisition facts建立local resource ownership，并
承接remote responsibility。源机器handoff Cleanup独立处理已封存local resource，不进入后续Finish inventory。
同一handoff不得让两台机器同时保持current association；destination consume后所有branch/HEAD-bound evidence
失效并由current phase owner重建。Consumed artifact从current tree删除，但其released、consumed与deletion
commit必须保持在该TaskId稳定ref可达历史中，作为path-free supersession receipt；该ref不进入Finish/Cleanup。
任何机器恢复旧association前
必须先读取该receipt并拒绝已被取代的binding epoch。

源机器不可用时，用户明确选择`unavailable_source_recovery`。目标机器从portable artifact建立新control
state前，先在explicit ref写入并同步`unavailable_source` mode的released recovery artifact；该artifact不转移
source ownership，只使此前machine-local association失去current资格。目标机器随后建立new epoch/revision 0，
所有pre-existing local/remote resource固定按caller-owned，未知源机器resource只允许后续manual cleanup，最后
写入consumed状态并删除current-tree artifact，保留可达history receipt。只有portable checkpoint中实际存在的
task/planning state可恢复，其余semantic/HEAD-bound evidence全部stale。目标ref不含task artifact时返回
`task_artifact_not_portable`；不得从branch name、Issue或目录猜测task。

若同一handoff已处于`prepared`而source随后不可用，目标机器不得创建第二个handoff；它在用户明确选择
unavailable-source recovery后，以同一handoff id把prepared artifact转换为`unavailable_source` released
recovery artifact。Prepared snapshot不产生ownership transfer，source resource仍进入orphan/manual-cleanup边界。

### R-454-15 Planning activation 与 re-entry

Create与Reactivate固定进入`planning`。Planning semantic owner只产生approved result，`guru-activate-task`独占
`planning -> in_progress` mutation。Activation结果丢失时只读恢复同一result，不重复status mutation。Task进入
`in_progress`后若scope、target或base impact使Planning stale，status保持`in_progress`，下游由evidence currentness
阻断并返回Planning；重新approval不创建新task、generation、branch association或session identity。

### R-454-16 Closure 到 Finish 的外部变化

Closure action set整体收敛后、Finish开始任何本地mutation前，Finish重新读取全部受控Issue。
`closed_verified`与`already_closed_at_review` item必须仍closed；`relation_has_no_close_authority`不依赖live
open/closed变化。需要closed的Issue重新open或identity/eligibility变化时，Finish不archive、不seal ledger、不关闭
association，固定返回Closure `external_change_conflict`进行semantic re-review。

## 验收标准

- `AC-454-01`：形成一份封闭状态矩阵，覆盖九类领域事实的合法、缺失、stale、conflict 和 terminal
  组合；每个可达组合只有一个下一 owner、一个 recovery route 或一个明确 stop。
- `AC-454-02`：统一模型证明 task rename、archive、Reactivate、branch rebind、checkout move 和已完成
  portable checkpoint/sync 的跨机器恢复均保持同一 task identity，且无路径字段参与身份判定；未进入
  可传输 Git history 的本机状态明确返回 `task_artifact_not_portable`。
- `AC-454-02A`：legacy task 缺失、非法或冲突 identity 时进入可恢复的显式 establishment；合法用户
  指定能建立 identity，非法或已占用 identity 被拒绝，任何目录名或 branch hint 都不会自动成为 identity。
- `AC-454-03`：Issue-backed 与 no-Issue 两条 create path 均闭合；Issue creation、task source relation、
  accepted scope、Completion 与 Closure disposition 没有重叠 owner。
- `AC-454-04`：预建 invocation checkout 与 Guru-provisioned checkout 两种入口得到相同 task lifecycle
  结果；前者不重复创建 worktree，后者只把实际新建资源记为 Guru-owned。
- `AC-454-05`：唯一合法 candidate 自动恢复；零 candidate 与多个 candidate 均进入可继续的用户选择；
  用户选定 candidate 与显式 target 均执行同一 live validation，合法 target 能恢复，非法 target 被拒绝。
- `AC-454-06`：`git worktree move` 与目录变化后无需更新 tracked task、session 或 branch association，
  下一次操作仍能通过 live Git facts 得到唯一 checkout。
- `AC-454-07`：session stored/public payload 只携带 `task_id + lifecycle_generation`，不携带 `task_ref`；context
  key 不可用时使用 `explicit_task_mode`。session binding 丢失、branch association 丢失、active ownership
  丢失、三者组合丢失与 terminal ownership 丢失均有互不矛盾的恢复结果；恢复不推断 Guru ownership。
- `AC-454-08`：task A → task B → task A、session 1 → session 2 与 Reactivate generation change 均不
  串用 task、session、receipt 或 branch state。
- `AC-454-09`：task 在同一 lifecycle incarnation 中完成至少一次显式 branch rebind 后，恰好一个 branch
  保持 current；旧 caller-owned 资源被保留，旧 Guru-owned 资源继续可由 terminal Cleanup 唯一处理。
- `AC-454-10`：同一 Git ref 不会同时代表两个尚未收敛的 resource incarnations；ref 再利用只有在前一
  incarnation 已失去全部 current 与 cleanup responsibility 后才可达。
- `AC-454-11`：非 current caller-owned branch/worktree 的 HEAD 后续变化不阻断 current lifecycle；Normal
  lifecycle不修改或删除该资源，只有用户逐项选择并确认的terminal manual cleanup能删除。
- `AC-454-12`：current checkout 被移动或原 checkout 不再存在时，Publication、Finish 与 Cleanup 分别
  通过 portable identity 与 live Git facts 得到唯一可执行位置或明确 recovery result，不读取历史 path、
  mapping 或 source checkout。
- `AC-454-13`：Cleanup 对 Guru-owned、caller-owned、already-absent、ownership-missing、identity-conflict
  五类结果具有唯一行为；正常 Cleanup 不删除 caller-owned 或 unknown-ownership resource，手工清理只
  影响用户本次选定、重新验证并再次确认的资源。
- `AC-454-14`：reconcile base 不修改 task metadata；每次成功reconcile固定使Task Commit pair、Phase 2、Branch
  Review、closeout Publication、Delivery Review、Delivery Publication、Completion、Closure与Finish eligibility
  stale；Planning只在semantic impact改变需求、设计
  或验收合同时stale。各原owner基于reconciled HEAD重建自己的evidence。
- `AC-454-15`：所有生产 reader、writer、resolver、session flow 与 terminal owner 不再创建、读取、修复
  task/workspace mappings，不再把 `task_workspace` 作为 public 或内部领域概念。
- `AC-454-16`：后续 design 必须把每个 Skill、public contract、private state、schema、migration 与 test
  case 映射回本 PRD 的唯一领域类别和 invariant；无法映射的状态或字段不得进入实现。
- `AC-454-17`：同一 archived task 的 Finish recovery 与 Reactivate 使用互斥 intent 和互斥 resolution
  result；任何 archive 状态都不会同时进入两条 mutation path。
- `AC-454-18`：dirty active task 能通过 `same-checkout-new-ref` 完成显式 rebind且 index/working tree bytes
  不变；existing-target rebind 只在 clean、artifact-matching、content-compatible target 上执行，不承担
  reconcile 或 commit migration。
- `AC-454-19`：计划内跨机器handoff在源association关闭后才建立目标association，全部未收敛portable remote
  responsibility只通过path-free transient handoff转移，并保留每个resource incarnation的原binding、state与
  responsibility role；remote set允许零个或一个`current_delivery`，零个表示尚未Publication且destination仍从
  checkpoint commit建立current branch，多个固定为handoff conflict；TaskId稳定supersession receipt ref长期保持
  released/consumed/deletion history可达且不进入
  Finish/Cleanup。源机器不可用恢复先写portable recovery receipt，不重造ownership，全部未知资源保守进入
  caller-owned/manual-cleanup边界。
- `AC-454-20`：Closure in-progress期间，任何会改变source、scope、target、branch、HEAD/content、Completion或
  action-set lineage的mutation均不可达；Closure收敛后到Finish mutation前，required-closed Issue重新open固定
  返回`external_change_conflict`，且Finish不产生任何本地terminal副作用。
- `AC-454-21`：所有新增、替换与实质变化的public Skill均声明完整typed exit集合、每个exit的唯一consumer与
  minimal projection；旧workspace producer、exit marker、consumer、schema、command与platform projection在
  one-step activation前引用数为0。Finalizer与Merge不得archive task；`delivered|merged -> Completion -> Closure
  -> Finish -> Cleanup`是唯一terminal顺序。Publication、Finalizer与Merge不得通过closing keyword、Issue mutation
  或closure verification提前执行Closure authority。

## 非目标

- 不修改具体业务 repository，不处理样例会话，不执行业务 repository 安装验证。
- 不在本 PRD 阶段定义 Skill id、command id、schema id、DTO 字段、文件路径、存储格式、
  recorder、executor、checker 或 migration step。
- 不在本需求中激活 #434 production lifecycle graph。
- 不合并 Completion、Closure、Finish、Cleanup 和 Reactivate 的 semantic ownership。
- Normal Cleanup 不删除调用方拥有的 branch、worktree 或 remote branch。Terminal manual cleanup 只删除
  用户本次逐项选择、重新验证并对 exact deletion plan 独立确认的资源。
- 不支持同一 task lifecycle incarnation 同时拥有多个 current branch。
- 不通过 rebind 迁移未交付提交，不执行 stash、cherry-pick、rebase、隐式 merge、reset 或 force push；
  `same-checkout-new-ref` 只改变当前 checkout 绑定的 branch ref，不改变 index 或 working tree bytes。
- 不从任意 checkout、目录名、branch naming convention、Issue number 或 title 猜测 task identity。
- 不把 live checkout resolution 重新包装为新的持久化 workspace、checkout locator 或 topology object。
- 不处理 hostile input、故意伪造、分布式锁、并发压力、crash consistency 或 fault injection。
- 不执行完整多平台 Release matrix；该证据继续由专门 Release owner 承担。

## 延期到后续规划阶段

以下内容必须由 `design.md` 在本 PRD 收敛后定义：

- 九类领域事实的具体 authority 与存储边界；
- 全量状态组合矩阵与 transition ownership；
- public Skill 拆分、typed exits 和 consumer projection；
- task metadata 的精确保留、忽略与兼容字段；
- branch association、session association 与 resource ownership 的具体 schema；
- legacy task/workspace mapping 退出策略；
- 公共 API、配置和术语迁移表；
- 实现顺序、兼容窗口、回退边界与验证分层。

## 开放问题

无。第一阶段所需的产品目标、范围、恢复行为、人工选择原则、ownership 保守规则和生命周期边界均已
由当前共识确定。
