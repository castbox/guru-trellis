# 当前测试计划与证据

当前 .62 来源：immutable predecessor `current-main-0.6.17-guru.61` 与 reviewed #454 C4 contribution；上游固定为 `castbox/Trellis@eb370008c7689d4e272ae626bd002190ecbb3296` / CI `35621578090` / CLI/core `0.6.17`，Guru manifest 与 release target 沿用 predecessor。Architecture public inheritance 为 `docs/architecture/README.md` / `current-main-0.6.17-guru.62` / `active`。
完整继承 immutable `.61` 业务合同，当前增量为 #454 C4 branch association/establishment/rebind substrate 与同范围 bounded Finalizer provenance recovery guard；本 promotion 只建立 current acceptance authority。

`.62` 完整继承 `.61`，吸收 reviewed #454 C4 contribution；RDT 与 Architecture current 均为 `.62/active`。截至 2026-09-24，提升前 `T454-C4-01..10` 的 focused acceptance 已建立；这些结果不替代 promotion-created diff 的 fresh Phase 2、Task Commit 与完整 Branch Review，Publication 必须消费后续 exact-range gate 结果。

版本：`current-main-0.6.17-guru.62`；状态：`active`；predecessor：`current-main-0.6.17-guru.61`；source baseline：reviewed #454 C4 contribution + inherited immutable `.61` authority；精确 revision 由 containing Git object/tree identity 绑定。

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

## 继承的 #332 历史边界

- latest stable 是 `v0.6.15-guru.4` / extension `0.6.15-guru.39` / Trellis `0.6.15`；#332
  current target 是 `.5/.40/CLI 0.6.15`，tag、GitHub Release、tag-pinned clean install 与 release smoke
  仍为 `unverified`。
- `.44` 只表示 current RDT/Architecture knowledge identity；promotion 不等于 exact-candidate Release pass，
  也不授权 tag、Release 或 Issue closure。
- #311 已于 2026-09-04 以 `completed` 关闭；其 source/target provenance 合同是 #332 的已完成前置，
  正式 `.5` installed business-repository Publication/Finalizer 仍须在 #332 exact candidate 上 fresh 验收。
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
| production and error retry | historical `unverified` | #311 当时保持 OPEN；现已 completed，其正式 release 安装态验收由 #332 fresh 承接 |

本 promotion 绑定 contribution digest
`a6e2835e2303c081c28296f9d635dabbb7bad2dffbe99466f2bd6d4e834058aa`、expected `.40` 与
successor `.41`。它不发布 extension `0.6.5-guru.37`，不执行 #267 的 release-wide matrix、tag 或
GitHub Release，也不把旧 candidate 的被阻断 closeout表述为当前通过。

## #267 release authority alignment evidence

| Check | Current result | Boundary |
| --- | --- | --- |
| reviewed contribution range | `origin/main@3efcce72…d3dca74b`；2 commits / 22 paths；Architecture Branch Review 与 independent Branch Review passed，P0-P3 open findings zero | promotion `351e61d1` 与 r19 修复 `490b302a` 均已完成 fresh Phase 2、task commit 与 independent Branch Review re-entry |
| RDT promotion | expected `.41` -> `.42`；Requirements/Design/Test version、navigation、history 与 contribution status 串行更新 | 不证明 Architecture promotion 或 downstream Phase 2 |
| Architecture promotion | expected `.41` -> `.42`；仅更新 README、CURRENT、evidence 与 contribution state；ADR `required=false` | 不改变 decision/owner/GAP/compatibility |
| version mapping | `v0.6.15-guru.3 -> 0.6.15-guru.39 -> Trellis CLI 0.6.15` | tag、Release、latest stable 与 smoke 仍 `unverified` |
| post-promotion lifecycle | r19 fresh Phase 2、task commit `490b302a`、independent complete-range Branch Review、PR readiness 与 Finalizer 已完成；PR #315 已 merge 为 `a41b8a34` | post-merge predecessor-to-candidate full-diff review 发现 P2 `BR-267-FULL-CAND-001`；修复 merge 与 fresh review 前 tag 保持阻断 |
| #311 business proof | historical `unverified` | `.3` 阶段未完成该 proof；#311 现已 completed，`.5` installed business proof 由 #332 承接 |

