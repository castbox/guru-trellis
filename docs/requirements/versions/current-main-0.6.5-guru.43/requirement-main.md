# Guru Team Trellis Extension 当前需求

版本：`current-main-0.6.5-guru.43`；状态：`superseded`；successor：`current-main-0.6.5-guru.44`；基线：contribution identity `architecture-contribution-335-repository-private-release-orchestration-v1`，继承 `.42` authority；#305 已确认的 `EVO-001..007` 保持独立 target authority。精确 revision 由包含本 authority 的 Git object/tree identity 绑定，正文不记录可变 HEAD 或 lifecycle 状态。

## 目标、角色与适用范围

- `REQ-001`：为采用 Trellis 的仓库提供 AI-first、Issue/task 可追踪、可审查且可恢复的完整开发生命周期。维护者、任务执行 Agent、reviewer 和发布操作者是主要角色。`source_confirmed`：Issue #266；`code_recovered`：workflow/registry。
- `REQ-002`：官方 Trellis workflow/spec marketplace 是上游扩展面；Guru Team 通过 Markdown workflow、step-local Skill、preset/overlay 与 companion runtime 扩展，不修改上游源码、全局 npm 或 `node_modules`。`source_confirmed`：仓库 AGENTS.md；`code_recovered`：canonical layout。
- `REQ-003`：全局 workflow 只拥有 phase 顺序、mandatory invocation、typed exit consumer 和 fail-closed stop；每个 Skill 独占内部 closed loop。`code_recovered`：`trellis/workflows/guru-team/workflow.md` 与 21 个 active interfaces。
- `REQ-004`：AI 负责 scope、充分性、finding、route 与发布判断；Python/shell 仅执行或校验确定性事实。只有真实选择或副作用才交互，授权不持久化。`source_confirmed`：仓库合同。
- `REQ-005`：Task、workspace、branch、history、archive、semantic naming 与 base/provider recovery 必须保持明确 ownership，且普通 mapped exit/recovery 不制造人类 handoff 文书。`code_recovered`：相关 active Skills。
- `REQ-006`：canonical、installed dogfood、Shared/Codex/Claude/Cursor 投影和 preset managed assets 必须保持同一 versioned contract；未知修改遵守 `.new/.bak` 语义。`code_recovered`：manifest、overlay、installer。
- `REQ-007`：Requirements/Design/Test 与 Architecture Baseline 是 repository authority；task 变更先做 impact/contribution，再 promotion，普通并行 task 不直接竞争 shared current 文件。`source_confirmed`：#263/#264/#265；`code_recovered`：三项 package。
- `REQ-008`：公共 Skill id、exit id、schema id、workflow id、preset path 与 command 是兼容 API，不能无迁移静默破坏。`source_confirmed`：仓库合同。
- `REQ-009`：安装、升级、release 结论必须由其责任 Issue 的 exact evidence 支持，skipped/static/package 证据不能冒充外部或 release proof。`source_confirmed`：Validation Scope Ownership。
- `REQ-010`：只处理 honest-but-fallible 正常路径；恶意伪造、对抗输入、未要求的锁/TOCTOU/竞态加固不属于当前产品范围。`source_confirmed`：仓库 AGENTS.md。
- `REQ-011`：task index/history query 必须能从 current task、archive 与 `finish-summary.json`
  找到任务最终结果；archive、acceptance、Finish 与 cleanup 只处理 exact task/resource，不覆盖
  其它并行任务。`code_recovered`：task scripts、Finalizer、Merge 与 finish contracts。
- `REQ-012`：task/branch/worktree 使用绑定 Issue 与语义动作的名称；base evolution、GitHub provider
  failure 与 partial recovery 返回唯一 owning route，不从 Phase 0 重建已存在的 task。
  `code_recovered`：workspace、reconcile、publication/finalization packages。
- `REQ-013`：install/update/upgrade/reapply 必须保持 Skill API、interface/schema/command、
  distribution、managed/installed path、executable mode、声明平台入口、template hash、sidecar
  与 extension identity/version binding 一致；任一不一致或未处理 `.new/.bak` 必须作为独立
  consistency/installation blocker 阻塞成功声明，但其变化本身不构成 capability loss。
  `source_confirmed`：preset/upgrade contracts；`code_recovered`：installer 与 validators。
