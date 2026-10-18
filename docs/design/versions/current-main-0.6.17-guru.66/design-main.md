# Guru Team Trellis Extension 当前设计

当前 .66 来源：reviewed #454 D436 contribution + inherited immutable `current-main-0.6.17-guru.65` authority；上游固定为 `castbox/Trellis@eb370008c7689d4e272ae626bd002190ecbb3296` / CI `35621578090` / CLI/core `0.6.17`，Guru manifest `0.6.17-guru.42`，release target `v0.6.17-guru.1`。Architecture inheritance：`docs/architecture/README.md` / `current-main-0.6.17-guru.66` / `active`。
完整继承 immutable `.65`，当前增量为 #454 D436 五个非激活 terminal lifecycle canonical package major；active registry 保持 32 packages / 142 exits / 102 commands 与六个 planned IDs，production workflow 保持 22 mandatory invokes / 98 exits。

`.66` 完整继承 immutable `.65` 并吸收 reviewed #454 D436 contribution；RDT 与 Architecture current 均为 `.66/active`。提升前 focused evidence 不证明 promotion-created diff；该 diff 仍须 fresh Phase 2、Task Commit 与完整 Branch Review，E434、#434 activation、installed/platform 和 Release matrix 均未完成或验证。

版本：`current-main-0.6.17-guru.66`；状态：`active`；predecessor：`current-main-0.6.17-guru.65`；source baseline：reviewed #454 D436 contribution + inherited immutable `.65` authority；精确 revision 由 containing Git object/tree identity 绑定。

## 分层与 ownership

- `DES-001` Canonical：`trellis/workflows/guru-team/`、`trellis/skills/guru-team/`、`trellis/presets/guru-team/` 是可分发源头；`.trellis/**`、shared `.agents` 与 pinned platform descriptor 指定的 native roots 是 installed projection，`guru-trellis` dogfood 只安装 Claude、Codex、Cursor。
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
- `DES-012` Finalizer terminal authority：正常 closeout 已退休 gate/transaction/plan 后，只有调用方提供的精确 retired owner locator 可触发 terminal reconstruction。runtime 读取 archive 中 `task.json`、`prd.md`、`design.md`、`implement.md`、`finish-summary.json` 五个 durable 文件，绑定 active/archive task locator、branch review commit、archive cleanliness，并重新读取 local/remote/Ready PR/title/body/base/branch；不重读 issue scope，全部一致才投影 `ready_for_merge`。
- `DES-013` Verifier inventory：source validator 从 registry/interface 形成 active package ids、commands 与 complete package commands；Throwaway verifier 只比较 validator projection 与 installed projection，不维护数量常量。
- `DES-014` Matrix orchestration：compatibility runner 由独立 cell executor 与 compact aggregator 组成；每个 cell 使用隔离 repo、npm prefix 与 runtime root，并输出 platform/scenario/version、pinned inventory identity、exact selection、template hash、sidecar 与 installed smoke 结论。runner 以 HEAD、tracked delta、untracked path/mode/content 与 isolated-index candidate tree 构成 source identity，且 run 前后必须一致。
- `DES-015` Platform authority：pinned upstream `AI_TOOLS` inventory 独占完整平台集合，目标仓库 manifest/provenance 独占 exact `selected_platforms`；canonical descriptors、installed ownership 与 native destinations 必须分别等于这两层的对应投影。`.agents` 是 shared projection，不是独立 platform；不得从 overlay、目录或 dogfood 反推第三层集合。
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
  PR，再处理初始 `prepared` provenance reprepare。无 predecessor transaction 时，executor 通过真实 Git ancestry
  接受 absent remote、exact reviewed head 或 strict historical ancestor，并拒绝 ahead、diverged 与
  unknown/unprovable commit；已有 predecessor transaction 继续绑定 exact old Publication HEAD。Reactivate branch
  reuse 已有身份匹配的 `ordinary_publication/push_content` transaction 时，该 transaction 是 current owner；先拒绝
  Open PR drift，并把同 branch/base terminal PR 仅保留为历史事实而非 current candidate。live remote exact
  `pre_push_remote_head` 时至多执行一次到 `publication_head` 的 fast-forward；exact `publication_head` 时按合法
  push-output-loss/converged state 接续。allowed heads 外的 remote、ahead/diverged/unknown topology 或 transaction
  identity drift 均 fail closed。该路径不增加宽泛 fallback、PR 人工选择 API、force push 或第二 ledger，也不删除
  transaction。terminal invoke 继续使用原始 publication input 与精确 retired locator。
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
  消费该动作，mapped exits 自动路由。canonical、exact installed selection 与 selected-platform actual-load
  共同验证投影切换不丢失流程状态；dogfood cell 的 selection 恰为 Claude、Codex、Cursor。

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
  meanings，不 dual-read；该 .46 before-state graph 是 23 Skills / 97 exits / 78 commands，新增 command 仅属于 Reconcile
  package，Architecture/RDT promotion 后强制 fresh Phase 2、Task Commit 与完整 Branch Review。

- `CON-005`：repo-private Skill 不声明 public interface/schema/runtime/typed exit，也不进入 registry、
  extension inventory 或业务仓 installed projection。
- `CON-006`：orchestrator 只消费既有 owner 的 public minimal outputs；不得读取其 private artifact、
  复制 transaction implementation 或把 action-local confirmation 扩张到其它动作。
