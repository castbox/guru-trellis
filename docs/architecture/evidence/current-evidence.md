# EVIDENCE

| Evidence ID | Class | Locator / identity | Supports |
| --- | --- | --- | --- |
| `EVD-001` | current source baseline | reviewed #332 contribution `architecture-contribution-332-release-wrapper-entry-correction-v1` + inherited `.44` authority；精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD | `ARCH-CUR-001..004,006..009,013..022` |
| `EVD-002` | stable release | annotated tag `v0.6.15-guru.4`；tag object `6e71362d9fdce5377431ba6b2923334299c7e08f`；peeled commit `40f8aa8312bfd9650f47e1fa9d6d21b4ff18d5b6`；extension `0.6.15-guru.39`；target/required/tested Trellis CLI `0.6.15`；non-draft/non-prerelease/zero-asset Release | `ARCH-CUR-005` only |
| `EVD-003` | RDT package | Issue #263 CLOSED；reviewed `d53335a7…`；archive `eaf955e0…`；PR #279 merge `891c2147…` | `ARCH-CUR-003` |
| `EVD-004` | Architecture package | Issue #264 CLOSED；reviewed `1cb2506b…`；PR #268 merge `37fdfe63…`；metadata head/merge `991080b6…` / `3b0f78c1…`；无 `finish-summary.json` | `ARCH-CUR-003` |
| `EVD-005` | Bootstrap package | Issue #265 CLOSED；reviewed `f2c67098…`；archive `de1c6e26…`；PR #280 merge `3c0d4a2f…`；archive/merge tree `45e8b402…` | `ARCH-CUR-003` |
| `EVD-006` | Bootstrap closeout | Issue #266 CLOSED；PR #281 merge `c2b1784654a95b999bbff71daf1393c22aa01048`；archive/merge tree `cb68fead327cc2cfb6ea03b8e81affcb9b7ad0e9` | active RDT/Architecture baseline |
| `EVD-007` | replacement release | Issue #275 CLOSED/COMPLETED；PR #282 rebase merge；review/archive head `83646987…`；merge/live main `5c059f49…`；post-tag install/version/closeout smoke 与 isolated consumer proof passed | `ARCH-CUR-005,007` |
| `EVD-008` | six-cell compatibility | `claude|codex|cursor × clean|existing` 6/6；capability comparison 覆盖 `workflow`、`task_data`、`docs_authority`；独立 consistency/installation comparison 覆盖 Skill API/schema/command、distribution/installed inventory、三类 mode、template hash、sidecar 与 extension identity；final runtime matrix 绑定完整 dirty candidate `source_state` 与 post-archive non-empty history；精确 tree/digest 不写回 tracked docs | `ARCH-CUR-008..009`, `ARCH-INT-006` |
| `EVD-009` | real GitHub A | disposable PR #2 source `6a7b721a…` -> rebase merge `a5c73c49…`；Issue #1 merge 后 CLOSED/COMPLETED；provider recovery 与 remote cleanup/reachability passed | `ARCH-CUR-010`, `ARCH-DOM-007` |
| `EVD-010` | focused compatibility | installed lifecycle 1/1；upgrade contract 20/20；preset/ownership 83/83；managed Python routing 44/44；RDT/Architecture/Bootstrap installed profiles passed | `ARCH-CUR-008..009` |
| `EVD-011` | #283 reviewed task range | base `2d34abfc…` -> reviewed task head `86a2cc1a…`；5 commits / 429 paths；schema 6.0 independent Branch Review PASS，open findings zero | `ARCH-FND-006`, `ARCH-GOV-006..008`, `ARCH-DOM-008`, `ARCH-INT-007`, `ADR-005` |
| `EVD-012` | #283 representative clean install | Trellis `0.6.15` + public marketplace bootstrap + exact local committed workflow + all-platform preset；21 packages / 72 commands / 4229 managed files，update/reapply/drift/sidecar checks passed | `ARCH-CUR-011..012`；local pre-push only，不是 formal verifier/release proof |
| `EVD-013` | #283 reviewed promotion | Architecture/RDT contribution locators、expected `.37`、successor `.38`、design constitution/change contract/ADR/history/traceability 与 serialized owner gate | `.38` current knowledge authority；post-promotion Phase 2/commit/Branch Review 必须 fresh 绑定最终 HEAD |
| `EVD-014` | #290 reviewed task and promotion | base `ec4df880…` -> reviewed task head `d4165f26…`；57 paths；fresh Architecture Branch Review 与 schema 6.0 independent Branch Review 均 passed，三个正常路径候选不再复现；expected `.38` -> successor `.39` serialized promotion | `ARCH-CUR-013`, `ADR-006`；post-promotion Phase 2/commit/Branch Review 必须 fresh 绑定最终 HEAD |
| `EVD-015` | #311 reviewed task and promotion | base `d907fcc5…` -> reviewed task head `651defee…`；7 commits / 85 paths；Architecture 与 distinct fresh-final Branch Review passed，open P0-P3 zero；Finalizer 59/59、verifier 17/17、routing 44/44、ownership 7/7、upgrade 36/36、preset 81/81；expected `.40` -> `.41`，contribution digest `a6e2835e…` | `ARCH-CUR-014..015`, `ARCH-DOM-009`, `ARCH-INT-008`, `ARCH-GAP-007`, `ADR-007`；真实 fixture/Publication/Finalizer/生产发布/错误文件重试仍 `unverified`，Issue OPEN |
| `EVD-016` | #267 reviewed release-authority alignment | base `3efcce72…` -> contribution head `d3dca74b…` -> promotion `351e61d1` -> r19 fix `490b302a` -> archive head `9ceeede2`；post-promotion fresh Phase 2、task commit、independent Branch Review、PR readiness 与 Finalizer passed；PR #315 merge/live main `a41b8a34`；RDT/Architecture contributions 绑定 expected `.41`、successor `.42`、extension `.39` 与 CLI `0.6.15` | `ARCH-CUR-004,008,016`；`a41b8a34` post-merge full-diff review 发现 P2 `BR-267-FULL-CAND-001`，修复 merge 后必须重新 freeze candidate 并 fresh review；#267 exact-candidate Release gates 与 #311 post-release proof 仍 `unverified` |
| `EVD-017` | repository-private release orchestration source | `.agents/.codex/.claude/.cursor/skills/release-guru-trellis-version/`、repo-private contract tests、canonical/current-checkout Finalizer owner 与 `docs/requirements-design-test-contributions/335-release-guru-trellis-version/` | `ARCH-CUR-017`, `ARCH-DOM-010`, `ARCH-INT-009`；只证明 current source locator 与 owner boundary，不替代 Publication、Finalizer、tag、smoke、GitHub Release 或 Issue closure live evidence |
| `EVD-018` | #332 release-current authority contribution and promotion | live Issue #332、`docs/architecture/contributions/332-release-v0615-guru5.md` 与 `docs/requirements-design-test-contributions/332-release-v0615-guru5/`；Architecture/RDT serialized owners 已分别完成 expected `.43` -> successor `.44` promotion，target `.5`、extension `.40`、CLI `0.6.15` | `ARCH-CUR-004,005,008,018`；只支撑 current-fact alignment 与 knowledge promotion，fresh Phase 2/commit/Branch Review、post-merge exact-candidate Release Gate、tag、Release 与 smoke 均未由本 evidence 证明 |
| `EVD-019` | #240 reviewed mechanism owner | Issue #240 CLOSED；PR #346 merged `2bafec11…`；PR body 记录独立 Branch Review `passed`、P0-P3 open findings 0；Architecture contribution 与 accepted ADR-008 已由 #332 promotion 纳入 `.44` current | `ARCH-CUR-019`, `ARCH-DOM-011`, `ARCH-INT-010`, `ADR-008`；不替代 #332 exact-candidate Release Gate |
| `EVD-020` | #348 reviewed archived-task recovery | Issue #348 CLOSED；PR #351 merged `5c6837b8…`；完整 `1fd63dab…0dd42063` Branch Review `passed`，fresh Architecture Branch Review `baseline_current` | `ARCH-CUR-020`, `ARCH-DOM-012`, `ARCH-INT-011`；不替代 #332 exact-candidate Release Gate |
| `EVD-021` | #332 original-entry correction and promotion | exact committed range `8a6e04eb…014c71ac`；initial Phase 2 与 independent Branch Review passed，open P0-P3 zero；affected package 9/9、restore 23/23、installed closeout 5/5、restore shared eval 8 scenarios、preset 85/85、source/installed/all-platform/reapply/drift/sidecar checks passed；reviewed RDT/Architecture contributions bound expected `.44` and promoted `.45` | `ARCH-CUR-001,021..022`, `ARCH-DOM-013`, `ARCH-INT-012`；promotion-created diff 必须 fresh Phase 2/commit/Branch Review，且不替代 post-merge exact-candidate Release Gate |
| `EVD-022` | #376 base-continuity contribution and promotion | exact committed range `e339d994…29ffa01b`；fresh Architecture Branch Review 与 official independent Branch Review passed，open P0-P3 zero；Reconcile、Review Branch、Finalizer、Publication、real cross-Skill integration、clean install、source/installed/platform parity 与 23/97/78 graph checks passed；reviewed RDT/Architecture contributions bound expected `.45` and promoted `.46` | `ARCH-CUR-023`, `ARCH-DOM-014`, `ARCH-INT-013`；promotion-created diff 必须 fresh Phase 2/commit/Branch Review；Issue #108 installed drift、full release/upgrade matrix 与 remote publication 均不由本 evidence 证明 |

