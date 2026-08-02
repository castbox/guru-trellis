---
name: guru-create-task-workspace
description: Create or exactly reuse a reviewed issue workspace and Trellis task through an AI-owned semantic gate, ephemeral scoped confirmation, deterministic execution, and three typed exits.
---

# Guru Create Task Workspace

Use this Skill only after `guru-review-change-request:ready`, or as a standalone
invocation that can supply and revalidate the same five prerequisite results.
Load [references/contract.md](references/contract.md) before acting.

Perform the semantic forward behavior and AI Review Gate, obtain the
invocation-specific human confirmation without persisting it, then run the
deterministic recorder/executor/checker and return exactly one declared typed
exit. GitHub issue mutation and workspace/task
mutation are mutually exclusive invocations. A created issue always returns
`refresh_review`; it never creates a workspace or task in the same invocation.
Retry recovery reuses one exact post-plan open issue, and mutation execution
reruns the shared base sync once before the first business write.

The package wrappers require the complete installed Guru Team preset and route
through `run-skill-command`. They are not standalone implementations. Missing,
stale, mismatched, ambiguous, or unconsumed evidence fails closed.

If the user refuses the displayed action, stop before the recorder/executor and
do not generate a plan, result, DTO, or typed exit. After the semantic gate and
owner recorder/executor/checker complete, invoke
`scripts/invoke.sh --input <execute-reviewed-plan.json> --owner-result <repo-relative-workspace-result> --owner-plan <repo-relative-workspace-plan>`
to serialize one minimal completion/refresh/stop DTO. The runtime reruns the
existing result checker, requires its embedded executor/checker evidence, and
derives the route from the checked executor result. It does not perform an
additional issue, worktree, branch, or task mutation.
