# Guru Team Trellis Extension 当前设计

当前 .49 来源：`castbox/Trellis@a2003296b4c4ce46c50d72ead3b2ec9c317f69fc` / CLI/core `0.6.17`；Guru manifest `0.6.16-guru.41`；repository release target `v0.6.16-guru.1`。Architecture public inheritance：`docs/architecture/README.md` / `current-main-0.6.5-guru.49` / `active`。
继承段落中的旧版本映射、矩阵及历史 promotion 只绑定其原版本，不声明当前 Fork 的完整兼容或 Release；当前 #329 增量见本文件末节及同版本 traceability。


版本：`current-main-0.6.5-guru.49`；状态：`active`；predecessor：`current-main-0.6.5-guru.48`；source baseline：reviewed #329 contribution `architecture-contribution-329-developer-free-trellis-v1` + inherited immutable `.48` authority；精确 revision 由 containing Git object/tree identity 绑定。

## 分层与 ownership

- `DES-001` Canonical：`trellis/workflows/guru-team/`、`trellis/skills/guru-team/`、`trellis/presets/guru-team/` 是可分发源头；`.trellis/**` 与 `.agents/.codex/.claude/.cursor` 是 installed/dogfood/platform 投影。
- `DES-002` Orchestration：global workflow 只声明 Phase、mandatory Skill id、typed exit consumer 和 stop；step-local Skill 声明 entry、semantic/deterministic profile、re-entry 与出口。
- `DES-003` Judgment/runtime：semantic Skill 由 AI 执行正向行为与 gate，runtime 只校验 owner-authored result；deterministic Skill 只有在全部 pass/route 均可机器判定时适用。
- `DES-004` Lifecycle：Phase 0 Intake -> Phase 1 Planning -> Phase 2 Execute/check -> Phase 3 commit/review/publication/finalize/merge。base reconciliation 可在稳定边界插入但不重放未变化语义。
- `DES-005` State：task planning 与 closeout archive 是 tracked history；短生命周期 gate/recovery 属于 gitignored owner-private runtime；Git/GitHub live facts按需重读。
- `DES-006` Distribution：manifest、registry、interfaces、schemas、workflow、preset inventory、overlay 和平台 copies 组成同一安装单元；installer 处理 managed hash、mode 与 `.new/.bak`。
- `DES-007` Repository SSOT：RDT 和 Architecture 分别拥有其语义；Bootstrap 依序调用 upstream spec bootstrap、两个 foundation owner、cross-review 与最小 projection。
- `DES-008` Evidence：static/unit/integration/throwaway/live/release 各自只证明对应层级，Issue owner 决定最小验证范围。
- `DES-009` History/cleanup：current task identity 来自 `task.json`、ignored workspace mapping、
  current checkout 与 live worktree facts；archive/`finish-summary.json` 是可查询历史，cleanup 只消费
  merge 后 exact branch/worktree/task reachability。
- `DES-010` Compatibility：公共 Skill/schema/exit/command、managed paths 与平台 routes 形成
  独立 consistency/installation inventory；update/upgrade 只能通过明确 migration/adapter
  改变，任何未迁移 projection drift 都阻塞安装成功，但不因此归类为 capability loss。
- `DES-011` Provider recovery：Git/GitHub drift、base evolution、partial finalization 与重试状态由
  当前 owning Skill 的短生命周期 private state 恢复；unknown/stale/mismatch 进入唯一 typed route。
- `DES-012` Finalizer terminal authority：正常 closeout 已退休 gate/transaction/plan 后，只有调用方提供的精确 retired owner locator 可触发 terminal reconstruction。runtime 读取六文件 archive 中的 durable summary，绑定 active/archive task locator、branch review commit、archive cleanliness，并重新读取 local/remote/Ready PR/title/body/base/branch/issue scope；全部一致才投影 `ready_for_merge`。
- `DES-013` Verifier inventory：source validator 从 registry/interface 形成 active package ids、commands 与 complete package commands；Throwaway verifier 只比较 validator projection 与 installed projection，不维护数量常量。
- `DES-014` Matrix orchestration：compatibility runner 由独立 cell executor 与 compact aggregator 组成；每个 cell 使用隔离 repo、npm prefix 与 runtime root，并输出 platform/scenario/version、inventory、template hash、sidecar 与 installed smoke 结论。runner 以 HEAD、tracked delta、untracked path/mode/content 与 isolated-index candidate tree 构成 source identity，且 run 前后必须一致。
- `DES-015` Platform derivation：canonical/installed manifest、ownership claims、overlay entries 与 registry destinations 交叉派生声明平台；`.agents` 是 shared projection，不是独立 platform，集合不一致即 fail closed。
- `DES-016` Capability comparison：before/after capability-loss gate 只比较 `workflow`、
  `task_data`、`docs_authority`；Docs authority 覆盖 recursive `docs/**` 且四个 domain 都含
  versioned body。`skill_api` 与 interface/schema/command projection、`distribution` 与
  managed/installed inventory、mode、template hash、sidecar、平台 parity 及 extension
  identity/version binding 由独立 consistency/installation gate 验证，任一漂移仍阻塞，
  但其变化本身不构成 capability loss。