- `CON-007`：Merge-to-recovery DTO 只含 repository、PR/head/branch、task/archive、finding 与
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
| review/publication | `guru-review-branch`, `guru-review-task-publication` | review 6 exits；publication 4 exits |
| finish/merge/recovery | `guru-finalize-task`, `guru-merge-task-pr`, `guru-restore-archived-task` | finalizer 6 exits；merge 5 exits（原四个 + review_refresh_required）；restore 2 exits |
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

Task index/history 查询来自 task/archive；finish-summary 是 compact closeout history。Provider/base 状态从 live Git/GitHub 恢复；stale/mismatch 返回 owning typed route。两个并行 task 只写各自 task/worktree/contribution，promotion 由唯一 shared authority owner 串行投影；Architecture promotion diff 必须重新进入 Phase 2、task commit 与独立 Branch Review。普通恢复不创建 handoff、shared state store 或授权记录。Compatibility evidence只向下游输出 source/version、Finish profile、archive locator、tracked-write、commit reachability 与结果边界，不输出完整日志、用户授权或临时仓库状态。

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

该 .48 设计保持当时 public graph 23 Skills / 97 exits / 78 commands。`.48` promotion 不证明 Publication、merge、
full throwaway matrix、business smoke、tag、GitHub Release 或 Issue closure 已完成。

## #329 Developer-free Trellis design

- `D329-01`：`trellis-source.json` 是唯一 source lock。固定 Fork checkout 自行安装依赖并 build，
  `packages/cli/bin/trellis.js`、CLI version、`pnpm@10.32.1` 与 `.guru-source-commit` 绑定实际 HEAD。
- `D329-02`：Trellis-owned managed assets 只由 `0.6.17` official update/migrate/generation 产生；
  Guru-owned workflow、Skill、runtime、installer、fixture、spec 与 overlay 在 canonical source 直接演进，
  再经 preset reapply 投影到 dogfood/installed copies。
- `D329-03`：current task resolution 使用 explicit selector、task metadata、Git common-dir/branch/worktree
  与 ignored task/workspace mappings；mapping 只表示隔离 checkout，不是 legacy journal。
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

该 .49 设计保持当时 23 Skills / 97 exits / 78 commands、extension `0.6.16-guru.41` 与 released
`v0.6.16-guru.1` 不变；不新增第二 identity authority、compatibility layer、ADR 或远端 writer。


## #408 Nightly 与正常调用合同

需求主定义为 [R408-01..08](../../../requirements/versions/current-main-0.6.17-guru.56/requirement-main.md)；

## #410 Release authority

`D410-01..06` 复用既有 release owner、Architecture/RDT promotion owner 与 exact-candidate
边界；不新增 public Skill、owner、compatibility layer 或 release state machine：

- `D410-01`：只推进 current release-facing mapping 与必要 canonical/dogfood projection，
  predecessor release 与 `.51` 文档保持 immutable history。
- `D410-02`：repository tag、extension revision、CLI/core 与 fixed Fork source 保持四条独立
  identity axis，不以任一版本号替代另一条来源 authority。
- `D410-03`：Architecture/RDT 继续由 serialized promotion owner 单写；promotion-created bytes
  使此前 Phase 2、commit 与 Branch Review stale，并要求 fresh 重跑。
- `D410-04`：preparation merge 后只从 fresh `origin/main` 冻结一个 exact candidate，禁止
  跨 SHA 复用 Stage 1 或旧 candidate evidence。
- `D410-05`：保留现有 owner 与 public API 边界，preparation PR 只使用 `Refs #410`，不提前
  关闭发布主 Issue。
- `D410-06`：annotated tag、tag-pinned smoke、GitHub Release 与 Issue closure 是依次独立的
  live action，每项重新绑定同一 exact candidate 和当前 authority。

本层只拥有设计责任。Architecture 继承 `docs/architecture/README.md` /
`current-main-0.6.17-guru.56` / `active`，引用 `ARCH-CUR-029`、`ARCH-INT-014..016`，
不复制 Architecture 正文，也不把 knowledge promotion 表述为发布完成。

- `D408-01` Source：现有 `trellis-source.json` 唯一拥有完整 commit 与正整数 `ci_run_id`。
  source validator 核验 Fork HEAD、run/head/success、CLI/core、package manager 和成功本地 build marker；
  `ci_run_id` 服务来源校验/安装 provenance，不承接语义判断或授权。current pin 由 R408-01 定义；
  predecessor fixture 仍使用其历史合同，不要求旧来源拥有不存在的 CI 字段。
- `D408-02` Generation：固定 Fork 自身 lockfile/build 后正式 update/init 生成 resolver、runtime 与
  hook；Guru preset 仅同步 owned assets 和 source record。正常顺序继承 D378-03/D329-02，
  不手改 Trellis-owned 脚本，不改变 workspace writer 或双端 mapping 算法。
- `D408-03` Stop/manual boundary：canonical workflow 拥有自动失败停止和独立手动请求的全局合同，
  既有 Skill 与三平台入口引用它。AI 报告错误及 known/unknown facts，独立操作使用现有 Git/gh
  能力并验证该项结果；不增加 Skill/exit/executor。Guru lifecycle 的 closure责任仍由Publication、
  Finalizer、GitHub与Merge各自单写；独立手动操作既不消费为Guru gate，也不补造Finalizer/archive/recovery state。
