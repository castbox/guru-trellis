# Current Capability Inventory

当前 .63 来源：reviewed #454 C5 contribution + inherited immutable `current-main-0.6.17-guru.62` authority；上游固定为 `castbox/Trellis@eb370008c7689d4e272ae626bd002190ecbb3296` / CI `35621578090` / CLI/core `0.6.17`，Guru manifest `0.6.17-guru.42`，release target `v0.6.17-guru.1`。Architecture inheritance：`docs/architecture/README.md` / `current-main-0.6.17-guru.63` / `active`。
完整继承 immutable `.62` 业务合同，当前增量为 #454 C5 path-free official session adapter、resource ownership ledger、Finish seal input 与 Cleanup resolution substrate；active registry 保持 32 packages / 142 exits / 102 commands与四个 planned IDs，production workflow 保持 22 mandatory invokes / 98 exits。

`.63` 完整继承 `.62`，吸收 reviewed #454 C5 contribution；RDT 与 Architecture current 均为 `.63/active`。C5 提升前 focused `113/113` 不证明 promotion-created diff；该 diff 仍须 fresh Phase 2、Task Commit 与完整 Branch Review，C6-C7、D443、D436、E434、#434 activation 和完整 Release matrix 均未完成或验证。

当前 inventory 完整继承 `.62` 并增加 reviewed #454 C5 contribution；registry/interface/command cardinality 不变。`guru-bind-task-session` 为 active/deferred，`guru-ensure-task-checkout`、`guru-establish-task-branch-binding`、`guru-rebind-task-branch`、`guru-establish-task-identity` 为 planned IDs，production graph 尚未由 #434 激活。

| Skill id | External exits |
| --- | --- |
| `guru-select-workflow-mode` | `standard_intake`, `task_free`, `blocked` |
| `guru-sync-base` | `synced`, `skipped`, `blocked` |
| `guru-discover-change-context` | `context_ready`, `refresh_base`, `blocked` |
| `guru-clarify-requirements` | `clear`, `needs_context`, `refresh_context`, `retarget_context`, `new_task`, `blocked` |
| `guru-review-contract-wording` | `pass`, `content_changed`, `blocked` |
| `guru-review-change-request` | `ready`, `clarify_requirements`, `review_wording`, `refresh_context`, `blocked` |
| `guru-create-task-workspace` | `created`, `refresh_review`, `blocked`, `invalid_task_state` |
| `guru-approve-task-plan` | `approved`, `revision_required`, `clarify_scope`, `blocked` |
| `guru-qualify-normal-scenario` | `classified`, `scope_confirmation_required`, `mechanism_revision_required`, `blocked` |
| `guru-qualify-solution-mechanism` | `classified`, `scope_confirmation_required`, `mechanism_revision_required`, `blocked` |
| `guru-execute-task-free-change` | `completed`, `resume_active_task`, `scope_change`, `location_required`, `reselect_mode`, `explicit_choice_required`, `blocked` |
| `guru-check-task` | `passed`, `implementation_required`, `planning_stale`, `blocked` |
| `guru-create-task-commit` | `committed`, `revision-required`, `blocked` |
| `guru-reconcile-task-base` | `reconciled`, `review_continuity_required`, `implementation_required`, `planning_stale`, `scope_confirmation_required`, `blocked` |
| `guru-review-branch` | `passed`, `continuity_passed`, `implementation_required`, `scope_confirmation_required`, `blocked`, `archived_review_passed` |
| `guru-review-task-publication` | `ready`, `return_to_task_work`, `blocked`, `archived_ready` |
| `guru-finalize-task` | `base_reconciliation_required`, `publication_review_stale`, `resume_finalization`, `reprepare_required`, `ready_for_merge`, `blocked` |
| `guru-merge-task-pr` | `merged`, `merge_blocked`, `phase2_reentry_required`, `closure_mismatch`, `review_refresh_required` |
| `guru-restore-archived-task` | `restored_to_phase2`, `restore_blocked` |
| `guru-bind-task-session` | `session_resumed`, `session_rebound`, `task_switched`, `reactivate_rebound`, `session_manually_recovered`, `binding_blocked` |
| `guru-review-task-delivery` | `ready`, `planning_revision_required`, `implementation_required`, `scope_confirmation_required`, `blocked` |
| `guru-publish-task-delivery` | `ready_for_merge`, `review_stale`, `resume_publication`, `reprepare_required`, `blocked` |
| `guru-merge-task-delivery` | `delivered`, `merge_blocked`, `implementation_required`, `review_refresh_required` |
| `guru-review-task-completion` | `remaining_work`, `evidence_pending`, `additional_delivery_required`, `requirements_revision_required`, `implementation_revision_required`, `completed`, `blocked` |
| `guru-complete-task-closure` | `no_mutation`, `closed`, `resume_closure`, `blocked` |
| `guru-finish-task` | `success`, `resume_finish`, `blocked` |
| `guru-cleanup-task-resources` | `cleaned`, `remaining_resources`, `blocked` |
| `guru-reactivate-task` | `reactivated_to_requirements`, `reactivated_to_planning`, `reactivated_to_implementation`, `reactivated_to_evidence_refresh`, `reactivate_blocked` |
| `guru-verify-extension-installation` | `verified`, `blocked` |
| `guru-maintain-requirements-design-test-ssot` | `ssot_current`, `sync_required`, `revision_required`, `baseline_incomplete`, `blocked` |
| `guru-maintain-architecture-baseline` | `baseline_current`, `sync_required`, `baseline_incomplete`, `architecture_conflict`, `contract_incomplete`, `fitness_regression`, `blocked` |
| `guru-bootstrap-repository-ssot` | `completed`, `baseline_incomplete`, `repair_required`, `blocked` |

