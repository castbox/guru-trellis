# Guru Team Trellis Extension 当前设计

版本：`current-main-0.6.5-guru.41`；状态：`active`；provenance：`code_recovered` + #311 reviewed Architecture/RDT promotion，绑定 task head `651defee…` + #311 serialized promotion delta。精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD。

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
- `DES-019` Platform script boundary：`preview-change-context-history.sh` 是 package-private validator wrapper；platform public projection只发布 `scripts/invoke.sh`，matrix显式证明 private wrapper 未泄漏。
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

- `CON-001`：21 个 active Skill 以 registry/interface 为 public graph，typed exit 必须有唯一 consumer 或 fail-closed stop。
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

## Capability owner map

| Capability | Skill / route | External exits |
| --- | --- | --- |
| mode | `guru-select-workflow-mode` | `standard_intake`, `task_free`, `blocked` |
| base/context | `guru-sync-base`, `guru-discover-change-context` | `synced/skipped/blocked`; `context_ready/refresh_base/blocked` |
| clarification/wording/readiness | `guru-clarify-requirements`, `guru-review-contract-wording`, `guru-review-change-request` | interface-defined closed exits |
| workspace/planning | `guru-create-task-workspace`, `guru-approve-task-plan` | `created/refresh_review/blocked`; `approved/revision_required/clarify_scope/blocked` |
| normal-path qualification | `guru-qualify-normal-scenario` | `classified/scope_confirmation_required/mechanism_revision_required/blocked` |
| task-free | `guru-execute-task-free-change` | 7 closed exits incl. `completed`/`blocked` |
| execute/check/commit | `guru-check-task`, `guru-create-task-commit` | check 4 exits；commit 3 exits |
| base evolution | `guru-reconcile-task-base` | 6 exits incl. continuity/implementation/planning routes |
| review/publication | `guru-review-branch`, `guru-review-task-publication` | review 5 exits；publication 3 exits |
| finish/merge | `guru-finalize-task`, `guru-merge-task-pr` | finalizer 6 exits；merge 3 exits |
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
