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
call the single recommended facade:

```bash
scripts/complete-task-pr-merge.sh --input <public-input.json> \
  --review-input <semantic-review.json> --json
```

It records the already-completed review, reuses one pre-merge snapshot, performs
one expected-head merge, captures one post-merge snapshot, projects exactly one
of `merged`, `merge_blocked`, or `closure_mismatch`, and retires the private
gate/body state before returning. On exact recovery, rerun the same facade with
the same `--input`; it resolves the package-owned current gate, or accepts that
exact locator through `--gate`. `--review-input` is not required when the
current gate already exists.

`record-task-pr-merge`, `check-task-pr-merge`, `execute-task-pr-merge`, and
`invoke-task-pr-merge` remain compatibility/testing/recovery commands. They are
not the recommended normal path.
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

If required CI is still pending, run exactly one repo/PR/expected-head-bound
watcher:

```bash
scripts/watch-task-pr-checks.sh --repo <owner/repo> --pull-request <number> \
  --expected-head <sha> --json
```

It returns `checks_succeeded`, `checks_failed`, `checks_pending_timeout`, or
`head_changed`. These are deterministic CI facts only; the Merge AI still owns
readiness and route judgment. Do not combine it with `gh run watch`,
`gh pr checks --watch`, or an Agent polling loop.