- `DES-017` Official migration order：existing cell 先运行 official upgrade/update dry-run 与条件式 migrate，再 workflow preview/switch，最后 preset reapply、backup reconciliation、recursive sidecar 与 ownership/drift gate。
- `DES-018` A/B compatibility：A=`worktree/github_pr`，B=`current/none`，使用隔离 clone；验证两种 merge order、零 metadata intersection、同 owner Finish/provider/cleanup recovery 与 retained-ref reachability；A archive 后 installed history preview 必须返回唯一 non-empty PR candidate并绑定其 `finish-summary.json`。真实 GitHub A proof与 deterministic local fixture 分开绑定。
- `DES-019` Platform script boundary：每个 package 的 Interface 是 public wrapper path 唯一 authority；
  platform projection 只发布该 exact wrapper，文件名不参与 public/private 判定，matrix 显式证明
  其它 record/check/execute/preview/helper wrapper 未泄漏。
- `DES-026` Architecture 双维合同：Guru Team 方法论维度拥有 mandatory stage invocation、semantic route 与 freshness；项目维度拥有 baseline、constitution、required concerns、project checks 与具体正确答案；两者只在 task-local Architecture change contract 相交且不复制对方正文。
- `DES-027` Architecture lifecycle：current baseline/constitution -> Planning impact/path -> qualified implementation discovery re-entry -> Phase 2 project checks + before/after -> task contribution/necessary ADR -> committed full-diff Branch Review -> serialized promotion -> fresh Phase 2/commit/Branch Review -> successor identity consumed by downstream stages/tasks。
- `DES-028` Design constitution authority：`docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / `current` 唯一拥有原则正文；公共 projection 只含 `mature-practice-applicability`、`concept-semantic-completeness`、`cohesion-change-isolation`、`minimum-necessary-complexity`、`debt-one-way-convergence` 五个 identity/short name。
- `DES-029` Architecture impact：恰好选择 `target_native|legacy_boundary_convergence|dedicated_refactor_slice`；#283 以 `target_native` 原子切换 2.0 consumers，不保留 1.0 dual-read/adapter，也不关闭 release GAP。
- `DES-030` Project change contract：`guru-trellis-architecture-change-contract-v1` 绑定 required concern set `guru-trellis-architecture-change-concerns-v1`，覆盖 authority、constitution、boundary/decision、owner/single-writer、compatibility/exit、GAP/deviation、parallel scope、evidence/freshness 与 review/promotion。
- `DES-031` Project check：current descriptor `guru-trellis-architecture-convergence:repository:1` / check `guru-trellis-architecture-convergence@1` 绑定每个 stage 的 applicable scope、rule/decision/GAP refs、before/after、evidence 与 freshness；AI 判定 applicability/blocking/route，runtime 只校验 descriptor/result 一一绑定。
- `DES-032` Architecture routes：缺适用 contract/constitution/check facts 为 `contract_incomplete`，与 current authority 冲突为 `architecture_conflict`，新增或恶化偏移/owner 扩张/无退出双写/closed GAP 重现为 `fitness_regression`，baseline/constitution/contribution/expected-current stale 为 `sync_required`。
- `DES-033` Contribution/promotion isolation：task writer 只写 task-owned contribution；Architecture owner 是 shared-current single-writer。promotion 绑定 independent committed range 与 expected current，live identity 推进时禁止覆盖并让旧 task re-entry。
- `DES-034` Distribution/validation boundary：2.0 schema/runtime、canonical/dogfood/installed、Shared/Codex/Claude/Cursor 与十个 project-neutral scenarios 原子一致；#283 只要求 targeted checks 与一个代表性 clean install，独立的重构前稳定版 Release Issue 独占 exact-candidate release matrix/tag/Release/immutable smoke。
- `DES-035` Base selection：`select_base` 只读取 caller explicit value、repo config、exact local/remote refs 与 remote default，按固定 precedence 返回 source/base/remote/ordered candidates；current branch 与 worktree inventory 不参与选择。
- `DES-036` Authority binding：selection 后解析同一 Git common-dir 的 registered worktrees，只接受 branch field exact 等于 `refs/heads/<selected_base>` 的唯一 checkout，并复核 toplevel、common-dir、branch、HEAD/local ref 与 clean identity。
- `DES-037` Session/authority separation：session checkout 仅作为 invocation shell并允许 detached；authority checkout 独占 fetch、可选 `merge --ff-only`、checker clean/equality 与 public handoff locator。
- `DES-038` Fail-closed binding：missing、ambiguous、dirty、branch/HEAD/ref mismatch 使用稳定 blocked route；不 checkout/switch/create/reset/rebase/stash/force update，也不重选 base。
- `DES-039` Fast-forward execution：execute 在 authority cwd 使用 explicit refspec fetch；local==remote 时不 merge，local 为 remote ancestor 时只执行 `merge --ff-only`，diverged 或 remote-behind 阻断。
- `DES-040` Public compatibility：closed result schema、Interface 1.4、`synced|skipped|blocked` exits 与 transition shape 不变；checker invocation-local authority path 仅投影到既有 locator 字段。
- `DES-041` Downstream freshness：workspace consumer 按 transition source 重新解析 explicit/config/config-candidate/remote-default current authority，并 exact 比较 selected base 与完整 ordered candidates；freshness 前不执行 config-only resolution，不导入 producer private runtime。
- `DES-042` Distribution evidence：canonical 与 installed package、Shared/Codex/Claude/Cursor projection、extension inventory、reapply/drift/mode/sidecar-zero 和一个 installed detached wrapper 分层证明 #290；release-wide matrix 仍由独立的重构前稳定版 Release Issue 独占。

## Public I/O 与 private state

- `CON-001`：23 个 active Skill 以 registry/interface 为 public graph，typed exit 必须有唯一 consumer 或 fail-closed stop。
- `CON-002`：public output 是最小 handoff DTO；不携带完整审查、Git 可推导事实、用户授权或 private digest。
- `CON-003`：producer output 到 consumer input 是显式、薄、可确定性验证的 projection；consumer 不理解 producer private artifact。
- `CON-004`：terminal projection 不把 durable archive 当作 live provider；archive 只提供已提交 identity，Git/GitHub current facts仍必须精确匹配，缺失 locator 或任何 drift 均 fail closed。

## #295 design promotion additions

- `DES-043`：Sync 只投影 `base_current`，Discovery active input 2.0 由 caller authoring `change_input`，Discovery owner-result 3.0 独占 `base_observation` 与 live authority binding。
- `DES-044`：Discovery public invoke/checker 在 semantic owner 之后只做 schema、identity、repo/ref/HEAD/clean 与 typed-route 校验；不得 import Sync private runtime、调用低层 executor 或伪造 result/digest。

## #311 installed Finalizer provenance design

- `DES-045` Closed binding resolver：Finalizer 从 target reviewed manifest 读取 source
  `repo/ref/commit/tree_state/is_mutable_ref`，复用 package-local repository normalization 与 Git
  primitives，构造 invocation-local `self_hosted|installed` binding。self-hosted source 固定为 target
  reviewed HEAD；installed source 只接受 canonical repository 的 immutable full OID，并在独立
  tempdir 完成 exact-OID fetch、detached checkout、origin/HEAD/clean 校验。
- `DES-046` Apply and tail ownership：target reviewed checkout 始终由 target repository 在 reviewed
  HEAD 建立；apply executable 只从 extension source checkout 定位，`--repo` 只指向 target。
  apply 后分别验证 source identity/clean 不变、target dirty path 仅 manifest、字段 allowlist、
  mode-specific source postimage、direct parent、single tail 与 publication head。preview 先分类 existing
  PR，再处理无 remote 的初始 `prepared` provenance reprepare；executor 仅接受 absent remote 或 exact
  reviewed head，terminal invoke 继续使用原始 publication input 与精确 retired locator。
- `DES-047` Distribution and isolation：Finalizer package-local runtime 独占 binding、两棵 checkout
  lifecycle 与 tail producer；installer 独占 manifest provenance；verifier lifecycle 与 Finalizer 无
  import、call、artifact 或 exit edge。canonical source 经 preset 投影到 dogfood/Shared/Codex/Claude/
  Cursor，package tests 从当前 package root 定位 shared runtime，生成副本不反向成为 source。
- `DES-048` Verifier failure evidence：compatibility runner 在 pre-matrix、matrix-cell 与 post-matrix
  异常边界输出 bounded structured failure；standalone verifier 在 cleanup 前解析并绑定 command
  evidence，无法解析时显式分类。matrix 外 command 或 inventory/ownership/sidecar/capability failure
  统一生成 `postcheck_failure`；该 private evidence 不进入 Finalizer authority。
- `DES-049` Historical serialized authority promotion：#267 的 Architecture owner 从 reviewed
  contribution 激活 `.42` baseline/current/evidence，RDT owner 随后建立完整 `.42`
  Requirements/Design/Test version、navigation 与 predecessor history；两步均绑定当时 live current
  `.41`，不得并行或覆盖 advance。该 `.42` authority 后由 `.43` successor 继承，当前由 `.44` 承接。
- `DES-050` Historical fact-only projection：#267 的 `.42` 从 `.41` 继承全部 runtime behavior、
  public contracts、Architecture decision、owner、GAP 与 compatibility exit，只更新 release/current
  mapping、traceability、evidence 和 predecessor/successor identity，不创建 ADR 或第二 authority。
- `DES-051` Release identity separation：历史 #267 knowledge `.42`、extension `0.6.15-guru.39`、
  Trellis CLI `0.6.15` 与 target tag `v0.6.15-guru.3` 是独立 identity axes；当前 `.44` 经 `.43` predecessor 继承该
  separation，tag、Release、latest-stable 与 tag-pinned smoke 仍只由 #267 exact candidate 的 live proof 晋升。
- `DES-052` Historical promotion re-entry：#267 owner promotion 只产生 shared-current working-tree
  diff；该 diff 按历史合同重新通过 Phase 2、task commit 和独立 complete-range Branch Review 后才恢复
  Publication。#311 的正式 `.3` business-repository proof 与 closure 保持独立后续 owner。

## #335 repository-private release orchestration design

- `DES-053` Private projection boundary：`.agents/skills/release-guru-trellis-version/` 是本仓库共享
  Markdown 语义定义，Codex/Claude/Cursor roots 保存 project-local discovery projection；公共 package、
  registry、marketplace、preset、overlay、extension manifest 与业务仓 installed inventory 均保持零包含。
- `DES-054` Invocation-local preflight：每次调用聚合六项最小输入与 fresh live Issue/Git/GitHub/version
  facts，分类 preparation 或 post-merge exact-candidate stage。缺失、歧义、mismatch、unknown/multiple/
  unmapped exit 均 fail closed；恢复时重读 live authority。
- `DES-055` Preparation composition：standard intake 后，最终 delivery 先完成 pre-promotion Phase 2、Task
  Commit 与覆盖完整 `origin/<base>...HEAD` 的独立 Branch Review；P0-P3 open findings 为零后，serialized
  Architecture/RDT owners 才可绑定 expected current promotion shared authority。promotion-created diff 必须
  再执行 fresh Phase 2、Task Commit 与完整 Branch Review，第二次 review 通过后才进入 Publication、
  Finalizer 与 Merge。每个 owner 独占内部 judgment、typed exit、确认与副作用；私有 Skill 不复制流程。
- `DES-056` Exact-candidate reset：preparation merge 后重新 fetch `origin/main`，仅从 live merge/base
  facts 建立 exact candidate；preparation identity、旧 gates 与旧 release evidence 全部丢弃，cross-SHA
  或 lineage gap 在 mutation 前停止。predecessor full diff、版本映射、source/installed validators、
  四平台 parity、install/update/reapply、secret scan、residue 与 tag-pinned smoke 必须绑定同一 candidate；
  完整累计多平台矩阵保留给专门 Release Gate owner。
- `DES-057` Live payload and durable-state boundary：Publication 在 PR 动作前即时生成并审查 PR payload；
  Release boundary 在 GitHub Release 动作前即时生成并审查 Release payload。payload 只存在于当前 owner
  handoff，不写 task-local release notes、body、status 或动态 checklist，也不持久化用户授权。
- `DES-058` Reviewed-content classification：实际交付、Skill、durable docs、配置、schema、script 与
  tests 进入 content identity 并触发 gate freshness；owner-private checkpoint 与 lifecycle metadata 不
  进入该 identity，consumer 完成后按 owner 合同退休。planless `base_reconciliation_required` 先验证
  exact base facts，再执行既有 generic plan identity 检查。
- `DES-059` Independent transactions：merge、annotated tag、tag-pinned smoke、GitHub Release、Issue
  closure 与 cleanup 各自拥有精确 preview、当前对话确认与 mutation；Skill 只路由下一 owner，不保存
  授权、阶段或动作结果，unsupported exit 无 fallback。

## #332 exact-candidate Release Gate design

- `DES-060` Release identity projection：RDT/Architecture、manifest、README、workflow、preset、fixture、
  canonical、dogfood 与 installed release-facing surfaces 共享 `.5/.40/CLI 0.6.15` target mapping；
  latest stable `.4/.39/CLI 0.6.15` 只作为 predecessor，历史 versioned authority/evidence 原文不回写。
- `DES-061` Preparation and candidate reset：#332 preparation 复用 standard Intake 到 expected-head merge
  的既有 owner，并 fresh 消费 #311/#333/#339/#358/#361 merged behavior。merge 后丢弃 preparation SHA 与
  gates，从 live `origin/main` 建立 lineage 可证明的 candidate SHA/tree，再执行 predecessor full-diff review。
- `DES-062` Serialized authority promotion：Architecture owner 已先绑定 expected `.43` 激活统一 `.44`
  baseline；RDT owner随后以同一 contribution、expected `.43` 和 Architecture `.44/current` 建立完整 `.44`
  Requirements/Design/Test authority。promotion-created diff 重新进入 Phase 2、task commit 与完整 Branch Review。
- `DES-063` Exact-candidate evidence graph：同一 candidate 依序绑定 full diff、版本面、source/installed
  validator、registry/interface/schema/ownership、managed parity、四平台 actual-load、clean/existing
  install/update/reapply、installed business-repository Publication/Finalizer、secret scan 与 recursive
  sidecar/residue-zero；failed/SKIP/stale/cross-SHA/unknown route 在 tag mutation 前 fail closed。
- `DES-064` Immutable release transactions：tag preview/confirmation 后创建 annotated tag；live 回读 tag
  object/peeled commit 后从 immutable tag 执行 post-publish smoke；随后 GitHub Release、#332 closure 与
  cleanup 分别 fresh preview、确认、执行和回读。任何失败不得移动、删除或重建已创建 tag。

## #240/#348 reviewed owner promotion design

- `DES-065` Qualification owner separation：`guru-qualify-normal-scenario` 只判断问题场景，
  `guru-qualify-solution-mechanism` 只判断拟采用机制；caller 依次提供同一 profile 的 current candidate
  set/live locators，两个 owner 的结果互不替代，机制 revision 只返回原 caller remove/replace 后 fresh 重跑。
- `DES-066` Application-level mechanism boundary：机制 owner 沿真实 dependency/caller graph 判断业务
  authority 的承载位置；OS lock/process/descriptor primitive 不合格，普通文件/目录作为普通 state 或
  artifact 合格。AI 独占语义，runtime 只验证 shape/identity/freshness/consumer binding，结果 invocation-local。
- `DES-067` Merge/recovery owner split：`guru-merge-task-pr` 保留 task-work 与 external blocker 分类，
  `phase2_reentry_required` 只投影最小 identity 到唯一 `guru-restore-archived-task`；外部 blocker 继续
  terminal，恢复成功只进入 `guru-resume-implementation` 的 Phase 2 route。
- `DES-068` Idempotent original-identity restoration：恢复 command 在 fresh live facts 与 semantic result
  闭合后，只执行 archive-to-active、`in_progress`、mapping/current-task 修复和 stale downstream authority
  清理；exact already-restored 为只读成功，dirty/duplicate/stale/merged/ambiguous 状态零业务写入。

## #332 original-entry convergence design

- `DES-069` Original public entries：Commit、Publication、Finalizer、Merge 的既有
  `scripts/invoke.sh` 分别绑定原稳定 command id，并继续作为唯一平台 public wrapper。
- `DES-070` Closed invocation modes：原 command 的 arguments 是 Happy Path 与旧参数 compatibility
  的 closed union；package runtime 在入口处选择单一模式，wrapper 只定位 managed dispatcher 并透传 argv。
- `DES-071` Invocation-local transaction：Happy Path 复用 invocation-local facts，只在 mutation
  boundary 与 post-mutation proof 做必要 fresh read；compatibility 不成为正常路径的前置链。
- `DES-072` Facade removal：只服务 PR #341 第二 public command 的 facade adapter、schema、example、
  fixture 和 projection 在确认无 consumer 后删除，transaction/recovery primitive 留在原 command 内部。
- `DES-073` Interface-driven projection：通用消费者读取 Interface 声明的 exact wrapper，并验证
  canonical/installed/platform bytes、executable mode 与 private-script leak。
- `DES-074` Managed-launcher validation：`runtime/validate.py` 对 Interface-declared public wrapper
  执行 platform launcher fallback 校验；qualification-only 固定路径不扩散到 generic runtime/eval。
- `DES-075` Managed removal：preset apply 删除旧 facade projection并同步 canonical、dogfood、installed
  与 Shared/Codex/Claude/Cursor；共享 scripts 目录不建立转发层。
- `DES-076` Non-invoke fixture：`guru-restore-archived-task` 的 `restore-archived-task.sh` 覆盖 generic
  source、installed、platform、actual-load 与 eval，证明 wrapper selection 不依赖文件名。
- `DES-077` Preserved gates：各 semantic owner、typed exit、consumer、confirmation、freshness、
  expected-head、recovery 与 fail-closed route 保持不变；低层命令仍为 package-private。
- `DES-078` Architecture path：本次使用 `dedicated_refactor_slice`，外部行为与 public identity 不变，
  只把双入口收敛为一个 owner/entry；无新 ADR、长期例外或第二 authority。
- `DES-079` Serialized promotion：reviewed contribution 绑定 expected `.44`，RDT 与 Architecture owner
  生成唯一 active `.45`；promotion-created diff 必须 fresh 重跑 Phase 2、commit 和完整 Branch Review。
- `DES-080` Candidate reset：`.45` 只建立 current knowledge authority，不证明 release；preparation merge
  后旧 candidate 全部失效，必须从 fresh `origin/main` 重建 exact candidate 并从零执行 #332 Release Gate。
- `DES-081` Exclusive Guru finish：global workflow 与平台 `guru-finish-work` launcher 排除 upstream
  `trellis-finish-work`；task discovery 先识别 archived incomplete closeout，Finalizer transaction 独占
  archive/journal ordering，非法状态返回 fail-closed typed exit。
- `DES-082` Review visibility and announcement：`guru-review-branch` 在 dispatch/return 两侧输出最小可见
  identity 与 finding summary；workflow 只把同一 identity 的 checker + public wrapper 双 `passed` 投影为
  正式 pass，并以该唯一出口进入 Publication。
- `DES-083` Confirmation continuity：平台 launcher 维护当前对话已展示动作的单次消费语义；普通“确认继续”
  消费该动作，mapped exits 自动路由。canonical/installed/三平台 actual-load 共同验证投影切换不丢失流程状态。

## #376 post-review base continuity design

- `DES-084` Independent clocks：Reconcile 独立比较 integration base、Issue/scope/approved assumptions 与 task
  content identity；base-only advance 保留原 resume target，真实 authority/content drift 继续进入
  Planning、Implementation 或 full Branch Review owner。
- `DES-085` Expected-head local executor：`execute-base-reconciliation` 是 Reconcile package-private command，
  只接受 branch-bound clean worktree、expected task/base heads、prior review、candidate tree 与 commit message；
  前后验证 ancestry/tree 后创建唯一 local commit，不执行 push 或 provider mutation。
- `DES-086` Minimal private recovery：reconciliation receipt 与 integration-pair checkpoint 只保留 checker
  直接消费的 identity，不记录授权；已创建 commit 的 recovery 先验证 current pair，再执行普通 stale guard。
- `DES-087` Bounded continuity review：Review Branch `base_continuity` 分别绑定 prior full-review commit 与
  current reconciled HEAD，gate review commit 绑定 current HEAD，只审查 exact pair、conflict resolution、
  candidate tree 与受影响验证；成功投影 current HEAD，不宣称第二次 full Branch Review。
- `DES-088` Strict Publication edge：Publication schema 与 `guru-reviewed-content-1.0` 保持严格；Finalizer
  `base_reconciliation_required` output 经 Interface seed/projection 把 `branch_review_commit` 传给 Reconcile，
  source/installed integration 从该声明 edge 构造 DTO 并进入真实 Publication recorder/checker/wrapper。
- `DES-089` Direct evolution and ownership：public Skill/exit identity 不变，current-only schema 替换 stale
  meanings，不 dual-read；current graph 是 23 Skills / 97 exits / 78 commands，新增 command 仅属于 Reconcile
  package，Architecture/RDT promotion 后强制 fresh Phase 2、Task Commit 与完整 Branch Review。

- `CON-005`：repo-private Skill 不声明 public interface/schema/runtime/typed exit，也不进入 registry、
  extension inventory 或业务仓 installed projection。
- `CON-006`：orchestrator 只消费既有 owner 的 public minimal outputs；不得读取其 private artifact、
  复制 transaction implementation 或把 action-local confirmation 扩张到其它动作。
- `CON-007`：Merge-to-recovery DTO 只含 repository、PR/head/branch、Issue、task/archive、finding 与
  `resume_target=phase-2` identity；不得携带用户授权、machine-local path、完整 provider payload 或旧 gate。
- `CON-008`：base-continuity handoff 只携带 exact task/base pair、prior/current review anchors、candidate tree、
  relevant paths 与原 resume target；producer-to-consumer projection 必须显式，任何旧 schema/checkpoint 直接 stale。

## Capability owner map

| Capability | Skill / route | External exits |
| --- | --- | --- |
| mode | `guru-select-workflow-mode` | `standard_intake`, `task_free`, `blocked` |
| base/context | `guru-sync-base`, `guru-discover-change-context` | `synced/skipped/blocked`; `context_ready/refresh_base/blocked` |
| clarification/wording/readiness | `guru-clarify-requirements`, `guru-review-contract-wording`, `guru-review-change-request` | interface-defined closed exits |
| workspace/planning | `guru-create-task-workspace`, `guru-approve-task-plan` | `created/refresh_review/blocked`; `approved/revision_required/clarify_scope/blocked` |
| normal-path qualification | `guru-qualify-normal-scenario` | `classified/scope_confirmation_required/mechanism_revision_required/blocked` |
| solution-mechanism qualification | `guru-qualify-solution-mechanism` | `classified/scope_confirmation_required/mechanism_revision_required/blocked` |
| task-free | `guru-execute-task-free-change` | 7 closed exits incl. `completed`/`blocked` |
| execute/check/commit | `guru-check-task`, `guru-create-task-commit` | check 4 exits；commit 3 exits |
| base evolution | `guru-reconcile-task-base` | 6 exits incl. continuity/implementation/planning routes |
| review/publication | `guru-review-branch`, `guru-review-task-publication` | review 5 exits；publication 3 exits |
| finish/merge/recovery | `guru-finalize-task`, `guru-merge-task-pr`, `guru-restore-archived-task` | finalizer 6 exits；merge 4 exits；restore 2 exits |
| installation verification | `guru-verify-extension-installation` | `verified`, `blocked`；standalone only |
| RDT authority | `guru-maintain-requirements-design-test-ssot` | `ssot_current/sync_required/revision_required/baseline_incomplete/blocked` |
| Architecture authority | `guru-maintain-architecture-baseline` | 7 baseline/conflict/fitness exits |
| Repository Bootstrap | `guru-bootstrap-repository-ssot` | `completed/baseline_incomplete/repair_required/blocked` |

完整 stable ids、schema ids、commands 与 exits 以 `trellis/skills/guru-team/registry.json`、各 package `interface.json`、`commands.json` 和 `trellis/guru-team-extension.json` 为准，本表不复制 schema 正文。

## 关键时序

```text
Issue/current request
  -> mode -> sync -> context -> clarify -> wording -> readiness -> workspace
  -> planning -> plan approval -> user plan pause -> implementation -> Phase 2
  -> semantic commit -> full branch review -> publication review
  -> finalization transaction -> Ready PR -> expected-head merge -> closure check
