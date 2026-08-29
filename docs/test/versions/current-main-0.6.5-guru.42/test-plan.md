# 当前测试计划与证据

版本：`current-main-0.6.5-guru.42`；状态：`active`；predecessor：`current-main-0.6.5-guru.41`；
source baseline：reviewed task head `d3dca74b3a94569a095594477c15b032526f2381` + #267 expected `.41` serialized promotion delta。

## Replacement before-state authority

- Issue #275：CLOSED/COMPLETED；PR #282 rebase-merged。
- annotated tag：`v0.6.5-guru.10`；tag object
  `b5fd47e9dc45ca4d6950f87f38d495776ce676ce`；peeled commit
  `5c059f4943edad7dfe25182a78af94759d41f9a1`。
- GitHub Release：non-draft、non-prerelease、zero assets；extension
  `0.6.5-guru.36`，official Trellis `0.6.5`。
- 该 release 是 existing cells 的 immutable before-state，不是 `.37` target release。

## #260 focused implementation evidence

| Check | Result | Boundary |
| --- | --- | --- |
| focused installed lifecycle A/B | 1/1 PASS | local deterministic installed lifecycle；A archive 后 history query 返回唯一 `PR #301` finish-summary candidate |
| upgrade contract | 20/20 PASS | exact version/matrix/reapply/migration/source-binding contract |
| preset / ownership unit suite | 83/83 PASS | installer、installed manifest、ownership、mode 与 reapply contract |
| managed Python routing | 44/44 PASS | declared caller graph |
| Python compile | PASS | affected Python syntax only |
| package/runtime installed profiles | PASS | RDT 6 cases/4 profiles；Architecture 4/4；Bootstrap 4 cases/3 profiles |

## Full six-cell compatibility matrix

live-derived platforms：`claude`、`codex`、`cursor`。每个平台使用独立 repo、npm
prefix 与 runtime，分别执行 clean `0.6.15` 和 existing `0.6.5 -> 0.6.15`：

| Cell family | Count | Result |
| --- | --- | --- |
| clean official `0.6.15` + current preset | 3 | 3/3 PASS |
| existing `v0.6.5-guru.10` + official migration + reapply | 3 | 3/3 PASS |
| final recursive `.new/.bak` | 6 | all `0` |
| template hash unknown drift | 6 | all `0` |
| candidate source binding | 1 | HEAD、tracked delta、untracked path/mode/content 与 isolated-index candidate tree 形成单一 `source_state`；run 前后 identity 相同 |
| capability projection | 6 | `workflow`、`task_data`、`docs_authority` 三组保持，无 blocking capability loss |
| consistency / installed projection | 6 | Skill API/interface/schema/command、Skill package、ordinary managed asset、overlay mode、template hash、sidecar 与 extension identity/version binding 保持；任一漂移独立阻塞 |
| Docs authority | 6 | recursive `docs/**` 全文件 hash 保持，Requirements/Design/Test/Architecture 均含 versioned body |
| installed Phase 0/workspace/closeout | 6 | PASS |
| post-archive history discovery | 1 | A archive 后返回唯一 non-empty `PR #301` candidate，locator 指向该 task 的 `finish-summary.json` |

最终 dirty candidate 使用 source HEAD
`868fada5f6296cca6c58ed725946b870865b1e0c`，target CLI=`0.6.15`，
extension=`0.6.5-guru.37`。精确 `source_state.candidate_tree`、source identity 与
matrix digest 由最终只读 run 输出绑定；它们不写回 tracked 文档，避免文档修改让
candidate tree 自引用失效。workflow evidence 是 `public_plus_local_candidate`；这不是
已发布 `.37` tag proof。

## A/B business-task compatibility

- A=`workspace_mode=worktree` / `finish_entry=github_pr`；B=`current` / `none`。
- local matrix Planning、Phase 2、Branch Review、Publication、fixture-local acceptance、
  Finish/archive、A provider failure、B Finish failure 与 cleanup failure recovery 全部通过。
- A archive 完成后，installed history preview 对非空 query 返回唯一 `PR #301`
  candidate，并精确指向该 archive 的 `finish-summary.json`。