`EVD-008` 的 matrix object 保留 `external_boundaries` 与
`real_github_verified:false`；它只证明六-cell与 local A/B。最终精确
`source_state.candidate_tree`、source identity 与 matrix digest 留在 runtime/conversation
evidence，避免 tracked evidence 对 candidate tree 形成自引用。
`EVD-009` 是独立完成的真实 provider evidence。当前 authority 组合消费两类证据，
不声称任何 matrix JSON 已被改写，也不构造伪造的 combined artifact。

`EVD-023`：#378 精确 `a2b32ea8dc730eecf0507e0adfb946ce9b8c7bc8...5f7a8a9a8d6d74f35c3fce10439fda9846508c57`
范围已通过 independent fresh-final Branch Review 及正式 checker/public wrapper。
它支撑 `ARCH-CUR-024`、`ARCH-INT-014` 与 `.47` contribution promotion：固定 Fork 源码与
installed 字节一致；canonical/installed isolation、#388/#389 integration、真实 focused clean
和两次 update/reapply 通过；三平台 reapply 无漂移，备份已保留。fixture provider closeout
不等于真实远端发布。完整历史矩阵、真实业务接续与独立 TypeCheck 未验证。

`EVD-024`：#392 reviewed candidate inputs 包含 live Issue/task planning、
`docs/architecture/contributions/392-release-v0616-guru1.md` identity
`architecture-contribution-392-release-v0616-guru1-v2`、五文件 RDT contribution、固定 Fork source lock、
current delivery mapping 与 pre-promotion 独立完整 Branch Review。它支撑 `ARCH-CUR-025`、
`ARCH-INT-015` 以及 expected `.47` -> `.48` serialized promotion；只证明 promotion 输入已通过既定
review boundary，不证明 promotion-created diff 的 fresh Phase 2/commit/Branch Review、Publication、merge、
exact-candidate Release Gate、tag、tag-pinned smoke、GitHub Release、business smoke 或 Issue closure。

`EVD-024` 建立的 `.48` 现为 immutable superseded authority；其 #392 promotion 与 release evidence
边界保持历史事实，不由 #329 改写。

`EVD-025`：#329 reviewed candidate inputs 包含 live Issue/task planning、
`docs/architecture/contributions/329-adopt-developer-free-trellis.md` identity
`architecture-contribution-329-developer-free-trellis-v1`、五文件 RDT contribution、fixed Fork source lock、
official `0.6.17` generated adoption、focused consumer migration、legacy preservation、three-platform installed
lifecycle、clean committed candidate provenance，以及 pre-promotion independent full Branch Review。它支撑
`ARCH-CUR-026`、`ARCH-INT-016` 与 expected `.48` -> `.49` serialized promotion；只证明 reviewed
promotion inputs，不证明 promotion-created diff 的 fresh Phase 2/commit/Branch Review、Publication、push、
PR、merge、tag、Release、remote marketplace publication、business production 或 Issue closure。

`EVD-025` 建立的 `.49` 现为 immutable superseded authority；其 #329 framework source、CLI、package
manager、extension 与 released axis保持 current inherited facts，不由 #247 改写。

`EVD-026`：#247 current inputs 绑定 live Issue r24、task/RDT planning、
`docs/architecture/contributions/247-remove-issue-scope-ledger.md` identity
`architecture-contribution-247-remove-issue-scope-ledger-v1`、accepted `ADR-009`、active-zero ledger
inventory、旧流程Publication/Finalizer/Merge/Restore回归、legacy inert、capability与canonical/dogfood/
installed/platform parity。r19 target-native review range仅为历史过程证据；r24 corrective commit后必须fresh review。
它支撑 `ARCH-CUR-027`、`ARCH-DOM-015`、`ARCH-INT-017`、`ARCH-GOV-009`、`ARCH-GAP-008`、accepted
`ADR-009` 与 expected `.49` -> `.50` serialized promotion；只证明 reviewed promotion inputs，不证明
promotion-created diff 的 fresh Phase 2/commit/Branch Review、Publication、push、PR、merge、tag、Release、
完整多平台 exact-candidate matrix、business production 或 Issue closure。

