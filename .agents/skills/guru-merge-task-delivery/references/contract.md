# Contract

## Ownership

`guru-merge-task-delivery` is the sole owner of Delivery merge readiness,
confirmation, expected-head mutation, merge-message trailers, and terminal
recovery. It consumes only the reviewed publication handoff plus live facts.
It does not own Delivery Review, publication, task completion, Issue closure,
archive, Finish, Reactivate, or cleanup.

The package is additive. Its interface may declare future consumers, but the
production workflow does not invoke it until the separate graph-cutover owner
activates the edge.

## Public Input

The `ready_for_merge` input contains only `task_ref`, call-local
`delivery_cycle_ref`, `repo_ref`, `pr_number`, `expected_head_sha`, and the
SHA-256 of the exact published PR body. Workflow and standalone modes apply
the same preconditions.

The task must remain `in_progress` in its mapped worktree. `task.json.id` is
the stable identity used in the merge trailer. The live PR must be Ready/Open,
same-repository, at the exact expected head, and its body bytes must match the
publication digest. Closing keywords are prohibited.

## Semantic Gate

The AI reviews exactly six dimensions: `active_task`, `pr_identity`,
`checks_and_reviews`, `mergeability`, `repository_policy`, and
`message_and_delivery_boundary`. The reviewed route is one of:

- `delivered`: all dimensions pass, no objective blocker exists, merge commit
  policy is supported, and the exact subject/body/trailers are reviewed;
- `merge_blocked`: a current external, provider, policy, permission, checks,
  or mergeability blocker prevents mutation;
- `implementation_required`: a current-slice task-work finding requires Phase
  2 and carries concrete `finding_refs`;
- `review_refresh_required`: current Delivery review authority is stale and
  carries a concrete `reason_code`.

Only `delivered` reaches the independent confirmation boundary. The private
gate stores current facts, semantic results, exact message bytes,
`pre_merge_base_head`, and an action digest. It never stores authorization.

## Mutation And Recovery

The executor calls exactly:

```text
gh pr merge <number> --repo <owner/repo> --merge \
  --match-head-commit <expected-head> --subject <subject> \
  --body-file <owner-private-temporary-file>
```

There is no squash/rebase fallback. The body file is removed after every
attempt. A successful post-read requires:

- PR state `MERGED` and one merge commit SHA;
- commit subject/body equal the reviewed bytes;
- parents exactly `[pre_merge_base_head, expected_head_sha]`;
- remote target base ref equals the merge commit;
- trailer task identity, schema `1`, and reviewed head are exact;
- the PR body still has no closing keyword;
- the active task identity remains current.

If mutation succeeded but stdout, post-read, or result projection was lost,
the same input and semantic review perform one read-only reconstruction. A
retained gate is checked when present. If the gate was already retired, parent
1 supplies the historical pre-merge base only after every other terminal fact
matches. Unknown or ambiguous terminal state fails closed and never triggers a
second merge.

## Delivery History Discovery

`discover-task-deliveries` is a deterministic, read-only package command. Its
closed query contains only the stable task identity, repository, and target
base. It scans the fresh target-base first-parent merge history, ignores merge
commits without Delivery trailers, and requires the exact schema-1 trailer
block for every matching task Delivery.

Each matching merge is cross-checked against exactly one GitHub merged PR:
same repository, target base, merge commit, reviewed head, and two-parent merge
identity. The command returns only immutable Delivery facts in target-base
order. It never reads a PR body, current task branch, worktree binding, task
creation branch, or ledger. Duplicate or drifted task/head/PR/merge identity
fails closed. Deleting an old head branch or changing the current active
binding therefore does not change historical Delivery identity, while a
bookkeeping merge without the trailers is excluded.

## Typed Outputs

`delivered` contains exactly `exit_id`, `task_ref`, `delivery_cycle_ref`,
`repo_ref`, `pr_number`, `reviewed_head`, and `merge_commit_sha`. It says
nothing about completion, closure, archive, Finish, Reactivate, or cleanup.

`implementation_required` contains `task_ref`, `finding_refs`, and
`resume_target=phase-2`. `review_refresh_required` contains `task_ref` and a
reason code. `merge_blocked` contains repository/PR identity plus a reason and
remediation. No output mutates task or Issue lifecycle state.
