# #332 Release current-fact alignment Test contribution

- `T332-AUTH-01`（R332-AUTH-01/02）：检查 `.44` promotion 后只存在一个 active
  Requirements/Design/Test/Architecture current，且 current release mapping 统一为
  `.5/.40/CLI 0.6.15`。
- `T332-AUTH-02`（R332-AUTH-03）：扫描 current navigation、version history、manifest、
  README、traceability 与 evidence，确认历史 `.3/.39/#267` 只保留在明确的 superseded 或
  released-history 边界，不被改写为当前事实。
- `T332-AUTH-03`（R332-AUTH-04）：对 `.43 -> .44` authority diff 做语义审查，确认没有
  新增行为、公共合同、runtime owner、Architecture decision、GAP、compatibility exit 或
  业务仓库范围。
- `T332-AUTH-04`（R332-AUTH-05）：在 contribution review 通过前检查 shared current 未写入；
  promotion 绑定 expected `.43`，并要求 promotion-created diff 重新走 Phase 2、task commit
  与独立 Branch Review。
- `T332-AUTH-05`（R332-AUTH-06）：确认 Issue ledger 只保留 #332 close scope，且 authority
  alignment、历史 evidence 或 focused package tests 不被标记为 exact-candidate Release Gate
  通过。

正式 Release Gate、clean throwaway、installed business repository、tag-pinned smoke、tag、
GitHub Release 与 Issue closeout 属于 #332 后续 exact-candidate 阶段，不由本 contribution
声明已通过。
