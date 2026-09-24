# Guru Team Trellis Extension 当前需求

当前 .62 来源：`castbox/Trellis@eb370008c7689d4e272ae626bd002190ecbb3296` / CI `35621578090` / CLI/core `0.6.17`；Guru manifest `0.6.17-guru.42`；repository release target `v0.6.17-guru.1`。Architecture public inheritance：`docs/architecture/README.md` / `current-main-0.6.17-guru.62` / `active`。
完整继承 immutable `.61` 业务合同，当前增量为 #454 C4 branch association/establishment/rebind substrate 与同范围 bounded Finalizer provenance recovery guard；旧 pin、release mapping、计数及 promotion/evidence 叙述只绑定其明确历史版本。当前 registry 保持 32 packages / 142 exits / 102 commands并增加三个 planned IDs，production workflow 保持 22 mandatory invokes / 98 exits。

`.62` 完整继承 `.61`，吸收 reviewed #454 C4 contribution；RDT 与 Architecture current 均前进到 `.62/active`。本次只提升已验证的 branch association/establishment/rebind delta；promotion-created diff 必须重新通过 fresh Phase 2、Task Commit、完整 Branch Review后才能进入 Publication，C5-C7、D443、D436、E434、Release 与生产验证仍未完成。

版本：`current-main-0.6.17-guru.62`；状态：`active`；predecessor：`current-main-0.6.17-guru.61`；source baseline：reviewed #454 C4 contribution + inherited immutable `.61` authority；精确 revision 由 containing Git object/tree identity 绑定。

## 目标、角色与适用范围

- `REQ-001`：为采用 Trellis 的仓库提供 AI-first、Issue/task 可追踪、可审查且可恢复的完整开发生命周期。维护者、任务执行 Agent、reviewer 和发布操作者是主要角色。`source_confirmed`：Issue #266；`code_recovered`：workflow/registry。
- `REQ-002`：官方 Trellis workflow/spec marketplace 是上游扩展面；Guru Team 通过 Markdown workflow、step-local Skill、preset/overlay 与 companion runtime 扩展，不修改上游源码、全局 npm 或 `node_modules`。`source_confirmed`：仓库 AGENTS.md；`code_recovered`：canonical layout。
- `REQ-003`：全局 workflow 只拥有 phase 顺序、mandatory invocation、typed exit consumer 和 fail-closed stop；每个 Skill 独占内部 closed loop。`code_recovered`：`trellis/workflows/guru-team/workflow.md` 与 23 个 active interfaces。
- `REQ-004`：AI 负责 scope、充分性、finding、route 与发布判断；Python/shell 仅执行或校验确定性事实。只有真实选择或副作用才交互，授权不持久化。`source_confirmed`：仓库合同。
- `REQ-005`：Task、workspace、branch、history、archive、semantic naming 与 base/provider recovery 必须保持明确 ownership，且普通 mapped exit/recovery 不制造人类 handoff 文书。`code_recovered`：相关 active Skills。
- `REQ-006`：canonical shared package、pinned upstream inventory 的全部平台投影、目标仓库 exact installed selection 与 preset managed assets 必须保持同一 versioned contract；dogfood 只验证其 manifest/provenance 声明的 exact selection，未知修改遵守 `.new/.bak` 语义。`code_recovered`：manifest、overlay、installer；平台集合解释由 `R452-01..10` 收敛。
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
| `BEH-014` Mechanism qualification | 已资格化场景采用的机制必须由独立 semantic owner 判断，禁止 OS primitive 承接业务 authority | `guru-qualify-solution-mechanism` |
| `BEH-015` Archived-task Phase 2 recovery | Merge 只对 current-scope task-work finding 投影恢复 DTO，原 task 身份恢复后强制重跑 Phase 2 至 Merge | `guru-merge-task-pr` + `guru-restore-archived-task` |

## 历史 #332 发布范围

`source_confirmed`：最新已发布 stable release 是 annotated tag `v0.6.15-guru.4`，peeled commit
`40f8aa8312bfd9650f47e1fa9d6d21b4ff18d5b6`，extension revision `0.6.15-guru.39`，目标 Trellis CLI
`0.6.15`。当时 #332 source candidate 为 extension `0.6.15-guru.40` / Trellis `0.6.15`，successor
Release target 固定为 `v0.6.15-guru.5`。`.5` annotated tag、GitHub Release、tag-pinned smoke、latest-stable
identity 与 Issue closeout 在同一 post-merge exact candidate 上完成前均为 `unverified`。

## 非目标

历史 #267 authority 中的 `.42` 是 knowledge identity，不是 extension/release revision。当前 `.44` authority 经 `.43` predecessor 继承该 release identity separation，不把 extension `.39` 或目标 tag `.3` 称为已发布 stable release，不替代 #267 exact-candidate gates 或 #311 post-release business proof，也不把业务仓库私有 PRD、完整日志、临时 hash bundle或用户授权写入 current intent。

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
  `reprepare_required/provenance_metadata_tail`。无 predecessor transaction 的对应 executor preflight 接受
  absent remote、exact reviewed head 或 reviewed head 的 strict historical ancestor；remote ahead、diverged 或
  commit identity/ancestry unknown/unprovable 时 fail closed。已有 predecessor transaction 仍要求 exact old
  Publication HEAD。Reactivate branch reuse 已有合法 provenance tail 与身份匹配的
  `ordinary_publication/push_content` transaction 时，该 transaction 是 current owner；没有 Open PR 时，同
  branch/base terminal PR 仅为历史事实，不是 current candidate。live remote 等于 transaction
  `pre_push_remote_head` 时允许一次到 `publication_head` 的 fast-forward；等于 `publication_head` 时作为合法
  push-output-loss/converged state 接续同一 transaction。remote 位于这两个 allowed heads 之外、
  ahead/diverged/unknown/unprovable，出现 Open PR drift 或 transaction identity drift 时均 fail closed。不得新增
  宽泛 fallback、PR 人工选择 API、force push 或第二 ledger，也不得删除或改写 transaction。push、PR、archive、
  Ready 与 Issue mutation 在合法 tail 前均为零，既有 fresh/post-bind recovery 与 public
  profile/exit/transaction 合同保持。
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
  extension `0.6.15-guru.39`、Trellis CLI `0.6.15`，Release target 为 `v0.6.15-guru.3`。该历史
  authority 后由 `.43` successor 承接；在该历史阶段唯一 active authority 为 `.44`。
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

## #332 v0.6.15-guru.5 exact-candidate Release Gate

