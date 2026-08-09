# Contract

`judgment_mode=semantic`. The AI reads the repo-bound live PR, base/head,
expected SHA, checks, reviews, mergeability, repository merge policy, close
keywords and pre-merge Issue state. It selects one method only when policy and
reviewed intent determine it, displays the exact action, and accepts
`确认继续` without asking the user to repeat identities.

The recorder/checker preserve only the current semantic gate. The executor runs
authenticated repo-bound `gh pr merge --match-head-commit`, then rereads the PR
and Issues. `merged` requires PR `MERGED`, a complete merge commit SHA, every
close Issue `CLOSED`/`COMPLETED`, and `closed_at >= merged_at`.
`closure_mismatch` reports exact mismatches without closing anything.
`merge_blocked` represents a pre-merge gate failure and performs no mutation.

The gate is ignored owner-private runtime and is deleted after its typed output
is consumed. It never stores authorization, Finalizer transaction, local base
state, task cleanup instructions, or full GitHub payloads.