- `REQ-014`：Finalizer 完成 archive、Ready PR 与 terminal cleanup 后，public wrapper 只可从已归档 durable summary、精确 retired owner locator 与当前 Git/GitHub ready facts 重建 terminal authority；缺 locator、archive/head/PR/scope 漂移或未退休 owner state 必须 fail closed。`source_confirmed`：Issue #275；`code_recovered`：Finalizer owner/runtime。
- `REQ-015`：Throwaway verifier 的 active package、command 与 complete-package inventory 必须从 canonical registry/interface validation 派生；不得维护随新增 Skill 漂移的固定数量。`source_confirmed`：Issue #275；`code_recovered`：verifier inventory projection。
- `REQ-016`：专项 compatibility owner 必须从 live manifest、ownership、overlay 与 registry 交叉派生声明平台，并对每个平台分别执行 clean official Trellis `0.6.15` 与 existing official `0.6.5 -> 0.6.15` 隔离 cell。`source_confirmed`：Issue #260；`verified`：六个 cell 全部通过。
- `REQ-017`：existing cell 的 Guru before-state 必须是 immutable `v0.6.5-guru.10` / extension `0.6.5-guru.36`，并按 official upgrade、update dry-run、条件式 migrate、workflow preview/switch 与 preset reapply 顺序执行。`verified`：三个 existing cell。
- `REQ-018`：升级前后的 capability-loss comparison 只比较 `workflow`、`task_data` 与
  `docs_authority`，三组均不得出现未审查能力丢失；Skill API/schema/command projection、
  distribution 与 installed inventory 继续由 `REQ-013` 的独立 consistency/installation gate
  阻塞。`verified`：三组 capability projection 保持。
- `REQ-019`：#263 RDT、#264 Architecture、#265 Bootstrap installed profiles 与 #266 双 SSOT/Architecture authority 必须在升级后保持；`.trellis/spec` 仍是最小 locator/index projection。`verified`：每个 cell 的 installed eval 与 docs projection check。
- `REQ-020`：同一 clean base 的两个业务 task 必须保持 workspace/provider/archive/Finish/cleanup ownership 隔离；B 的 `none` route 不调用 GitHub，A 的真实 `github_pr` route 必须使用单独确认的 disposable repository，并在 cleanup 前后证明 required commit reachability。`verified`：local A/B matrix 与真实 GitHub A route。
- `REQ-027`：Architecture Baseline 是标准 task 从 Planning、qualified implementation discovery、Phase 2、Branch Review、Publication 到 Acceptance/Finish 的唯一项目架构 SSOT；schema/runtime 只支撑 lifecycle，不成为架构判断 owner。
- `REQ-028`：每个标准 task 必须进入 Architecture semantic owner，并在 task-local contract 同时绑定 Guru Team 方法论 identity 与项目 Architecture Baseline/change-contract identity；任一缺失、过期、冲突或材料边界扩大均 fail closed/re-entry。
- `REQ-029`：项目 Architecture Baseline 必须唯一声明 current 设计宪法 locator 及 version/content identity。Guru Team 只消费 `mature-practice-applicability`、`concept-semantic-completeness`、`cohesion-change-isolation`、`minimum-necessary-complexity`、`debt-one-way-convergence` 五个 identity/short name，不拥有原则正文、解释、评分或逐项 verdict。
- `REQ-030`：`architecture_impact` 必须恰好选择 `target_native`、`legacy_boundary_convergence` 或 `dedicated_refactor_slice`；`no_architecture_impact` 是独立快速结果。#283 采用 `target_native`，不新增 legacy authority、dual-read 或 migration adapter。
- `REQ-031`：Architecture change contract 必须完整绑定 requirement/behavior authority、baseline/constitution、domain/integration/decision/GAP、required concerns、current/target owner、single-writer、compatibility exit、parallel scope、deviation/deletion conditions、design responsibility、before/after、project checks、evidence、contribution/ADR/review/promotion 与 expected current identity。
- `REQ-032`：Phase 2 首次判断 candidate before/after，Branch Review 从 exact committed full diff 独立重算。项目检查结果绑定 current descriptor identity、applicability、rule/decision/GAP refs、`pass|fail|unverified`、evidence/unavailable reason 与 freshness；AI 根据真实依赖判断 blocking，新增或恶化偏移返回 `fitness_regression`。
- `REQ-033`：普通 task 只写自己的 RDT/Architecture contribution；仅当 decision、原则权衡/例外、GAP lifecycle、owner/single-writer 或 compatibility exit 改变时创建 ADR candidate。shared current 由唯一 Architecture owner 在 independent review 后按 expected current identity 串行 promotion。
- `REQ-034`：并行 task 使用不同 contribution locator，不得 review 前写 shared current、竞争同一 GAP/owner、形成双写或两个 current authority。任一 promotion 推进 current 后，旧 identity task 必须 `sync_required` 并重做 impact、satisfaction 与 parallel-scope 判断。
- `REQ-035`：Architecture 2.0 schema/runtime、canonical/dogfood/installed/platform projection 与项目中立十场景必须原子承接上述 lifecycle，stable Skill/profile/exit ids 不变；外部 evidence 不可得时保持 `evidence_gap|unverified`。#267 Release matrix/tag/Release/immutable smoke 与 post-release business-repository proof 不属于 #283，必须由各自 live owner 和 exact evidence 晋升。
- `REQ-036`：base selection 必须固定按 explicit、config scalar、ordered exact local/remote refs、remote default 执行；current branch 与 worktree availability 不参与 selection，selected base 缺 checkout 时不得回退低优先级 candidate。
- `REQ-037`：selected base 确定后只绑定同一 Git common-dir 中 registered、exact `refs/heads/<selected_base>`、clean 且 branch/HEAD/ref identity 一致的唯一 authority checkout。
- `REQ-038`：Codex session checkout 允许 detached 且只作为 invocation shell；fetch、可选 `merge --ff-only`、checker equality 与 public repository locator 只使用 authority checkout。
- `REQ-039`：authority missing、ambiguous、dirty 或 identity mismatch 必须稳定 `blocked`；不得 checkout、switch、创建 branch/worktree、reset、rebase、stash、force update 或重选 base。
- `REQ-040`：invocation checkout 自身已绑定 selected base 时保持成功路径；behind authority 只允许 explicit remote-tracking refspec fetch 与 `merge --ff-only`。
- `REQ-041`：`guru-base-sync-result-1.0`、Interface 1.4、public `synced|skipped|blocked` schemas、typed exits 与 transition shape 保持兼容，既有 locator 字段指向真实 authority checkout。
- `REQ-042`：`guru-create-task-workspace` 必须按 producer provenance source 对 explicit、config、config-candidate、remote-default 的 current source、selected base 与完整 candidates exact revalidate，且不得导入 producer private runtime。
- `REQ-043`：canonical、dogfood、installed 与 Shared/Codex/Claude/Cursor projection、preset reapply/drift/mode 和 sidecar-zero 必须一致；代表性 installed detached wrapper 只证明 #290 normal path。#267 的 `.3/.39/CLI 0.6.15` release matrix、tag 与 Release 必须在最终 exact candidate 上 fresh 执行，不能继承历史 task 或 package evidence。

