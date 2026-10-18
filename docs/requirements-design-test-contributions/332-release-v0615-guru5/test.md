# #332 Release current-fact alignment Test contribution

- `T332-AUTH-01`（R332-AUTH-01/02）：检查 `.44` promotion 后只存在一个 active
  Requirements/Design/Test/Architecture current，且 current release mapping 统一为
  `.5/.40/CLI 0.6.15`。
- `T332-AUTH-02`（R332-AUTH-03）：扫描 current navigation、version history、manifest、
  README、traceability 与 evidence，确认历史 `.3/.39/#267` 只保留在明确的 superseded 或
  released-history 边界，不被改写为当前事实。
- `T332-AUTH-03`（R332-AUTH-04/07）：对 `.43 -> .44` authority diff 做语义审查，确认
  #240/#348 的已合入、已独立审查合同被完整提升，current inventory 为 23 Skills / 97 exits /
  81 commands，`ADR-008` accepted，且没有第二 authority、GAP/compatibility 扩张或业务仓库范围。
- `T332-AUTH-04`（R332-AUTH-05）：在 contribution review 通过前检查 shared current 未写入；
  serialized promotion 已绑定 expected `.43` 完成，并要求 promotion-created diff 重新走 Phase 2、
  task commit 与独立 Branch Review。
- `T332-AUTH-05`（R332-AUTH-06）：确认 Issue ledger 只保留 #332 close scope，且 authority
  alignment、历史 evidence 或 focused package tests 不被标记为 exact-candidate Release Gate
  通过。
- `T332-AUTH-06`（R332-AUTH-04/07）：回读 live PR #346/#351 与 Issue #240/#348，确认
  committed full-diff Branch Review、merge 与 closure 已完成；旧 contribution pending 状态只可由
  serialized promotion 更新，不得据此伪造新的 review。

正式 Release Gate、clean throwaway、installed business repository、tag-pinned smoke、tag、
GitHub Release 与 Issue closeout 属于 #332 后续 exact-candidate 阶段，不由本 contribution
声明已通过。
