# 06 Live Execution Checkout Resolution

## 1. 要解决的问题

Execution checkout 是当前命令实际读取、编辑和验证 task 内容的位置。路径会因 `git worktree move`、目录
重命名、重新 clone 和机器差异变化，因此任何历史 path 都不能参与 identity 或 freshness。每次需要
working tree 内容的 owner都必须从 current branch association 与 live Git topology 重新解析。

## 2. Resolver input

Resolver 的完整输入只有：

- current repository context 与 verified common dir；
- TaskLifecycleKey；
- current branch association；
- current TaskRef；
- caller 声明的 expected task status；
- caller 声明的 operation suitability profile。

Resolver 不接受 stored checkout path、workspace slug、source checkout、task/workspace mapping 或 session path
作为 authority。

## 3. Candidate discovery

Resolver 每次执行以下步骤：

1. 在 verified common dir 执行 `git worktree list --porcelain`；
2. 解析全部 registered primary/linked worktree；
3. 只保留 branch 等于 association `branch_ref` 的记录；
4. 对每个记录 fresh 读取其 common dir、HEAD、cleanliness 与 task artifact；
5. 验证 task artifact 中 TaskId、generation、TaskRef 与 expected status；
6. 应用 caller 的 operation suitability profile；
7. 返回 validated candidate set。

Candidate path、HEAD、dirty paths、worktree type 与 discovery timestamp 只存在于当前调用内存及当前对话
展示，不进入 task metadata、session、association、ledger 或 public cross-Skill DTO。

## 4. Operation suitability profiles

Identity validation 与 operation suitability 分层执行：

| Profile | 附加条件 |
| --- | --- |
| `read_task` | task artifact identity/status 匹配 |
| `edit_task` | identity 匹配，checkout 未被 foreign transaction占用 |
| `rebind_same_checkout_new_ref` | identity匹配、唯一current checkout、无Git operation；允许dirty，由Rebind owner验证前后index/working tree不变 |
| `rebind_existing_target` | source checkout clean；target artifact identity与content relation通过 |
| `publication` | identity 匹配，current branch 与 reviewed content identity 可 fresh 验证 |
| `finish` | identity 匹配，Finish owner 要求的 clean/HEAD/target facts通过 |
| `cleanup` | 不要求 task checkout；直接进入 repository-control resolution |

Resolver 只报告事实与封闭 resolution result。Semantic owner继续判断当前 operation 是否足够、是否需要
scope revision、review refresh 或用户确认。

## 5. Resolution results

### 5.1 Exactly one candidate

恰好一个 validated candidate 时返回 `checkout_resolved`。返回值只在当前 owner调用内使用，包含当前
path 与 fresh live facts。下游跨 Skill handoff 重新解析，不传递该 path。

### 5.2 Zero candidate

没有任何 registered checkout 绑定 current branch 时返回 `checkout_required`，并附当前调用诊断分类：

- branch ref 不存在；
- branch 存在但没有 registered checkout；

`checkout_required` 进入 reviewed acquisition。Existing branch 仍属于调用方；本次新建 linked worktree 才
标记为 Guru-owned。Resolver 不自行创建 checkout，固定交给`guru-ensure-task-checkout`。

已经发现绑定 current branch 的 registered checkout，但 identity validation失败时，不得通过创建第二个
checkout绕过：

- foreign common dir、TaskId/generation/status mismatch 返回 `checkout_identity_conflict`；
- task artifact 缺失返回 `task_artifact_missing`；
- operation suitability mismatch 返回 `checkout_unsuitable` 与 exact correctable reason；
- detached checkout不属于 current branch candidate；current branch同时没有其它 checkout时，resolver返回
  `checkout_required`，detached checkout保持独立 live fact。

### 5.3 Multiple candidates

多个 validated candidate 返回 `checkout_topology_conflict`。Resolver 不按 invocation cwd、最短路径、primary
checkout、mtime、cleanliness 或列表顺序自动选择。

恢复分两步完成：

1. 用户选择一个 candidate 作为 retain target；
2. 对其余每个 registered checkout 选择并确认 exact repair action。

Repair action 只有以下封闭类型：

- `detach_non_retained`：保留目录与 working tree，把非 retain checkout 从 current branch 脱离；
- `remove_non_retained`：仅在 checkout clean、无未提交内容、且 exact deletion plan 已确认后移除；
- `stop_for_manual_repair`：不执行 mutation，等待调用方先处理 dirty 或外部占用。

Repair 完成后必须从 common dir 重新运行完整 discovery。只有重新得到一个 validated candidate 才返回
`checkout_resolved`。

## 6. Moved checkout

`git worktree move` 成功后，Git registration 中的 path 随之变化。下一次 resolver只读取 live porcelain，
因此直接返回新 path。以下 state 全部不更新：

- task metadata；
- TaskRef；
- current branch association；
- session association；
- resource ownership ledger。

如果目录被文件系统直接移动且 Git registration 未更新，该目录不是 validated candidate。Resolver 返回
topology/registration mismatch，要求先修复 Git worktree registration。

## 7. Repository-control operations

下列操作不需要 execution checkout：

- 枚举 worktrees 与 refs；
- 验证 local branch/remote branch identity；
- 删除未被 checkout 的 local branch；
- 删除 remote branch 与 remote-tracking ref；
- 读取 repository-local ignored control state。

