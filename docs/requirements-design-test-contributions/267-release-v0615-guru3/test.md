# #267 Release authority alignment Test contribution

- `T267-AUTH-01`（R267-AUTH-01/02）：检查 RDT/Architecture current navigation 只存在
  一个 active `.42`，`.41` 明确为 superseded，successor/predecessor identity 一致。
- `T267-AUTH-02`（R267-AUTH-03）：扫描 active Requirements、Design、Test、Architecture
  current surfaces，current/canonical extension candidate 只为 `0.6.15-guru.39`，CLI
  只为 `0.6.15`；`0.6.5-guru.37` 只允许出现在明确的 superseded/released-history 文本。
- `T267-AUTH-03`（R267-AUTH-04）：对 `.41...42` authority diff 做语义审查，确认没有新增
  requirement/behavior、Design responsibility、Architecture decision/ADR、owner、GAP、
  compatibility exit 或 runtime change。
- `T267-AUTH-04`（R267-AUTH-05）：在 contribution commit 的独立 Branch Review 通过前，
  shared current `.42` locator 不存在且 `.41` 仍为唯一 live current。
- `T267-AUTH-05`（R267-AUTH-05/06）：promotion-created diff 重新运行 Phase 2、task
  commit 与独立 Branch Review；旧 `2a546100…` review、contribution review 或 prior Phase 2
  均不能替代 post-promotion evidence。
- `T267-AUTH-06`（R267-AUTH-06）：expected `.41` mismatch、traceability 缺失、active
  `.37` 残留、multiple active versions 或 stale review 均阻断 Publication。
- `T267-AUTH-07`（R267-AUTH-07）：`issue-scope-ledger.json` 保持 `close_issues=[]`，#311
  保持 related/open，PR payload 只使用 `Refs #267`。

本 contribution 阶段只运行 planning、scope、RDT/Architecture contribution 与定向静态验证；
正式 Release matrix、tag-pinned smoke、tag、GitHub Release 与业务仓 #311 proof 仍属于后续
exact-candidate/post-publish 阶段。