`EVD-027`：#408 的已审查输入绑定精确提交范围
`8bb16516e211e9bd7b9560c025fe48a18fee0fb3...18df89680b9eae187b2b23c543ba08304212e211`、
当前 Issue/task/RDT contribution 与固定 `db4ca1df...` / CI `34838784963` 来源。独立完整 Branch Review
及正式 checker/public wrapper 通过；来源/build/CI、197 个构建模板、17 个官方脚本/hook 字节、
source/dogfood/installed 投影与当前 23/97/78 图已核对。正常 authoring 经实际 wrapper 创建双端 mapping，
脚本与文档澄清后的 native 演练均完成受控激活和双端 context/hook 检查；这些调用的 GitHub/fetch
为 mock，不证明宿主自动 hook 分发或真实远端 mutation。它支撑 `ARCH-CUR-028`、`ARCH-INT-014/016`、
`ARCH-DOM-015` 的 Guru/独立操作边界及 `.50 -> .51` 知识提升，不证明软件发布或完整升级矩阵。

上述 #408 历史 promotion 的 knowledge successor 为 `.51`，predecessor 为 `.50`。
旧 source pin 的证据保留历史用途，pin/CI 的来源证据由 `EVD-027` 承接；该历史范围的 CLI/core、package manager、
23 Skills / 97 exits / 78 commands、extension `0.6.16-guru.41` 与 released `v0.6.16-guru.1` 保持独立版本轴。
promotion-created combined diff 仍须 fresh Phase 2、
task commit 与完整 Branch Review，后续远端动作由各 live owner 独立验证。

## EVD-028: #418 Reviewed Promotion Source

本证据支撑 `ARCH-CUR-030`、`ARCH-INT-018`、`ADR-010` 及 `.52 -> .53` 知识提升。
提升前独立完整 Branch Review、正式 checker 和 public wrapper 已针对
`78651e2068184e9e52a778fe33eda8b2bd7c8e0b...c30eadd6cf6fe4ba204c32c6e89f3f25f892e8f4`
通过，四个已记录 finding 已关闭。该范围固定了当前 source contract，不是提升后新 diff 的通过证明。

| 层级 | 提升前已验证事实 | 边界 |
| --- | --- | --- |
| package | Finalizer 108、Merge 65、Branch Review 35、Publication 67、Architecture 26，共 301 tests fresh 通过 | 包含恢复后的普通 4.0/7.0 与 additive 5.0/archived-1.0 合同测试，不以旧 pass 代替 |
| focused installed | installed 合同 1、包/投影 14、archived fixtures 3、installed chain 3 通过 | 实际 wrappers/DTO、三段 Architecture、H/A/B、PR/base drift、checkpoint retirement 与零业务 mutation；post-owner fixtures 不证明 native 语义 |
| distribution | 23 packages / 100 exits / 78 commands；4872 package files 与 3 overlays 的 source/hash/mode 一致，三平台投影及零 sidecar | 缓存不属于分发；不证明远端 tag-pinned 安装或完整升级矩阵 |
| authority | source contribution `418-archived-review-refresh-v1` 与 R418/D418/T418 链完整 | shared successor 为 `.53`，不是新的软件版本 |

独立检查还确认 39 份原 profile/output schema 与基线一致，普通 mutation 与旧 gate 拒绝行为不放宽。
文档修复产生过真实合同测试失败，修复后重新执行上述测试；不能仅因 runtime 文件未变就跳过
读取 Markdown 的合同测试。具体稳定测试入口位于 canonical package tests 和
`trellis/skills/guru-team/tests/test_archived_review_integration.py`。

Native 归档语义执行、原业务实例、完整多平台 upgrade/Release matrix 仍为 `unverified`。
Promotion-created diff 的 fresh Phase 2、task commit、distinct complete Branch Review 以及后续
Publication、push、PR、merge、tag、Release、Issue closure 均不由本提升前证据推定完成。

## EVD-029: #419 Reviewed Promotion Source

本证据支撑 `ARCH-CUR-031`、`ARCH-DOM-016`、`ARCH-INT-019`、`ARCH-GOV-010`、`ADR-011` 与
`.53 -> .54` knowledge promotion。提升前独立完整Branch Review绑定
`f5ebf9f92b0f174b48f6c8ed04038eb32a5f054e...0b46f0b0f7ae0e9a76dca22053a29d1835c09812`
并通过正式Architecture与review wrappers；activation pre-validation、完整successor subtraction和bytecode
residue三个findings已在同一current candidate闭合。

定向证据包括 continuation/activation 13、workspace recovery 8、Phase 2 package 16、Finalizer contract 27、
preset/ownership 158，以及exact upstream candidate identity、extractor/continuation/thin-entry tests、source/
installed runtime、真实Git/task fixture、projection parity、ownership、dogfood drift、sidecar/residue与diff检查。
这些结果不包含throwaway、install/update/workflow-switch/preset-reapply Release Gate matrix；该完整证明由#410
在#419 merge后的fresh main独立建立。Promotion-created diff仍须fresh Phase 2、Task Commit和完整Branch Review。

## EVD-030: #435 Reviewed Promotion Source

本证据支撑`ARCH-CUR-032`、`ARCH-DOM-017`、`ARCH-INT-020`、`ARCH-GAP-009`、`ARCH-GOV-011`、
`ADR-012`与`.54 -> .55` knowledge promotion。提升前独立完整Branch Review绑定
`a410a97fad127b9cc9bce1680666f6149d3ba616...83909737ebb67fdc505d68e6bcb39acf759101c1`；
review发现的Publish recovery、closing keyword、terminal recovery、closed public schema、resolved-tree
first-parent tree与active command count问题均已在同一committed candidate闭合。

定向证据包括canonical/installed Delivery Review、Publish、Merge与Reconcile package tests，重复Delivery、
deleted-head-branch、Reactivate-style binding、bookkeeping exclusion、identity drift、#405 equal-head recovery、
#407 resolved-tree commit及cross-package integration；preset apply/reapply、upgrade contract、ownership、package
closure、source/installed/platform parity、dogfood drift、task validation与diff checks通过。active registry聚合为
26 packages / 114 package exits / 96 commands；production workflow保持22 mandatory invokes / 98 exits。

上述证据不激活production graph，不实现或验证#436 Completion、Closure、Finish、Cleanup、Reactivate，也不把
继承的Finish-family失败声明为通过。完整多平台Release matrix仍为`unverified`。Promotion-created diff仍须
fresh Phase 2、Task Commit与independent complete Branch Review；后续Publication、push、PR、merge、Release与
Issue closure均不由本提升前证据推定完成。

## EVD-031: #436 Reviewed Promotion Source

本证据支撑 `ARCH-CUR-033`、`ARCH-DOM-018`、`ARCH-INT-021`、`ARCH-GAP-009`、`ADR-013`
以及 `.55 -> .56` knowledge promotion。#436 contribution
`architecture-contribution-436-post-delivery-completion-finish-v1` 已完成独立 committed full-diff
review，RDT/Architecture promotion 绑定 expected `.55` 与 successor `.56`。