## #335 repository-private release orchestration verification authority

| Contract surface | Required proof | Boundary |
| --- | --- | --- |
| private identity | Shared/Codex/Claude/Cursor project-local definition parity；public registry/marketplace/preset/overlay/manifest/installed inventory zero inclusion | 不安装到业务仓库 |
| preparation composition | standard intake、Phase 2、Task Commit、一次完整 Branch Review、Publication、Finalizer、Merge owner 引用完整且不复制内部 contract | 不创建真实 PR 或 merge |
| honest-path convergence | 稳定 planning 与 final delivery commit 后，lifecycle metadata 创建/替换/退休不改变 reviewed identity 或 delivery commit，Publication/Finalizer 无第二次 Review | 不把运行结果写回 tracked SSOT |
| freshness | Skill/durable/config/schema/script/test bytes 变化使相关 gate stale；owner-private lifecycle metadata 不触发内容重审 | 不覆盖 hostile-input 或竞态模型 |
| post-merge contract | exact candidate lineage、required minimum checks、cross-SHA/FAIL/SKIP/stale stop 与完整累计矩阵边界明确 | 不执行 tag、Release 或 smoke |
| independent mutations | merge、tag、tag-pinned smoke、Release、Issue closure、cleanup 分别要求 fresh preview 与当前对话确认 | 一次确认不得复用 |

该表定义 #335 的可重复验证责任，不记录本次 task 的 HEAD、Gate 结果、finding closure、tag/smoke/
Release 状态或时间。实际结果由对应 Phase 2、Branch Review、Publication、Finalizer 与 post-merge
owner 在其候选上即时生成。

## #332 v0.6.15-guru.5 Release Gate authority

| Gate | Required proof | Current state |
| --- | --- | --- |
| authority promotion | Architecture/RDT expected `.44 -> .45`、reviewed #332 original-entry contribution、23 Skills / 97 exits / 77 commands、唯一 active、完整 navigation/traceability | promotion-created diff；须 fresh Phase 2/commit/Branch Review |
| release identity | latest stable `.4/.39` 与 target `.5/.40/CLI 0.6.15` 在所有 current release-facing surfaces 一致 | authority mapping 已定义；exact candidate 尚未冻结 |
| merged prerequisites | #311/#333/#339/#358/#361 在 installed candidate 上重新消费 | `unverified`；历史 evidence 只作定位 |
| predecessor review | `v0.6.15-guru.4..candidate` complete committed diff，P0-P3 open findings zero | `unverified`；等待 post-merge fresh main |
| distribution/install | source/installed validators、registry/interface/schema/ownership、managed parity、四平台 actual-load、clean/existing install/update/reapply | `unverified` |
| installed business chain | Publication/Finalizer initial reprepare、fresh rebind、push/PR/archive/Ready/terminal 与 Issue recovery | `unverified`；不得用 package test 替代 |
| pre-tag hygiene | secret scan、recursive `.new/.bak`、sidecar、owner-private residue、tracked gate report zero | `unverified` |
| release transactions | annotated tag、tag object/peeled commit reread、immutable-tag smoke、GitHub Release/latest stable、#332 closure、cleanup | 全部 `unverified` 且分别需要 fresh confirmation |

本表是稳定 Test authority，不记录 candidate SHA、运行时间、动态 gate pass 或用户授权。任一 FAIL、SKIP、
stale、cross-SHA、unknown/multiple/unmapped exit 都阻断后续 release mutation。

## #376 base-continuity verification authority

| Check | Current result | Boundary |
| --- | --- | --- |
| committed contribution review | fixed range `e339d994…29ffa01b`；fresh Architecture Branch Review 与 official independent Branch Review passed，open P0-P3 zero | promotion-created delta 尚须 fresh Phase 2/commit/Branch Review |
| Reconcile package | source/installed 各 `24/24` | semantic route、expected-head executor、commit recovery 与 zero-write negatives |
| Review Branch package | source/installed 各 `26/26` | current schema、pair/tree ancestry、bounded scope 与 minimal output |
| Finalizer / Publication | Finalizer source/installed 各 `102/102`；Publication `48/48` | producer projection 与 strict downstream identity；不证明远端发布 |
| cross-Skill continuity | source/installed 各 `2/2`；Skill package integration `9/9` | Finalizer projection -> Reconcile commit -> continuity -> Publication ready |
| graph and authority | source validator 23 packages / 78 commands；independent graph 23 Skills / 97 exits / 78 commands；Architecture `22/22`、RDT `9/9` | installed full validator 的 #108 `.bak`/Claude drift 保持独立 blocker |
| distribution boundary | task validation、canonical/installed/platform parity、ownership、overlay drift、manifest、JSON/Python/diff checks passed | 未运行 full preset reapply 或完整多平台 Release/upgrade matrix |