- `D408-04` Verification/distribution：现有 source preparation、session、package、finish-family 与
  focused installed fixture 分别拥有来源、session、旧链和分发证明；同一实际 Fork CLI 消费 managed
  record。测试层记录 native、fixture、真实 installed 与远端限制，静态文字不替代行为证明。
- `D408-05` Authoring：Discovery/Wording/Clarification/Readiness/Workspace 的 Agent-visible 合同给出
  repo-root cwd 与 `.trellis/guru-team/skills/packages/<skill>/` 的实际脚本/示例及各自参数。
  Clarification recorder 从完整 AI 语义输入派生现有 content/proposal/action/target bindings，保留
  upstream opaque duplicate token；Readiness recorder 从当前 source/transition 和已完成判断派生
  linkage/scope digests 与客观 finding count。checker 核验同一派生规则，缺 AI 判断仍拒绝，正常
  内容变化使旧绑定失配；不新增 public shape、dual-reader 或语义默认 pass。既有 installed transcript
  使用 Workspace `transition + authoring` 的 record 路径，以真实 stdout 接续创建、双端 mappings、
  boundary 和受控 `start-task.sh`；不依赖 eval runtime、手算 private plan 或补 mapping。

完整旧 lifecycle、23/97/78、developer retired-zero 与 recovery contract 继承历史 current authority。
source pin 的直接演进不改变 extension/release 轴，不新增 owner/GAP/ADR 或 #398/#407 恢复链。
对应关系和验证入口见 [traceability.md](./traceability.md)；本段不声明 post-promotion gate 已完成。

## #418 只读复审设计

来源：[历史 contribution](../../../requirements-design-test-contributions/418-closeout-identity-recovery/design.md)；
需求为 [R418-01..07](../../../requirements/versions/current-main-0.6.17-guru.56/requirement-main.md)，
双向索引见 [traceability.md](./traceability.md)。

- D418-01：Finalizer 的原 executor 验证精确 committed archive 与同一 task 的既有 source/target mappings 后收敛 locator。缺 mapping、不同身份或 archive continuity 失败即停止；preview、boundary 及新只读 profile 不修映射。
- D418-02：Merge 在已知错误发生点保留 input/provider/stale 诊断，经原 CommandError 与正式 wrappers 传播。输入 diagnostic 不伪装成完整语义 typed exit；未知异常仍 generic fallback。
- D418-03：原 public invocation 增加下表四个隔离 profile。completed、committed/clean archive 与准确 Ready Open PR 是入口条件；正常 Ready handoff 和已正常退休 checkpoint 继续走原链，不强制复审。
- D418-04：H 是原归档前 review tip，由 committed finish-summary 的 commit 集合中唯一 ancestry 支配顶点推导，不依赖数组末项。A 是当前 archive HEAD；B 是本轮真实 reviewed base，Branch Review 审查完整 B...A，要求本地 selected-base 与 live base 同指 B 且 B 在 A ancestry。Finalizer 用 H 校验原 review/content/archive continuity，用 A 校验当前复审与 local/remote/PR HEAD；Publication/Finalizer 继续核对 B。缺对象、不唯一或漂移即停止，不 fetch/update refs、不改 summary、不以 A 覆盖 H。
- D418-05：Merge 的 PR snapshot 只对 title/body 计算 hash；head 与 Ready 状态分别通过 live checks 核验，不属于该 snapshot hash，也不生成 Publication 判断。Publication 在独立只读 preflight 重新审查现有 bytes 的十个维度；全部 current 才 archived_ready。metadata/task_work finding 保留真实分类，external_blocker 保留对应 blocked 维度；任何缺口停止，不编辑 PR、不运行 active prepare_closeout。Finalizer 精确比较新 Publication bytes 与 live PR，不能沿用旧 payload 或用 snapshot 当 pass。
- D418-06：Architecture 既有 profile 仅增加下表三个 source/stage 配对；独立 owner 完成当前判断，仅可 current 或 blocked。需 promotion/repair/业务写入的结果停止；validator 拒绝写入 continuation 或 stage mismatch，不新增 Architecture profile。

| Owner | 新 profile | 只读成功出口 / 唯一下一 consumer |
| --- | --- | --- |
| Merge | archived_review_request | review_refresh_required -> Branch Review |
| Branch Review | archived_review | archived_review_passed -> Publication |
| Publication | archived_publication_review | archived_ready -> Finalizer |
| Finalizer | archived_review_refresh | 原 ready_for_merge -> Merge |

| Architecture source_exit | 既有 stage |
| --- | --- |
| review_refresh_required | branch_review |
| archived_review_passed | publication |
| archived_ready | acceptance_finish |

Finalizer 新 profile 直接验证并投影原 ready_for_merge，不进入 archive/push/PR/Ready transaction loop。
旧 transaction 未完成时先回原恢复诊断；业务 task/archive/summary、mappings、Git refs、PR/Issue 零 mutation。
允许的写入仅为各原 owner-private recorder/checker 的短期结果及退休，不创建长期 recovery state 或跨 owner private-state reader。