```

```text
existing_repository Bootstrap
  -> source analysis -> trellis-spec-bootstrap
  -> RDT bootstrap_foundation <-> Architecture bootstrap_foundation
  -> cross-SSOT review -> minimal .trellis/spec projection -> validation -> current
```

```text
install / update / upgrade
  -> 选择 immutable workflow source 或明确 latest/canary source
  -> official Trellis init/update/upgrade 与 workflow preview/switch
  -> Guru preset initial apply/reapply
  -> 校验 extension manifest、managed inventory、platform bytes/mode
  -> 解析全部 .new/.bak -> source/installed/dogfood drift gate
```

```text
compatibility matrix
  -> live inventory derives claude / codex / cursor
  -> each platform runs clean-0.6.15 and existing-0.6.5-to-0.6.15
  -> installed RDT / Architecture / Bootstrap profile evals
  -> exact capability comparison + zero unknown drift/sidecar
  -> A/B local lifecycle matrix + separately authorized real GitHub A route
```

```text
delivery / Finish / cleanup
  -> Phase 2 passed -> semantic task commit -> full branch review
  -> publication readiness -> Finalizer expected-head transaction
  -> push / non-draft PR / archive / finish-summary -> Ready
  -> expected-head merge -> Issue closure verification
  -> exact branch/worktree/task cleanup（仅在 retained ref/reachability 已证明后）