`.46` 只提升上述稳定合同和已审查的 focused evidence，不把 39 个 Issue #108 `.bak`、未完成的 installed
full validator 或未运行的 Release/upgrade matrix表述为通过，也不记录用户授权或动态 gate artifact。

## #378 reviewed focused evidence

来源定位：`docs/requirements-design-test-contributions/378-pinned-fork-runtime/` 与 task `09-09-378-pinned-fork-runtime/implement.md`。下表是 promotion 消费的既有定向结果，不是本次 Docs 编辑重新执行 runtime 测试。

| Test | Reviewed evidence | Boundary |
| --- | --- | --- |
| T378-01 | Fork 固定 SHA 自身构建；修复后的 prepare/source/routing 84 项通过，成功构建标记校验 | CLI/core 0.6.16；不证明独立 TypeCheck 或发布 |
| T378-02 | 显式 source/installed 路径下两项 canonical/installed 隔离回归通过，无 skip；含两个临时 worktree | 仅正常 session/hook fixture，不是业务接续 |
| T378-03 | source-lock 字节一致；三平台 worktree reapply/drift 通过；五份备份逐项核对并移到仓库外保留，第二次 reapply 无未解决 sidecar | 不运行完整多平台 throwaway；#388/#389 保留为关联前置 |
| T378-04 | 原 shell focused clean 与两次同候选 update/reapply 通过 | 本地未发布 workflow 样本，不是 predecessor 或 remote release |
| T378-05 | caller/routing 99 项历史定向回归；真实 installed wrapper closeout initial 与 after-reapply 通过 | fake provider；after-reapply 本身不代表再次 Fork update；full 历史执行未验证 |

完整历史矩阵、真实业务 #31/#127、独立 TypeCheck、remote Release/tag/npm/tag-pinned smoke 均保持 `unverified`。
`.47` 只保留为 immutable predecessor；`.48` promotion-created diff 不继承先前 Branch Review pass，后续正式 owner 需 fresh 检查。

## #392 v0.6.16-guru.1 verification contract

| Gate | Required proof | Stable boundary |
| --- | --- | --- |
| authority promotion | expected `.47`、reviewed contribution v2、当时唯一 active `.48`、R392/D392/T392/SCN 与 Architecture refs 闭合 | `.47` immutable predecessor；`.48` 现为 immutable superseded；不证明后续 gate outcome |
| release mapping | `v0.6.16-guru.1` / `0.6.16-guru.41` / CLI `0.6.16` / fixed Fork full SHA 在 #392 authority 一致 | reviewed historical contract；不证明 published 或当前 `.49` framework identity |
| post-promotion review | promotion-created diff 的 fresh Phase 2、task commit 与完整 Branch Review，P0-P3 open findings zero | 必须绑定 fresh reviewed-content identity；Publication 前置 blocker |
| preparation publication/merge | Publication、Finalizer、PR 与 expected-head merge | 各 owner fresh-read live authority并消费前序最小结果 |
| exact-candidate gate | fresh `origin/main` candidate 的 lineage/full diff、source/installed、四平台、ownership/reapply/drift、clean/existing/update/switch、Fork build、business smoke、secret scan、residue | 所有 proof 绑定同一 exact candidate；历史/focused evidence 不可替代 |
| release transactions | annotated tag、tag-pinned smoke、GitHub Release/latest stable、Issue #392 close、cleanup | 各自 fresh 验证并进入独立 mutation boundary |

