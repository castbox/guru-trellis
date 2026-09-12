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

当前 Architecture knowledge successor 为 `.49`；`.48` 是 immutable superseded predecessor。
released `v0.6.16-guru.1` 不包含 #329 candidate。promotion-created combined diff 仍须 fresh Phase 2、
task commit 与完整 Branch Review，后续远端动作由各 live owner 独立验证。
