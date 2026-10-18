# Guru Team Trellis Extension 当前需求

版本：`current-main-0.6.5-guru.39`；状态：`superseded`；基线：task head `d4165f268d36e19139266d28519148c290f773a4` + #290 serialized promotion delta（精确 revision 为当前 Git HEAD）。

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
- `REQ-013`：install/update/upgrade/reapply 必须保留完整 capability inventory、managed path、
  executable mode 与声明平台入口；未处理 `.new/.bak`、版本或 projection drift 必须阻塞成功声明。
  `source_confirmed`：preset/upgrade contracts；`code_recovered`：installer 与 validators。
- `REQ-014`：Finalizer 完成 archive、Ready PR 与 terminal cleanup 后，public wrapper 只可从已归档 durable summary、精确 retired owner locator 与当前 Git/GitHub ready facts 重建 terminal authority；缺 locator、archive/head/PR/scope 漂移或未退休 owner state 必须 fail closed。`source_confirmed`：Issue #275；`code_recovered`：Finalizer owner/runtime。
- `REQ-015`：Throwaway verifier 的 active package、command 与 complete-package inventory 必须从 canonical registry/interface validation 派生；不得维护随新增 Skill 漂移的固定数量。`source_confirmed`：Issue #275；`code_recovered`：verifier inventory projection。
- `REQ-016`：专项 compatibility owner 必须从 live manifest、ownership、overlay 与 registry 交叉派生声明平台，并对每个平台分别执行 clean official Trellis `0.6.15` 与 existing official `0.6.5 -> 0.6.15` 隔离 cell。`source_confirmed`：Issue #260；`verified`：六个 cell 全部通过。
- `REQ-017`：existing cell 的 Guru before-state 必须是 immutable `v0.6.5-guru.10` / extension `0.6.5-guru.36`，并按 official upgrade、update dry-run、条件式 migrate、workflow preview/switch 与 preset reapply 顺序执行。`verified`：三个 existing cell。
- `REQ-018`：升级前后 active Skill、interface、schema、exit、command、consumer、route、managed path、mode、template-hash 与 Docs authority 的完整投影不得出现未审查能力丢失。`verified`：21 active Skills、89 exits 与 installed projection 保持。
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
- `REQ-035`：Architecture 2.0 schema/runtime、canonical/dogfood/installed/platform projection 与项目中立十场景必须原子承接上述 lifecycle，stable Skill/profile/exit ids 不变；外部 evidence 不可得时保持 `evidence_gap|unverified`。#267 release matrix/tag/Release/immutable smoke 与 business-repository refactor不属于 #283。
- `REQ-036`：base selection 必须固定按 explicit、config scalar、ordered exact local/remote refs、remote default 执行；current branch 与 worktree availability 不参与 selection，selected base 缺 checkout 时不得回退低优先级 candidate。
- `REQ-037`：selected base 确定后只绑定同一 Git common-dir 中 registered、exact `refs/heads/<selected_base>`、clean 且 branch/HEAD/ref identity 一致的唯一 authority checkout。
- `REQ-038`：Codex session checkout 允许 detached 且只作为 invocation shell；fetch、可选 `merge --ff-only`、checker equality 与 public repository locator 只使用 authority checkout。
- `REQ-039`：authority missing、ambiguous、dirty 或 identity mismatch 必须稳定 `blocked`；不得 checkout、switch、创建 branch/worktree、reset、rebase、stash、force update 或重选 base。
- `REQ-040`：invocation checkout 自身已绑定 selected base 时保持成功路径；behind authority 只允许 explicit remote-tracking refspec fetch 与 `merge --ff-only`。
- `REQ-041`：`guru-base-sync-result-1.0`、Interface 1.4、public `synced|skipped|blocked` schemas、typed exits 与 transition shape 保持兼容，既有 locator 字段指向真实 authority checkout。
- `REQ-042`：`guru-create-task-workspace` 必须按 producer provenance source 对 explicit、config、config-candidate、remote-default 的 current source、selected base 与完整 candidates exact revalidate，且不得导入 producer private runtime。
- `REQ-043`：canonical、dogfood、installed 与 Shared/Codex/Claude/Cursor projection、preset reapply/drift/mode 和 sidecar-zero 必须一致；代表性 installed detached wrapper 只证明 #290 normal path，#267 继续独占 release matrix/tag/Release。

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

`source_confirmed`：最新已发布 stable release 是 annotated tag `v0.6.5-guru.10`，tag object `b5fd47e9dc45ca4d6950f87f38d495776ce676ce`，peeled commit `5c059f4943edad7dfe25182a78af94759d41f9a1`，extension revision `0.6.5-guru.36`，目标 Trellis CLI `0.6.5`。当前 source candidate 为 extension `0.6.5-guru.37` / Trellis `0.6.15`；stable tag 与 GitHub Release 仍由 #267 拥有。

## 非目标

本 authority 的 `.39` 是 knowledge identity，不是 extension/release revision。本 authority 不把 extension `.37` 称为已发布 stable release，不实现 #248/#252 public owner，也不把业务仓库私有 PRD、完整日志、临时 hash bundle 或用户授权写入 current intent。