## Registry、schema、command 与平台 closure

- 每行的 authoritative interface locator 是 `trellis/skills/guru-team/packages/<skill-id>/interface.json`；schema 与 consumer locator 由该 interface 声明，command 由同包 `commands.json` 声明。
- Registry 标记 32 个 package 为 `active`；22 个 workflow-integrated，九个 capability packages 为 `deferred`，`guru-verify-extension-installation` 为 `standalone_only`；合计 142 个 external exits / 102 commands；业务 workflow 保持 22 invokes / 98 exits。
- Interface schema ids 当前包含 `guru-team-skill-interface-1.4`、`1.5`、`1.6`；完整 input/output schema id 列表以 `trellis/guru-team-extension.json` 为准。
- 平台 authority 只有两层：pinned upstream `AI_TOOLS` 的完整 22-platform inventory，以及目标仓库 manifest/provenance 的 exact `selected_platforms`。`shared` 是共享投影，不是平台；不得从 canonical 目录、overlay 数量或 Guru dogfood 状态派生第三层支持集合。
- 重复 `--platform <cli-flag>` 选择 exact subset；canonical inventory 同时保留唯一映射的 `AITool` id 与 `cliFlag`。未指定时才使用 `claude,codex,cursor` 默认值。公开 CLI 不提供全集安装入口；业务仓升级从目标仓 current manifest/provenance 读取 exact `cliFlag` selection 并用重复 `--platform` reapply。
- `guru-trellis` dogfood 的 exact selection 为 Claude、Codex、Cursor。OpenCode 是 upstream 22 平台的普通成员，参与显式选择，但不因 canonical support 自动进入 dogfood。
- Workflow route/consumer closure 以 `trellis/workflows/guru-team/workflow.md` markers 与 interface consumer projection 为准。本 inventory 只索引 stable identity，不取代这些 public contracts。

Inventory freshness：registry entries、interface exits、manifest schema lists、workflow markers 或 source commit 发生变化时，本页必须经 RDT task-impact/promotion 更新，不能单独沿用旧计数。

#275 verifier 不再复制上述 package/command 数量；运行时从 canonical registry、interfaces 与 validator 输出派生 active ids、commands 和 complete-package set，并与 installed projection 做 exact equality。

