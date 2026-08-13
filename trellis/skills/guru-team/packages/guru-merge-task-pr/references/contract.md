# Contract

`judgment_mode=semantic`. The AI reads the repo-bound live PR and compares its
base/head branches, expected SHA, and PR-body close keywords with the minimal
reviewed authority supplied by Finalizer or the standalone caller. It also reads
checks, reviews, mergeability, repository merge policy and pre-merge Issue state.
It selects one method only when policy and
reviewed intent determine it, displays the exact action, and accepts
`确认继续` without asking the user to repeat identities.

The recorder/checker preserve only the current semantic gate. The executor runs
authenticated repo-bound `gh pr merge --match-head-commit`, then rereads the PR
and Issues. `merged` requires PR `MERGED`, a complete merge commit SHA, every
close Issue `CLOSED`/`COMPLETED`, and `closed_at >= merged_at`.
`closure_mismatch` reports exact mismatches without closing anything.
`merge_blocked` represents a pre-merge gate failure and performs no mutation.

After post-merge verification, the executor persists the minimal terminal
output before returning it to the dispatcher. If stdout is lost, the same gate
must reread the exact PR, expected head and branches, merge commit, close
keywords, and Issue closure facts. Only an exact terminal match is returned;
the executor performs zero repeated GitHub mutation, and a persisted
`closure_mismatch` remains that exit until consumed.

`expected_close_issues` is an ordered unique exact set with zero allowed
cardinality. For `[]`, parsed PR close keywords must also be `[]`; after a
successful merge, closure is vacuously complete and the executor performs no
Issue reads or closure effects. For a non-empty set, keywords and pre/post-merge
Issue facts must match every expected number exactly.

The gate is ignored owner-private runtime and is deleted after its typed output
is consumed. It never stores authorization, Finalizer transaction, local base
state, task cleanup instructions, or full GitHub payloads.