Branch Review 普通 aggregate input 4.0 / gate 7.0 保持；additive aggregate input 5.0
包含新增 profile，其 gate 为 archived-1.0。完整 DTO、schema、字段和 invocation 仍由
[Branch Review](../../../../trellis/skills/guru-team/packages/guru-review-branch/interface.json)、
[Publication](../../../../trellis/skills/guru-team/packages/guru-review-task-publication/interface.json)、
[Finalizer](../../../../trellis/skills/guru-team/packages/guru-finalize-task/interface.json)、
[Merge](../../../../trellis/skills/guru-team/packages/guru-merge-task-pr/interface.json) 的 package SSOT 独占。
原 profiles、status、review anchors、旧成功/失败出口与 mutation 条件不放宽，既有 closure ownership/Restore 不变。
当前能力表中的总数覆盖新增边；继承 D408 等历史条目的四出口及 23/97/78 只说明原路径/before-state。

Architecture 只引用 [ADR-010](../../../architecture/adr/010-archived-review-authority.md)、
[ARCH-CUR-030](../../../architecture/01-current/system.md)、ARCH-INT-018 和
[EVD-028](../../../architecture/evidence/current-evidence.md)，inheritance 为 .53/active；不复制原则正文。

## #419 Active-task continuation design

- `D419-01`：上游提供结构化 continuation protocol 和 workflow-neutral thin entries；Guru workflow 的唯一
  非空区块独占 Guru detailed route，Phase Index、workflow-state、hooks 与 platform entries 只提供 facts/breadcrumbs。
- `D419-02`：先绑定 exact current task，再区分 adjacent DTO 与 lost DTO；adjacent 走 Interface consumer，
  deterministic loss 回 producer，semantic loss fresh 重跑，unknown/multiple/stale state fail closed。
- `D419-03`：Phase 1 按最早 current owner恢复；workspace created loss 只走 read-only same-owner recovery；
  activation `initial|recovery` 均先验证 task/worktree/branch/mapping/status，再决定一次 mutation或零 mutation。
- `D419-04`：Phase 2 retained checkpoint 只通过既有 checker 与 public invoker重投影，不新增 recovery API。
- `D419-05`：Task Commit 复用 same-candidate transaction recovery；Branch Review/Publication checkpoint正常退休，
  output loss 分别 fresh重跑；continuation只恢复到 existing Finalizer entry。
- `D419-06`：dialogue-local confirmation 与 typed-exit auto-consumption 分离；payload/authority变化使旧确认失效，
  executor failure 不产生 success exit。
- `D419-07`：Guru preset 只拥有 Guru packages/runtime/schema/projections；upstream entries不进入 inventory或overlay。
- `D419-08`：回归使用 canonical/installed workflow、正式 wrappers 与真实 Git/task/worktree fixtures，不预填 pass。
- `D419-09`：先绑定 exact upstream SHA、ordered parents与tree，再运行 extractor、continuation mode和thin-entry tests。
- `D419-10`：#410 在 #419 merge 后从 fresh main重新冻结release candidate并独立执行Release Gate。

## #435 Active Task Delivery Loop design

- `D435-01`：`guru-review-task-delivery` 使用 semantic profile：AI authoring -> private recorder -> objective
  checker -> one typed projection。成功投影退休 checkpoint；semantic output 丢失必须 fresh 重跑。
- `D435-02`：`guru-publish-task-delivery` 使用 `push_content -> bind_pr -> converge_metadata -> mark_ready ->
  ready` Delivery-only transaction。每个 mutation 前 fresh reread，并先记录同计划 recovery 所需的最小
  owner-private state；terminal `ready` 可零 mutation 重物化 DTO。
- `D435-03`：`guru-merge-task-delivery` 在 current semantic gate 后展示一次 exact action plan，使用
  `gh pr merge --merge --match-head-commit --subject --body-file`。post-read 验证 exact message、parents、base
  与 reviewed head；已合并 terminal facts 支持零第二 merge recovery。
- `D435-04`：Planning artifacts分别表达 `task_scope`、`delivery_slice`、`remaining_work` 与
  `independent_delivery_conditions`。Check/Branch Review 对完整 candidate 做影响检查并只对 current slice做
  满足性判断；Task Commit只消费 fresh Check。普通 remaining-work 推进不创建替代 task。
- `D435-05`：merge body使用 closed versioned trailers：`Guru-Task-Identity`、`Guru-Delivery-Schema: 1`、
  `Guru-Delivery-Head`。Discovery 从 target base history 解析并与 repository/base/PR/commit/parents交叉验证；
  不使用 ledger、PR body、current branch、remote branch存活或 task creation branch/base作为 identity authority。
- `D435-06`：Publish transaction以单一 current schema覆盖 initial、strict-ancestor adoption、equal-head bind
  recovery、metadata convergence、Draft/Ready 与 terminal output loss。每次剩余 mutation前记录同计划恢复
  必需的最小 private state；旧 Finalizer transaction不被双读或转换。
- `D435-07`：Merge gate绑定 first live PR snapshot、expected head、pre-merge base、exact message/trailers与当前
  confirmation plan。Post-read验证 MERGED、exact message、ordered parents、base ref与Refs-only；terminal facts
  只恢复同一 `delivered` DTO，不执行第二次 merge。
- `D435-08`：Reconcile resolved-candidate profile绑定 HEAD、MERGE_HEAD、stage-0 tree、index digest、ordered
  parents、message、task/worktree/branch与fresh Phase 2。Executor只在 clean resolved Git state创建唯一 local
  merge commit，output loss只恢复同parents/tree/message commit，并继续完整 Branch Review。
