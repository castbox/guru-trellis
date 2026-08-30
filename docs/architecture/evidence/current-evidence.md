# EVIDENCE

| Evidence ID | Class | Locator / identity | Supports |
| --- | --- | --- | --- |
| `EVD-001` | current source baseline | reviewed task head `d3dca74b3a94569a095594477c15b032526f2381` + #267 expected `.41` serialized promotion delta；精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD | `ARCH-CUR-001..004,006..009,013..016` |
| `EVD-002` | stable release | annotated tag `v0.6.5-guru.10`；tag object `b5fd47e9dc45ca4d6950f87f38d495776ce676ce`；peeled commit `5c059f4943edad7dfe25182a78af94759d41f9a1`；non-draft/non-prerelease/zero-asset Release | `ARCH-CUR-005` only |
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

`EVD-008` 的 matrix object 保留 `external_boundaries` 与
`real_github_verified:false`；它只证明六-cell与 local A/B。最终精确
`source_state.candidate_tree`、source identity 与 matrix digest 留在 runtime/conversation
evidence，避免 tracked evidence 对 candidate tree 形成自引用。
`EVD-009` 是独立完成的真实 provider evidence。当前 authority 组合消费两类证据，
不声称任何 matrix JSON 已被改写，也不构造伪造的 combined artifact。

详见 `docs/test/versions/current-main-0.6.5-guru.42/test-plan.md`。`v0.6.15-guru.3` / extension
`0.6.15-guru.39` stable tag、GitHub Release、tag-pinned install 与 release smoke 仍保持
`unverified`，owner 为 Issue #267 exact-candidate Release lifecycle；#311 post-release
business-repository proof 保持独立。