candidate 的五个 lifecycle packages、closed public contracts、owner-private recovery、canonical/
installed/platform projections、task/lifecycle SSOT 与定向 tests 已通过；live registry 为 31 packages /
136 external exits / 101 commands，production workflow 保持 22 mandatory invokes / 98 exits。

本证据不证明 #434 production graph activation、真实 Issue close、bookkeeping PR/merge、生产 Cleanup、
完整 Release/upgrade matrix、push、PR、远端 merge、tag、Release 或 Issue closure。promotion-created
diff 仍须 fresh Phase 2、Task Commit 与 independent complete Branch Review 后才能进入 Publication。

## EVD-042: #434 atomic lifecycle activation candidate

本证据支撑 `ADR-016`、`ARCH-CUR-044`、`ARCH-DOM-029`、`ARCH-INT-032` 与
`ARCH-GAP-009/011` 的 current activation 子缺口。#434 在 selected
`origin/main@bab8cfcd534692735b9240b25dd8bc63e40a5cb4` 上消费 #435/#436/#443
与 #454 D443/D436 exact interfaces；七个 E434 packages 与 active graph/selector/manifest/
installed/声明平台投影为同一候选。旧归档按 Issue 查找验证唯一已提交终态；旧链在途任务
只允许 pinned-old 或人工处置，#154/PR #156 不是新 Delivery。

当前 Fork 锁从历史 `eb370008`、PR #10 的 `c49ad996` 前进到合并提交
`645c817e4830a44564b0dc43b2adf75e306b1e81`、tree
`0845f24e9f22cbca524370887166e183b454c147`、成功 push CI `36312060945`。
PR #11 在旧 checkout 留有同 TaskId/代次副本时使用正式绑定分支的注册 checkout；
Fork CLI `2303/2303`、core `422 passed/1 skipped`、build/typecheck/lint 及 PR/main CI 通过。
#434 dogfood 的官方 session resolver 已按新模板更新；组合 source/installed、preset reapply、
零 sidecar 与本地续接场景需对新锁重验，不沿用 PR #10 的旧候选结果。
新锁下 source/installed validator 已分别通过（34 active / 104 commands；33 invokes /
153 production exits，零 sidecar）；本地 Codex clean/focused 样本两次 update/reapply
及 session binding 通过，当前图/文案 28/28，现行 Stage 0 readiness 初装/reapply
1/1。广义 installer 旧 fixture 的 Workspace `ready` consumer 与现行
`guru-task-intake-router` 不同；旧 Workspace/Finalizer/parallel-Finish 链仅作 pinned-old
证据或人工处置，不可凭旧测试失败恢复退役 API，也不可将其视为现行 gate 通过。
最终组合 gate、两轮全新只读审核和正式 Phase 2/Branch Review 尚需刷新。
首轮全新审核发现 Finish 归档仍留下当前代 session pointer，妨碍按 Issue 发现已归档原 task；该 P1 使连续无 finding 计数归零。修复在 canonical Finish 投影前精确清除当前 TaskId/代次指针，缺官方 API 时保留 active task 并阻断；其他 TaskId 指针保留，未封存投影只回到原 Finish transaction 或逐案人工处置。定向 Finish 3/3、路由文案 1/1 通过；installed 投影与完整候选门禁尚未刷新。
修复后的投影经二次 apply 收敛，六个本轮生成的旧版 Finish `.bak` 清理后零 sidecar，workflow 字节和 dogfood drift 一致。Finish/Cleanup/Reactivate 55/20/35、图/终态/续接 97/97、runtime 88 pass/1 skip、installer/upgrade/reapply 99/99、source/installed validator、task validate 与 diff check 通过。较宽本地入口组 149 pass/2 skip/1 fail；唯一失败是 pinned-old `test_installed_closeout_owner_boundary` 的六步 Workspace/Publication fixture 在新安装中找不到已退役脚本，不当作新图失败也不声称全组通过。独立连续审核和正式后续门禁仍待刷新。

后续全新审核发现无 context key 的单会话 fallback 可从另一个注册 checkout 借用 task。
`castbox/Trellis` PR #12 已将 fallback 限定为调用工作树，合并为
`main@80ffa4efb6040572c15e7597eb1ecc3732096c68`（tree
`69ab91d009857735f08dffdf8190accf820da71d`，main CI `36321117001` 成功）。
#434 安装侧 linked-worktree 回归先在旧 resolver 上失败、按新模板同步后通过；
显式 context key 的跨 worktree 路径保持原样。本次 source lock 提升使此前组合和审核
结果失效，须重新验证、正式 Phase 2、Task Commit 及独立 Branch Review。

promotion 前组合 gate：installer/graph `118/118`、定向 runtime `132/132`、宽扫
runtime/graph `155/155`，此前完整 runtime `333/333`；source/installed、dogfood
drift、task validation、diff check、代表性本地 clean install、两次 reapply 和递归零
`.new/.bak` 均通过。对同一未提交候选的两轮独立只读审核连续无 P0-P3；首个
`origin/main...HEAD@ce8158ef4f6b99d73faa5c3e6a2b97f6a5be43c8` 的正式
Phase 2、九维 Check 和 committed Branch Review 亦通过，但均早于此次 RDT/
Architecture promotion-created diff，不能跨 SHA 复用。后者必须 fresh Phase 2、
Task Commit、完整独立 Branch Review 后才可 Publication。远端 marketplace 安装
非 #434 使用路径；完整多平台 Release matrix 和业务仓生产验证不由本证据证明。

Fork PR #12 的无 key 跨工作树 fallback 修复后，当前锁为
`80ffa4efb6040572c15e7597eb1ecc3732096c68`、tree
`69ab91d009857735f08dffdf8190accf820da71d`、成功 main CI `36321117001`。
T434-38 在旧 resolver 上复现借用，在新模板上通过；显式 key 路径不变。
本地初装与二次 reapply、source/installed、dogfood drift、零 sidecar、
生命周期 197 pass/2 skip、现行图 91 pass/1 skip、installer/upgrade 98/98、
#434 29/29、Task Validate 与 diff check 通过。旧 predecessor 的四项失败仍为
pinned-old 夹具与现行终态已退役合同，不纳入新图 pass；旧 #154/PR #156
只允许兼容旧版或逐案人工处置。此条不证明新的正式 Phase 2、完整 Branch Review、
两轮独立审核、live Delivery 或专门 Release matrix，以上均需独立取证。

2026-09-27 首位新鲜只读审核指出 current RDT/Architecture 的 installed 索引仍绑定
`.66` 与旧 Fork `eb370008`（P2）。两处索引已对齐 `.67`、34/155/104、33/153
及 `80ffa4ef`；canonical/dogfood data contract 也统一到同一 source lock，新增四份
current 文档、design manifest 与双 source lock 一致性回归。#434 定向候选 38/38，
重投影后 30/30、dogfood drift、diff check 与零 `.new/.bak` 通过。先前两轮
审核不覆盖这些编辑，连续无 finding 计数重置；正式 Phase 2/Branch Review 未复用。