- `REQ-063`：#332 是 `v0.6.15-guru.5` 正式发布的唯一 current contract 与 semantic owner。三个独立
  版本轴固定为 repo tag `v0.6.15-guru.5`、extension revision `0.6.15-guru.40`、target/required/tested
  Trellis CLI `0.6.15`；predecessor 固定为 `v0.6.15-guru.4` / peeled commit
  `40f8aa8312bfd9650f47e1fa9d6d21b4ff18d5b6`。
- `REQ-064`：preparation 必须以 fresh `origin/main` 为标准 Intake 基线，完整承接 #311、#333、#339、
  #358、#361 已合入变更。#311 已完成前置不等于本次 Release Gate 通过；其正式 release 安装态业务仓
  Publication/Finalizer 验收由 #332 在 exact candidate 上 fresh 执行。
- `REQ-065`：preparation candidate 必须将所有 current release-facing manifest、README、workflow、preset、
  fixture、canonical、dogfood、installed 与 RDT/Architecture projection 收敛到 `.5/.40/CLI 0.6.15`，同时
  保留历史 tag、Release、versioned authority 与 evidence 的原始事实。
- `REQ-066`：preparation PR 合并后必须从 fresh `origin/main` 重新冻结 candidate SHA/tree，并对
  `v0.6.15-guru.4..candidate` 完整 committed diff 执行 open P0/P1/P2/P3 为零的独立 review；旧 task、
  preparation gate、历史 focused evidence、SKIP、stale 或 cross-SHA 结果不得复用。
- `REQ-067`：pre-tag Release Gate 必须在同一 exact candidate 上完成 source/installed package、registry/
  interface/schema/ownership、managed byte/mode parity、四平台 actual-load/projection equality、clean/existing
  install/update/reapply、installed business-repository Publication/Finalizer、secret scan 与 recursive
  sidecar/residue-zero 验证；任一 failed、SKIP、stale、unknown/multiple/unmapped exit 阻断 tag。
- `REQ-068`：annotated tag、tag-pinned post-publish smoke、GitHub Release、#332 closure 与 cleanup 是独立
  transaction；每项 mutation 前必须 fresh 展示精确 target/payload 并取得不可复用的当前对话确认。
  本 authority 不修改或关闭 #267、#311、#333、#339、#358、#361，也不升级或部署业务仓库。

- `BEH-013` Exact-candidate Release Gate：preparation merge 后从 fresh main 冻结唯一 candidate，完成
  predecessor full-diff、版本映射、分发/安装/业务仓全链与 residue gate，再按独立确认顺序执行 tag、
  immutable tag smoke、GitHub Release、Issue closeout 与 cleanup。

## #240/#348 reviewed authority promotion

- `REQ-069`：问题场景资格与解决机制资格必须由两个独立 semantic owners 承接；
  `guru-qualify-solution-mechanism` 直接读取 current requirement、planning、Architecture/spec、
  dependency/caller graph、diff 与 tests，caller 和 deterministic runtime 不复制其判断。
- `REQ-070`：OS lock、`flock`/`fcntl`、lock file/inode authority、`/proc`、PID/PGID/SID、process
  tree、FD identity/inheritance、signal/kill/process-group control 及同类 primitive 不得承接业务正确性、
  身份、fencing、monitor、inspection、cancel、recovery、publication 或 evidence authority；普通文件和
  目录仅作为 state/artifact/log/cache/config/durable record 时保持允许。
- `REQ-071`：Merge 发现已归档 task 的 current-scope content finding 时，必须使用
  `phase2_reentry_required` 将最小 repository/PR/head/branch/task/archive/finding identity 投影给
  `guru-restore-archived-task`；外部 provider、permission、ruleset、CI、scope 或 identity blocker 继续
  `merge_blocked` 且零恢复写入。
- `REQ-072`：恢复 owner 必须复用原 Issue、task、branch、worktree、remote branch 与 PR，恢复
  `in_progress`、修复 owner-private mapping/current-task pointer、清理旧 Phase 2/Review/Publication/
  Finalizer authority，并强制 fresh 重跑 Phase 2、Task Commit、Branch Review、Publication、Finalizer
  与 expected-head Merge；精确已恢复重试只读成功，歧义或 drift fail closed。
- `REQ-073`：`.45` public graph 由 registry/interface 派生为 23 active Skills、97 external
  exits、77 commands，22 个 workflow-integrated 与一个 standalone verifier；canonical、dogfood、
  installed、Shared/Codex/Claude/Cursor、workflow markers 与 preset inventory 必须一致。

## #332 original public-entry convergence

- `REQ-074`：Commit、Publication、Finalizer 与 Merge 必须继续使用既有 `scripts/invoke.sh` public
  wrapper 和稳定 command id；性能优化不得要求 caller 切换到第二套 Happy Path wrapper 或 command。
- `REQ-075`：#330 的 invocation-local snapshot、事务执行、mapped/stdout-loss recovery、watcher 与
  terminal stop 必须直接由原 command 消费，不得回退为多命令正常路径。
- `REQ-076`：同一 public wrapper 只按互斥参数形态选择一次 Happy Path 或旧参数 compatibility branch；
  正常路径不得先运行兼容检查、双写状态或重复读取同一完整 live facts。
- `REQ-077`：PR #341 新增的四个 facade command/wrapper 不再属于 current public API、canonical、
  installed、manifest 或平台 projection；record/check/execute/preview/helper 保持 package-private。
- `REQ-078`：installer、source/installed validator、compatibility matrix、throwaway verifier、generic
  eval/runtime 与 platform projection 必须从 `interface.json.public_contracts.invocation.wrapper` 读取
  唯一 wrapper path，不得全局假定文件名为 `scripts/invoke.sh`。
- `REQ-079`：`guru-restore-archived-task/scripts/restore-archived-task.sh` 保持既有 public identity，
  并作为非 `invoke.sh` 的 source/installed/platform/actual-load/eval 正向回归样本。
- `REQ-080`：`.trellis/guru-team/scripts/bash/**` 只包含真实跨 package shared asset，不补建
  Finalizer 或其它 Skill 私有 facade；README、manifest、ownership inventory 与 installed disk 必须一致。
- `REQ-081`：四阶段 semantic gate、freshness、expected-head、独立副作用确认、Issue disposition、
  recovery 与 fail-closed route 保持不变；收敛只删除无 consumer 的第二入口和正常路径重复工作。
- `REQ-082`：`.44` 是 immutable predecessor，`.45` 是唯一 active successor。promotion 使此前
  Phase 2 与 Branch Review evidence stale，必须对 promotion-created diff 重跑 Phase 2、Task Commit
  与完整 Branch Review。