## 继承历史与适用边界

以下 #260 至 #408 的版本、current/active、graph 和验证叙述均绑定其原 snapshot，不重复声明 .53 current。未被 D418-01..06 明确扩展的业务 ownership、retired-zero 与 Restore 合同继续有效。

## #260 compatibility result

- live-derived platforms：`claude`、`codex`、`cursor`；每个平台均完成 clean/existing 两个隔离 cell，6/6 passed。
- Trellis/project target：`0.6.15`；existing before：official `0.6.5` + `v0.6.5-guru.10` / extension `0.6.5-guru.36`。
- after extension：`0.6.15-guru.39`；active Skills=`21`，external exits=`89`；capability-loss
  comparison 的 `workflow`、`task_data`、`docs_authority` 三组无 blocking loss，
  source/installed/platform interface/schema/command/route 集合由独立 consistency/installation
  gate 保持一致。
- 每个 cell执行 RDT 6-case/4-profile、Architecture 4-case/4-profile、Bootstrap 4-case/3-profile installed eval，并通过 Phase 0、workspace 与 closeout smoke。
- six-cell recursive sidecar count=`0`，template-hash unknown drift=`0`；已知 update backups 仅在 reconciliation 中出现并在最终状态移除。
- current-head dual PATH-runtime matrix SHA-256：`660422848f6efba9f1c3c6fcf2d9d23a1e8b710af8ffd10bf0f12e0954910f49`；workflow sample=`public_plus_local_candidate`，不等于 `.37` 已发布。Per-run wrapper summary digest包含临时 A/B fixture commit identity，因此不作为跨重跑稳定 comparison identity。

## #283 Architecture convergence result

- `guru-maintain-architecture-baseline` 保持 4 profiles / 7 exits，public input/output 原子切换到 schema 2.0；旧 1.0 selector 与 dual-read inventory 为零。
- 本节保留 #283 原 reviewed range 的 Architecture 检查与设计宪法引用：`docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1`。当前 Architecture binding 见页首，不以 `.53` 重绑定该历史检查。
- 项目 change contract 是 `docs/architecture/06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1`，current project check 是 `guru-trellis-architecture-convergence@1`。
- source/dogfood package、两套十场景 eval、Planning/Phase 2/Branch Review consumers、RDT/finish/package closure 与一个代表性 clean install 已在 reviewed task head `86a2cc1a…` 通过；promotion delta仍须 fresh Phase 2/commit/Branch Review。
- extension candidate 为 `0.6.15-guru.40`；`.46` 是 RDT/Architecture knowledge identity，不构成已发布
  tag 或 Release。latest stable 为 `v0.6.15-guru.4` / extension `.39`；#332 target
  `v0.6.15-guru.5` 在 exact-candidate gates、tag-pinned smoke 与 live Release reread 前保持 `unverified`。

## #335 repository-private capability

`release-guru-trellis-version` 不属于上表 public Skill；#335 当时不改变 23 Skills / 97 exits，当前总数见上表。
它只在本仓库 Shared/Codex/Claude/Cursor project-local roots 中提供正式发布的两阶段语义编排：
preparation 在 promotion 前后分别执行 fresh Phase 2/commit/full review，第二次 review 后才进入
Publication/Finalizer/Merge；post-merge 从 fresh `origin/main` 建立 exact
candidate 并把 required checks 与独立 mutation confirmations 路由给既有 owner。公共 registry、
marketplace、preset、overlay、extension manifest 与业务仓 installed inventory 必须保持零投影。

该能力的 reviewed-content 只包含稳定 Skill、tests、durable docs、配置和脚本 bytes；live HEAD、Gate
结果、tag/smoke/Release 状态与用户授权不进入 current authority。`.43` 是 knowledge identity，既不
表示目标 tag 已发布，也不执行发布动作。

## #332 release-current authority