- `D435-09`：canonical source包含三个新 package、现有 owner的最小合同变更、Reconcile扩展、workflow/spec/
  README、preset与tests；installer完整分发 Shared/Codex/Cursor/Claude projection。#435不改 production markers，
  #434独占原子激活；不新增 adapter、dual graph、squash/rebase fallback或Delivery ledger。

## #436 Post-Delivery Completion And Finish Design

- `D436-01`：Completion 使用 semantic owner authoring 和 closed projection；`completed` 才携带 fresh completion/Closure seed。
- `D436-02`：Closure 将 source disposition 与 provider mutation 分离；exact close transaction 只保存同一 repo/Issue/action 所需的 owner-private recovery。
- `D436-03`：Finish 使用 archive projection、bookkeeping publication、expected-head merge 三阶段 transaction；allowlist 只含 exact lifecycle paths，payload 禁止 closing keyword 与 Delivery trailer。
- `D436-04`：Cleanup result 绑定 current Finish receipt 与 exact resource set；executor 只删除已确认且无 active consumer 的 resources。
- `D436-05`：Reactivate 以 stable task id 与 archive Git facts选择 `reuse` 或 `create` workspace plan；恢复后删除旧 Finish receipts。
- `D436-06`：五个 packages 保持 active/deferred，installer 同步 canonical、installed、Shared/Codex/Cursor/Claude projections；production workflow markers 与旧 lifecycle edge 不变。
- `D436-07`：public I/O 按 exit 最小化并绑定唯一 consumer；provider snapshots、授权过程和 recovery internals 不进入 public DTO。
- `D436-08`：同月/跨月 rearchive 使用显式 final archive ref；历史 Completion/Closure/Finish 仅作历史事实，Reactivate 后必须 fresh 重跑。

当前 registry 为 31 packages / 136 exits / 101 commands；production workflow 保持 22 mandatory invokes /
98 exits。五个 lifecycle packages 保持 deferred，完整 Release matrix 保持 `unverified`。

## #443 Task Identity Session Binding Design

- `D443-01`：`guru-bind-task-session` 是 lifecycle-aware bind/rebind/switch/resume/manual-recovery 的唯一 semantic owner与deterministic writer/validator；official Trellis task/session store继续拥有底层 identity与persistence。
- `D443-02`：五个 public profiles与route discriminator形成闭集；AI Gate先判断合法route，runtime只验证schema、identity、freshness与确定性side effect。
- `D443-03`：resolver组合task.json、artifact locator、repository common dir、live branch/worktree/HEAD、base provenance、task/workspace mappings、session id与lifecycle generation；缺失或冲突统一zero-write blocked。
- `D443-04`：resume/rebind/switch/reactivate复用official active-task writer；manual recovery只在受控missing-mapping分支写既有payload shape，写后重新运行同一boundary validator。
- `D443-05`：base provenance只来自task metadata或既有mapping；generation与current route阻止旧binding、Finish/Cleanup receipt跨task或跨lifecycle复用。
- `D443-06`：五个成功exits与一个blocked exit各自拥有独立schema/example/consumer；public DTO不携带runtime binding identity、绝对路径、授权、semantic pass或private recovery。
- `D443-07`：package、registry、manifest与managed projections additive分发并保持deferred；#438拥有creation attach，#436拥有terminal lifecycle，#434独占global cutover。

当前 registry 为 32 packages / 142 exits / 102 commands；production workflow保持22 mandatory invokes /
98 exits。#443 的平台 evidence 只绑定其历史 candidate，不能替代 #452 的完整平台 inventory、selection、
ownership 或 native actual-load 验证。

## #452 All Platform Support Design

- `D452-01`：preset 保存一个 pinned `upstream_platforms` inventory，记录 source identity、inventory identity/digest，以及每个平台的 canonical `AITool` id、唯一 public `cliFlag`、template/root、native destination、entry form 和 projection descriptor。inventory 当前完整 cardinality 为 22，解析器不从文件夹存在性推导平台能力。
- `D452-02`：目标仓库 manifest/provenance 保存以 registry `cliFlag` 表示的排序、去重、非空 `selected_platforms`；每个值必须唯一映射回一个 `AITool` id。install、skill package、platform projection 与 ownership records 必须指向同一 exact selection；任何 section 缺失或不一致均 fail closed。
- `D452-03`：installer 只公开 repeated `--platform <cli-flag>`。显式 repeated flags 形成 exact subset，无 flag 才选择 `default_platforms=[claude,codex,cursor]`；parser 不声明 `--all-platforms`，manifest 与 JSON output 不记录 `all_platforms` 状态。
- `D452-04`：selection resolver 在所有文件 mutation 前完成 inventory binding、unknown/duplicate/empty 检查、projection descriptor 完整性检查与模式选择。参数冲突、inventory drift 或 projection 缺失返回确定性错误，并保持目标仓库零写入。
- `D452-05`：upgrade resolver 只从目标仓库 current installed manifest/provenance 读取 selection，验证各 manifest section 一致后，将 exact ordered set 投影为重复 `--platform` 参数。它不读取 source checkout dogfood 文件来替代目标 selection，也不把默认集合或完整 inventory 当作升级 fallback。
- `D452-06`：`guru-trellis` dogfood apply/reapply 显式传入 Claude、Codex、Cursor；drift checker 从 dogfood manifest 读取同一 selected set，只检查 shared assets 与这三个平台的 installed projection，同时独立验证 canonical inventory/ownership 的全平台完整性。
- `D452-07`：OpenCode descriptor 声明 `.opencode` native discovery、command/skill destination 与 actual-load adapter。OpenCode 与其它 21 个平台共享 inventory/selection/ownership 合同，但各平台按自身 native surface 投影，不要求同构目录或相同 overlay cardinality。
- `D452-08`：ownership inventory 由 shared managed paths、完整 canonical platform descriptors 和 target-selected installed paths 分层计算。reapply/update 复用 previous managed hash、`.new`/`.bak` 与 removal provenance；unknown local edits 保留并报告冲突，不静默覆盖。
- `D452-09`：public package projection 排除 package-private `tests/`，并校验 canonical、installed 与各 selected native surface 的 bytes、mode、manifest mapping 和 managed ownership。任一显式选择平台缺失 required projection 时安装失败，不允许 deferred success。
- `D452-10`：验证分层为 inventory/argument unit tests、exact-selection upgrade fixtures、canonical/installed/platform parity、ownership/reapply/update/drift、代表性 clean throwaway，以及 OpenCode representative native actual-load。production workflow 继续保持 #434 未激活；release/tag 与外部生产验证保留为未验证边界。