这些操作从 common dir scoped Git command执行。Cleanup 不因历史 task checkout 已删除而失败。

需要 archive/task file 内容的 terminal recovery 先解析能包含该 artifact 的 exact branch checkout；无 checkout
时进入 reviewed acquisition，不读取旧 `worktree_path`。

## 8. Cross-machine artifact availability

Live checkout resolution不能让未进入Git history的task artifact跨机器出现。跨机器resume固定执行：

1. 验证repository identity与用户提供的explicit task ref；
2. fetch/解析该ref可达的Git objects；
3. 在ref对应tree中按TaskId解析canonical TaskRef与generation；
4. 建立或采用目标机器checkout；
5. 按selected machine-transfer route与实际acquisition facts建立association和resource ledger；planned handoff
   必须使用artifact声明的current branch ref与checkpoint commit，不从checkpoint ref或remote role推断branch；
   planned handoff
   承接全部未收敛portable remote ownership，unavailable-source recovery把pre-existing resource记为caller-owned，本次
   新建resource按create facts记账；
6. 建立session binding或进入explicit-task mode。

`guru-checkpoint-task-state`只stage当前TaskRef内的task control/planning artifact，创建明确checkpoint commit，
再按已确认transport同步explicit ref。它不stage业务文件、不声称Phase 2 check或Task Commit通过，也不生成
Delivery/Completion结果。Exact artifact已经由普通Task Commit随后由Publication传输，或Publication直接进入
目标机器可获取的portable history时返回
`already_portable`，不创建第二个commit。Checkpoint transport首次创建remote ref时建立Guru-owned remote
resource，采用pre-existing remote ref时建立caller-owned remote resource；两者均记为
`responsibility_role=checkpoint_transport`与`state=portable_auxiliary`，后续写入不改变ownership。

新checkpoint commit改变current HEAD，因此base reconcile、Task Commit pair、Phase 2 check、Branch Review、
closeout Publication、Delivery Review、Delivery Publication、Completion、Closure与Finish eligibility全部失效；
Planning bytes未改变时Planning approval保持
current。后续owner必须基于新HEAD重建。Closure或Finish transaction进行中时checkpoint不可达。

源机器必须先由`guru-checkpoint-task-state`、普通Task Commit随后由Publication传输、或Publication直接形成
包含exact task artifact且目标机器可获取的portable checkpoint。Checkpoint只携带已提交task control/planning bytes；
未提交业务内容、ignored control state与本机path不会被恢复。

Active lifecycle继续执行还必须消费以下一条route：

- `planned_machine_handoff`：`guru-transfer-task-machine`把源Guru-owned local resource封存进独立handoff
  Cleanup inventory，关闭源association/session，再在TaskId稳定supersession receipt ref发布包含current branch ref的
  path-free transient handoff；目标机器在该branch ref与checkpoint commit上建立new epoch/rev0并承接全部未收敛
  portable remote responsibility；
- `unavailable_source_recovery`：用户明确声明源机器不可用；`guru-transfer-task-machine` recovery profile在
  目标机器先写同一supersession receipt ref，再建立new epoch/rev0，全部pre-existing resource按caller-owned，未知源resource只进入terminal
  manual cleanup；随后Session owner只建立pointer。

Destination consume后Planning与全部非artifact evidence stale。Supersession receipt ref固定为retained control，
不进入Finish或Cleanup。

目标ref缺少artifact时返回`task_artifact_not_portable`，不得把zero checkout误报为普通acquisition并创建
第二个task。

## 9. Failure matrix

| Live topology | Result |
| --- | --- |
| 一个 branch-bound、artifact-matching candidate | `checkout_resolved` |
| branch 存在但无 checkout | `checkout_required` |
| branch 不存在 | `checkout_required` + branch-missing classification |
| 一个 checkout 但 detached | `checkout_required` + detached classification |
| 一个 checkout 但 foreign common dir | invalid candidate |
| artifact TaskId 不匹配 | `checkout_identity_conflict` |
| artifact generation 不匹配 | `checkout_identity_conflict` |
| identity valid但 operation suitability失败 | `checkout_unsuitable` |
| 多个 validated checkout | `checkout_topology_conflict` |
| path 经 `git worktree move` 改变 | live 新 path 正常 resolve |
| 历史 checkout 已删除，Cleanup 只处理 refs | common-dir repository-control route |
| 目标机器explicit ref含matching task artifact | 建立目标机器checkout与local control state |
| 目标机器explicit ref不含task artifact | `task_artifact_not_portable`，返回源机器checkpoint/sync owner |

## 10. 当前设计结论

本问题固定以下结论，最终状态仍由全量审核决定：

1. 每个需要 working tree 的调用都从 live Git topology重新解析；
2. checkout path 永不跨 Skill 持久化；
3. zero candidate 进入 acquisition，不终止 lifecycle；
4. multiple candidates 进入显式 topology repair，不自动选路径；
5. moved worktree 不要求更新任何 identity/control artifact；
6. repository-control operation 不依赖 task checkout；
7. 跨机器恢复只承诺已进入explicit ref可达Git history的task artifact，不伪造未同步local state。
