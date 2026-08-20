---
name: guru-merge-task-pr
description: Merge one Ready task PR through a semantic live gate, expected-head mutation, and post-merge closure verification.
---

# Guru Merge Task PR

Use this Skill only for the remote post-publication merge boundary. In workflow
mode consume `guru-finalize-task:ready_for_merge`; in standalone mode accept one
repo-bound PR identity plus the expected base/head branches and reviewed close
Issue set. Before invocation, author and review the exact Chinese
`chore(merge)` subject/body plus its primary Issue and concrete Chinese summary,
then rebuild the same live evidence.

Read [references/contract.md](references/contract.md), run the preview, perform
the semantic gate, and ask once for the exact merge action. After confirmation,
record/check the gate, execute with the expected head, and return exactly one of
`merged`, `merge_blocked`, or `closure_mismatch`.
An already persisted terminal output is recovered only after read-only live
revalidation of the exact merge SHA, two parents, reviewed subject/body, remote
base ref and closure facts; recovery never repeats the merge mutation.

Fail closed on stale head, base/head branch drift, PR-body close-scope drift,
Draft/Open/readiness drift, unknown policy, incomplete GitHub response, or
unmapped output. Never enter Phase
0, sync a base, update/rebase the PR branch, close Issues directly, synchronize
local `main`, or clean task resources.

`expected_close_issues=[]` is a valid refs-only merge contract: the PR body must
contain no close keyword, and successful merge requires no Issue closure reads
or effects. Non-empty sets still require exact equality and post-merge closure.
