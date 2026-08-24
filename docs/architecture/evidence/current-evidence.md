# EVIDENCE

| Evidence ID | Class | Locator / identity | Supports |
| --- | --- | --- | --- |
| `EVD-001` | current source baseline | task head `d4165f268d36e19139266d28519148c290f773a4` + #290 serialized promotion delta；精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD | `ARCH-CUR-001..004,006..009,013` |
| `EVD-002` | stable release | annotated tag `v0.6.5-guru.10`；tag object `b5fd47e9dc45ca4d6950f87f38d495776ce676ce`；peeled commit `5c059f4943edad7dfe25182a78af94759d41f9a1`；non-draft/non-prerelease/zero-asset Release | `ARCH-CUR-005` only |
| `EVD-003` | RDT package | Issue #263 CLOSED；reviewed `d53335a7…`；archive `eaf955e0…`；PR #279 merge `891c2147…` | `ARCH-CUR-003` |
| `EVD-004` | Architecture package | Issue #264 CLOSED；reviewed `1cb2506b…`；PR #268 merge `37fdfe63…`；metadata head/merge `991080b6…` / `3b0f78c1…`；无 `finish-summary.json` | `ARCH-CUR-003` |
| `EVD-005` | Bootstrap package | Issue #265 CLOSED；reviewed `f2c67098…`；archive `de1c6e26…`；PR #280 merge `3c0d4a2f…`；archive/merge tree `45e8b402…` | `ARCH-CUR-003` |
| `EVD-006` | Bootstrap closeout | Issue #266 CLOSED；PR #281 merge `c2b1784654a95b999bbff71daf1393c22aa01048`；archive/merge tree `cb68fead327cc2cfb6ea03b8e81affcb9b7ad0e9` | active RDT/Architecture baseline |
| `EVD-007` | replacement release | Issue #275 CLOSED/COMPLETED；PR #282 rebase merge；review/archive head `83646987…`；merge/live main `5c059f49…`；post-tag install/version/closeout smoke 与 isolated consumer proof passed | `ARCH-CUR-005,007` |
| `EVD-008` | six-cell compatibility | `claude|codex|cursor × clean|existing` 6/6；final runtime matrix 绑定完整 dirty candidate `source_state`、三类 mode、recursive Docs authority、extension identity 与 post-archive non-empty history；sidecar/unknown template drift all zero；精确 tree/digest 不写回 tracked docs | `ARCH-CUR-008..009`, `ARCH-INT-006` |
| `EVD-009` | real GitHub A | disposable PR #2 source `6a7b721a…` -> rebase merge `a5c73c49…`；Issue #1 merge 后 CLOSED/COMPLETED；provider recovery 与 remote cleanup/reachability passed | `ARCH-CUR-010`, `ARCH-DOM-007` |
| `EVD-010` | focused compatibility | installed lifecycle 1/1；upgrade contract 20/20；preset/ownership 83/83；managed Python routing 44/44；RDT/Architecture/Bootstrap installed profiles passed | `ARCH-CUR-008..009` |
| `EVD-011` | #283 reviewed task range | base `2d34abfc…` -> reviewed task head `86a2cc1a…`；5 commits / 429 paths；schema 6.0 independent Branch Review PASS，open findings zero | `ARCH-FND-006`, `ARCH-GOV-006..008`, `ARCH-DOM-008`, `ARCH-INT-007`, `ADR-005` |
| `EVD-012` | #283 representative clean install | Trellis `0.6.15` + public marketplace bootstrap + exact local committed workflow + all-platform preset；21 packages / 72 commands / 4229 managed files，update/reapply/drift/sidecar checks passed | `ARCH-CUR-011..012`；local pre-push only，不是 formal verifier/release proof |
| `EVD-013` | #283 reviewed promotion | Architecture/RDT contribution locators、expected `.37`、successor `.38`、design constitution/change contract/ADR/history/traceability 与 serialized owner gate | `.38` current knowledge authority；post-promotion Phase 2/commit/Branch Review 必须 fresh 绑定最终 HEAD |
| `EVD-014` | #290 reviewed task and promotion | base `ec4df880…` -> reviewed task head `d4165f26…`；57 paths；fresh Architecture Branch Review 与 schema 6.0 independent Branch Review 均 passed，三个正常路径候选不再复现；expected `.38` -> successor `.39` serialized promotion | `ARCH-CUR-013`, `ADR-006`；post-promotion Phase 2/commit/Branch Review 必须 fresh 绑定最终 HEAD |

`EVD-008` 的 matrix object 保留 `external_boundaries` 与
`real_github_verified:false`；它只证明六-cell与 local A/B。最终精确
`source_state.candidate_tree`、source identity 与 matrix digest 留在 runtime/conversation
evidence，避免 tracked evidence 对 candidate tree 形成自引用。
`EVD-009` 是独立完成的真实 provider evidence。当前 authority 组合消费两类证据，
不声称任何 matrix JSON 已被改写，也不构造伪造的 combined artifact。

详见 `docs/test/versions/current-main-0.6.5-guru.40/test-plan.md`。`v0.6.15-guru.1` / extension
`.37` stable tag、GitHub Release、tag-pinned install 与 release smoke 仍保持 `unverified`，
owner 为独立的重构前稳定版 Release Issue；#267 属于后续重构链。