## 生命周期行为

| Behavior | 必需行为 | 当前 owner |
| --- | --- | --- |
| `BEH-001` Intake | mode selection 后，标准路径依序完成 base sync、context、clarification、wording、readiness、workspace | global workflow + Phase 0 Skills |
| `BEH-002` Planning | 三份 task planning、semantic approval 与一次 current plan review pause | `guru-approve-task-plan` |
| `BEH-003` Execute | worktree boundary、approved scope implementation、完整 Phase 2 semantic check | `guru-check-task` |
| `BEH-004` Review | exact commit、完整 branch range review、finding closure 与 fresh final review | commit/review Skills |
| `BEH-005` Publish | PR readiness、deterministic finalization、expected-head merge、Issue closure verification | publication/finalize/merge Skills |
| `BEH-006` Recovery | base evolution、provider recovery、stale/re-entry 保留唯一 mapped consumer，fail closed | reconcile 与 owning Skill |
| `BEH-007` SSOT | RDT、Architecture、Bootstrap 维护 version/status/freshness；Architecture 全阶段消费 current constitution/change contract，并通过 reviewed promotion 单向收敛 | RDT/Architecture/Bootstrap semantic owners |
| `BEH-008` History/Finish | acceptance 后产生唯一 archive/finish result，index/history 可查询并保护 exact retained refs | Finalizer/Merge/task history owners |
| `BEH-009` Distribution | marketplace install、official update/upgrade、workflow selection、preset reapply、sidecar/drift validation 按序执行 | marketplace/preset/verification owners |
| `BEH-010` Terminal projection | Finalizer terminal cleanup 后从 archive/live ready authority 投影 `ready_for_merge`，真实 stale 继续拒绝 | `guru-finalize-task` |
| `BEH-011` Compatibility matrix | live-derived platform × clean/existing matrix、capability equality、installed contracts、A/B Finish 与真实 provider proof | #260 compatibility verifier；不是新的 public owner |