```

任一步出现 base/provider/content drift 时返回该 owning Skill 的 re-entry；已创建 commit/PR/archive
事实由当前 owner 恢复，不重复副作用，也不回到 Phase 0 猜测状态。

## 数据与恢复

Task index/history 查询来自 task/archive；finish-summary 是 compact closeout history。Provider/base 状态从 live Git/GitHub 恢复；stale/mismatch 返回 owning typed route。两个并行 task 只写各自 task/worktree/contribution，promotion 由唯一 shared authority owner 串行投影；Architecture promotion diff 必须重新进入 Phase 2、task commit 与独立 Branch Review。普通恢复不创建 handoff、shared ledger 或授权记录。Compatibility evidence只向下游输出 source/version、Finish profile、archive locator、tracked-write、commit reachability 与结果边界，不输出完整日志、用户授权或临时仓库状态。

## #378 固定 Fork runtime 设计

- `D378-01` Source/build：canonical `trellis/presets/guru-team/source/trellis-source.json` 是唯一固定来源记录；显式 Fork checkout 核验 remote、完整 HEAD、CLI 版本后，使用 Fork 自身 lockfile 和构建命令，成功后写入 `packages/cli/dist/.guru-source-commit`。校验器比较该构建标记与固定 HEAD，拒绝同版本源码前进却未重建的普通错误。直接运行 `packages/cli/bin/trellis.js`，不新增 launcher、打包器、cache manager 或 dist-copy 层；构建链逐步失败即停止。
- `D378-02` Resolver/hook：Fork 拥有 session resolver 与主 hook。主会话和普通 CLI 不启用 single-session fallback；显式 child 路径保留该接口。缺失、未匹配、stale 与跨 worktree 情况保持 non-owner session 不变，不新增 session model。
- `D378-03` Distribution：preset 将唯一 source record 投影为 `.trellis/guru-team/trellis-source.json` 并纳入 managed inventory；记录不是第二来源 authority。固定 Fork CLI 执行 update dry-run、按结果选择 preserve-mode migrate/update；核验 workflow 字节，按需 preview/switch，再同平台 preset reapply，逐项审查 sidecar。Guru 不覆盖 Trellis-owned runtime，不恢复旧 stash manifest，不覆盖 #388/#389 前置。
- `D378-04` Verifier：原 shell 只承接参数与 managed Python dispatch；full/focused 场景由现有 Python matrix 单独拥有，删除 dispatch 后不可达尾部，不保留双份场景编排。standalone 兼容调用承接显式 `TRELLIS_FORK_SOURCE`；full predecessor 使用独立 checkout/SHA，缺失即报告来源验证失败。closeout fixture 在 verifier 内准备，经实际 installed record/check/public wrappers 执行；fake provider 结果不是远端发布或真实业务交付。

当前安装顺序为固定来源核验/构建 -> 同一 Fork Node CLI init 或 update -> 同平台 Guru preset -> source/installed/ownership/drift/sidecar 检查。
这直接替换 DES-014/017 的旧 npm-prefix/stock upgrade 运行假设；其历史 matrix 证据保持原版本边界。
构建标记仅证明本地成功构建来源，不承接语义批准、授权或发布身份。Architecture 只引用同版本 public baseline，不复制其正文或私有状态。

## #392 serialized release promotion design

- `D392-01`：四个发布轴保持独立 authority，但 current surfaces 统一映射
  `v0.6.16-guru.1` / extension `0.6.16-guru.41` / CLI `0.6.16` /
  `castbox/Trellis@ad332e3fe5a19d7274cb03e7c2f3e2128f8de291`。
- `D392-02`：task writer 只写 delivery 与 reviewed contributions；Architecture/RDT owners 绑定 expected
  `.47` 串行建立唯一 `.48` current，`.47` 仅在 navigation/history 中成为 immutable superseded。
- `D392-03`：current consumers subtraction-first 直接迁移，不新增 dual-read、fallback、alias、adapter、
  第二 release state machine、公共 API 或 runtime lifecycle artifact。
- `D392-04`：Stage 1 唯一顺序为 pre-promotion fresh Phase 2/commit/full review -> serialized promotion ->
  post-promotion fresh Phase 2/commit/full review -> Publication/Finalizer/Merge；promotion-created diff 未复核时
  后续 owner 不可达。
- `D392-05`：Stage 2 在 merge 后 fresh-fetch `origin/main`，以同一 exact commit/tree 绑定 lineage、完整 diff、
  version mapping、source/installed、四平台、ownership/reapply/drift、install/update/switch、Fork build、业务
  smoke、secret scan 与 residue；tag、smoke、Release、Issue close、cleanup 各自独立。
- `D392-06`：durable authority 只记录稳定 identity、locator、关系与未验证边界；动态 SHA、Gate、时间、
  tag/Release 状态与用户授权不进入 tracked Docs。

本设计保持 public graph 23 Skills / 97 exits / 78 commands。`.48` promotion 不证明 Publication、merge、
full throwaway matrix、business smoke、tag、GitHub Release 或 Issue closure 已完成。

## #329 Developer-free Trellis design

- `D329-01`：`trellis-source.json` 是唯一 source lock。固定 Fork checkout 自行安装依赖并 build，
  `packages/cli/bin/trellis.js`、CLI version、`pnpm@10.32.1` 与 `.guru-source-commit` 绑定实际 HEAD。
- `D329-02`：Trellis-owned managed assets 只由 `0.6.17` official update/migrate/generation 产生；
  Guru-owned workflow、Skill、runtime、installer、fixture、spec 与 overlay 在 canonical source 直接演进，
  再经 preset reapply 投影到 dogfood/installed copies。
- `D329-03`：current task resolution 使用 explicit selector、task metadata、Git common-dir/branch/worktree、
  ignored task/workspace mappings 与 issue ledger；mapping 只表示隔离 checkout，不是 legacy journal。
- `D329-04`：新 task 的 creator/assignee 由 workspace owner executor 显式传入 official task store；
  Issue 未分配时仅在 repository access preflight 通过后使用 authenticated GitHub login，失败则 write 前停止。
- `D329-05`：update/reapply 前后对 legacy roots 建立 path/mode/byte snapshot；snapshot 只服务 preservation
  validator，不成为 semantic authority、authenticity 或 anti-tamper boundary。
- `D329-06`：受控 consumer subtraction-first 迁移并删除旧 Guru path；不保留 adapter、fallback、
  dual-read/write 或 hidden global identity。上游 retired stub、negative assertion 与 immutable history
  分别按其现有 owner 保留。
- `D329-07`：三平台 lifecycle matrix 使用 target checkout managed runtime 与 fixture GitHub provider，
  分层验证 source build、generated adoption、focused regression、installed lifecycle 与 legacy preservation；
  local workflow sample 明确 unpublished boundary，installed closeout 从 clean committed candidate source reapply，
  capability comparison 对删除/缺失阻塞并单独接受 additive-only evolution。
- `D329-08`：task writer 只写 #329 delivery/contributions；shared current writer 仅为 serialized RDT/
  Architecture promotion owners。promotion-created diff 重新进入 Phase 2、Task Commit 与 full Branch Review。

该设计保持 23 Skills / 97 exits / 78 commands、extension `0.6.16-guru.41` 与 released
`v0.6.16-guru.1` 不变；不新增第二 identity authority、compatibility layer、ADR 或远端 writer。