- `REQ-083`：preparation 合并后必须从 fresh `origin/main` 重新冻结 exact candidate；旧 candidate
  因 delivery bytes 与 authority 变化失效，完整 #332 Release Gate 必须从零执行。
- `REQ-084`：Guru task 收尾排他使用 `guru-finish-work`；Finalizer 前不得直接 archive 或写 journal。
  archived incomplete closeout 必须 fail closed 且零写入，不得伪装成 `no_task` 重入 Intake。
- `REQ-085`：Branch Review dispatch/return 必须分别展示 reviewer/range/target 与 findings/owner；只有同一
  identity 的 checker 与 public wrapper 都 `passed` 后才能正式宣告通过并进入 Publication。
- `REQ-086`：普通“确认继续”只消费当前对话最近已展示且尚未消费的精确动作；mapped exits 自动推进且
  不重复确认，确认不授权任何未展示的 commit、push、PR、merge、tag、Release 或 cleanup 动作。

## #376 post-review base continuity

- `REQ-087`：integration clock 与 authority/task-content clock 必须独立；base 前进本身不得使
  Planning stale，真实 Issue、scope、approved assumptions 或 task content 变化继续进入原 owner route。
- `REQ-088`：完整 Branch Review 后的 compatible base advance若只需要刷新 current reviewed-content
  identity，Reconcile 必须返回 `review_continuity_required`，不得伪造 full-review identity或强制重新实施。
- `REQ-089`：Reconcile semantic owner 在展示并取得当次确认后，只能通过 package-private
  expected-head executor 创建唯一 local reconciliation commit；dirty/stale/head/tree/ancestry mismatch
  必须零写入失败，且不得执行 push 或 provider mutation。
- `REQ-090`：bounded continuity 必须分别绑定 prior full-review commit 与 current reconciled HEAD，只审查
  exact base delta、冲突解决、candidate tree 与受影响验证，并把 current HEAD 交给严格 Publication gate。
- `REQ-091`：Finalizer 的 `base_reconciliation_required` output、consumer seed 与 projection 必须把
  `branch_review_commit` 传给 Reconcile `finalizer_base_mismatch`；integration 必须从声明的 public edge
  生成 DTO，不得通过手工构造输入绕过 producer contract。
- `REQ-092`：public Skill/exit identity 保持不变；current-only schema 直接演进且旧 checkpoint stale，
  不新增 legacy dual-read、兼容 wrapper、第二状态机、remote mutation 或授权持久化。current graph 从
  live registry/interface 派生为 23 Skills / 97 exits / 78 commands，其中新增 command 仅为 Reconcile
  package-private executor。

- `BEH-016` Post-review Base Continuity：compatible base-only advance 经 expected-head local reconciliation
  commit 与 bounded continuity review 刷新当前 Publication identity；任何 authority、scope、task-content、
  candidate-tree 或 lineage drift 返回原 Planning、Implementation 或 full Branch Review owner。

## #378 固定 Fork runtime 与会话隔离

来源：reviewed #378 contribution；稳定 ID 保留。R378-01 的 SHA/CLI 是 `.47` 历史 pin，后来由 R329-01 承接、再由 R408-01 更新；它不是当前安装要求。R378-02..04 的隔离、ownership 与证据边界继续适用。

- `R378-01`：新安装和已有项目更新必须实际消费 `castbox/Trellis@ad332e3fe5a19d7274cb03e7c2f3e2128f8de291`，CLI/core 源码版本为 `0.6.16`。版本号不能替代来源证明；准备、网络、构建或来源校验失败即停止，不回退原 Trellis npm 包、原仓库、全局 CLI 或其它 ref。
- `R378-02`：主 Codex SessionStart、workflow-state 与普通 CLI 缺身份、身份未匹配或 task pointer stale 时不借用 single-session fallback，不读取接续或清理其它 session 的 task。仅显式支持的 child-agent 路径可以选择 fallback；零个、一个、多个 session 与两个独立 worktree 均保留非所属 session 的内容和文件集合。
- `R378-03`：Fork CLI 独占 Trellis-owned runtime 更新，Guru preset 只维护 Guru namespace 及同源 source-record 投影。source/installed resolver、hook、模板和 CLI 构建身份必须对应固定 SHA；更新与同平台 reapply 保留 Claude/Codex/Cursor 已安装集合、workflow、本地定制与 #388/#389 已合入行为，逐个处理 sidecar，不整体恢复旧 stash manifest。
- `R378-04`：保留 verifier 原 shell/standalone 入口与 full/focused 调度。focused clean 和两次同候选 update/reapply 只证明定向链路；full historical matrix 继续需要独立 predecessor source。closeout fixture 通过实际 installed public wrappers 组合，不借用 native adapter 或 production fixture 私有编排。源码、安装态、独立 TypeCheck、真实业务接续与 remote Release 分层报告，不能相互替代。

`REQ-002` 的扩展面与 ownership 原则保持：框架修复由 Fork 源仓拥有，Guru 不以安装后补丁或第二框架实现接管它。
`BEH-009` 的当前来源由 R408-01 定义，来源机制继承 R378-03；REQ-016/017、BEH-011 的旧 official-version matrix 保留为历史版本合同，不再作为当前安装入口。
#388/#389 是关联前置，不由 #378 关闭；#240/#348/#332/#376 与 Evolution 既有 authority 不扩张。

## #392 v0.6.16-guru.1 当前发布合同

来源：reviewed five-file RDT contribution、Architecture contribution
`architecture-contribution-392-release-v0616-guru1-v2` 与 expected `.47` serialized promotion。
以下 stable ID 在 `.48` 为 accepted/current；它们定义 authority 与验证边界，不记录动态 gate、tag、
Release、时间或用户授权。

- `R392-01`：canonical、dogfood 与 installed manifest 一致声明 extension `0.6.16-guru.41`；
  target、required 与 tested Trellis CLI 均保持 `0.6.16`。
- `R392-02`：current release-facing README、workflow/preset 文档、fixture、schema、validator 与稳定安装
  入口统一投影 repository tag / GitHub Release target `v0.6.16-guru.1`、extension
  `0.6.16-guru.41`、CLI `0.6.16` 与 framework source
  `castbox/Trellis@ad332e3fe5a19d7274cb03e7c2f3e2128f8de291`。
- `R392-03`：旧 target、旧候选状态与“`v0.6.15-guru.6` 尚未发布”等陈述不得保留在 current
  surfaces；历史 released/superseded 文件保持原事实，`.47` 只通过 navigation/history 标记为 immutable
  superseded。
- `R392-04`：Requirements、Design、Test 与 Architecture 从 `.47` 派生唯一 `.48` active successor，
  并闭合 R392/D392/T392/SCN-077..078 与 `ARCH-CUR-025`、`ARCH-INT-015`、`EVD-024` trace。