后续独立只读审核指出两个正常路径缺口：显式跨工作树 session 的 Phase Index 与
continuation 从不同 workflow 读取（P2），以及新 TaskId 被旧 slug 的官方创建预检
阻断（P3）。#434 的 `get_context.py` 现在对两种 mode 使用相同 task checkout，
端到端双 workflow 夹具通过。Fork PR #13 合并为
`castbox/Trellis/main@622179c2b47a022134f867433518a399f7f183db`，tree
`e740f6b7c4de7791691e8f1d2d1d139dee7568d3`，main CI `36326723322`
成功；官方 create 可选 `--task-id`，默认 slug 语义不变，显式 ID 在创建前验唯一。
Fork 完整提交钩子 CLI 2305/2305，build/typecheck/lint 成功。#434 固定新锁，
官方双脚本与合并模板字节一致，Guru Create Task 直接传入审核过的 TaskId 并验证
初始 artifact；定向 33 pass/1 skip。一次 preset apply 产生且只产生本轮旧 Create Task
runtime 的一个 `.bak`，逐项核对并清除后第二次 apply `ok`，source/installed
validator、drift 和零 sidecar 通过。两轮全新独立审核、正式 Phase 2/Task Commit/
完整 Branch Review、live Delivery 与专门 Release matrix 尚未由此证明。

Fork PR #14 合并到 `castbox/Trellis/main@9d14daf4f92d28ad38b7ceb8eb0817b76aca8794`，tree
`356035b50e35302ea7542abcbc84b89674f60a7f`，main CI `36329643951` 成功。
显式 `--task-id` 在官方创建前拒绝与 Guru lifecycle 不兼容的 ID；通用 `task.py start`
保留普通 Trellis 行为，Guru 安装的三平台 `trellis-meta` 入口明确使用
`guru-activate-task`。Fork 非 marketplace CLI `2277/2277`、build/typecheck/lint
通过；marketplace 测试不是 #434 使用路径。#434 的新 source lock、投影与 `T434-39`
须在完整候选组合 gate 和 fresh 独立审核中重新验证；此段不证明 Phase 2、committed
Branch Review、Delivery、专门 Release matrix 或业务生产。

Fork PR #15 合并到 `castbox/Trellis/main@71f43cd8955c676f8ab8215216f61376fe9c01fe`，tree
`c2b523b40a3bd59a715d26017cf61bfef47b3b0a`，main CI `36332562361` 成功。
固定 Fork 的 `get_context.py --mode continuation` 与 `phase` 现从同一显式绑定
task checkout 读取 workflow；提交钩子 CLI `2306/2306`、core `422 passed / 1 skipped`，
build/typecheck/lint 通过。#434 的 installed 脚本与精确 Fork 模板 byte parity 和
current Requirements source pin 回归须在修复候选组合 gate 中重验；远端 marketplace
不在本任务使用路径。此修复不替代正式 Phase 2、committed Branch Review 或 Release matrix。

## EVD-041: #454 D436 canonical package candidate

来源为 [D436 contribution](../contributions/454-task-lifecycle-d436.md)、#456 `436-*` migration rows
与 generation 6 的五个 canonical package。Finish 的真实两父 merge/PR-head resource seal、Cleanup 的
common-dir ledger 与 machine-handoff、Reactivate generation 独立性是本增量的重点验证对象。
本切片 fresh 五包与共享 runtime 合跑 `206/206`，package integration `20/20`，source validator
`passed`（32 packages、102 commands），task validator 与 `git diff --check` 通过；
本记录不以历史 #436 package tests 或 D443 result 冒充 `.66` 的提交后完整 Branch Review。
`ARCH-CUR-043`、`ARCH-DOM-028`、`ARCH-INT-031`
只证明非激活 source current；E434/#434 graph/selector/installed/platform 与 #410 Release matrix
均为独立未验证边界。

## EVD-040: #454 D443 reviewed source candidate

来源为 [D443 contribution](../contributions/454-task-lifecycle-d443.md) 与 generation 5 的
canonical Bind package。Fixed Fork source-lock SHA `eb370008c7689d4e272ae626bd002190ecbb3296` 的
实际 session port/real Git fixture 下，Bind 12/12（含旧 checkout 保留后的换绑/恢复）、source package graph、Python compile 与
`git diff --check` 已通过。全局 integration 19/20，未通过项属于 Closure relative `$ref`；
这不能冒称 full suite 通过。`ARCH-CUR-042`、`ARCH-DOM-027`、`ARCH-INT-030` 只证明 D443
非激活 source current；promotion-created diff 的 fresh gates、E434 installed/platform 与完整 Release
matrix 仍须独立执行。

## EVD-036: #454 C3 Checkout Acquisition Provenance Promotion

本证据支撑 `ARCH-CUR-038`、`ARCH-DOM-023`、`ARCH-INT-026` 与 `.60 -> .61` promotion。
独立完整 Branch Review 绑定
`origin/main@9c2238bad7e73ea4a1f23dddcb7e8e9204c244da...HEAD@b816aca8d6520bf90c52c6210ff3155174da86f3`；
`BR454-C3-P2-010` 与 `BR454-C3-P2-011` 均 resolved，当前范围无新 P0-P3 finding。

Focused evidence包括checkout substrate `27/27`、task lifecycle runtime `56/56`、Python compile、JSON parse、
ownership `32 active + 1 planned`、task/workspace/static/line/diff checks。Package `19/20`、shared runtime
`119/128`、lifecycle integration `38/44`、preset 272 with 2 errors/3 skips与完整Release matrix不声明通过。

本证据不证明C4-C7、D443、D436、E434、production activation、push、PR、merge、tag、Release或Issue closure；
promotion-created `.61` diff仍须fresh Phase 2、Task Commit与independent complete Branch Review。

## EVD-037: #454 C4 Branch Association Promotion

本证据支撑 `ARCH-CUR-039`、`ARCH-DOM-024`、`ARCH-INT-027`、`ARCH-GAP-011` 与
`.61 -> .62` Architecture knowledge promotion。独立完整 Branch Review 绑定
`origin/main@77fa1a2250998ad8c71f0fffedf9a99a15a76dec...HEAD@c7fab600e6e29385c23c276ac2b1828d0465fd77`，
P0/P1/P2/P3 为 `0/0/0/0`。Admission 时，`BR454-C4-P3-001` 在 `6ab9dde1` 为可复现的
`qualified_finding`，并由 `c7fab600` 修复闭环；随后针对修复后的 current supported path 重新执行 qualification，
normal-scenario 返回 `classified / rejected_not_reproduced`，solution-mechanism 返回
`classified / qualified_current`。