## 当前发布范围

`source_confirmed`：最新已发布 stable release 是 annotated tag `v0.6.15-guru.2`，tag object `641ed35e91c4a58cc7083ab2e4811d30e392fbed`，peeled commit `d907fcc5e17f23b6499648e5e9a208457f2d6f8b`，extension revision `0.6.15-guru.38`，目标 Trellis CLI `0.6.15`。当前 source candidate 为 extension `0.6.15-guru.39` / Trellis `0.6.15`；#267 successor target 固定为 `v0.6.15-guru.3`。该 tag、GitHub Release、tag-pinned smoke 与 latest-stable identity 在 exact candidate 发布前仍为 `unverified`。

## 非目标

历史 #267 authority 中的 `.42` 是 knowledge identity，不是 extension/release revision。当前 `.43` authority 继承该 release identity separation，不把 extension `.39` 或目标 tag `.3` 称为已发布 stable release，不替代 #267 exact-candidate gates 或 #311 post-release business proof，也不把业务仓库私有 PRD、完整日志、临时 hash bundle或用户授权写入 current intent。

## #295 current promotion additions

- `REQ-044`：Sync public `base_current` 是进入 mandatory Discovery 的唯一 public transition；Discovery active input 2.0 与 owner-result 3.0 不得依赖或重建 Sync-private result/digest。
- `REQ-045`：Discovery 独占 live `base_observation`，正常 current/refresh/blocked 路由和 managed runtime dependency contract 必须由 public wrapper 与声明的 Python resolver 验证。
- `REQ-046`：canonical、dogfood、installed、Shared/Codex/Claude/Cursor、preset/reapply/update/drift、sidecar、interfaces/schemas/examples/tests/evals 作为同一 #295 active unit 收敛；验证范围仅为 accepted targeted checks 与一个代表性 clean throwaway。

## #311 installed Finalizer provenance promotion

- `REQ-047`：Finalizer provenance reprepare 必须建立互相独立的
  `target_reviewed_checkout` 与 `extension_source_checkout`。前者独占业务 repository
  mutation、metadata-tail lineage 与 commit；后者只提供 canonical preset bytes。closed
  `self_hosted|installed` mode 分别绑定 target reviewed HEAD 或 target manifest 中 immutable
  extension `repo/ref/commit`，不得 fallback、dual-read 或把 business HEAD 写成 extension source。
- `REQ-048`：首次 `publication_ready` preview 必须先分类 exact existing PR；无 PR、无 remote
  branch 且缺 metadata tail 时，`prepared` 返回
  `reprepare_required/provenance_metadata_tail`。对应 executor preflight 只接受 absent remote 或
  exact reviewed head；push、PR、archive、Ready 与 Issue mutation 在合法 tail 前均为零，既有
  fresh/post-bind recovery 与 public profile/exit/transaction 合同保持。
- `REQ-049`：source binding、两棵临时 checkout 与 tail producer 归
  `guru-finalize-task` package-local runtime；installer 独占 manifest source provenance。
  source resolution、fetch、checkout、apply 或 postimage validation 失败时在任何远端副作用前
  fail closed。Finalizer 不调用或读取 verifier lifecycle、gate、artifact、owner state 或 exit。
- `REQ-050`：canonical、dogfood installed、Shared/Codex/Claude/Cursor package bytes、mode、
  contract、preset reapply、drift 与 recursive sidecar 必须一致；installed package test 从当前
  package/shared installed runtime 解析依赖，不要求 business target 携带 canonical source tree。
  本 Issue 的验证范围包含 focused runtime、installed no-source-tree 与一个代表性 business
  closeout，不吸收独立 Release owner 的完整矩阵、tag 或 GitHub Release。
- `REQ-051`：standalone extension verification 必须在 temporary workspace cleanup 前保留
  schema-valid 的 failure stage、适用 matrix cell、稳定 command label、exit code 与 bounded
  credential-safe error tail，并保留既有 stdout/stderr hash/size。matrix 外 command、asset
  inventory、ownership、sidecar 或 capability failure 收敛为 `postcheck_failure`；failed execution
  不得保留 null failure。该 evidence 只属于 verifier，Finalizer 零消费。

