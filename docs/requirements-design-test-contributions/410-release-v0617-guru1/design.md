# #410 Release v0.6.17-guru.1 Design contribution

状态：`reviewed_promoted`；change path：`target_native`。immutable superseded
predecessor 为 `current-main-0.6.5-guru.51`，promoted/current active authority 为
`current-main-0.6.17-guru.52`。Architecture public inheritance 同为 `.52` / `active`。

- `D410-01`: advance only current release-facing version mapping and required
  canonical/dogfood projections; preserve historical facts.
- `D410-02`: keep repository tag, extension version, and CLI/source lock as
  separate identity axes.
- `D410-03`: route Architecture and RDT through serialized promotion; any
  promotion-created bytes invalidate earlier Phase 2, commit, and review.
- `D410-04`: after preparation merge, derive one exact candidate from fresh
  `origin/main` and prevent cross-SHA evidence reuse.
- `D410-05`: retain existing owner boundaries and use `Refs #410` for the
  Publication reference without implying Issue closure.
- `D410-06`: perform annotated tag, tag-pinned smoke, GitHub Release, and Issue
  closure as separate live actions with separate authority checks.

本 contribution 的 promotion identity 只确认稳定设计责任已进入 `.52`。它不证明
post-promotion Phase 2、Branch Review、exact-candidate gate、tag、GitHub Release 或
Issue closure 已完成。