Fresh focused evidence 为 task-lifecycle runtime `93/93`、Python compile、task validation、`git diff --check`
与 touched non-generated file line checks。Generation 2 的真实 common-dir binding 仍不存在，因此测试没有
写入 live task control state。Preset Python suite 的既有结果为 `85/86`，唯一错误来自 E434 前刻意未同步的
installed task-lifecycle README/schema/registry sidecars；该 broader suite 未在 narrow finding-fix 中重跑，
不得声明为通过。

本 evidence 不证明 C5-C7、D443、D436、E434、#434 production activation、完整 Release matrix、push、PR、
merge、tag、Release 或 Issue closure。Promotion-created `.62` diff 仍须 fresh Phase 2、Task Commit 与
independent complete Branch Review 后才能进入 Publication。

## EVD-038: #454 C5 Session And Resource Control Promotion

本证据支撑 `ARCH-CUR-040`、`ARCH-DOM-025`、`ARCH-INT-028`、`ARCH-GAP-011` 与
`.62 -> .63` Architecture knowledge promotion。独立完整 Branch Review 绑定
`origin/main@5064292675e9dabb4c6382c9397f3469b6b38ea4...HEAD@f18a51d40f5084b514abc5c062507e926b74f783`，
覆盖三个提交、21 个路径；C5 current 正常路径 P0/P1/P2/P3 未留下 finding。先前 remote HEAD 与
PRD slice 两个候选已修复，normal-scenario fresh 分类为 `rejected_not_reproduced`；Architecture
Branch Review 返回 `baseline_current / reviewed_candidate`。这些判断只绑定提升前的已提交 candidate。

Focused lifecycle suite `113/113`、task validator、Draft 2020-12 schema、Python AST、行数及 diff check
在提升前 C5 范围通过；独立只读 reviewer 没有重跑测试。Fixed Fork 实际联调、installed/platform、
production graph activation 与完整 Release matrix 未由本证据证明。C6-C7、D443、D436、E434 与
#434 activation 仍在后续 owner 边界；Issue #454 不因本次 C5 promotion 关闭。

本次 `.63` promotion-created diff 仍须 fresh Phase 2、Task Commit 与独立完整 Branch Review，之后才可
进入 Publication/Finalizer/Delivery。此证据不证明 push、PR、merge、Release 或 Issue closure。

## EVD-039: #454 C6/C7 Nonactivated Substrate Promotion

本证据支撑 `ARCH-CUR-041`、`ARCH-DOM-026`、`ARCH-INT-029`、`ARCH-GAP-011` 与
`.63 -> .64` Architecture knowledge promotion。独立完整 Branch Review 绑定
`origin/main@0a062919ff568a1fc0259ed7c01b5b67345fd29a...HEAD@9dab07fb0fdf47912e1d907c695feb37efb68c4a`，
覆盖两个提交、21 个路径，正式 checker 与 public wrapper 返回 `passed`。首轮普通 selected-base drift
候选已由 C6 input 的 live base/ref/ancestry 检查关闭；第二位独立 reviewer 报告当前 slice 无 finding。

提升前 focused lifecycle `125/125`、planned inventory `3/3`、ownership、dogfood drift、task validator
与 `git diff --check` 通过。Package integration `19/20` 的 unchanged closure schema 错误在 clean main 同样
复现，managed verifier fixture 未通过；这两项不记作通过。Fixed Fork 本轮无新增本地 build，完整 #410
多平台 Release matrix 未运行。六个 IDs 仅 planned，32/142/102 active inventory 与生产 22/98 graph 未变。

本次 `.64` promotion-created diff 必须重新通过 fresh Phase 2、Task Commit 与独立完整 Branch Review，
随后才可进入 Publication。D443、D436、E434、#434 activation、installed/platform 切换、push、PR、merge、
Release、生产升级与 Issue closure 均不由本证据证明。

## EVD-032: #443 Reviewed Promotion Source

本证据支撑 `ARCH-CUR-034`、`ARCH-DOM-019`、`ARCH-INT-022`、`ARCH-GAP-009`、`ADR-014`
以及 `.56 -> .57` knowledge promotion。#443 integrated committed range为
`a74d729ed84449ce603d112e277fa567e87a7bf3..4dd9f7b7d4df2167819745565225001355adb5ee`；
Issue #443已于2026-09-19关闭，range已进入main历史。contribution
`architecture-contribution-443-task-identity-session-binding-v1`以该闭合capability和live package authority为promotion输入。

当前fresh执行canonical package contract/runtime 26 tests，覆盖profile/route闭集、A→B→A、跨session、
mapping locator、base provenance、manual recovery、generation/receipt invalidation与zero-write；live registry/
interface/commands聚合为32 packages / 142 external exits / 102 commands，production workflow保持22 mandatory
invokes / 98 exits。installed interface/runtime与canonical bytes一致；package-private tests按当前安装合同不分发。

本证据不证明当前#452 OpenCode/platform combined diff的完整source/installed/platform、preset reapply、ownership、
dogfood或representative throwaway gate，也不证明#434 production graph activation、完整Release matrix、生产binding、
push、PR、远端merge、tag、Release或Issue closure mutation。promotion-created diff仍须fresh Phase 2、Task Commit与
independent complete Branch Review后才能进入Publication。

## EVD-033: #452 All-Platform Projection And Exact Selection Promotion

本证据支撑 `ARCH-CUR-035`、`ARCH-DOM-020`、`ARCH-INT-023`、`ARCH-GAP-010` 以及
`.57 -> .58` Architecture knowledge promotion。独立完整 Branch Review 绑定
`origin/main@361da96327824503ffb4fb4189291b3b9b4e23ae...HEAD@b4b4ebfdd29188a36866fd832b65cc6438420acf`；
Architecture contribution `architecture-contribution-452-all-platform-projection-v1` 已完成
expected-current-bound serialized promotion。当前定向 evidence 覆盖 pinned 22-platform inventory、重复
`--platform` 与旧参数拒绝、三平台默认/dogfood、manifest/provenance exact-selection upgrade、OpenCode
representative actual-load、ownership/manifest/mode/parity、reapply/update/removal provenance、dogfood drift
及 package-private `tests/` 排除；实现事实详见对应 RDT `.58` test contribution。

本 evidence 不证明 #434 production graph activation、22-client native compatibility matrix、正式
Release/tag/GitHub Release、业务生产升级、push、PR、merge 或 Issue closure；promotion-created diff 必须
重新通过 fresh Phase 2、Task Commit 与 independent complete Branch Review。

## EVD-034: #454 Task Lifecycle C2 And Stage-Evidence Promotion

本证据支撑 `ARCH-CUR-036`、`ARCH-DOM-021`、`ARCH-INT-024`、`ARCH-GAP-011`、`ADR-015`
以及 `.58 -> .59` Architecture knowledge promotion。提升前独立完整 Branch Review 绑定
`origin/main@0381f4ee060398f42bd2dded6ec14d7fced21393...HEAD@4421662f17b2b3adcfd3faeec6fd782d11bc947f`，
覆盖 193 个 changed paths，P0/P1/P2/P3 为 `0/0/0/0`；Architecture contribution
`architecture-contribution-454-task-lifecycle-state-model-v1` 完成 expected-current-bound serialized promotion。