`.45` 在 immutable `.44` 上消费 reviewed #332 original-entry correction contribution，使四个 closeout
Skill 恢复各自原 `invoke.sh` public identity，并把 PR #341 的 transaction/recovery 能力收敛到原 command。
Interface 是 generic wrapper selection 的唯一 authority，`guru-restore-archived-task` 的非 `invoke.sh`
wrapper 是正向回归样本；该 `.45` graph 与当时 live 23 public Skills / 97 external exits / 77 commands 一致。
本 promotion 不改变 typed exit、semantic/mutation boundary、#240/#348 owner 或 Evolution target。
latest stable 固定为 `v0.6.15-guru.4` / extension `0.6.15-guru.39`，current target 固定为
`v0.6.15-guru.5` / extension `0.6.15-guru.40` / Trellis CLI `0.6.15`。#311、#333、#339、#358、#361
的 merged behavior 由 #332 post-merge exact candidate Release Gate fresh 验收；本 inventory 不记录动态
candidate SHA、gate pass、tag、Release、smoke 或 Issue closure 状态。

## #376 base-continuity authority

`.46` 在 immutable `.45` 上消费 reviewed #376 contribution。Reconcile 继续拥有 semantic classification，
新增一个 package-private `execute-base-reconciliation` expected-head local executor；Review Branch 新增
current-only bounded continuity profile，并把 current reconciled HEAD 投影到严格 Publication gate。Finalizer
通过声明的 output/seed/projection 传递 prior `branch_review_commit`，source/installed integration 验证真实
producer-to-consumer edge。public Skill 数与 exit 数保持 23/97，command 总数变为 78；没有 public API、
remote mutation、第二 writer、legacy dual-read、ADR、GAP 或 Evolution target 扩张。

## #378 固定来源与验证边界

`.47` 的 #378 source 由 `trellis/presets/guru-team/source/trellis-source.json` 固定到 `castbox/Trellis@ad332e3fe5a19d7274cb03e7c2f3e2128f8de291`，CLI/core `0.6.16`；当时 Guru extension manifest 为 `0.6.15-guru.40`。该历史增量不新增公共 Skill/exit/command，graph 为 23/97/78。来源、session 隔离、source-record 投影与 verifier composition 分别见 D378-01..04。
历史 #260 official matrix 与 #376 focused 结果只绑定原 candidate；#378 focused clean/two-update、source/installed 与三平台 worktree reapply 不补齐历史 predecessor matrix、独立 TypeCheck、业务 #31/#127 或 remote Release evidence。

## #392 historical release capability boundary

`.48` 消费 reviewed #392 contributions 并保持 23 public Skills / 97 external exits / 78 commands。
该历史 release mapping 为 `v0.6.16-guru.1` / extension `0.6.16-guru.41` / CLI `0.6.16` / fixed Fork full SHA。
repository-private release orchestration 只增加 pre-promotion review、serialized promotion、post-promotion
fresh review 的 Stage 1 顺序，不进入 public inventory。Promotion-created diff 必须通过 fresh Phase 2、
task commit 与完整 Branch Review 后才能进入 Publication；merge 后必须重新冻结 exact candidate，
matrix、business smoke、tag、Release 与 Issue closure 分别由其后续 owner 依据 fresh live facts 独立验证。

## #329 current capability delta

- #329 historical framework source 为 `castbox/Trellis@a2003296b4c4ce46c50d72ead3b2ec9c317f69fc`，current pin 由 R408-01 替代；
  CLI/core `0.6.17`，package manager `pnpm@10.32.1`。
- task/session/owner lifecycle 消费 task metadata、Git/worktree facts、ignored runtime mappings 与 explicit
  caller authority；developer identity、legacy workspace journal/index、agent trace、recording 与 `--mine`
  不再属于 current consumer graph。
- legacy data preservation、three-platform installed lifecycle、clean candidate provenance 与 additive-capability
  comparison 成为 current verification contract；public Skill/exit/command graph 保持 23/97/78。


## #408 current capability delta

