# Implementation Plan

## Ordered Work

1. Re-read current Publication, Finalizer and Merge interfaces, schemas, examples, runtime recovery helpers and package tests; identify the single existing parsed-close-set authority.
2. Update Publication/Finalizer contract and projection logic so ledger delivery scope remains available for review while `ready_for_merge.expected_close_issues` represents only PR auto-close intent.
3. Apply the same rule to Finalizer existing-PR recovery and terminal recovery; preserve stale and closure-mismatch exits.
4. Add/adjust tests for refs-only with non-empty ledger scope, legal non-empty close keywords, body scope drift, illegal close keywords, existing PR recovery, terminal recovery, and no duplicate side effects.
5. Synchronize any generated/canonical package examples or installed projections required by the repository, then run drift checks.
6. Run Phase 2 check and inspect the complete task diff for scope, contract, compatibility and documentation consistency.

## Validation Commands

```bash
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-review-task-publication/tests -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-finalize-task/tests -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-merge-task-pr/tests -p 'test_*.py'
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

## Risk Points

- Do not replace the complete ledger `close_issues` review scope with an empty list; only the Merge auto-close projection changes.
- Do not weaken Merge exact-set equality or post-merge verification.
- Do not update historical task archives or business-repository evidence.
- Check every Finalizer producer path, not only the normal `ready_for_merge` line.

## Deferred Verification

The full multi-platform throwaway installer and release-candidate matrix remains outside Issue #393 ownership. Canonical, dogfood, installed package and declared platform projection checks for the touched active packages are required.
