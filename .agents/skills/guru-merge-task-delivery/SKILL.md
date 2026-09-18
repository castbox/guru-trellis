---
name: guru-merge-task-delivery
description: Merge one reviewed active-task Delivery PR through a semantic live gate, exact merge-commit trailers, and terminal recovery.
---

# Guru Merge Task Delivery

Use this Skill only after `guru-publish-task-delivery:ready_for_merge`. Read
[references/contract.md](references/contract.md), preview the exact active task
and live PR facts, then complete the six-dimension semantic review.

`delivered` requires one dialogue-local confirmation for the displayed
repository, PR, expected head, merge method, subject, body, and action identity.
After confirmation invoke the sole public transaction entry:

```bash
scripts/invoke.sh --input <ready-for-merge.json> \
  --review-input <semantic-review.json> --json
```

The reviewed merge body ends with exactly these trailers:

```text
Guru-Task-Identity: <stable-task-id>
Guru-Delivery-Schema: 1
Guru-Delivery-Head: <40-hex-reviewed-head>
```

The public invocation performs one pre-read, at most one expected-head
`--merge` mutation, and one post-read. Repeating the same invocation after
output loss reconstructs the same `delivered` result from live PR, commit,
parent, base-ref, and trailer facts without repeating the mutation.

The package also exposes the deterministic read-only command:

```bash
scripts/discover-task-deliveries.sh --input <delivery-history-query.json>
```

It reconstructs all matching historical Delivery facts from the target-base
first-parent merge history and exact GitHub PR/merge identity. It ignores
merges without Delivery trailers and is independent of PR body text, deleted
head branches, and the task's current branch or worktree binding.

`merge_blocked`, `implementation_required`, and `review_refresh_required` do
not request merge confirmation and perform no remote mutation. Fail closed on
stale task, head, base, PR body, checks, policy, message, gate, or terminal
identity. Never use squash or rebase fallback, parse PR body as Delivery
history, mutate an Issue, complete or archive a task, run Finish, or clean a
branch/worktree/runtime owned by another step.
