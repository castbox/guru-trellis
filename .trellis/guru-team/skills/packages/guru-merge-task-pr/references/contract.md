# Contract

`judgment_mode=semantic`. The AI reads the repo-bound live PR and compares its
base/head branches, expected SHA, and PR-body close keywords with the minimal
reviewed authority supplied by Finalizer or the standalone caller. It also reads
checks, reviews, mergeability, repository merge policy and pre-merge Issue state.
The Finalizer edge remains a seed: the Merge AI authors `primary_issue`, one
concrete Chinese `summary`, and the exact fixed Chinese `subject/body` before
the semantic gate. Active input and gate schemas are 2.0; all 1.0 assets remain
immutable compatibility inventory and are rejected by the current runtime.
It selects one method only when policy and
reviewed intent determine it, displays the exact action, and accepts
`确认继续` without asking the user to repeat identities.

The recorder/checker preserve only the current semantic gate, including the
reviewed-message identity and pre-merge base head. The executor materializes the
reviewed body in its ignored owner directory and runs authenticated repo-bound
`gh pr merge --match-head-commit --merge --subject --body-file`; every success,
failure and terminal recovery removes that file. It then rereads the PR, merge
commit, remote base ref and Issues. `merged` requires PR `MERGED`, a complete
merge commit SHA, parents exactly `[pre-merge base head, expected head]`, exact
reviewed subject/body, remote base at the merge SHA, and every
close Issue `CLOSED`/`COMPLETED`, and `closed_at >= merged_at`.
`closure_mismatch` reports exact mismatches without closing anything.
`phase2_reentry_required` represents one AI-reviewed current-scope task-work
finding that requires changing the archived task content. It carries only the
exact PR/task/archive/finding identity required by
`guru-restore-archived-task`, performs no remote mutation, and does not require
merge confirmation. Provider, permission, ruleset, required-check,
mergeability, and other external blockers remain `merge_blocked`, which also
performs no mutation.

## Original Public Invoke Contract

`invoke-task-pr-merge` through `scripts/invoke.sh` is the sole public
post-confirmation Happy Path. A new transaction requires the current public
input and AI-authored semantic review;
it performs exactly one complete pre-merge snapshot, records the gate from that
same checked object, runs the unique expected-head mutation, performs exactly
one complete post-merge snapshot, persists the terminal result, projects the
existing public DTO, and removes the gate/body state. It does not call the
package-private recorder/checker/executor commands and therefore does not
repeat their full reads.

If the mutation completed but stdout, the post-read, or terminal persistence
was lost, the next invocation with the same `--review-input` performs one
read-only snapshot. A
retained non-terminal gate remains the primary recovery receipt. If successful
terminal cleanup already removed that gate, the caller must resupply the same
AI-authored semantic review; an exact already-merged PR reconstructs an
in-memory gate from the live merge commit's two parents, validates the reviewed
message and terminal facts, and returns without writing private state or
repeating the mutation. An unmerged state continues only when the same retained
gate/input/base/head facts remain current. A persisted terminal output is
similarly revalidated once, projected, and cleaned. After any terminal or
re-entry DTO is selected, the public invocation performs only local gate/body
cleanup and returns; it does
not start CI polling or any other Git, GitHub, Trellis, workflow, Issue,
base-sync, or cleanup operation.

The `record`, `check`, and `execute` commands remain package-private diagnostics
and bounded recovery surfaces. The old gate-only `invoke-task-pr-merge`
argument shape remains compatibility-only and projects an existing checked
gate; the normal `--review-input` branch does not call it or duplicate its live
reads.

## Required Check Watcher

`watch-task-pr-checks` is one deterministic external-CI watcher bound to exact
`repo`, PR number, and expected head SHA. Each poll first verifies the same PR
head and then reads only GitHub's required checks. It returns one stable fact
status: `checks_succeeded`, `checks_failed`, `checks_pending_timeout`, or
`head_changed`, plus the observed checks, poll count, and
`external_ci_wait_ms`. It performs no merge mutation, semantic readiness
decision, route selection, Issue mutation, or terminal follow-up, and it must
not be combined with another watcher or Agent while-loop.

The reviewed body canonical form ends at the final `Refs #<primary_issue>`
line without a trailing newline. This is the exact body returned by GitHub's
commit API after `--body-file` persistence, so the post-merge comparison does
not weaken or normalize either side.

After post-merge verification, the executor persists the minimal terminal
output before returning it to the dispatcher. If stdout is lost, the same gate
must reread the exact PR, expected head and branches, merge commit message and
parents, remote base ref, close keywords, and Issue closure facts. Only an exact terminal match is returned;
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