## 历史 #267 release authority alignment

- `REQ-052`：#267 的 `.41 -> .42` authority alignment 合同要求
  `current-main-0.6.5-guru.42` 成为当时唯一 active Requirements/Design/Test 与 Architecture
  knowledge authority，`.41` 成为 superseded predecessor；该历史合同固定 source candidate 为
  extension `0.6.15-guru.39`、Trellis CLI `0.6.15`，Release target 为 `v0.6.15-guru.3`。当前 active
  authority 已由 successor `.43` 承接。
- `REQ-053`：#267 历史合同要求 full-diff review、exact-candidate matrix、annotated tag、GitHub Release
  与 tag-pinned smoke 分别由 live evidence 晋升；promotion 或 package PASS 不得冒充已发布结果。
- `REQ-054`：#267 的历史 `.41 -> .42` delta 只更新 release/current facts、navigation、
  traceability、evidence 与 predecessor/successor binding；产品行为、Skill public API、Architecture
  decision、owner、single-writer、GAP lifecycle 与 compatibility exit 保持不变，且不创建 ADR。
- `REQ-055`：#267 历史合同要求 RDT 与 Architecture reviewed contributions 按 expected `.41`
  串行 promotion；promotion-created diff 重新执行 Phase 2、task commit 与独立 committed full-diff
  Branch Review，通过前 Publication 和 Release preparation fail closed。

## #335 repository-private release orchestration

- `REQ-056`：正式发布入口的 Skill ID 固定为 `release-guru-trellis-version`，只存在于本仓库
  Shared/Codex/Claude/Cursor project-local discovery roots；公共 Skill package、marketplace、preset、
  overlay、registry、extension manifest 和业务仓库 installed projection 均不得包含它。
- `REQ-057`：每次 invocation 必须从当前请求取得 repository、current release Issue、目标 repo tag、
  目标 extension revision、official Trellis CLI version 与 predecessor tag，并 fresh 读取 live Issue、
  Git/GitHub、version surfaces 和现有 lifecycle owner contracts。preparation merge 后必须从 fresh
  `origin/main` 冻结 lineage 可证明的 exact candidate；旧 preparation identity 与 evidence 不可复用。
- `REQ-058`：preparation 阶段必须复用 standard intake、Phase 2、Task Commit、一次完整 Branch Review、
  Publication、Finalizer 与 Merge owners；本 Skill 不复制、替代、缩短或削弱这些 owner 的判断、typed
  route、freshness、confirmation 或 fail-closed 合同。
- `REQ-059`：PR title/body 由 Publication 根据 live Issue、完整 diff、验证结果与当前 candidate 即时
  生成并审查；GitHub Release title/body 在 Release 动作前按 post-merge exact candidate 即时生成并
  审查。两类 payload 只交给各自唯一 consumer，不建立 task-local handoff。
- `REQ-060`：owner-private lifecycle checkpoint 只按既有 owner 合同短期存在并退休；正常 lifecycle
  metadata 不改变 reviewed-content identity，不产生 release-status metadata commit 或第二次内容 Review。
  Skill、source、durable docs、配置、schema、script 或 test bytes 变化必须使受影响的
  Phase 2、Branch Review、Publication、Finalizer 或 exact-candidate gate stale，并返回对应 owner
  重新验证。
- `REQ-061`：stale、cross-SHA、lineage 不可证明、live identity mismatch、FAIL、SKIP、unknown、
  multiple 或 unmapped exit 必须停止在当前 owner；不得用 metadata commit 建立恢复点或继续发布动作。
- `REQ-062`：post-merge minimum gate 保留 predecessor-to-candidate full diff、版本映射、source/
  installed validators、四平台 parity、install/update/reapply、secret scan、residue check 与 tag-pinned
  smoke；本仓库私有编排不扩张为完整累计多平台 Release Gate 矩阵。merge、annotated tag、
  tag-pinned smoke、GitHub Release、Issue closure 与 cleanup 是独立 transaction，每项动作前取得
  不可复用、不可持久化的当前对话确认。

- `BEH-012` Repository Release Orchestration：从 preparation owner composition，经唯一完整 Branch
  Review、Publication、Finalizer 与 merge，到 post-merge exact candidate、scoped validation 和独立
  release actions；任一 stale/mismatch/failure 返回当前 owning boundary。