- 两种 merge order均通过，tracked Guru metadata intersection=`[]`，B GitHub PR call
  count=`0`，workspace journal存在但不 tracked。
- cleanup 后 protected work/archive/Finish commits 对 retained refs 仍可达。

真实 GitHub A route 在单独确认后完成：private disposable repo PR #2 从 source head
`6a7b721adfd8a70be9cc56883bf5e2b2133fdf84` expected-head rebase merge为
`a5c73c49ca38e593e11bafb62a2f142ca208f97f`；Issue #1 于 merge 后一秒 CLOSED/COMPLETED。
首次 provider failure 分类 `github_api_unavailable`，同一 Finalizer transaction恢复；
remote branch 与 disposable repository 已删除，本地 scenario resources移动到 Trash且可恢复，
删除远端后 retained-ref reachability 已重验。

## #283 Architecture convergence and reviewed promotion

| Check | Current result | Boundary |
| --- | --- | --- |
| complete committed task range | PASS：base `2d34abfc…` -> reviewed head `86a2cc1a…`，5 commits / 429 paths | promotion delta excluded until fresh re-entry |
| Architecture semantic Branch Review | `baseline_current` / `architecture_impact` / `target_native` / `reviewed_candidate` | exact committed range、current descriptor/result、before/after independently recomputed |
| independent `guru-review-branch` | schema 6.0 `passed`，open findings zero | current gate consumed；旧 gate只保留 ignored stale backup |
| representative clean installation | PASS：Trellis `0.6.15`、public marketplace bootstrap、exact local committed workflow、all-platform preset、21 packages / 72 commands / 4229 managed files | local pre-push evidence；不是 formal verifier typed exit 或重构前稳定版 Release matrix |
| Architecture/RDT promotion | `.37` expected current -> `.38` current knowledge identity；design constitution/change contract/ADR/history/traceability 同步 | serialized owner gate 后必须 fresh Phase 2/commit/Branch Review |

Architecture package的 source/dogfood `22/22`、两套固定十场景 `10/10`、Planning/Phase 2/Branch Review consumers `21/21`、`9/9`、`15/15`、RDT/package/finish/retrieval `9/9`、`8/8`、`6/6`、`4/4` 与 preset ownership/apply/upgrade `7/7`、`78/78`、`20/20` 均绑定 reviewed task candidate。promotion 仅把这些已审查的 contract/evidence 提升到 shared current；它不把 promotion-created diff 冒充为已复核。

## #290 detached base authority checkout

| Check | Current result | Boundary |
| --- | --- | --- |
| canonical package tests | sync-base 15/15；workspace 6/6；integration 8/8 PASS | exact #290 package and producer-consumer behavior |
| installed package tests | sync-base 15/15；workspace 6/6 PASS | installed dogfood behavior, not release matrix |
| source/installed validators | 21 packages / 72 commands；sidecar/conflict/removal zero | current package graph and managed inventory |
| projection/reapply/drift | canonical/installed affected bytes equal；all-platform apply and dogfood drift passed；`.new/.bak` zero | current candidate distribution only |
| representative Codex detached wrapper | synced；authority locator and three-way equality passed | one normal installed path，不是重构前稳定版 Release matrix |
| independent committed review | base `e7df696a…` -> task head `51609250…`；141 paths；Architecture and Branch Review passed with no P0-P3 finding | promotion-created diff requires fresh Phase 2/commit/Branch Review |

The serialized Architecture/RDT promotion binds expected `.39`, reviewed contribution
`architecture-contribution-295-sync-discovery-public-handoff-v1`, and successor `.40`.
It does not publish extension `0.6.5-guru.37`.

## Current boundaries

- `v0.6.15-guru.3` / extension `0.6.15-guru.39` / Trellis `0.6.15` 是 #267 current target；stable tag、GitHub Release、tag-pinned clean install 与 release smoke 仍为 `unverified`。
- `.42` 只表示 current RDT/Architecture knowledge identity；promotion 不等于 exact-candidate Release pass，也不授权 tag、Release 或 Issue closure。
- #311 正式 `.3` business-repository Finalizer 原失败路径与错误文件重试仍为 `unverified`，Issue 保持 OPEN。
- full matrix logs、临时 repository/runtime、用户授权与完整 hash bundle不进入 current SSOT。

