# #410 Release v0.6.17-guru.1 Test contribution

- `T410-01`: inspect canonical manifest, dogfood extension manifest, and all
  current release-facing README/version locators for the target mapping.
- `T410-02`: validate the package, workflow, preset, source lock, and selected
  projections without changing Trellis-owned upstream files.
- `T410-03`: run fresh Phase 2 and complete committed Branch Review over
  `origin/main...HEAD` before and after serialized promotion.
- `T410-04`: after merge, verify fresh candidate commit/tree identity and
  predecessor ancestry before release mutations.
- `T410-05`: run the release contract's targeted source/installed, ownership,
  drift, residue, and secret checks; the dedicated cumulative matrix remains
  outside this Issue's scope.
- `T410-06`: validate tag-pinned smoke and GitHub Release only against the same
  exact candidate; close Issue #410 only after publication evidence is live.
