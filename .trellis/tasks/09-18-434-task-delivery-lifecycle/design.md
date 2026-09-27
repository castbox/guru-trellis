# Design: #434 Task Delivery Lifecycle Global Activation

## 1. Current State

协调后的 selected base 为 `origin/main@bab8cfcd534692735b9240b25dd8bc63e40a5cb4`。Architecture/RDT current authority 为 `current-main-0.6.17-guru.66`。以下 32/149/102 与 22/98 是切换前快照；本地候选已为 34/155/104 与 33/153，尚待完整门禁，因此不能称为可发布激活。旧 closeout 主链为：

```text
guru-review-branch
  -> guru-review-task-publication
  -> guru-finalize-task
  -> guru-merge-task-pr
  -> merged terminal
```

`guru-finalize-task` 在 merge 前归档 task；`guru-merge-task-pr:phase2_reentry_required` 因而必须调用 `guru-restore-archived-task`。这使 Delivery、Completion、archive 和 recovery 共用同一 closeout transaction。

#434 branch 已协调到 `bab8cfcd`；原有草稿与过期 1.0 schema 修改保存在 stash。D443/D436 canonical majors、七个 E434 packages 与旧包退休已经在同一未提交候选中投影；source/installed 检查通过但广义集成、代表性安装和迁移负例尚未闭合。

## 2. Target Graph

```text
Phase 2 Check
  -> Task Commit
  -> Branch Review
  -> Delivery Review
  -> Delivery Publish
  -> Delivery Merge
  -> Task Completion
       | remaining_work -----------------> Phase 2
       | evidence_pending ----------------> Completion fresh evidence refresh
       | additional_delivery_required ----> next-slice Planning -> Delivery Review
       | requirements_revision_required --> Requirements Clarification
       | implementation_revision_required -> Phase 2
       | completed ------------------------> Issue Closure
  -> Issue Closure
  -> Official Finish
  -> Resource Cleanup
```

Reactivate 是独立入口：

```text
explicit restore request / reopened Issue trigger
  -> guru-reactivate-task
       | reactivated_to_planning ----------> current Phase 1 router
       | session_binding_recovery_required -> session recovery router
       | resume_reactivation --------------> reactivation resume router
       | source_correction_required -------> source correction router
       | reactivate_blocked ---------------> stop
```

## 3. Interface And Version Dependency Table

所有新 public package 使用当时 repository current 的 Interface schema selector，最低要求为 Interface `1.4` 的完整 public I/O/consumer/projection 合同；若 #435/#436 已经以更高 current selector 合入，#434 必须绑定其 live registry 中的精确 selector，不做降级兼容。

