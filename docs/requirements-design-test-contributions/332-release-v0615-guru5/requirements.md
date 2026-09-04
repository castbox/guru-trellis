# #332 Release current-fact alignment Requirements contribution

本 contribution 承接 live Issue #332，建立从 active
`current-main-0.6.5-guru.43` 到 successor `.44` 的 current release-fact alignment
候选。Architecture 与 RDT serialized promotion 已将其提升为 shared current `.44`；
promotion-created diff 必须重新进入 fresh Phase 2、task commit 与独立 Branch Review。

- `R332-AUTH-01`：`.44` 必须成为唯一 active Requirements/Design/Test 与 Architecture
  knowledge authority，`.43` 保留为 superseded history，predecessor/successor identity
  必须一致。
- `R332-AUTH-02`：`.44` 的 current release mapping 必须为
  `v0.6.15-guru.5 -> 0.6.15-guru.40 -> Trellis CLI 0.6.15`，并明确 repository
  `castbox/guru-trellis` 与 predecessor `v0.6.15-guru.4` 的边界。
- `R332-AUTH-03`：current release-facing facts、navigation、traceability、evidence
  与 predecessor/successor binding 必须收敛到 #332；历史 tag、Release、旧 authority
  和历史 evidence 的原始事实不得改写。
- `R332-AUTH-04`：`.44` 必须同时消费已合入 `main`、已通过独立 committed full-diff
  Branch Review、但尚未进入 shared current 的 #240 与 #348 authority contribution：
  `guru-qualify-solution-mechanism`、`guru-restore-archived-task`、对应 typed exits、
  Requirements/Design/Test 合同与 `ADR-008`。这不是新增实现，而是使 current authority
  与 latest `main` 的 23-Skill / 97-exit / 81-command 图一致。
- `R332-AUTH-05`：RDT/Architecture contribution 在独立 committed full-diff Branch Review
  通过前保持 shared current write 为零；serialized promotion 随后绑定 expected `.43` 完成，并在
  promotion-created diff 上重新执行 Phase 2、task commit 与 Branch Review。
- `R332-AUTH-06`：本 contribution 不把 package、历史 Issue/PR 或旧 Release evidence
  当作 exact-candidate Release Gate 通过证明；#332 的 close scope 仍只包含 #332。
- `R332-AUTH-07`：#240/#348 的 promotion 只接受其已合并 PR #346/#351 所记录的独立
  Branch Review 与 live closed Issue 身份；不得把 contribution 中旧的 pending 文案继续当作
  current 状态，也不得改写 #260/#283/#290/#311 等历史候选的原始计数和证据。
