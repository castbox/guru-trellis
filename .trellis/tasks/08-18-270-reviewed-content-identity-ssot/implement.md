# #270 Implementation Plan

## 1. Implementation

- [x] I1 Add the durable reviewed-content contract to workflow Docs SSOT.
- [x] I2 Add canonical shared `reviewed_content.py` with the fixed algorithm id, unified metadata exclusion, NUL-safe Git entry handling and path-byte sorting.
- [x] I3 Migrate Branch Review to the helper; remove `base_commit` and `kind` from content identity while retaining independent base/range/ancestry checks.
- [x] I4 Migrate Publication, Finalizer and Verifier to the same helper and delete their algorithm copies without removing unrelated atomic behavior.
- [x] I5 Make the Branch Review owner-private checkpoint current-only; reject old gates as stale and require fresh Branch Review.
- [x] I6 Update schemas, examples, evals, direct consumers, runtime/extension inventory and package contracts.
- [x] I7 Add real cross-package wrapper acceptance at one HEAD, including metadata-only stability, path/mode/oid drift, independent freshness and old-gate re-entry.
- [x] I8 Reapply the preset to synchronize dogfood/shared/Codex/Claude/Cursor copies; resolve every `.new`/`.bak` and verify executable modes.
- [x] I9 Run targeted package/runtime/integration/ownership/drift validation and fix all in-scope findings.
- [x] I10 Run fresh Phase 2 semantic check and preserve the full-matrix boundary in PR/final reporting.
- [x] I11 Fix the independent Branch Review findings: remove the Phase 2 algorithm-id collision and synchronize Branch Review schema 6.0 authority.
- [x] I12 Reapply projections, rerun targeted validation, complete fresh Phase 2, commit the fixes, close finding continuity and pass a distinct fresh final Branch Review.

## 2. Targeted Validation

```bash
python3 -m unittest trellis/skills/guru-team/packages/guru-review-branch/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/packages/guru-review-task-publication/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/packages/guru-verify-extension-installation/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/tests/test_finish_family_integration.py
python3 -m unittest trellis/skills/guru-team/runtime/tests/test_runtime.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
python3 trellis/skills/guru-team/scripts/validate_skill_packages.py --root . --mode source --json
python3 trellis/skills/guru-team/scripts/validate_skill_packages.py --root . --mode installed --json
find . -type f \( -name '*.new' -o -name '*.bak' \) -not -path './.git/*' -print
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-18-270-reviewed-content-identity-ssot
git diff --check
```

Command paths will be revalidated against the live tree before execution. The complete multi-platform Throwaway installer matrix is intentionally not run for this ordinary workflow defect Issue.

## 3. Risk Controls

- Preserve all unrelated atomic Guru Trellis capabilities; deletion is limited to duplicated reviewed-content algorithm code replaced by the shared helper.
- Do not weaken semantic gates or let deterministic scripts choose routes.
- Re-read current HEAD and full diff before Phase 2, Branch Review, Publication and merge.
- Treat generated-copy or mode mismatch, unresolved sidecars, old checkpoint acceptance, wrapper-only gaps or copied expected hashes as blocking findings.
- Do not touch #263 or later Issues, Issue bodies, tags or Releases.