| Owner Issue | Required package | Required public capability | #434 activation dependency |
| --- | --- | --- | --- |
| #435 | `guru-review-task-delivery` | current slice、Refs-only、remaining-work disclosure、predecessor freshness；ready/work/planning/scope/blocked closed exits | Branch Review success 的唯一下游；替代旧 Publication semantic owner |
| #435 | `guru-publish-task-delivery` | exact reviewed HEAD push；唯一 current Draft/Ready PR；binding/output-loss recovery；零重复副作用 | 只消费 Delivery Review ready；产生 Delivery Merge seed |
| #435 | `guru-merge-task-delivery` | independent merge confirmation、expected head/base/checks、merge-result recovery、Delivery result | successful result 的唯一后继为 Completion，不得包含 completion/archive/closure 字段 |
| #435 | existing Planning/Check/Commit/Branch Review adaptations | delivery policy、current slice、remaining work、独立可交付条件 | 必须与三个 Delivery packages 同版本 bundle 就绪，避免旧 owner 仍要求 whole-task-complete |
| #454 D436 | `guru-review-task-completion` | current TaskLifecycleKey、merged Delivery lineage、evidence-refresh；七个 exits | `delivered` 的唯一 semantic successor；`remaining_work` 返回 active continuation，`additional_delivery_required` 返回下一 slice Planning |
| #454 D436 | `guru-complete-task-closure` | current Completion ResultRefDTO、封闭 source/action set、no-mutation/close/recovery | `completed` 的唯一 consumer；`no_mutation/closed` 只投影 current Closure result 到 Finish |
| #454 D436 | `guru-finish-task` | current Closure ResultRefDTO、archive bookkeeping、目标基线校验及 C5 ledger seal | `success` 才交 ResourceSealRefDTO 给 Cleanup；另有 `closure_refresh_required`、`manual_cleanup_required` 路由 |
| #454 D436 | `guru-cleanup-task-resources` | ResourceSealRefDTO、fresh ledger resource discovery、manual selection/handoff | 只消费本代 seal；`cleaned`、remaining/manual/handoff 各自闭合 |
| #454 D436 | `guru-reactivate-task` | archived TaskId/source、current base、C3-C5 acquisition/binding/ownership | `reactivated_to_planning` 为正常出口，另外 session recovery/resume/source correction/blocked；不沿用旧 Restore DTO |
| #454 D443 | `guru-bind-task-session` | TaskId/generation path-free official session、resume/rebind/switch/reactivate/manual、explicit task mode | 七个 exits（含 `blocked`）；#434 只接入其 public routes，不复制 binding owner |
| #454 Phase E434 | six reserved stable IDs plus independent Issue owner | `guru-activate-task`、`guru-create-task`、`guru-ensure-task-checkout`、`guru-establish-task-branch-binding`、`guru-establish-task-identity`、`guru-rebind-task-branch` 与 `guru-create-issue` 已有候选完整目录及定向测试 | 候选 source validation 不等于组合 package-ready 或 installed/graph 通过；切图前仍须唯一 consumer 和当前版本闭合，禁止旧 task-workspace alias |
| #434 | global graph activation bundle | registry/workflow/manifest/consumer/cardinality/platform/installed 一致 | 上述全部 source + installed contracts 通过后才能切图 |

### 3.1 #435 merged interface binding

| Package | Interface/profile | Current exits relevant to #434 | Integration state |
| --- | --- | --- | --- |
| `guru-review-task-delivery` | `1.4` / `delivery_review` | `ready -> guru-publish-task-delivery`; planning、implementation、scope、blocked 各自回现有 owner/stop | `active/deferred` |
| `guru-publish-task-delivery` | `1.4` / `review_ready`, `same_plan_resume`, `reprepare_publication` | `ready_for_merge -> guru-merge-task-delivery`; stale/resume/reprepare/blocked 保持 package-owned closed route | `active/deferred` |
| `guru-merge-task-delivery` | `1.4` / `ready_for_merge` | `delivered -> guru-review-task-completion`; blocker、implementation、review-refresh 有唯一 consumer | `active/deferred` |

上述接口以 PR #437 head `4b9e65dbfce9ce4ec4299b2085789acc4f12276c`、merge commit `bf7a5213ddb9b4fb258778cb66bf5645551943ff` 为当前事实。`delivered` 的目标 package 属于已合入的 #436，当前仍是 deferred candidate graph，不能成为 production edge，直到 #434 组合 gate 完成。

### Version binding

激活 bundle 增加一个 deterministic graph compatibility assertion，由 live registry 派生，不手写固定 package count 作为 authority。assertion 完整绑定：

- 新旧 active skill id 集；
- 每个 active package 的 Interface selector、input profile ids、exit ids、consumer ids 和 projection ids；
- canonical extension manifest 与 installed manifest 的同一 package/source identity；
- canonical workflow mandatory invoke/exit markers与 registry integrated package closure；
- Shared/Codex/Claude/Cursor 实际加载路径；
- #435/#436/#443 historical merges 与 #454 C2-C7、D443 PR #473 merge `0ac48e5d24e6d2c32cf2d69080109a6a7adaee9e`、D436 PR #474 merge `bab8cfcd534692735b9240b25dd8bc63e40a5cb4` 均须成为 activation selected base ancestor；activation 时仍需 fresh reread。