- `R392-05`：Stage 1 preparation 在 serialized Architecture/RDT promotion 前必须完成 fresh Phase 2、
  task commit 与覆盖 `origin/main...HEAD` 的独立 Branch Review；P0-P3 open findings 为零后 owner 才可
  绑定 expected `.47` promotion `.48`。promotion-created diff 必须再执行 fresh Phase 2、task commit 与
  完整 Branch Review，第二次 review 通过前 Publication/Finish 不可达。
- `R392-06`：preparation PR 合并后必须 fresh-fetch `origin/main` 并冻结唯一 commit/tree exact
  candidate；Stage 1 HEAD、#378 focused evidence 或其它 SHA 结果不得复用。
- `R392-07`：同一 exact candidate 必须完成 source/installed、四平台投影、ownership、dogfood drift、
  clean/existing install、update、workflow preview/switch、preset reapply、Fork source/build、代表性业务仓库
  installed smoke、真实 secret scan 与 recursive residue 验证。
- `R392-08`：task commit、push、PR、merge、annotated tag、tag-pinned smoke、GitHub Release、Issue close
  与 cleanup 各自读取 live authority，并保持独立 owner、preview、确认与验证边界。
- `R392-09`：发布流程不得创建 task-local release notes、PR/Release body handoff、动态 checklist、
  tracked lifecycle state，也不得持久化 HEAD、Gate 结果、时间或用户授权。

`BEH-017` Release v0.6.16-guru.1：pre-promotion review -> serialized promotion -> post-promotion fresh
Phase 2/commit/Branch Review -> Publication 是唯一 Stage 1 顺序；合并后只从 fresh `origin/main` exact
candidate 执行 Stage 2。任一 required `FAIL`、`SKIP`、stale、cross-SHA 或 unknown/multiple/unmapped
exit 都在后续 mutation 前停止。

当前 `.48` promotion 只建立 shared knowledge authority。post-promotion fresh Phase 2/commit/Branch Review、
Publication、merge、完整 throwaway matrix、业务 smoke、tag、GitHub Release 与 Issue closure 均未由本正文
声明完成。

## #329 Developer-free Trellis adoption

来源：reviewed five-file RDT contribution、Architecture contribution
`architecture-contribution-329-developer-free-trellis-v1` 与 expected `.48` serialized promotion。
以下 stable ID 在 `.49` 为 accepted/current；它们直接演进 framework source 与 identity lifecycle，
不改写 `v0.6.16-guru.1` released history，也不记录动态 gate、时间或用户授权。

- `R329-01`（仅下列 pin 为 `.49/.50` 历史，current pin 由 R408-01 替代；其余一致性要求继承）：framework source 当时固定为
  `castbox/Trellis@a2003296b4c4ce46c50d72ead3b2ec9c317f69fc`，CLI/core 为 `0.6.17`，
  package manager 为 `pnpm@10.32.1`；build、generation、source marker、installed record 与 current docs
  使用同一 immutable identity。
- `R329-02`：Trellis-owned managed files 只来自固定 Fork checkout 的正式 build、init、update/migrate
  与模板生成；不得依赖全局 CLI、npm fallback、`node_modules` patch、wrapper 或 generated-file patch。
- `R329-03`：Guru canonical、dogfood、installed/runtime、平台入口、installer、fixture 与 current docs
  的正常生命周期不得读取、创建、恢复、复制、迁移、索引或写入 developer identity、旧
  `.trellis/workspace/**` journal/index、agent trace、session recording 或 `--mine`。
- `R329-04`：creator、assignee、owner 与 actor 只来自显式 task metadata、显式输入或通过 repository
  access preflight 的 authenticated GitHub caller；无法解析时必须在任何 write 前停止并要求输入。
- `R329-05`：task checkout/worktree authority 继续绑定 `task.json.worktree_path`、branch/base、live Git
  worktree facts 与 ignored task/workspace mappings；该 mapping 表示隔离 checkout，不读取 legacy journal。
- `R329-06`：既有 identity/workspace/index/journal/agent-trace 数据保持 path、mode 与 bytes 不变，
  不作为 current task、owner、recovery 或 migration 输入。
- `R329-07`：所有受控 consumer subtraction-first 直接迁移到 developer-free contract；失去 consumer 的
  Guru 旧 entry、schema/config field、fixture、test 与 current docs 同 task 退出，不保留 adapter、fallback、
  dual-read/write；上游正式 retired command stub 只保留迁移提示。
- `R329-08`：Requirements/Design/Test 与 Architecture 通过 task-isolated contribution 和 serialized
  promotion 承接 source、identity-free lifecycle、task-worktree boundary 与 verification contract。
- `R329-09`：Codex、Claude、Cursor 的 canonical/installed 投影及 clean install、existing update、reapply、
  linked worktree、session resume 与完整 task lifecycle 使用同一 candidate，且无 unresolved sidecar；
  未发布 workflow sample 必须标记 local boundary，不得冒充远端 marketplace proof。
- `R329-10`：验证按 source build、generated adoption、focused tests、installed matrix 与 remote/release
  boundary 分层；installed closeout 来自排除 legacy/runtime/task/backup 的 clean committed candidate source，
  capability comparison subtraction-first，纯新增能力不误报 regression；本 task 不创建新 tag 或 Release。

`BEH-018` Developer-free lifecycle：在相同 task/Git/caller authority 下，legacy 数据 absent、present-A
与 present-B 的 lifecycle outcome 相同；present fixture 的 path、mode 与 bytes 在 update/reapply 前后不变。

`.49` promotion 建立 developer-free shared current authority。promotion-created diff 仍须 fresh Phase 2、
task commit 与完整 Branch Review；Publication、Finalizer、push、PR、merge、tag、Release 与 Issue closure
由各自 owner 独立验证。`v0.6.16-guru.1` 不包含本 #329 candidate。


## #408 Nightly 会话绑定与独立手动操作