提升前 fresh 定向证据包括 lifecycle runtime `22/22`、Reconcile package `34/34`、base-continuity integration
`3/3`、active continuation `7/7`、Reactivate `17/17`、created-Issue provenance `1/1`，以及 selected-base
ancestry、canonical/preset/dogfood parity、source/README identity、task validation、JSON/Python checks、zero
`.trellis/scripts/**` diff 与 `git diff --check`。Fork source 固定为
`eb370008c7689d4e272ae626bd002190ecbb3296`、tree `bd1f133cc55d0562ad9ec5f426bca70d1584194b`、
CI `35621578090`。

两个 base-identical 全局测试 observation 属于 #454 range 外既有问题，不写成通过，也不阻塞本次 scoped
promotion。本证据不证明 C3-C7、D443、D436、E434、production activation、完整 installer/upgrade/
workflow-switch 或多平台 Release matrix、push、PR、merge、tag、GitHub Release、业务生产验证或 Issue closure。
本 evidence 不替代 promotion-created diff 后续 fresh Phase 2、Task Commit 与 independent complete Branch Review；Publication 必须消费后续 exact-range gate 结果。

## EVD-035: #454 C3 Checkout Substrate Promotion

本证据支撑 `ARCH-CUR-037`、`ARCH-DOM-022`、`ARCH-INT-025`、`ARCH-GAP-011` 与
`.59 -> .60` Architecture knowledge promotion。独立完整 Branch Review 绑定
`origin/main@9c2238bad7e73ea4a1f23dddcb7e8e9204c244da...HEAD@e965b7e8b6850614a2cd21f899a02b3ea9da73f3`；
原 C3 findings 已关闭，当前范围无 open P0-P3 finding。Architecture contribution
`architecture-contribution-454-task-lifecycle-state-model-c3-v1` 完成 expected-current-bound promotion。

Focused evidence 包括 lifecycle runtime `51/51`、39 named DTO/schema、live checkout discovery/acquisition、
identifier/error contracts、planned ownership、source/installed-active、task/workspace/compile/static/line/diff checks。
Global package suite 保持 `19/20`，preset suite 保持 `85/86`；前者是 unchanged closure relative-ref defect，
后者是 C3 禁止同步 installed projection 后 raw apply 的预期 conflict，二者均未声明为通过。

本 evidence 不证明 C4-C7、D443、D436、E434、production activation、完整 installer/upgrade/workflow-switch/
multi-platform Release matrix、push、PR、merge、tag、GitHub Release、业务生产验证或 Issue closure。promotion-created
diff 仍须 fresh Phase 2、Task Commit 与 independent complete Branch Review 后才能进入 Publication。

## EVD-043: #454 Generation 7 TaskId Domain Candidate

This records the pre-Fork-PR-21 candidate. The current source and post-fix
validation are recorded in `EVD-044` below; this older result is not the final
Branch Review or Delivery gate.

固定 Fork 为 `castbox/Trellis@18ccbf0356ebcc61f3557e1427d1ad8a6351559a`，
tree `933069dbda8ac02d64e1fc8e3a1c3af513c1ae17`，main CI `36460551909`
成功。提升前候选 `origin/main@4d7cd74f3803ca924ac3802dcc12afd1f2cac06c...
HEAD@63de89e3a47686f8b1fd505ba6fae89ce5658931` 的完整 Branch Review
通过；34 包隔离测试为 `685 passed, 2 skipped`，installer/upgrade/Fork
定向子集 `90 passed`，source/installed、Claude/Codex/Cursor drift、sidecar 与
`git diff --check` 已定向检查。先前更宽 installer 运行的 `172 passed, 2 failed`
未整体重跑，不把它计为通过。promotion-created diff 与最终同候选审查、
远端 Delivery/merge/Closure/Finish/Cleanup 尚未在此条中证明；完整 Release matrix
和 marketplace 不属于本次验收。

## EVD-044: #454 Final Source Candidate Before Branch Review

Fixed Fork PR #21 merged to `castbox/Trellis` main at
`a9e0b5dcb40e9dd0a54f990ad4d215e427939856`, tree
`38a2e226a03ca7899ae3504bf3763dc1aac0cb35`; main push CI
`36486251351` succeeded. Its installed Guru Team session reader returns
`binding_required` on a missing current TaskBranchBinding rather than using
an old checkout copy. The official template and Guru dogfood session script
are byte-identical. Ordinary Trellis retains its no-binding fallback.

The fixed Fork checkout passed frozen install, build and `validate-source`.
On the Guru candidate, 34 package suites passed in isolated processes with
two scoped skips; shared lifecycle kernel 142/142, Architecture owner 26/26,
RDT owner 9/9, and installer/Fork/preset combination 189/189 passed. The
new installed-reader binding-loss regression passed. Source and installed
package validators, preset reapply, selected Claude/Codex/Cursor drift,
task validation and `git diff --check` passed; no `.new` or `.bak` sidecar
remains. Full multi-platform Release matrix, marketplace and business-repo
production validation were not run. This evidence does not substitute for
fresh Phase 2, committed complete-range Branch Review, two independent
zero-finding reviews, Delivery or terminal closeout.

## EVD-045: #454 TaskId History And Manual Cleanup Finding Fix

The next independent review of `origin/main@4d7cd74f...7d40f6b8` found two
normal-path gaps: TaskId reuse after a checkout and control-state loss when
only a remote-tracking ref retained the prior task, and manual deletion of
another active task's remote branch after its commit was merged to main.
Neither finding was a malicious-input or concurrency scenario; that review
did not pass Branch Review or count toward the two zero-finding rounds.

Fork PR #22 merged as `castbox/Trellis@8336e78b8fafe2a4bc4ea3d01815a61cf4f08983`,
tree `31a83927ed215fb23c04f357e259b45a39c13b7b`; main CI run
`36519692082` succeeded. The Fork task writer now checks visible local and
remote-tracking task artifacts before creation, while non-Git Trellis keeps
its prior directory-based behavior. Guru's creation preflight checks the
same reachable refs. Terminal manual Cleanup rejects a selected local or
remote HEAD carrying another active TaskId/generation even when its commit
and artifact survive on main; it still does not infer historical ownership.

Fork's commit hook passed 2318 tests across 100 files. The Guru finding-fix
real-Git creation/Cleanup subset passed 56 tests; the 34 isolated package
suites passed 689 tests with two scoped skips. The current source/installed
package projection, preset reapply and declared Claude/Codex/Cursor drift
passed with no sidecars. Shared lifecycle, Architecture/RDT, Phase 2, full
committed Branch Review, two final independent reviews and live Delivery
remain separate gates; this entry does not claim them. The legacy
`guru-create-task-workspace` throwaway verifier is not a current package
gate and its retired-path tests are not claimed as passing. Marketplace is
unused and the full multi-platform Release matrix remains a dedicated gate.