任何缺失、额外、旧 selector、consumer mismatch 或 dangling target 都在 workflow 写入/安装前 fail closed。

### Planning sequence after #435

1. #434 保持 planning，仅冻结 global graph、migration 和 package-ready contract。
2. #436 按其 Issue authority 交付 Completion、Closure、Finish、Cleanup、Reactivate 与 evidence-refresh packages，不切 production graph。
3. #436 合并后，#434 fresh 读取两个 child Issue、全部 live interfaces、registry、installed/platform projection 和 current baseline。
4. 将 #434 base 同步/reconcile 到包含 #435/#436/#443 最终 merge 的 selected base；若 reconciliation 发现规划或 authority 漂移，先返回对应 owner 修订。
5. 在 reconciled checkout 上执行组合 package-ready gate；仅在 gate 通过后进入原子激活实现。

## 4. Atomic Activation Strategy

### 4.1 Package-ready gate

在修改生产 workflow 前先交付 Phase E434 canonical packages，并对完整 source candidate 执行只读 gate：

1. 从 live registry 和 package `interface.json` 发现 #435、#454 D443/D436 及 Phase E434 的全部 required packages；生产初始 cardinality 为 32/149/102。退役 `guru-create-task-workspace`、Publication、Finalizer、旧 Merge、Restore 共 5 个 predecessor packages（21 exits / 22 commands），并激活六个 planned ID 与独立的 `guru-create-issue` 共 7 个 E434 packages（27 exits / 24 commands），派生目标为 34/155/104。该数字只作为 live inventory 的可复算断言。七个 E434 packages 已进入候选 source inventory（39/126 commands），但仍须跨包接口/consumer 和 installed/graph gate 才能切换生产 selector。
2. 验证 source package、其 declared consumers/projections 与 command inventory 自洽；当前 installed `.trellis` 和平台 selector 仍是旧生产图，必须如实标记为 pending。候选切换后再运行 source/installed/platform/extension manifest 同版本闭合 gate，不用旧安装反证 source package readiness。
3. 验证每个新 exit 的唯一 consumer/projection；D443 七个 external exits、D436 当前 majors 和 old-edge subtraction 均必须与新图闭合。
4. 旧前驱集成基线的四项失败：Publication/old Merge 出口断言漏掉 `archived_ready`/`review_refresh_required`、旧 Finish `task_ref/closure_ref` fixture、旧 eval discovery 路径、旧终态 eval 执行（两个子案例）。前三项已有 source 修复或由当前 ledger 跨代 seal 测试取代；两个终态 eval 现先在 preset owner staging 因七个未注册候选目录触发 `canonical_package_set_mismatch`，尚未执行到 Finalizer，不得宣称 `finalization_stale` 是本轮观测结果。切换候选须将不适用旧终态用例退休或更新到有效旧版事实，并由新 owner 终态测试承接，不放宽旧 DTO schema。旧 installed Finalizer 另有三个 runtime digest drift，须在切换候选重建投影并验证。
5. 旧归档按 Issue 检索要通过 finish-summary/index 与 Git archive identity 验证唯一 source；#154 已合并终态旧 PR 阻断要明确 pinned-old/manual 处置，不作为新 Delivery result。任何 hard prerequisite 不满足即止于规划/准备，不执行部分生产切图。

### 4.2 Single activation change set

一次 change set 同时完成：

- 更新 canonical `trellis/workflows/guru-team/workflow.md` 和 dogfood `.trellis/workflow.md`；
- 更新 source/installed registry、extension manifest、contracts、schemas、README 与 graph/cardinality checks；
- 将 #435/#436/#443 新 package 标为 integrated active，并删除 `guru-create-task-workspace` 与四个旧 closeout package 的 active registry selection；
- 应用 preset 生成 installed/platform projections；
- 删除旧 workflow markers、consumer paths、current manifest selectors 和 current-only tests；
- 加入 new-only graph integration 和 negative half-graph tests。