实施还必须遵守 touched non-generated code file 的 3000 行上限。当前接近阈值的 installer、compatibility matrix 与 installer test 主文件在增加 #452 行为前先做机械拆分或小型解耦，拆分本身保持行为等价并由现有测试覆盖。

上述条目定义 `.58` current Design authority，但不表示代码已实现或 `T452-01..12` 已执行。
历史三平台或四平台 evidence 只绑定其原 candidate，不能推导当前 upstream inventory 或目标仓库 selection。

## #454 Task Lifecycle State Model C2 + D0

- `D454-01`：`task-lifecycle-dtos.schema.json` 是 Draft 2020-12 单一 catalog，声明 35 个 named DTO；consumer 选择 exact `$defs/*DTO`，handoff receipt 使用 TaskId-stable control-ref primitive，cleanup 与 remaining-work 字段保持 closed enum。
- `D454-02`：`identity.py` 分离 TaskId、TaskRef 与 generation，扫描 active/archive canonical artifacts，拒绝 non-canonical locator、control-ref-invalid TaskId、exact/case-fold collision 与 invalid generation，并返回 immutable `TaskArtifactIdentity`。
- `D454-03`：`source.py` 只规范化 closed source union、portable repository ref、Git-valid branch ref 与 Delivery target；schema/runtime 使用同一值域，不接管 Closure disposition、branch association、checkout acquisition 或 Git mutation。
- `D454-04`：`schema.py` 从固定 sibling contract root 加载 regular schema，验证 Draft 2020-12 并拒绝 remote/parent `$ref`、nested `$id`、symlink escape 与 unknown DTO；`results.py` 只构造 minimal named DTO。
- `D454-05`：`LifecycleContractError` 提供稳定 code/field_path/remediation；runtime 不写 task/session/mapping，不导入 Fork private code，不修复 metadata，不选择 semantic route，也不持久化 validation result。
- `D454-06`：Fork source lock 固定到 reviewed commit `eb370008c7689d4e272ae626bd002190ecbb3296`、tree `bd1f133cc55d0562ad9ec5f426bca70d1584194b` 与 CI `35621578090`；canonical/preset durable SSOT 一致，C3-C7 与 #434 activation 不提前投影。
- `D454-07`：D0 由 Reconcile 拥有 pre/post-review integration，Task Commit 只输出 exact committed candidate，Branch Review 分别拥有 full 与 continuity profile。Pre-review compatible route 创建 parents 为 `[prior_task_head, new_base_head]` 的本地 merge commit；`post_check/post_commit` 回 fresh Phase 2，continuity 只允许已有 prior full review 并验证 new-base ancestry 与 candidate tree identity。

本节不新增 Skill、exit、registry selector、active manifest 或 production edge；C3-C7、D443、D436、E434 仍由后续 owner 承接。

## #454 Task Lifecycle State Model C3

- `D454-C3-01`：catalog 从 35 扩展为 39 个 named DTO；四个 checkout DTO 为 closed call-local projections，candidate/resolution 使用互斥 conditional shape，zero-candidate recovery 由 `selection_required` 表达。
- `D454-C3-02`：`git_facts.py` 从 `git worktree list --porcelain -z` 与当前 common-dir 派生 repository/worktree facts，不读取 mapping、历史 path 或 installed runtime state。
- `D454-C3-03`：`checkout_resolution.py` 统一验证 candidates、pre-task artifact/authority 和 explicit selection；authority conflict、invalid 或 multiple candidate 不得被降级为 usable。
- `D454-C3-04`：`checkout_acquisition.py` 只提供 adopt 与 provision，mutation 前后复用同一 validator；primary checkout provision 返回 adoption remediation。
- `D454-C3-05`：provision transaction 保存 call-local expected identity；rollback 只删除 transaction-created matching resources，output-loss recovery 不重复 mutation。
- `D454-C3-06`：shared identifier primitive 同时约束 schema/runtime；error shape 仅有 `code`、`field_path`、`remediation`。
- `D454-C3-07`：`guru-ensure-task-checkout` registry row 为 `state=planned`，canonical manifest 使用 `planned_skill_ids`；planned ID 不得有 package directory。
- `D454-C3-08`：active selector、workflow、active graph、installed copy 与平台 projection 保持不变；canonical/installed 暂时不同不是 compatibility layer。
- `D454-C3-09`：focused evidence 与 deferred suite/release evidence 分开；package `19/20`、preset `85/86` 不声明为通过，E434 后由对应 owner 重验。
- `D454-C3-10`：transaction-created linked worktree 的 `git_dir` 保存 closed `guru-checkout-acquisition-provenance.json`，payload复用 acquisition plan/result exact identity 与 ownership projection。
- `D454-C3-11`：recovery 对 created-worktree disposition要求 marker key set、value type、value 与 fresh result exact match；different/same-path replacement、missing/invalid/mismatched marker统一 fail closed。
- `D454-C3-12`：provision post-validation后写 marker；direct handoff先 retire再调用 consumer。marker write/remove或callback失败进入既有 bounded rollback，recovery不修改 marker或Git。