`EVD-045`（#467 preparation）：`origin/main@8abf52ed...728c313e` 的
31 文件 pre-promotion committed range 经独立完整 Branch Review，零 P0-P3；
TaskId 聚焦测试 22/22、完整 lifecycle 148/148，通过 source/installed、
声明平台投影、preset reapply 与 drift。Architecture/RDT `.69` 晋升形成的
新字节还须 fresh Phase 2、Task Commit 与完整 Branch Review。前一版本既有安装
升级时退役资产的实际删除，以及最终 tag/Release，均未由本条证明。

## EVD-046: #481 task-personnel retirement candidate

已合并 Fork PR #24 的精确 source lock 为
`castbox/Trellis@64fe9a15a68df1add3a2a7fd182f3d84e6eba4ac`，tree
`a964088ffa3f8df0deafc8f042f91911e3e8ecbe`，CLI/core
`0.7.0-castbox.1`，成功 CI `36755826713`；source validator 已通过。
Guru 候选的 lifecycle 152/152、create-task 13/13、Reactivate 25/25、
Finish 56/56、session 8/8（另 1 项环境 skip）、checkout 4/4、branch 3/3、
installer 101/101、compatibility contract 73/73 通过。代表性 Codex 新装验证
native loading、preset apply、两次 reapply、同候选 update、template hash 与
session binding；dogfood drift 通过且无残留 `.new`/`.bak`。旧 dogfood
`.trellis/.version=0.6.17` 的 update 被该 Fork 明确拒绝，旧版本升级不能记为通过。
历史 `test_434_activation_candidate.py` 有 3 失败、1 跳过，不记为通过的 #481 gate。
完整多平台 Release/前驱升级矩阵、远端 marketplace、生产安装，以及本次
promotion-created diff 的 fresh Phase 2 和完整 committed Branch Review 尚未由本条证明。

## EVD-047: #490 reference-only/source adoption

已独立读取正式 creator 16/16、current lifecycle 152/152、Closure 18/18、dogfood 9/9 证据，source/installed/platform validator 与183-file official projection通过；直接 live回读 CI37179218822 success at9c36002a。Focused Codex local-workflow sample clean install、initial preset、两次 same-candidate update/reapply、session/template 与零 drift/sidecar通过，native_load=projection_parity。pre-promotion完整committed review已通过，promotion-created diff仍须fresh Phase2/commit/不同reviewer完整Branch Review。remote/native-host/full matrix、predecessor refusal/no-write、tag/Release尚未由本条证明，归#489。

## EVD-048：#495迁移候选与本地证据

绑定expected `.71 -> .72`知识晋升与正式Fork PR27 `8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1`/CI37473087582。候选core411pass/1历史SQLite skip、CLI1879pass，lint/typecheck/build通过；clean built source与183文件official投影/9tests通过。Guru installer101、upgrade73、ownership9、migration14通过；runtime64完整轮62pass/2dependency失败后原样重试2pass，不称单轮64通过。

public六场景6/6证明planning/dirty未发布dev接续、mixed/deferred正式creator、普通partial recovery、无新工作实际写后精确rollback/旧runtime smoke，以及新meta/notes禁止覆盖。current `.2` dry-run/update与local canonical workflow/apply/reapply、3844hash/preservation/零drift-sidecar通过，10真实业务checkout/Fork状态保持；共享managed Python cache为bootstrap边界。上述Guru来源是local_candidate，不证明remote source_locked/provider。

PR195 exact HEAD旧manifest的4896 managed来源核对、58未展开hash解析、零冲突/现存编辑、一条absent路径只关闭来源读取缺口；openPR处置与真实旧Finalizer/Finish在途完整验收仍缺，merged历史终态不能替代。ARCH-GAP012保持open，全部MIG01..09完成前禁止merge/Completion。本次promotion-generated diff必须重新fresh Phase2/TaskCommit/不同reviewer完整BranchReview；本条不声明该后续gate通过。完整矩阵/软件发布/真实业务安装未执行。

## EVD-049：#495 固定来源最终验收

expected `.72 -> .73` 承接 [验收增量](../../requirements-design-test-contributions/495-legacy-installation-upgrade-acceptance/test.md)，该文件是结果唯一入口。旧 source `a32ffdca61f432bc6c3e0557fe68486c1422d08f`，新远端 Guru `6a563f5f06cb1284c0935b3a2be68524d93df988`，Fork `8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1`。正式七场景首轮 5/7、exit1；两原失败样本 public same-owner 恢复/剩余断言通过，未单轮7/7。registry timeout provider重试后通过；未分类 internal/node 首次失败根因未知。source/actual installed/Shared/Codex、实际update/create-new/字节审查/force/preset reapply、3853hash与modes、零sidecar通过。

真实 PR195 OPEN/deferred 的 old task/live base/head 区别、PR58/210 merged但无确认TaskRef/trailer，均只读诊断，不构造当前 MergeResult/Completion。MIG06 原始业务在途不可取得，依据 live scope 使用正式native旧task/plan/recorder/checker/writer/executor/archive、本地Git与canonical test doubles；原路径正常终态，observer仅复制正式writer已写出的push_content。新source_locked public迁移 deferred/preserve，首次失败后一次resume upgraded/unverified[]，16旧文件bytes/modes及refs保持；directold明确unsupported_legacy_task，新current neighbor正式创建后installed再次通过。

EVD-048/v1/.72 为不可变前驱证据；本条不把旧首次失败删除或说成网络，不证明业务原始在途/真实GitHub发布/new文档HEAD重跑/当前旧gate/Release/真实业务安装/完整累计矩阵。晋升前 committed review 仅放行 expected-current promotion；晋升diff仍须freshPhase2/TaskCommit/不同reviewer完整BranchReview，再按正式Delivery/merge/Completion owners承接。

## EVD-050：#495 版本系列本地 slice

expected `.73→.74`；[唯一增量 Test](../../requirements-design-test-contributions/495-upgrade-version-families/test.md)拥有实际结果与首次失败/恢复边界。19 tag 全归组，G1..G8 actual before/preview/upgrade/实际来源回退/smoke，current linked control/session 与 lifecycle 横向覆盖；正式 Fork PR28/CI 固定 `.3`。26 package/2helper、Skill/overlay canonical-only及暂停新工作四格和 companion组合、source/installed/drift已定向验证。三个回退finding修复并关闭，`11ef591c...6cd766dd` 完整独立复审及正式 Branch Review passed；该 pass 不覆盖本次晋升 diff。REMOTE 同 Guru public/source_locked/provider/deferred 尚缺，旧 EVD-049 不代替；不声称 full-suite全通过、Release、真实业务安装或累计矩阵。