不采用 feature flag、双 registry、old/new runtime adapter、schema dual-read 或按 task 自动选择 graph。旧在途 task 通过 pinned 旧版本完成或人工处置；session binding 丢失按 #443 contract 处理，而不是让当前 main 同时运行两套生产图。

## 5. Edge Migration Matrix

| Current edge / target | Target edge / target | Action |
| --- | --- | --- |
| Branch Review `passed` -> Publication | Branch Review delivery-ready exit -> Delivery Review | 同步修改 producer consumer declaration 与 workflow marker |
| Publication `ready` -> Finalizer | Delivery Review `ready` -> Delivery Publish | 删除旧 projection，不转换旧 DTO |
| Finalizer `ready_for_merge` -> Merge | Delivery Publish ready -> Delivery Merge | Delivery Publish 不 archive，不产 finish authority |
| Merge `merged` -> finish response | Delivery Merge delivered -> Completion | task/Issue 保持 active/open |
| Merge `phase2_reentry_required` -> Restore | Delivery/Completion finding -> 原真实 work owner | 删除旧 Restore edge 与 stop；不提前 archive 即无需 restore |
| Publication/Finalizer/Merge archived read-only review chain | 正常结束后 Reactivate -> fresh owners | 历史复审能力不伪装为 Reactivate；按 #436 新合同进入 |
| Publication closure intent + closing keyword | Completion -> explicit Closure | Delivery payload 固定 Refs-only；Closure 独占 Issue mutation |
| Finalizer archive before merge | Finish bookkeeping after Closure | archive 持久化成功后才发 Finish success |
| terminal finish response | Cleanup success response | Cleanup failure不撤销 Completion/Closure/Finish |

## 6. Ownership Boundaries

- Global workflow：只拥有阶段顺序、mandatory invocation、typed exit 唯一 consumer、stop/route targets 与对话边界。
- #435 packages：只拥有业务 Delivery cycle，不判断 whole task completion，不 archive/close/cleanup/reactivate。
- #436 packages：拥有 whole-task completion 及 post-delivery lifecycle，不修改 Delivery payload/merge readiness。
- Deterministic runtime：只执行 Git/GitHub/Trellis 事实动作和 schema/identity/freshness 校验，不判断 completion、route、scope 或 plan adequacy。
- RDT/Architecture owners：独占 durable authority contribution 与 serialized promotion；#434 不直接把 task 文档升级成 current authority。

## 7. Reactivate Identity Model

### Durable identity

Reactivate 保留：task id、source Issue、历史 planning、历史 Delivery 的 immutable Git/GitHub identities、上次 archive Git identity。当前 branch/worktree 是可替换绑定，不覆盖初次 creation fact。

### Workspace selection

- 原 branch/worktree 存在且满足当前 base、cleanliness、ownership 和 scope 时可复用。
- 否则从 current selected base 创建新 branch/worktree，并更新同一 task 的 current binding。
- 当前树中同一 identity 只能存在一个 active 或 archive 实例；跨月恢复必须删除/移动旧 archive 后再形成新的唯一 archive。

### Freshness

上一轮 Completion、Closure、Finish、review 与 Cleanup 都是历史，不能作为本轮 pass。Cleanup input 必须绑定当前 Reactivate generation 后产生的 Finish success；不得消费旧 success。

## 8. In-Flight Legacy Handling

切图发布说明列出三类：

1. 未进入旧 Publication：重新核对 task identity、current accepted scope、base 与新 binding 后，才可按新版本从 Delivery Review 继续；不能把旧 checkpoint 当新 gate。
2. 已进入旧 Publication/Finalizer/Merge 且状态一致：固定旧 extension/workflow version 完成旧链，并 fresh 验证终态；不能把版本切换等同于迁移。
3. 旧链状态不完整或依赖 Restore：停止自动推进，记录 exact task/PR/remote/local/base/Finalizer facts，由人工逐项选择 pinned-old completion 或资源处置。`castbox/ai-chat-roleplay-backend#154` 的旧 PR #156 已 merged、remote head 落后于本地 reviewed head、旧 Finalizer preview 为 prepared 而执行遇 terminal PR 前置拒绝；预览/执行必须就同一前置事实给出一致阻断，不允许直接改映射、复用 merged PR 或伪造新 Delivery。