Nightly source、正常 authoring/linked-worktree session 接续与独立手动操作由
[D408-01..05](./design-main.md) 承接；`ARCH-CUR-028` 为 Architecture locator。
当前 source 为 `db4ca1dfbb5abaf9be62b2a01b70dda3f80df0f0` / CI `34838784963`，
CLI/core `0.6.17`、`pnpm@10.32.1`、extension `0.6.16-guru.41` 与 released `v0.6.16-guru.1`
均保持独立。没有新公共 Skill/exit/command，23/97/78、旧 lifecycle 与两项 retired-zero 不变。
证据与未验证边界见同版本 Test，不以 knowledge promotion 声称新 release 或后续 gate 完成。

## #418 历史增量

四个新 profile 依次为 archived_review_request、archived_review、archived_publication_review、
archived_review_refresh，分属 Merge、Branch Review、Publication、Finalizer；
三个新 success exits 为 review_refresh_required、archived_review_passed、archived_ready。
Finalizer 沿用 ready_for_merge。Architecture 只增加三个 source/stage 配对，不增加 profile。
`.54` 当时总数为 23 Skills / 100 exits / 79 commands；业务图为 22 invokes / 98 exits。
原 Merge 四出口、Finalizer 四个普通 profile 和 Restore 保持。

普通 Branch Review input 4.0/gate 7.0 与 additive input 5.0/archived-1.0 共存；
schema/DTO 正文仍以 package SSOT 为准，设计及双向引用见 [D418-01..06](./design-main.md)
和 [traceability.md](./traceability.md)。当前软件版本轴与固定 Fork 均不因知识提升改变。

## #419 历史增量

- canonical/dogfood workflow 各有且仅有一个 `[trellis-continuation]`，覆盖 planning、in-progress、completed
  与 invalid state；自然语言续接与 upstream thin entries 加载同一 authority。
- `guru-create-task-workspace` 增加 same-owner created-result recovery；activation wrapper 增加
  `initial|recovery`，不新增 Skill、external exit 或第二 lifecycle router。
- Phase 2、Task Commit、Branch Review、Publication 继续使用既有 public API 和 owner；`.54` graph 为
  23 Skills / 100 exits / 79 commands。
- Release Gate matrix仍由 #410拥有。

## #435 当前增量

- `guru-review-task-delivery`、`guru-publish-task-delivery`、`guru-merge-task-delivery` 进入 active registry，
  package closure 增至 26 packages / 114 exits / 96 commands。
- 三包 workflow integration state 保持 `deferred`；#435 只完成 package、runtime、schema、installer 与
  Shared/Codex/Cursor/Claude projection。production workflow 仍为 22 mandatory invokes / 98 exits。
- Delivery cycle 只交付 approved current slice，merge 后 task 仍 active；Completion、Closure、Finish、Cleanup
  与 Reactivate 由 #436 独占。
- #434 独占 production graph 原子激活与旧 edge retirement。#435 不新增 adapter、ledger、dual graph、
  squash/rebase fallback 或第二 lifecycle router。
- 完整 Release matrix 仍 `unverified`，不得由 package/reapply/representative clean evidence推定。

## #452 当前平台投影合同

- Canonical inventory 固定绑定 upstream `AI_TOOLS` 的 22 个平台 descriptor；target-installed
  inventory 只记录该业务仓库经解析和验证后的 exact `selected_platforms`。
- repeated `--platform` 与无 flag 默认两种 selection mode 共享同一写前 resolver；旧 `--all-platforms` 不进入 resolver；
  upgrade 不使用默认值、source checkout dogfood 或完整 inventory 作为 fallback。
- canonical ownership 可以覆盖全部 22 个平台，但 installed ownership、native projection、reapply 和
  drift 只覆盖目标仓库 selected set。OpenCode 与其它 21 个平台遵守同一选择合同。
- 历史三平台或四平台矩阵只证明其绑定的历史 candidate，不定义 `.58` 的平台 authority，也不证明
  #452 实现或 `T452-01..12` 已通过。#434 production activation 与正式 release 保持独立边界。

