# #332 Release current-fact alignment Requirements contribution

本 contribution 承接 live Issue #332，建立从 active
`current-main-0.6.5-guru.43` 到 successor `.44` 的 current release-fact alignment
候选。它只写 task-isolated contribution，不直接修改 shared current。

- `R332-AUTH-01`：`.44` 必须成为唯一 active Requirements/Design/Test 与 Architecture
  knowledge authority，`.43` 保留为 superseded history，predecessor/successor identity
  必须一致。
- `R332-AUTH-02`：`.44` 的 current release mapping 必须为
  `v0.6.15-guru.5 -> 0.6.15-guru.40 -> Trellis CLI 0.6.15`，并明确 repository
  `castbox/guru-trellis` 与 predecessor `v0.6.15-guru.4` 的边界。
- `R332-AUTH-03`：current release-facing facts、navigation、traceability、evidence
  与 predecessor/successor binding 必须收敛到 #332；历史 tag、Release、旧 authority
  和历史 evidence 的原始事实不得改写。
- `R332-AUTH-04`：本次 authority alignment 不新增产品行为、公共 Skill I/O、runtime
  owner、Architecture decision、GAP lifecycle、compatibility exit 或业务仓库范围。
- `R332-AUTH-05`：RDT/Architecture contribution 在独立 committed full-diff Branch Review
  通过前必须保持 shared current write 为零；后续 promotion 必须绑定 expected `.43`，并在
  promotion-created diff 上重新执行 Phase 2、task commit 与 Branch Review。
- `R332-AUTH-06`：本 contribution 不把 package、历史 Issue/PR 或旧 Release evidence
  当作 exact-candidate Release Gate 通过证明；#332 的 close scope 仍只包含 #332。
