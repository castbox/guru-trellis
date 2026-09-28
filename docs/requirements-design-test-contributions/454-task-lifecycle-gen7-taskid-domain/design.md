# #454 Generation 7 TaskId Domain Design Contribution

Status: reviewed promotion from immutable `.67` to `.68/active`; post-promotion gates remain independent.

- `D454-G7-01`: Pin the merged official Fork commit
  `a9e0b5dcb40e9dd0a54f990ad4d215e427939856` as the implementation
  candidate. The official task writer validates explicit and slug-derived IDs. Guru
  `identity.py` and the shared DTO schema use the exact same TaskId pattern.
- `D454-G7-02`: Derive handoff receipt refs in one runtime owner. Preserve
  the prior ref for Git-valid IDs; otherwise use
  `guru-task-lifecycle-id/<sha256(TaskId UTF-8)>`. Keep the generated ref
  separate from the immutable TaskId and validate retained-control ownership
  against the resulting Git-valid namespace.
- `D454-G7-03`: Project the source to installed and declared platform
  copies through the preset mechanism. Remove no session or task binding
  flexibility: a session focus can switch or rebind by TaskId without
  treating Git HEAD, Issue, checkout, developer or assignee as task identity.
- `D454-G7-04`: Evolve the existing Cleanup owner directly. Its terminal
  missing-ledger exit projects only call-local Git resource candidates;
  selection uses stable candidate IDs and fresh live resource checks, not
  ledger reconstruction or ownership inference. Normal and manual Finish both
  retain the exact minimal terminal result for a later ledger-loss recovery.
  The portable Finish branch in that result is a liveness hint, not ownership:
  an empty confirmed selection seals a zero-deletion result only when the
  branch is absent; old results without this hint remain manual.
  Rename the public manual
  profile and exit to the Issue contract without a compatibility alias.
- `D454-G7-05`: Evolve the official Fork task create/archive store in place:
  direct standalone creation defaults to `source.kind=no_issue`, Guru creation
  replaces it with the reviewed structured source, and archive no longer
  consumes `task.json.branch`. Preserve TaskId/source/generation on rename
  and archive; keep branch and checkout resolution in their existing owners.
- `D454-G7-06`: Reactivate reads the current Cleanup `selected-*` receipt as
  well as prior `manual-*` receipts, checking the same TaskId, generation,
  Finish result and cleaned exit before admitting the new generation. When
  the terminal ledger was lost after normal Finish, the exact terminal result
  branch and target identity also bind that normal Finish transaction.
- `D454-G7-07`: Keep TaskBranchBinding and resource ownership on the live
  five-field contract without an epoch. Cleanup's missing-control selection
  checks active task artifacts and a retained containing branch before deleting
  a selected local branch.
- `D454-G7-08`: Align the official Fork source parser with Guru's
  `normalize_repo_ref` contract and project that writer and the current
  five-field session reader byte-for-byte into the dogfood official scripts.
- `D454-G7-09`: In an installed Guru Team checkout, the official session
  reader returns `binding_required` when the current TaskBranchBinding is
  missing. Only ordinary Trellis retains its existing no-binding fallback;
  neither path creates a replacement binding or guesses a current branch.