`SCN-077` 验证 promotion 前后两轮 review；`SCN-078` 验证 post-merge exact-candidate 与独立 release
transactions。任一 required `FAIL`、`SKIP`、stale、cross-SHA 或 unknown/multiple/unmapped exit 阻断后续动作。

## #329 developer-free promotion evidence contract

| Gate | Required proof | Stable boundary |
| --- | --- | --- |
| source/generated adoption | Fork `a2003296...` build、CLI `0.6.17`、`pnpm@10.32.1`、official generated assets 与 source records exact 一致 | 不证明远端 marketplace/tag/Release |
| focused consumer migration | developer/workspace consumer inventory 归零；task owner/resolution、legacy preservation 与 current schema regression 通过 | historical stubs/tests 保留不等于 active consumer |
| installed lifecycle | Codex/Claude/Cursor clean/update/reapply/worktree/session/task lifecycle、ownership/drift/sidecar 与 clean provenance 通过 | fixture GitHub 与 local sample 不是 production publication |
| authority promotion | expected `.48`、reviewed contributions、唯一 active `.49`、R329/D329/T329/SCN-079..084 与 Architecture refs 闭合 | `.48` immutable；promotion 后 fresh Phase 2/commit/review 必需 |
| remote transactions | Publication、Finalizer、push、PR、merge、tag、Release、Issue close、cleanup | 各 owner 独立 fresh-read 与确认；本 current authority不声明 outcome |

`v0.6.16-guru.1` 是 immutable released predecessor，未包含 #329 candidate。`.49` 只提升 reviewed
developer-free source/lifecycle authority，不把此前 focused/installed evidence写成远端发布事实。


## #408 已审查来源与验证边界