本节不新增 ADR；`ADR-015` 继续拥有 lifecycle identity 与 framework-extension boundary。C4-C7、D443、
D436、E434 与 production activation 保持后续 owner。

## #454 Task Lifecycle State Model C4

- `D454-C4-01`：`branch_store.py` 在 `<git-common-dir>/trellis/task-branches/<task-id>/<generation>.json` 读写 closed six-field TaskBranchBinding；binding epoch 是 repository-local application control identity，new epoch 从 revision 0 开始。
- `D454-C4-02`：C2 `TaskLifecycleKey` 与 `BranchBindingRefDTO` 复用同一 epoch/revision identity；durable branch name 为 bare portable ref，public DTO仍不携带 branch/path/HEAD。
- `D454-C4-03`：`branch_resolution.py` 只从 live registered worktree 与 local refs构建 candidate，先排除 retained lifecycle control refs，并通过 OwnershipPort读取 current epoch/revision/branch 与 unresolved refs。
- `D454-C4-04`：establishment 比较 binding/ownership 四象限；单侧存续时补齐缺失侧并保留 epoch/revision/branch，两侧均缺失时生成 new epoch/revision 0，异常按 exact snapshots 逆序恢复。
- `D454-C4-05`：checkout snapshot 绑定 HEAD、symbolic ref、真实 index bytes、Git-visible working-tree bytes、porcelain status 与 reviewed expected HEAD；candidate label/id 不进入 mutation/recovery freshness。
- `D454-C4-06`：same-checkout route 只执行 absent target ref 的 `git switch -c`；existing-target route 不迁移内容。两条 route 都先 fresh重建 expected-HEAD plan，再保持 epoch、递增 revision并使 binding/ownership post-state一致。
- `D454-C4-07`：same-checkout rollback 切回 source ref，并仅在 target仍指向 reviewed pre-state HEAD且未被checkout时删除本 transaction创建的ref；existing-target failure只恢复control state。
- `D454-C4-08`：output-loss recovery只读验证 exact successor、live checkout/artifact、epoch、expected HEAD、cleanliness与ancestry，不调用 mutation owner或增加revision。
- `D454-C4-09`：durable binding schema与两条 closed rebind checkpoint route分别建模；checkpoint是owner-private短生命周期activation input，不是public DTO或第二authority。
- `D454-C4-10`：registry/extension manifest只增加两个planned rows。Package absence、active graph absence与installed/platform absence由回归固定，完整package composition继续由E434交付。

`.62` C4 design source binding 还明确复用 `DES-046` 的 Finalizer recovery owner：无 predecessor transaction
时按真实 Git ancestry 接受 strict historical ancestor remote；executor 创建 replacement transaction 时保存 exact
`pre_push_remote_head`，随后的 pre-mutation preflight 必须重新读取并匹配该值。该组合不产生第二 ledger、public
DTO 或 production activation edge；执行级验证由 `TST-032/SCN-044` 承接。

`FIN454-C4-P1-002` 复用该 owner，补充 identity-matched transaction current ownership、同 branch/base terminal
PR 历史分类、`pre_push_remote_head` single-fast-forward、`publication_head` output-loss convergence 与
allowed-head/Open-PR/transaction-identity drift fail-close；不得引入宽泛 fallback、PR 人工选择 API、force push、
第二 ledger 或通过删除 transaction 恢复。

`FIN454-C4-P1-004` 仍由 `DES-046` 承接：classifier 在 predecessor review-to-Publication 为 equal 或合法
manifest-only tail、unchanged selected base 已属于 predecessor lineage、current review/Publication/live HEAD
相等且严格后继时，允许同一 unbound transaction 进入既有 reprepare route。它只检查 Open PR，不把 terminal PR
inventory 当作 current candidate；preflight 只接受 exact `pre_push_remote_head` 或 `publication_head`。中间 review
endpoint、archive、identity、ancestry 或 tail drift 均在 mutation 前停止。

本 C4 历史 slice 不新增 ADR；`ADR-015` 继续拥有 lifecycle identity 与 framework-extension boundary。

## #454 C5 Session And Resource Control