来源：[Issue #408](https://github.com/castbox/guru-trellis/issues/408) 与
[贡献来源](../../../requirements-design-test-contributions/408-nightly-session-binding-manual-fallback/requirements.md)。
以下为 `.51` current 需求；Design 的实现责任和 Test 的实际证明各由同版本对应层独占。

## #410 Release v0.6.17-guru.1 current contract

`R410-01..07` 由隔离 contribution 与 live Issue #410 承接：四条版本轴统一为 repository
`v0.6.17-guru.1`、extension `0.6.17-guru.42`、CLI/core `0.6.17` 与固定 Fork source；发布
必须经过 promotion 后 fresh Phase 2、task commit、完整 Branch Review，并在合并后从 fresh
`origin/main` 冻结唯一 exact candidate。该 current authority 不声明 tag、Release、业务 smoke
或 Issue closure 已完成。

- `R408-01`：框架精确采用 `castbox/Trellis@db4ca1dfbb5abaf9be62b2a01b70dda3f80df0f0` 与 CI
  `34838784963`，CLI/core 保持 `0.6.17`，package manager 保持 `pnpm@10.32.1`。build、生成来源、
  installed source record 与实际 CLI 使用同一来源；不依赖上游 `v0.6.18`。只替代 R329-01 的旧 pin，
  不改变 R329-02..10；R378 的旧 pin 仅是历史，不构成第二 current source。
- `R408-02`：Trellis-owned 文件通过固定 Fork 正式 build、update/init 生成，Guru-owned 文件从
  canonical 同步；source/dogfood/installed 一致，reapply、ownership、drift 与 sidecar 检查保持，
  未知用户修改保留，不对 generated hook 或全局包打补丁。
- `R408-03`：同一明确 session 从 primary 经正常 Guru authoring/创建器建立 linked-worktree task，
  双端 mappings 与 boundary 通过后受控激活；返回 primary 时 `task.py current`、`get_context.py`、
  SessionStart 与 workflow-state 仍解析同一 task。裸 Git/task-store probe 不替代正常创建链，
  R378-02 的非所属 session 隔离继续有效。
- `R408-04`：正常 Agent 按实际安装合同调用现有 owner，不依赖 eval runtime、手算 recorder 私有
  派生值或手工补 mappings。保留 Phase 2、Task Commit、Branch Review、Publication、Finalizer、Merge
  的旧完整生命周期、23 Skills / 97 exits / 78 commands，以及 developer retired-zero；
  不增加节点、Skill、exit、恢复 checkpoint 或另一条自动流程。
- `R408-05`：session/task routing、hook、checkpoint 或 wrapper 的普通异常使自动链停止时，准确报告
  失败步骤、原始错误、已知 repo/task/worktree/branch/Issue/PR 与未完成步骤；读不到的事实标为
  unknown，不以异常推断新 no_task、不重入 Intake、不自修复或虚报完成。
- `R408-06`：用户明确指定的手动 commit、push、PR 创建/更新、merge、Issue closure、tag/Release
  或 cleanup 各自独立处理。每项重读 live facts、展示精确目标/path/HEAD/命令/预期结果并取得该项
  当前对话确认；前项不触发后项，授权不进入任何持久化产物。操作本身的正确性、权限与远端规则仍有效。
- `R408-07`：手动 Git/GitHub 成功与 task/runtime/Finalizer/archive residue 分别报告，不补写 Guru gate、
  archive 或完成标记；residue 不禁止独立确认的操作。Guru lifecycle 的 closure owner 仅限正式 Publication、Finalizer、GitHub 与 Merge owner，
  手动请求不追认为该生命周期完成，也不构造第二 Guru closure owner。
- `R408-08`：source、installed、Agent 行为、mock provider 与真实远端证据分层；未执行或缺失的
  验证明确为 `unverified`，上游 CI、静态文案与 mock 不替代真实 installed/远端结果。知识 `.51`
  不等于产品 release；promotion-created diff 的 fresh Phase 2、commit、完整 Branch Review 及后续
  Publication/远端发布均仍由各自 owner 验证。

本增量不实施 #398/#407，不改变 Constitution、GAP、ADR 或 Evolution。
继承合同见前述 R329/R378；双向关系见 [traceability.md](./traceability.md)。

## #418 归档身份收敛与只读复审

来源：[Issue #418](https://github.com/castbox/guru-trellis/issues/418)、
[历史 contribution](../../../requirements-design-test-contributions/418-closeout-identity-recovery/requirements.md)
及本任务已审查设计。R418 是对完整 .52 合同的窄增量，不替换既有生命周期。

| ID | 必须交付的行为 |
| --- | --- |
| R418-01 | 正常归档和同一事务恢复后，源/目标既有 task mapping 收敛到同一精确 archived locator；缺失、冲突或异 task 映射停止，不猜测重建 |
| R418-02 | completed archive、task/worktree/branch/repository 与 Ready Open PR 唯一绑定；普通 preview 和 boundary 保持只读 |
| R418-03 | 已知 input、provider、identity/stale 错误从发生点保留脱敏结构化诊断及可执行 remediation；未知异常保留 generic fallback |
| R418-04 | 当前必要审查不可用时，经独立 Branch Review、Publication、Finalizer 的真实新审查重建 Merge handoff；旧 gate 和 PR snapshot 均不能冒充新 pass |
| R418-05 | 专属复审链保持 task completed、archive/history、PR/Issue、local/remote refs 不变；不自动 Restore、metadata revision、PR edit 或放宽原 mutation path |
| R418-06 | 验证双端身份、全链 public wrapper、H/A/B、title/body/Ready/head/base drift、真实 finding 与零业务 mutation，普通 checkpoint 退休不触发多余复审 |
| R418-07 | canonical、installed、Shared/Codex/Claude/Cursor、preset reapply/drift、mode 与 sidecar 保持同一增量合同 |

在 #418 增量完成时，图为 23 Skills / 100 exits / 78 commands，业务 workflow 为 22 invokes / 98 exits；
本 `.54` 吸收 #419 producer recovery command 后，当时 graph 为 23 Skills / 100 exits / 79 commands。
#418 只增加四个 owner-local profile 和三个 success exits；Architecture 只增加三个只读 source/stage 配对。
既有 closure ownership、原 Merge 四出口和 Restore 行为继续有效，新增复审出口不改变它们。
R408-04 等继承条目中的 23/97/78 是其 .51 before-state，不限制本次 additive graph；旧版本正文不改写。
#305 Evolution target、#398/#419/#421、原业务实例与完整 Release matrix 不纳入交付声明。

实现见 [D418-01..06](../../../design/versions/current-main-0.6.17-guru.56/design-main.md)，
验收见 [T418-01..14](../../../test/versions/current-main-0.6.17-guru.56/test-strategy.md)，
双向关系见 [traceability.md](./traceability.md)。

## #419 Active-task continuation

来源：[Issue #419](https://github.com/castbox/guru-trellis/issues/419) 合同
`2026-09-17-r7`、reviewed task contribution 与 accepted `ADR-011`。本增量修复 exact active task
从 Phase 1 到 Finalizer 前的跨会话续接，不扩张 archived、Merge 或 Release Gate ownership。

- `R419-01`：canonical Guru workflow 必须且只能包含一个非空 `[trellis-continuation]` 区块，完整分发
  `planning`、`planning-inline`、`in_progress`、`in_progress-inline`、`completed` 和 invalid task state。
- `R419-02`：Phase 1 continuation 保持 task attachment、planning、wording、Architecture、Approval、
  confirmation 与 activation 的原 owner；activation 在任何 mutation 前绑定 exact task pair，并以
  `initial|recovery` 区分首次 transition 和已成功 transition 的零重复重物化。
- `R419-03`：current adjacent public DTO 直接交给唯一 consumer；DTO 丢失时，deterministic result 只由
  原 producer 正式恢复，semantic result 必须 fresh 重跑原 owner。status、Git shape、旧摘要、旧确认或
  已退休 checkpoint 不得重建 pass。
- `R419-04`：Phase 2 只复用既有 checker-to-invoker 重物化 current retained `passed` output；Task Commit
  只复用 same-candidate recovery；Branch Review 和 Publication output 丢失时分别 fresh 重跑。
- `R419-05`：SessionStart、UserPromptSubmit、显式 start/continue 和自然语言续接必须加载同一 continuation。
  “确认继续”只授权当前仍 current 的已展示副作用；正式 success exit 可自动进入无新副作用的唯一 consumer。
- `R419-06`：upstream extractor、start/continue、hooks、platform entries 与 meta 保持 upstream-owned；Guru
  preset 只分发 Guru packages/runtime/schema/projections，不 patch 或 managed-upgrade upstream-owned paths。
- `R419-07`：定向验证绑定 immutable upstream merge candidate
  `43fffc170927c85d9f7fc106cc5a059e80d4530b`、ordered parents 与 tree，覆盖 extractor、continuation mode、
  thin entries、Guru continuation、producer recovery、source/installed runtime 和真实 Git/task fixture。
#410 独占 clean install、supported update、workflow switch、preset reapply 与多平台 Release Gate matrix，
并须在 #419 合并后的 fresh `origin/main` candidate 上独立建立证据。

## #435 Active Task Delivery Loop

来源：[Issue #435](https://github.com/castbox/guru-trellis/issues/435) 与
[reviewed contribution](../../../requirements-design-test-contributions/435-active-task-delivery-loop/requirements.md)。
本增量在现有 active task 内建立可重复的 Review -> Publish -> Merge Delivery cycle，但不接管终态生命周期。

- `R435-01`：`guru-review-task-delivery` 作为 semantic owner，按 approved current slice 审查 requirement、
  Delivery policy、remaining work、independent delivery conditions、validation、RDT/Architecture、base 与
  Branch Review，只产生 closed minimal typed exit。
- `R435-02`：`guru-publish-task-delivery` 绑定 reviewed HEAD、repository/base/head branch 与 exact PR payload，
  执行一次 push/create-or-adopt/converge/Ready；equal-head output loss 恢复同一 PR，不重复 mutation。
- `R435-03`：`guru-merge-task-delivery` 只允许 merge commit，以 expected head、checks、base、method 与 exact
  subject/body 执行一次 mutation；stable trailers 绑定 task、schema 1 与 reviewed head，terminal facts 支持
  同一 Delivery result 的零第二 merge 恢复。
- `R435-04`：Planning/Approval 区分 task scope、current delivery slice、remaining work 与 independent delivery
  conditions。Check、Task Commit 与 Branch Review 审查完整 current candidate，但只按 approved current slice
  判断满足性；remaining work 不得被误判为当前遗漏或标记完成，也不新增第二组既有 gate owner。
- `R435-05`：同一 active task 支持多个顺序 Delivery cycles。Delivery history 通过 closed merge trailers 与
  GitHub PR/merge、merge commit、parents、repository/base 交叉验证后跨 branch/worktree 重建；禁止 ledger、
  PR-body identity、current-branch 推断或覆盖 immutable task creation facts。
- `R435-06`：#436 完成 Reactivate 与 current workspace binding 后，本闭环只消费新的 current active binding；
  historical merged PR 保持 immutable，新业务变更进入新 PR，tracked archive-to-active move随业务 Delivery
  提交，validation-only Reactivate 不产生空 Delivery，旧 Completion/Finish success 不得证明当前 cycle。
- `R435-07`：#407 base conflict 经 implementation route 与 fresh Phase 2 后，由 Reconcile 消费 exact resolved
  tree，绑定 prior task head、new base、tree object、index digest、ordered parents 与 semantic review，只创建或
  恢复同一个 local merge commit；该路径不 push、不修改 PR/Issue、不绕过完整 Branch Review。
- `R435-08`：三个新 package、closed schemas、consumer declarations、canonical/installed/platform projection、
  preset 与 package-local eval additive 完整分发并保持 `deferred`。#434 前 production graph、mandatory markers
  与旧 lifecycle assets不变；禁止 adapter、dual graph 与提前 retirement。代表性验证不等于完整 Release matrix。

#436 独占 Completion、Closure、Finish、Cleanup 与 Reactivate。当前 registry 为 31 packages / 136 exits /
101 commands；五个 lifecycle packages 保持 workflow-deferred，完整多平台 clean/existing/update/workflow-switch/
release-candidate Release matrix 保持 `unverified`，由专门 Release owner 在 exact candidate 上执行。

## #436 Stable Requirement Contract

本节将 reviewed contribution 的六个稳定要求提升到 `.56` current；正文仍不复制 package schema。

- `R436-01`：Completion fresh 汇总 accepted scope、全部 Delivery facts、current authority、remaining work 与 evidence；仅全部完成时返回 `completed`。
- `R436-02`：Closure 只消费 Completion approval；no-Issue/reference-only/follow-up/parent 返回 `no_mutation`，exact source Issue close 需要精确动作展示、独立确认与同事务恢复。
- `R436-03`：Finish 只在 Closure 后执行 archive projection、lifecycle-only bookkeeping publication 与 expected-head merge，并验证 remote terminal post-state。
- `R436-04`：Cleanup 只消费当前 Finish receipt，fresh 审查本轮 owned resources 后删除，失败不回滚前序 terminal facts。
- `R436-05`：Reactivate fresh 验证正常结束 archive、原 scope、历史 Delivery、current base 与恢复原因，保留 task/Issue identity 并使旧 Finish receipts 失效。
- `R436-06`：五个 packages、closed schemas/consumers、canonical/installed/platform projections、lifecycle SSOT 与定向 tests additive 完整分发；#434 前 production graph 保持 22/98。

## #443 Task Identity Session Binding

来源：[Issue #443](https://github.com/castbox/guru-trellis/issues/443) 与
[reviewed contribution](../../../requirements-design-test-contributions/443-task-identity-session-binding/requirements.md)。

- `R443-01`：task identity 是唯一长期主身份；session、branch、worktree 与 runtime mapping 是可替换承载资源，不得因 binding 丢失创建替代 task。
- `R443-02`：binding 使用 official Trellis `active_task` / `session_storage` authority，保持 ignored owner-private；不进入 tracked artifact、public DTO、Issue ledger、授权记录或第二 store。
- `R443-03`：resume/rebind fresh 验证 task、repository、branch、worktree、HEAD、base provenance、mappings、session 与 lifecycle generation；任一 mismatch 在写入前 fail closed。
- `R443-04`：跨 session continue 与 A→B→A switch 每次重新验证目标 identity；不得跨 task复用 route、checkpoint、旧 semantic pass或 terminal receipt。
- `R443-05`：Reactivate generation使旧 binding与旧 Finish/Cleanup receipt失效；binding owner不接管 #436 lifecycle owners。
- `R443-06`：manual recovery只在 live identity与base provenance完整一致时重建最小 mappings和当前 binding；不创建业务资源，不修改 tracked task artifact，合法重试幂等。
- `R443-07`：package 暴露五个成功 exits 与一个 `binding_blocked`，按 exit最小化并绑定唯一 consumer。
- `R443-08`：package 以 active/deferred 进入 32/142/102 registry closure；#434 前 production workflow 保持 22 mandatory invokes / 98 exits。

## #452 All Platform Support

来源：[Issue #452](https://github.com/castbox/guru-trellis/issues/452) 与
[reviewed contribution](../../../requirements-design-test-contributions/452-all-platform-support/requirements.md)。
本节建立平台选择的 current Requirements authority；实现与测试状态仍由后续代码和 Test owner 独立证明。

- `R452-01`：平台 authority 只能包含两层：由固定 Trellis source identity 绑定的 upstream `AI_TOOLS` 完整平台集合，以及目标业务仓库 installed manifest/provenance 记录的 exact selected platform set。不得新增 Guru-supported、dogfood-supported、deferred 或 unsupported 中间集合。
- `R452-02`：upstream inventory 的 canonical `AITool` id、唯一 public `cliFlag`、template/root、native destination 与 entry form 必须来自 pinned `AI_TOOLS` registry 或其显式映射。当前 inventory cardinality 为 22；实现不得通过目录名、统一 overlay 数量或 ambient upstream checkout 猜测平台集合，也不得把 `claude-code` 与 `claude` 混为同一字段。
- `R452-03`：公开 installer 必须完整删除 `--all-platforms` 选项及其选择分支、manifest 状态、upgrade/throwaway 入口和专项测试；旧参数作为未知参数在目标仓库写入前失败，不得保留隐藏的全集安装语义。
- `R452-04`：重复 `--platform <cli-flag>` 必须接受一个或多个合法 registry `cliFlag`，并形成去重、稳定且非空的 exact subset；installed `selected_platforms` 使用相同表示，每个值唯一映射回一个 canonical `AITool` id。unknown platform、缺少 projection descriptor、重复映射或 selection 与 inventory 不一致时必须在目标仓库写入前 fail closed。
- `R452-05`：未提供 `--platform` 时默认 selected set 恰为 Claude、Codex、Cursor；提供一个或多个 `--platform` 时只使用显式 exact subset，不与默认集合合并。
- `R452-06`：三平台默认值只属于无参数新安装策略，不构成第三层平台 authority，也不得覆盖显式 selection 或 upgrade selection。
- `R452-07`：业务仓库升级必须先读取并验证 current installed manifest/provenance 中以 registry `cliFlag` 表示的 exact selected set，再以重复 `--platform <cli-flag>` 原样 reapply。单平台、任意 subset、三平台和完整 22 平台 selection 都不得被默认值、source checkout dogfood 或新 upstream inventory 自动扩张或收缩。
- `R452-08`：`guru-trellis` dogfood 是普通业务仓库安装状态的特例，其 exact selected set 固定为 Claude、Codex、Cursor。dogfood reapply 与 drift 只消费该 selection；canonical 拥有全平台 projection 不要求当前 checkout 安装其它平台。
- `R452-09`：OpenCode 是 upstream 22 平台的普通成员，必须支持显式安装、ownership、manifest/provenance、reapply/update、throwaway 与 native actual-load；它不因 canonical support 自动进入 `guru-trellis` dogfood。
- `R452-10`：全部 selected platform projection 必须保持 canonical/installed/native-surface parity、executable mode、managed ownership、sidecar/removal provenance 与 package-private `tests/` 排除。#434 production graph activation、正式 release/tag/GitHub Release 和业务仓库生产验证均不在本 Requirements promotion 的完成声明内。

## #454 Task Lifecycle State Model C2 + D0

来源：[Issue #454](https://github.com/castbox/guru-trellis/issues/454) 与
[reviewed contribution](../../../requirements-design-test-contributions/454-task-lifecycle-state-model/requirements.md)。
本节只提升已完成并审查的 C2 shared kernel 与 D0 stage-evidence correction。

- `R454-01`：每个 task 使用 immutable repository-local TaskId，TaskRef 只作为 mutable locator；rename、archive、Reactivate、branch rebind 与 checkout move 不得改变 TaskId，exact/case-fold collision 必须拒绝。
- `R454-02`：`lifecycle_generation` 初始及 legacy missing value 均为 `0`，仅 Reactivate 可递增；generation-sensitive handoff 绑定 TaskId 与 generation。
- `R454-03`：Task source 是 closed `IssueSource | NoIssueSource` union；Delivery target 只表达 portable repository/ref identity，source、scope、Completion 与 Closure disposition 保持独立。
- `R454-04`：公共 handoff 使用 named closed DTO，仅携带唯一 consumer 所需字段；machine path、session、authorization、generic evidence、resource list 与未声明 Git facts 不得进入 DTO。
- `R454-05`：Fork official task/session primitives 是唯一 framework authority；Guru 只提供 schema、normalization、resolver adapter 与稳定错误，不创建 durable identity index、第二 session store、workspace mapping reader、alias、dual-read 或 dual-write。
- `R454-06`：C2 canonical/preset durable SSOT、source lock、README source identity、task-owned contribution 与 focused tests 必须一致；registry、workflow graph、active manifest 和 production activation 不由 C2 修改。
- `R454-07`：D0 使 pre-review compatible reconcile 形成 expected-head-bound committed merge HEAD，`post_check/post_commit` 回 fresh Phase 2；首次/full Branch Review 要求 selected base 是 review HEAD 祖先，bounded continuity 只承接已有 prior full review。Old/new base SHA 仅服务当前 operation 与相邻 consumer，不进入 durable task identity。

## #454 Task Lifecycle State Model C3

来源：[reviewed C3 contribution](../../../requirements-design-test-contributions/454-task-lifecycle-state-model-c3/requirements.md)。

- `R454-C3-01`：新增 acquisition plan、candidate、resolution、selection 四个 named checkout DTO，使 catalog 为 39 个 DTO；machine path 只存在于 call-local DTO/transaction。
- `R454-C3-02`：pre-task acquisition 在 mutation 前拒绝当前 task artifact、其它 active task authority 与 ambiguous authority。
- `R454-C3-03`：candidate/resolution/selection 使用 closed state，valid candidate 必须有 live HEAD、branch、primary/linked topology 与空 dirty set；authority conflict 不得被 selection 降级。
- `R454-C3-04`：adopt 与 provision 复用同一 live repository/worktree validator；primary checkout 只能 adopt，provision 必须返回 adoption route。
- `R454-C3-05`：checkout runtime identifier 使用 `^[A-Za-z0-9][A-Za-z0-9._:-]*$`；schema/runtime 同时拒绝空值、leading separator、空白、slash 与越界字符。
- `R454-C3-06`：checkout runtime error 只使用共享 `code`、`field_path`、`remediation`，不得出现 message/details alias 或 package-private error shape。
- `R454-C3-07`：`guru-ensure-task-checkout` 仅以 `state=planned` registry row 与 canonical `planned_skill_ids` 预留，不得存在 canonical package directory或被 active selector/source installer消费。
- `R454-C3-08`：active selector、`active_skill_ids`、active graph、production workflow、installed copy 与所有平台 projection 保持不变；E434 独占完整 package 与 activation。
- `R454-C3-09`：C3 acceptance 绑定 focused schema/runtime/ownership/source/static checks；global package suite `19/20`、preset suite `85/86` 均不声明为通过，完整 Release matrix 保持 unverified。
- `R454-C3-10`：transaction-created linked worktree 在其 Git administrative directory 持有闭合 owner-private provenance marker；marker 不进入 public DTO 或 durable lifecycle authority。
- `R454-C3-11`：output-loss recovery 必须同时验证 fresh live Git facts 与 exact marker；same-path 或 different-path replacement 缺少原 transaction provenance时 fail closed，不得继承 `guru_owned` cleanup ownership。
- `R454-C3-12`：existing-checkout reuse 不写 marker；direct handoff 在 consumer invocation 前 retire marker；marker lifecycle 或 callback failure只回滚 transaction-created matching resources，recovery保持只读。

## #454 C4 Branch Association Contract

来源：[reviewed contribution](../../../requirements-design-test-contributions/454-task-lifecycle-state-model-c4/requirements.md)。

- `R454-C4-01`：TaskBranchBinding 位于 Git common-dir，以 TaskId + lifecycle generation 为 key，durable record 只含 schema version、task id、generation、binding epoch、binding revision 与 bare branch name。
- `R454-C4-02`：binding epoch 是 repository-local application control identity；new epoch 从 revision 0 开始，成功 rebind 保持 epoch 并严格递增 revision，stale expected epoch/revision 与 same-branch no-op fail closed。
- `R454-C4-03`：establishment 覆盖 binding/ownership 四象限；任一侧存续时缺失侧复用其 epoch/revision/branch，仅两侧均缺失时创建 new epoch/revision 0。
- `R454-C4-04`：candidate 只来自 live registered worktree 与 local refs，并验证 common-dir、ref/HEAD、exact task artifact、status、generation、branch exclusivity 与 unresolved incarnation；retained lifecycle control refs不参与选择。
- `R454-C4-05`：C4 只通过窄 OwnershipPort 消费 C5 current ownership 能力，不定义第二 ledger/store/schema/authority。
- `R454-C4-06`：rebind 只支持 dirty-safe `same_checkout_new_ref` 与 clean ancestor-compatible `existing_target`，并在 mutation/recovery 前 fresh验证 reviewed expected source/target HEAD。
- `R454-C4-07`：不同历史返回 named reconcile stop；不得 stash、merge、rebase、cherry-pick、reset、force push、commit migration 或 working-tree copy。
- `R454-C4-08`：target ref 有 unresolved resource incarnation 时禁止复用；成功换绑后 binding 与 current ownership 的 epoch/revision/branch 必须一致。
- `R454-C4-09`：transaction 捕获 exact control/Git pre-state；失败只恢复 snapshots 与本 transaction 创建的 ref，output-loss recovery 只读重建 exact successor且不重复递增 revision。
- `R454-C4-10`：`guru-establish-task-branch-binding` 与 `guru-rebind-task-branch` 仅为 planned IDs；E434 前不创建 package、selector、workflow、active graph、installed copy 或平台 projection。

本 C4 source binding 同时承接既有 `REQ-048` 的 Finalizer provenance recovery guard：无 predecessor transaction
时允许 absent、exact reviewed HEAD 或 strict historical ancestor remote；replacement transaction 固定 exact
`pre_push_remote_head`，后续 pre-mutation preflight 必须验证同一 remote identity。该映射只补齐 provenance，不
新增 C4 public API、lifecycle authority 或 activation；执行级证据见 `TST-032` / `SCN-044` 与
`guru-finalize-task/tests/test_provenance.py`。

`FIN454-C4-P1-002` 复用同一 source binding，补充 transaction-bound Reactivate branch reuse、历史 terminal PR
非 current-candidate 条件、`pre_push_remote_head` single-fast-forward、`publication_head`
push-output-loss/converged recovery，以及 allowed-head/Open-PR/transaction-identity drift fail-close；它不新增 C4
requirement identity、宽泛 fallback、PR 人工选择 API、force push 或第二 ledger。

`FIN454-C4-P1-004` 在该 owner 下补充 same-base fresh-reviewed reprepare：predecessor review-to-Publication
必须相等或为合法 provenance tail，selected base 已在 predecessor Publication lineage，current Branch Review、
Publication 与 live HEAD 相等且严格后继，并且 task 未 archive、没有 Open PR。remote 只接受 transaction-owned
`pre_push_remote_head` 或 `publication_head`；历史 terminal PR 不作为 current candidate，中间 review commit 与其它
endpoint 均拒绝。该合法路径复用现有 `reprepare_required/provenance_metadata_tail`，不增加 branch/session/path
authority、人工 selector、fallback、force push、第二 ledger、schema 或 public DTO。

C5-C7、D443、D436、E434、#434 activation 与完整 Release matrix 继续保持独立后续边界。