来源为提交中保留的 [#408 contribution](../../../requirements-design-test-contributions/408-nightly-session-binding-manual-fallback/test.md)

## #410 Release validation boundary

`T410-01..08` 覆盖四轴映射、lineage、source/installed parity、ownership/preset/drift、focused
install/update/reapply、secret scan 与 exact-candidate live mutation proof；本 Issue 不承担累计
多平台 Release Gate matrix，也不把知识 promotion 当作 tag、Release 或 Issue closure 证明。
及 [EVD-027](../../../architecture/evidence/current-evidence.md)。下表继承 source evidence，
不是本轮 Docs 编辑重新执行 runtime 测试，也不是 promotion-created diff 的 gate 结果。

| Test | 已取得的 source evidence | 证明边界 |
| --- | --- | --- |
| `T408-01` | 固定 Fork `db4ca1dfbb5abaf9be62b2a01b70dda3f80df0f0` 构建/独立 TypeCheck；CI `34838784963` 对应同 SHA success；CLI/core `0.6.17` | 上游来源和本地构建分开证明，不证明 Guru Release |
| `T408-02` | canonical/dogfood session 回归与三平台 Guru 投影；本地 candidate Codex focused installed 两轮 update/reapply | 真实 installed 定向结果，不是远端 exact-ref marketplace 或完整 predecessor 矩阵 |
| `T408-03` | installed six-step stdout 与 24 个出口族通过；四份 mapping、boundary、空上下文拒绝、受控激活和双端四次 hook 检查通过 | script fixture 使用正常 authoring，不以裸 Git/task-store 代替 Guru 链 |
| `T408-04` | 相关四包 82 项、Planning 22 项通过；三个 retired-data profile 的 workspace 集成通过；native 按 installed 合同完成六步、Architecture/Planning、start、双端 current/context/hook | native 是文档澄清和正常输入更正后的成功，不是零提示首次通过；Planning 未预填私有 token；GitHub/fetch 为 mock，直接 hook 不证明宿主自动分发 |
| `T408-05` | 读取 canonical 合同的 native 只读演练，分别报告普通失败、known/unknown 与停止边界 | 静态合同只证明文字投影；不据此宣称真实宿主所有失败均已触发 |
| `T408-06`, `T408-07` | stateful test 用真实临时 Git/bare remote 与内存 fake provider 核验单项副作用、后项零执行、unknown 与 residue 字节；同一隔离 fixture 的 native 连续演练实际驱动 local commit/push 和内存 provider PR 创建 | stateful test 不包含 AI 授权函数；native 与命令效果分层，连接证据限该本地链，不外推真实 gh/GitHub 或其它远端动作 |
| `T408-08` | 一个 target-build Codex focused installed 及两轮 update/reapply；源码、安装态、native/mock 分开记录 | 完整累计发布矩阵、真实业务生产、远端 mutation、tag/Release、tag-pinned smoke 均 unverified |

可重复验证入口：

- [Fork session regression](../../../../trellis/presets/guru-team/scripts/python/test_fork_session_isolation.py)。
- [Installed Phase 0 transcript](../../../../trellis/presets/guru-team/scripts/python/verify_installed_phase0_transcript.py)。
- [Stateful manual operation test](../../../../trellis/skills/guru-team/tests/test_manual_git_fallback_stateful.py)。

以上是已审查的 committed source 证明，不是新 commit 或本次重新运行声明。
知识 `.50 -> .51` 保留历史 bytes 与完整继承；正式 promotion 校验和后续 fresh Phase 2、Task Commit、
完整 Branch Review、Publication、push、PR、merge、Issue closure 与发布结果均不由本页推定完成。

## #418 Pre-promotion 证据与剩余门禁

来源：[#418 contribution](../../../requirements-design-test-contributions/418-closeout-identity-recovery/test.md)、
任务 implement.md 的命令记录和 [EVD-028](../../../architecture/evidence/current-evidence.md)。
以下均为知识提升前证据，不是 .54 Docs 编辑后的新测试或 post-promotion validation。

| 检查 | Pre-promotion 结果 | 证明边界 |
| --- | --- | --- |
| 完整独立 Branch Review | exact 78651e2068184e9e52a778fe33eda8b2bd7c8e0b...c30eadd6cf6fe4ba204c32c6e89f3f25f892e8f4 passed；四项 findings 已闭合 | 不覆盖随后 promotion-created diff |
| 五个 owner package 全集 | 301 passed：Finalizer 108、Merge 65、Branch Review 35、Publication 67、Architecture 26 | package/runtime 正常路径及回归 |
| focused package integration | 14 passed | package graph/contract 联接 |
| installed contract | 1 passed | 定向 installed contract，不是完整安装矩阵 |
| archived fixture staging | 3 passed，覆盖 8 个 post-owner recipes | deterministic staging/transport，不是 native AI authoring |
| installed archived chain | 3 passed | 实际 installed wrappers 与真实 DTO 联接，H/A/B、title/body/head/Ready drift、checkpoint 退休和零业务 mutation |
| source/installed/platform/reapply/drift | 已通过；Shared/Codex/Claude/Cursor 保留，最终 sidecar=0 | pre-promotion candidate 投影，不是完整 Release matrix |

可重复入口为 canonical packages 下各 owner tests，以及
[package integration](../../../../trellis/skills/guru-team/tests/test_skill_packages.py)、
[archived fixtures](../../../../trellis/skills/guru-team/adapters/eval/test_archived_fixtures.py)、
[installed chain](../../../../trellis/skills/guru-team/tests/test_archived_review_integration.py)；
入口实际路径与执行环境由当前 owner 核验，不从文档数字推导 gate pass。

fresh native 语义执行、原业务实例、完整累计/Release matrix 仍为 unverified。
主 owner 串行完成 Architecture 与 RDT promotion 后，必须对 combined promotion-created diff
重新执行 fresh Phase 2、Task Commit、完整 Branch Review，随后才可进入 Publication；
pre-promotion 结果不跨 content identity 复用。没有新增软件版本或远端完成声明。

## #419 Pre-promotion evidence 与剩余门禁

来源为 exact committed range `origin/main...0b46f0b0f7ae0e9a76dca22053a29d1835c09812`、
task contribution、`ADR-011` candidate 与 `EVD-029`。提升前已通过 continuation/activation 13、workspace
recovery 8、Phase 2 package 16、Finalizer contract 27、preset/ownership 158，以及 upstream ownership、
dogfood drift、projection byte parity、shell syntax、residue/sidecar 和 `git diff --check`。

这些结果只绑定 promotion 前 candidate。`.54` 文档写入后必须重新执行 fresh Phase 2、Task Commit和完整
Branch Review；#410 Release Gate matrix不得使用上述结果。

## #435 Pre-promotion evidence 与剩余门禁

来源为 committed reviewed HEAD `83909737ebb67fdc505d68e6bcb39acf759101c1`、#435 contribution 与 task
Branch Review。提升前已验证 Delivery packages/runtime/eval、两个顺序 Delivery、equal-head PR recovery、
resolved-tree reconciliation、trailer discovery、Refs-only/bookkeeping exclusion、canonical/installed/platform
projection、representative clean install/reapply、ownership、dogfood drift、task validation 与 diff hygiene。

| 检查 | Pre-promotion 结果 | 证明边界 |
| --- | --- | --- |
| registry/interface/commands | 26 active packages / 114 external exits / 96 commands | 三个 Delivery packages 仍 `deferred`，不证明 production activation |
| production workflow markers | 22 mandatory invokes / 98 exits | #434 前保持原图，不声明新 route 已生产启用 |
| Delivery behavior | Review/Publish/Merge package、A/B cycles、recovery 与 discovery 定向通过 | fake provider/local fixture 不是真实 GitHub 生产 mutation |
| distribution | canonical/installed/Shared/Codex/Cursor/Claude、representative clean/reapply 与 drift checks | 不等于完整多平台 Release matrix |
| lifecycle boundary | task merge 后保持 active，terminal fields/mutations 排除 | Completion/Closure/Finish/Cleanup/Reactivate 仍由 #436 拥有 |

这些结果只绑定 promotion 前 candidate。`.55` 文档写入后必须重新执行 fresh Phase 2、Task Commit和完整
Branch Review；完整 clean/existing/update/workflow-switch/release-candidate Release matrix 仍 `unverified`。

## #436 Pre-promotion evidence 与剩余门禁

来源为 #436 task contribution、独立 committed Branch Review 与当前 candidate 的定向 package/distribution
检查。Completion、Closure、Finish、Cleanup、Reactivate 五个 package 的定向 contract/runtime/eval、closed
projection、canonical/installed/platform parity、preset reapply、ownership、task validation 与 diff hygiene
已通过；live registry 为 31 packages / 136 external exits / 101 commands，production workflow 保持 22
mandatory invokes / 98 exits。

这些结果仅绑定 promotion 前 candidate，不证明 promotion-created diff 的 fresh Phase 2、Task Commit 或
完整 Branch Review；也不证明真实 Issue close、bookkeeping PR/merge、生产 Cleanup、#434 graph activation、
push、PR、远端 merge、tag、Release 或完整 Release matrix。既有 Finish-family 的三个基线失败保持原样，
不通过修改旧 Finalizer 合同掩盖。

## #443 Pre-promotion evidence 与剩余门禁

来源为 integrated committed range
`a74d729ed84449ce603d112e277fa567e87a7bf3..4dd9f7b7d4df2167819745565225001355adb5ee`、
#443 Architecture/RDT contribution与closed Issue authority。当前fresh执行canonical package contract/runtime
26 tests，覆盖profile闭集、A→B→A、跨session、base provenance、manual recovery、generation/receipt invalidation
与zero-write；live registry/interface/commands为32/142/102，production workflow为22/98，installed
interface/runtime与canonical bytes一致。

这些结果只证明#443 capability与promotion输入，不证明promotion-created combined diff的fresh Phase 2、
Task Commit或完整Branch Review，也不把当前#452 OpenCode/platform candidate倒填为#443历史证据。完整
source/installed/platform、preset reapply、ownership、dogfood drift与普通Issue representative throwaway仍需fresh执行；
完整Release matrix、#434 activation、生产binding、push、PR、merge、tag、Release与Issue closure不在本证据内。

## #452 Current acceptance 与执行边界

来源为 reviewed [#452 test contribution](../../../requirements-design-test-contributions/452-all-platform-support/test.md)
及其 [traceability](../../../requirements-design-test-contributions/452-all-platform-support/traceability.md)。
`.58` 将 `T452-01..12` 提升为 current acceptance authority。promotion 时十二项全部为
`not_executed`，这是历史快照而非当前结果；截至 2026-09-21，fresh implementation
evidence、Architecture/RDT 与 Phase 2 更新后的 current state 如下：

| Test | Current state | Required fresh proof |
| --- | --- | --- |
| `T452-01` | `passed` | pinned 22-platform inventory、descriptor identity 与 source closure 均通过 |
| `T452-02` | `passed` | 旧 option/state 删除及写前拒绝通过；活动代码无公开 `--all-platforms` 合同 |
| `T452-03` | `passed` | repeated exact subset、重复归一化与 unknown id 拒绝通过 |
| `T452-04` | `passed` | 无参数三平台默认、显式 subset 与 removed-option 拒绝通过 |
| `T452-05` | `passed` | default/explicit/upgrade 两层边界通过 |
| `T452-06` | `passed` | exact installed selection provenance/replay 与非法输入拒绝通过 |
| `T452-07` | `passed` | dogfood/reapply/drift 精确为 Claude、Codex、Cursor |
| `T452-08` | `passed` | OpenCode 显式 install/provenance 与 1.18.30 representative actual-load 通过 |
| `T452-09` | `passed` | 22 descriptors canonical/installed/native/ownership parity 与 private-test 排除通过 |
| `T452-10` | `passed` | reapply/update/removal/drift、正常修改与 sidecar 行为通过 |
| `T452-11` | `passed` | Codex focused clean/update/reapply、selected subset 与 hygiene 通过 |
| `T452-12` | `in_progress` | fresh RDT 已完成；Task Commit、完整 Branch Review 与后续门禁待执行 |

fresh evidence 包括核心五模块 `180 passed`、Finalizer provenance `20 passed`、workflow mode 与
extension verification `22 passed`、throwaway Python routing `44 passed`、ownership/dogfood checks、
OpenCode actual-load，以及 Codex focused clean/update/reapply。未执行 22-client native matrix；除
OpenCode 与 Codex 代表性验证外，外部平台 CLI actual-load 保持 `unverified`。正式 release/tag/GitHub
Release、tag-pinned smoke、业务仓库生产升级与 #434 production graph activation 继续独立且未验证。

## #454 Promotion-time evidence 与后续门禁

Promotion 输入绑定 exact range
`0381f4ee060398f42bd2dded6ec14d7fced21393...4421662f17b2b3adcfd3faeec6fd782d11bc947f`。
提升前 fresh evidence 包括 lifecycle runtime `22 passed`、Reconcile package `34 passed`、base-continuity
integration `3 passed`、active continuation `7 passed`、Reactivate `17 passed` 与 created-Issue provenance
`1 passed`；同时通过 selected-base ancestry、canonical/preset/dogfood parity、source identity、task validation、
JSON/Python checks、zero `.trellis/scripts/**` diff 与 `git diff --check`。

两个 base-identical 全局 observation 属于 #454 range 外既有问题，记录为 `rejected_out_of_scope`，不写成
本 task 通过项。`.59` promotion diff 完成后必须 fresh 执行 Architecture/RDT task-impact、normal-scenario、
solution-mechanism、Phase 2、Task Commit 与完整 committed-range Branch Review；在这些门禁完成前不得进入
Publication。C3-C7、D443、D436、E434、完整 installer/upgrade/Release matrix 与生产 mutation保持未验证。

## #454 C3 Promotion-time evidence 与后续门禁

Promotion 输入绑定 exact range
`9c2238bad7e73ea4a1f23dddcb7e8e9204c244da...e965b7e8b6850614a2cd21f899a02b3ea9da73f3`。
提升前 focused evidence 包括 lifecycle runtime `51/51`、39 named DTO Draft 2020-12 validation、live checkout
discovery/acquisition、identifier/error contract、planned ownership、source/installed-active、task/workspace、compile、
static zero legacy/path-authority、line-limit 与 `git diff --check`。

Global package suite 为 `19/20`，unchanged `guru-complete-task-closure` relative-ref defect 在 C3 range 外；preset
suite 为 `85/86`，raw apply 因 C3 禁止同步 installed projection 而报告 conflict。两项 suite 都不写成通过。
`.60` promotion diff 完成后必须 fresh 执行 Architecture/RDT task-impact、Phase 2、Task Commit 与完整
committed-range Branch Review。C4-C7、D443、D436、E434、完整 Release matrix 与生产 mutation保持未验证。

## #454 C3 Provenance Promotion-time evidence

Promotion 输入绑定 `9c2238bad7e73ea4a1f23dddcb7e8e9204c244da...b816aca8d6520bf90c52c6210ff3155174da86f3`。
Focused evidence 为 checkout `27/27`、task lifecycle `56/56`、compile、JSON、ownership、task/workspace、static/line/diff checks。
Package `19/20`、shared runtime `119/128`、lifecycle integration `38/44`、preset 272 with 2 errors/3 skips 与完整 Release matrix不声明通过。

## #454 C4 Promotion-time evidence 与后续门禁

Promotion 输入绑定 exact range
`77fa1a2250998ad8c71f0fffedf9a99a15a76dec...c7fab600e6e29385c23c276ac2b1828d0465fd77`。
独立完整 Branch Review 的 P0/P1/P2/P3 为 `0/0/0/0`。Admission 时，`BR454-C4-P3-001` 在
`6ab9dde1385c03f406ef3663e61dd010533462b7` 为可复现的 `qualified_finding`，并由
`c7fab600e6e29385c23c276ac2b1828d0465fd77` 修复闭环；随后针对修复后的 current supported path 重新执行
qualification，normal-scenario 返回 `classified / rejected_not_reproduced`，solution-mechanism 返回
`classified / qualified_current`。

Fresh focused evidence 为 task-lifecycle runtime `93/93`、Python compile、task validation、`git diff --check`
与 touched non-generated file line checks。Task validation 将不存在的可选 `implement.jsonl`、`check.jsonl`
标为 skipped；generation 2 的真实 common-dir binding 仍不存在，测试没有写入 live task control state。

Preset Python suite 的既有结果为 `85/86`，唯一错误来自 E434 前刻意未同步的 installed task-lifecycle
README/schema/registry sidecars；该 broader suite 未在 narrow finding-fix 中重跑，未声明为通过。`.62`
promotion diff 完成后必须 fresh 执行 Architecture/RDT task-impact、Phase 2、Task Commit 与完整 committed-range
Branch Review。C5-C7、D443、D436、E434、完整 Release matrix 与生产 mutation 保持未验证。

本 promotion 的 Finalizer provenance source binding 还必须消费 `TST-032/SCN-044`：新增执行级 fixture 证明真实
Git predecessor/reviewed graph 下 strict historical ancestor 可继续，replacement transaction 保存 exact
`pre_push_remote_head`，后续 pre-mutation preflight 使用同一 remote identity，且 push/PR/archive/Issue mutation
保持为零。该 evidence 只闭合现有 Finalizer authority，不替代 promotion-created diff 的 fresh Phase 2、Task
Commit 或完整 Branch Review。

`FIN454-C4-P1-002` 的 required evidence 继续归属 `TST-032/SCN-044`：正式
且 identity-matched 的 `ordinary_publication/push_content` transaction 是 current owner；无 Open PR 时，同
branch/base terminal PR 只作为历史事实。remote exact `pre_push_remote_head` 证明单次 fast-forward，remote exact
`publication_head` 证明 push-output-loss/converged recovery；allowed heads 外的 remote、ahead/diverged/unknown、
Open PR drift 与 transaction identity drift 均 fail closed。证据不得依赖宽泛 fallback、PR 人工选择、force push、
第二 ledger 或删除 transaction。当前 recovery `47/47` 与完整 Finalizer package `111/111` 通过；Python compile、
canonical/dogfood parity、task validation 与 `git diff --check` 同时通过。该 evidence 不替代 fresh Phase 2、Task
Commit、Branch Review、Publication 或 Finalizer gate。

`FIN454-C4-P1-004` 继续使用 `TST-032/SCN-044`：真实 Git topology 必须包含 predecessor reviewed commit、合法
manifest-only Publication tail 与两个 same-base finding-fix commits；current review/Publication/live HEAD 相等且
严格后继，selected base 已在 predecessor lineage。分别验证无 Open PR 时 terminal PR inventory 不参与 current
classification、exact `pre_push_remote_head` 与 exact `publication_head` 可恢复、Open PR 与 intermediate reviewed
remote 拒绝，以及 replacement transaction 绑定 current plan 与实际 observed remote。不得使用 path、session、
branch-name guess、人工 selector 或 fallback 作为证明。
