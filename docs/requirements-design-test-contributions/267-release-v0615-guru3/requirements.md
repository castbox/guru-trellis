# #267 Release authority alignment Requirements contribution

本 contribution 承接 live Issue #267 `2026-08-29-r18`。它修复 committed release
manifest `0.6.15-guru.39` 与 active `current-main-0.6.5-guru.41` authority 中
`0.6.5-guru.37` current-candidate facts 的冲突。该 candidate 已通过独立 committed full-diff
Branch Review，并由 expected `.41` RDT promotion owner 提升到 shared current `.42`；
promotion-created diff 的 fresh Phase 2、commit 与 Branch Review 仍待执行。

- `R267-AUTH-01`：successor knowledge authority 必须固定为
  `current-main-0.6.5-guru.42`，expected current 固定为 `.41`。
- `R267-AUTH-02`：promotion 后 `.42` 必须是唯一 active Requirements/Design/Test 与
  Architecture authority；`.41` 必须作为 superseded history 保留。
- `R267-AUTH-03`：`.42` 的 current/canonical extension candidate 必须为
  `0.6.15-guru.39`，target/required/tested Trellis CLI 必须保持 `0.6.15`，repo
  Release target 必须保持 `v0.6.15-guru.3`。
- `R267-AUTH-04`：authority alignment 只更新 release/current facts、traceability、
  navigation、evidence 与 predecessor/successor binding；不得改变产品行为、Skill
  public API、Architecture decision、owner、single-writer、GAP lifecycle 或
  compatibility exit。
- `R267-AUTH-05`：task-owned RDT/Architecture contributions 必须先通过 Phase 2、task
  commit 与独立 committed full-diff Branch Review；通过前 shared current write 必须为零。
- `R267-AUTH-06`：serialized promotion 必须绑定 expected `.41`；live current advance、
  incomplete traceability、current `.37` 残留或 promotion-created diff 未复核时，PR
  readiness 与 Release publication 必须 fail closed。
- `R267-AUTH-07`：#311、#267 与其它 Issue closure 边界保持不变；authority alignment
  不产生新的 close target，也不把 package test 表述为 exact-candidate Release pass。

本 contribution 不修改 runtime、workflow、Skill package、schema、business repository、tag、
GitHub Release 或 Issue 状态，也不创建 ADR。当前 `.42` promotion 不等于 #267 Release pass，
#311 post-release business proof 仍为独立未验证边界。