- `D454-C5-01`：`session_adapter.py` 验证 TaskLifecycleDTO 并委托 official schema-2 session primitive 读写、解析；不复制 store 或 TaskId-to-TaskRef resolver。
- `D454-C5-02`：context key 是调用能力；缺失时显式 task mode 不写记录，write error 独立返回而不回滚 lifecycle result。
- `D454-C5-03`：`resource_ledger.py` 以 common-dir TaskId/generation key 保留完整 incarnation/role/revision；active lost-output 识别 exact whole-ledger successor，remote lost-output 仅核验 current incarnation，不使用 ledger-wide token。
- `D454-C5-04`：唯一 ledger 提供 C4 `OwnershipPort` current/snapshot/restore/establish/rebind/unresolved-ref，写前验证 revision/epoch/branch，写后 fresh 投影。
- `D454-C5-05`：active missing 按 current binding 与 pre-existing live resources 保守恢复 caller-owned；terminal missing 只返回 manual-selection resolution。
- `D454-C5-06`：rebind 保留 retired resource 与 cleanup responsibility，target 建新 current incarnation；未收敛同 ref 拒绝复用。
- `D454-C5-07`：Finish 接收 exact head seal 全部责任清单；Cleanup resolution 区分普通、人工选择与 already-clean，不保存用户选择或授权。
- `D454-C5-08`：remote portable name/repository/ref 精确匹配；同 incarnation 正常 HEAD 只按 ancestry 前进、equal 只读，rebind seal 最新 HEAD；普通 Cleanup 排除 retained control refs 与 caller-owned。
- `D454-C5-09`：三个 closed schema 分别约束 ledger、Finish seal input 与 Cleanup resolution；official session schema 仍单写，不新增 transaction store。
- `D454-C5-10`：registry 仅增加 planned row，完整 package/graph/installed/platform activation 由 E434 独占。

`ADR-015` 继续负责 identity 与 extension boundary；C6-C7、D443、D436、E434 与 #434 activation 均未完成。（此段是 `.63` C5 历史边界。）

## #454 C6/C7 Nonactivated Creation Composition

`D454-C6C7-01..08` 从 [reviewed design contribution](../../../requirements-design-test-contributions/454-task-lifecycle-state-model-c6-c7/design.md)
进入 `.64` current。C6 shared `composition.py` 连接 reviewed source/target、C3 acquisition、C4 binding、
C5 ledger/session 与 Fixed Fork task primitive，但不复制 framework store 或建立 planned Skill package。
`new_branch`、`existing_branch`、`existing_checkout` 与 adopt primary/linked 五类 resource 逐项标明 caller/Guru
ownership；binding/ledger revision 与 TaskId/generation 对齐，creation result loss 只读恢复。

Activation input schema 明确 selected base ref 与 base-current reviewed base HEAD 或 reconciled new base HEAD；
shared input preparation fresh 读取 task planning status、current binding/ledger 和 live Git ref/ancestry，
不自行批准 Planning 或执行 status mutation。六个 planned IDs 不携带 package/interface/route/I/O；E434 才交付
完整 semantic gate、typed exits、consumer closure 和原子 production graph activation。C7 的零新 mapping/path
reader/writer 只约束 Phase C substrate，旧生产前驱与历史字段直到 E434 才退役。

## #454 D443 Bind package target design

`D454-D443-01..04` 由 [reviewed contribution](../../../requirements-design-test-contributions/454-task-lifecycle-d443/design.md)
进入 `.65` current。Bind runtime 用 Phase C `TaskLifecycleKey`、C4 branch/ownership、C3 live checkout
validator 先选唯一 current checkout，再由 Fixed Fork task identity resolver 仅检查该 checkout 验证目标
lifecycle；保留的旧 branch checkout 不参与 current 解析。随后仅经 C5 official session adapter
读写 schema-2 pointer。Resume 验证当前 exact pointer；switch 验证源和目标；Reactivate 只替换同 TaskId
的旧 generation；manual recovery 仅恢复缺失的官方 pointer，不创建第二 store 或旧 mapping。
同一目标幂等，stale/conflict 在写入前以 ReasonDTO 阻塞。无 context key 时交付 `explicit_task_mode`。

历史 `D443-01..07` 保留为 #443 前驱合同，不覆盖本节的目标实现。D443 只修改 canonical package
及其 source 模板；consumer 的 TaskRef fresh 派生、完整路由接线和 installed/platform 一致性由 E434 拥有。
`ADR-015` 已拥有 lifecycle identity 和 extension boundary，本增量不产生新 ADR。

## #454 D436 terminal lifecycle package target design

`D454-D436-01..06` 由 [reviewed contribution](../../../requirements-design-test-contributions/454-task-lifecycle-d436/design.md)
进入 `.66` current。Completion 的 semantic review 与 deterministic validation 分离，七个出口分别投影
ResultRefDTO 或 TaskArtifactDTO + ReasonDTO。Closure 冻结 Completion/source/scope/target/binding/evidence
与 action set，在同一 transaction 中收敛 provider result；external change 返回 Closure review，不以
provider snapshot 冒充公共 handoff。

Finish 以当前 Closure result 和 required-closed Issue reread 为前置，完成 lifecycle-only bookkeeping PR、
expected-head merge、archive post-state，再将 PR head 写入 terminal resource seal 的 cleanup-head，
目标 merge SHA 仅验证 archive；封存后退役本 generation 的 branch binding。Cleanup normal profile
只读 seal/ledger，manual 和 machine-handoff 分别选择、复验、执行其自身目标；缺失/旧代 ownership
不能自动删除。Reactivate 复用 C3 acquisition、C4 binding、C5 ledger 与 D443 session，为 `g+1`
建立新控制态，历史结果保持历史。

这五个 package 只提升 canonical source；#434/E434 才拥有 workflow router、selector、manifest、
installed/platform 原子投影。历史 `D436-*` 是 predecessor，不作为 `.66` runtime authority。