## #295 promoted verification scope

- `T295-13`：Discovery active input/owner-result、Sync/Clarify projections、managed Python/runtime、四平台 projection、preset reapply/update/drift、sidecar 与 native eval 均通过 targeted validation。
- `T295-14`：installed Phase 0 transcript 与一个 representative clean throwaway 完成真实 Sync -> Discovery -> Clarify、re-entry/refresh、active-task recovery 与 final drift；未将 external semantic grading 或 unpublished feature-ref marketplace 证据声明为通过。
- 所有 matrix run 都保持 `real_github_verified:false`；最终 candidate 的精确
  source/matrix identity 只保留在 runtime/conversation evidence，不替代独立真实
  GitHub A evidence。

promotion-created diff 的 Phase 2 `guru-check-task`、新 task commit、独立 Branch Review 与 Publication/Finalizer仍须绑定最终完整 diff执行；此前证据不替代这些 gate。

## #311 installed Finalizer provenance evidence

| Check | Current result | Boundary |
| --- | --- | --- |
| exact committed source range | `origin/main@d907fcc5…651defee`；7 commits / 85 paths；Architecture 与 distinct fresh-final Branch Review passed，P0-P3 open findings zero | promotion delta 仍需 fresh re-entry |
| Finalizer package | canonical/installed 各 `59/59` | focused source/target、tail、prepared-state 与 terminal harness |
| verifier package | canonical/installed 各 `17/17` | structured failure evidence；不是 Finalizer owner |
| routing / ownership | `44/44` / `7/7` | caller inventory anchor 已刷新到 current generated helper identity |
| upgrade / preset | `36/36` / `81/81` | targeted #311 regression；不替代独立 release matrix |
| source / installed validation | 21 packages / 72 commands；installed 4263 managed files；reapply/drift/platform parity/sidecar zero passed | current candidate distribution only |
| local complete Finish integration | 第 3 次且最后一次运行通过；禁止第 4 次 | fake GitHub harness，不替代真实 fixture |
| representative real fixture | `unverified`：旧 candidate 已完成到 Branch Review并暴露 source findings；current `651defee` 尚未 fresh reinstall/Publication/Finalizer | 下一阶段必须复用现有 fixture，不创建新真实 repo |
| production and error retry | `unverified` | Issue #311 保持 OPEN；完成 merge/生产发布/错误文件重试后另行判断最大根因 |

本 promotion 绑定 contribution digest
`a6e2835e2303c081c28296f9d635dabbb7bad2dffbe99466f2bd6d4e834058aa`、expected `.40` 与
successor `.41`。它不发布 extension `0.6.5-guru.37`，不执行 #267 的 release-wide matrix、tag 或
GitHub Release，也不把旧 candidate 的被阻断 closeout表述为当前通过。

## #267 release authority alignment evidence

| Check | Current result | Boundary |
| --- | --- | --- |
| reviewed contribution range | `origin/main@3efcce72…d3dca74b`；2 commits / 22 paths；Architecture Branch Review 与 independent Branch Review passed，P0-P3 open findings zero | promotion-created diff 必须 fresh re-entry |
| RDT promotion | expected `.41` -> `.42`；Requirements/Design/Test version、navigation、history 与 contribution status 串行更新 | 不证明 Architecture promotion 或 downstream Phase 2 |
| Architecture promotion | expected `.41` -> `.42`；仅更新 README、CURRENT、evidence 与 contribution state；ADR `required=false` | 不改变 decision/owner/GAP/compatibility |
| version mapping | `v0.6.15-guru.3 -> 0.6.15-guru.39 -> Trellis CLI 0.6.15` | tag、Release、latest stable 与 smoke 仍 `unverified` |
| post-promotion lifecycle | pending fresh Phase 2、task commit 与 independent complete-range Branch Review | 旧 contribution review 不替代 |
| #311 business proof | `unverified` | 正式 `.3` 发布后独立安装与错误路径重试；Issue 保持 OPEN |
