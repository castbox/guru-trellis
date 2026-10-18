# #410 Release v0.6.17-guru.1 Test contribution

状态：`reviewed_promoted`；immutable superseded predecessor `.51` 已由 `.52`
取代为 current active authority。以下 `T410-01..08` 只拆分 Issue #410 已接受的稳定
发版验证合同，不记录动态执行结果，也不替代后续 exact-candidate live evidence。

- `T410-01`: inspect canonical manifest, dogfood extension manifest, and all
  current release-facing README/version locators for the target mapping.
- `T410-02`: validate the package, workflow, preset, source lock, and selected
  projections without changing Trellis-owned upstream files.
- `T410-03`: run fresh Phase 2 and complete committed Branch Review over
  `origin/main...HEAD` before and after serialized promotion.
- `T410-04`: after merge, verify fresh candidate commit/tree identity and
  predecessor ancestry before release mutations.
- `T410-05`: validate source/installed package and Shared/Codex/Claude/Cursor
  projection parity against the same candidate identity.
- `T410-06`: validate ownership, preset reapply, dogfood drift, secret scan,
  recursive residue, sidecar, and diff hygiene without altering unrelated files.
- `T410-07`: run the focused clean install and existing-project
  update/workflow-preview/switch/reapply path required by the release contract;
  the dedicated cumulative multi-platform matrix remains outside this Issue.
- `T410-08`: validate annotated tag, tag-pinned smoke, GitHub Release, and Issue
  closure only against the same exact candidate and as separate live actions.

Any required `FAIL`, `SKIP`, stale, cross-SHA, unknown, multiple, or unmapped
result stops the release at its owning gate. Promotion does not convert historical
or preparation evidence into a Stage 2 pass.