不新增 current-main legacy dispatcher。正常结束的旧 archive 可按 source Issue 从历史 finish-summary/index 中发现，再核对唯一 TaskId、source、Git archive identity 与 terminal facts，由 Reactivate fresh 验证；旧 `task.json` 无结构化来源但 summary/ledger 指向该 Issue 时，只产生候选，必须先审查并走 `source_correction_required`，再进入 Reactivate。未完成 residue 不满足该入口。业务仓的 live Test Application/Deployment 仍归其 owner。

## 9. Docs And Architecture Design

本任务具有 architecture impact，候选 change path 为 `target_native`：新 lifecycle 直接成为唯一 target graph，同时删除旧 active owner/edge，不保留 dual-run compatibility。命中：

- `concept-semantic-completeness`：Delivery、Completion、Closure、Finish、Cleanup、Reactivate 各有唯一 owner、identity 和 lifecycle。
- `cohesion-change-isolation`：child packages 拥有 step-local semantics，#434 只拥有 global activation。
- `minimum-necessary-complexity`：不建立 ledger、feature flag、双图、通用 archive recovery 或旧 output adapter。
- `debt-one-way-convergence`：旧 Publication/Finalizer/Merge/Restore active path 一次性退休。

预计需要新的 Architecture contribution 和 ADR，记录“Delivery 与 Completion 解耦、Finish 后置、Reactivate 取代 pre-merge Restore”的长期决策；是否 promotion 及最终 ADR identity 由 Architecture owner决定。

## 10. Alternatives

### 保留旧图并按 task 选择版本

拒绝。它需要 durable graph selector、双套 consumer、长期兼容测试和退出机制，且没有 current runtime direct consumer。

### 修改旧 Finalizer 继续承载全部职责

拒绝。它保留 Delivery、archive、Ready、Completion 的职责耦合，无法形成多 Delivery active task。

### 将旧 Restore 改名为 Reactivate

拒绝。旧 Restore 只处理 merge 前提前归档回 Phase 2；新 Reactivate 面向已正常完成 task，入口、身份、workspace 和出口均不同。

### 新增独立 Acceptance

拒绝。Issue authority 明确由 Completion 承担 whole-task judgment，本轮不新增阶段。

## 11. Main Risks

- child package contracts 在 #434 实现时发生版本漂移：由 package-ready live discovery 和 exact interface binding 阻断。
- current docs 中旧 cardinality/owner 文字散落：通过 repo-wide current-authority scan 和 installed parity 检查收敛，历史 version docs 不机械改写。
- Finish bookkeeping PR 被 Delivery discovery 误识别：通过显式 PR kind/owner contract 和负例 fixture 阻断，不依赖正文模糊扫描。
- Reactivate 后误用旧 Cleanup authority：Finish success 绑定当前 lifecycle generation，旧结果不参与 public handoff。
- installer/reapply 回退 workflow：canonical workflow source + preset manifest + drift check + representative local clean throwaway 联合验证。

## 12. Official Trellis Alignment

- Workflow 行为通过 `trellis/workflows/guru-team/workflow.md` / `.trellis/workflow.md` 定义。
- Workflow 与 preset 使用官方 custom workflow 和 custom spec template 扩展面；远端 marketplace 分发不在本任务验收范围。
- 不修改 Trellis 上游源码、全局 npm、`node_modules` 或 upstream-owned start/continue/hooks。
- 公共 package 与 project-local `.trellis/spec` 分层，active task 状态不进入 reusable spec template。