## #454 Current lifecycle substrate

- Canonical contract root 为 `trellis/skills/guru-team/contracts/task-lifecycle/`，runtime root 为
  `trellis/skills/guru-team/runtime/task_lifecycle/`；catalog 声明 35 个 named DTO，未新增 public Skill。
- TaskId、TaskRef、generation、closed source union、portable Delivery target、schema loader 与 result constructors
  形成 package-neutral C2 substrate；Fork official task/session primitives 仍是 framework authority。
- D0 修正 Reconcile/Task Commit/Branch Review 的 stage-evidence lineage：pre-review committed reconcile、
  full-review base ancestry、post-review bounded continuity 相互分离，old/new base 不进入 durable identity。
- active registry 保持 32 packages / 142 exits / 102 commands，production workflow 保持 22 mandatory invokes /
  98 exits。C3-C7、D443、D436、E434、installed/platform activation 与完整 Release matrix不属于本增量。

## #454 C3 Current checkout substrate

- lifecycle catalog 从 35 扩展为 39 个 named DTO，新增 call-local checkout plan、candidate、resolution、selection。
- `git_facts.py`、`checkout_resolution.py`、`checkout_acquisition.py` 提供 common-dir live facts、closed resolution、
  adopt/provision transaction、bounded rollback 与 read-only recovery；不读取 legacy mapping/path authority。
- `guru-ensure-task-checkout` 只存在于 `state=planned` registry metadata 与 canonical `planned_skill_ids`，没有
  canonical package directory、interface、I/O、active selector、workflow edge 或 installed/platform projection。
- active registry 保持 32 packages / 142 exits / 102 commands，另有一个 planned ID；production workflow保持
  22 mandatory invokes / 98 exits。C4-C7、D443、D436、E434 与完整 Release matrix不属于本增量。

## #454 C4 Current branch association substrate

- `branch_store.py` 维护 Git common-dir 中以 TaskId + generation 为 key 的 six-field TaskBranchBinding；epoch/revision/branch 与 C5 current ownership 窄投影一致。
- `branch_resolution.py` 从 registered worktree 与 local refs 解析 candidate，排除 retained lifecycle control refs，并要求 exact task artifact、generation、HEAD、branch exclusivity 与 unresolved-incarnation closure。
- Establishment 保留 surviving binding/ownership side，仅 complete control-state loss 建立 new epoch/revision 0；rebind 只支持 same-checkout new ref 与 clean existing target，并保持 epoch、递增 revision。
- `guru-establish-task-branch-binding` 与 `guru-rebind-task-branch` 和既有 `guru-ensure-task-checkout` 一样只存在于 planned registry metadata 与 canonical `planned_skill_ids`，没有 package/interface/active selector/workflow/installed/platform projection。
- active registry 保持 32 packages / 142 exits / 102 commands，另有三个 planned IDs；production workflow保持 22 mandatory invokes / 98 exits。C5-C7、D443、D436、E434 与完整 Release matrix不属于本增量。

## #454 C5 Current session/resource substrate

- `session_adapter.py` 投影 TaskId/generation 到 Fixed Fork official schema-2 session store；无 context key
  显式 task mode，session write failure 不回滚 lifecycle mutation。
- `resource_ledger.py` 在 Git common-dir 维护唯一 TaskId/generation incarnation ledger，复用 C4
  `OwnershipPort`，提供 conservative active recovery、remote HEAD advance、Finish seal 与 Cleanup resolution。
- 唯一合法 candidate 自动选择，零/多个需要人工选择；未发现的显式 target 也经同一 live validator。
- `guru-establish-task-identity` 仅加入 planned registry metadata；没有 package/interface/command/active
  graph/installed/platform projection。active 32 packages / 142 exits / 102 commands 加四个 planned IDs，
  production 仍为 22 invokes / 98 exits；C6-C7、D443、D436、E434 与 Release matrix 未完成。
